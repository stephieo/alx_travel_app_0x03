from django.shortcuts import render
from rest_framework import viewsets, views 
from .models import User, Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from django.conf import settings
import requests
from django.db import transaction
from .tasks import send_booking_confirmation_mail


class ListingViewSet(viewsets.ModelViewSet):
    """This class contains all the varous views connected to the CRUD actions for this model.
    the basic setup is specifying the queryset to use for any returned data and the serializer handling any input/output"""
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location', 'price_per_night', 'max_guests']



class BookingViewSet(viewsets.ModelViewSet):
    """This class contains all the varous views connected to the CRUD actions for this model.
    the basic setup is specifying the queryset to use for any returned data and the serializer handling any input/output"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['start_date', 'listing__title', 'status']

    def create(self, request, * args, **kwargs):
        """ creation overide to  trigger booking confirmation email Celery task"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        booking = Booking.objects.get(id=serializer.data['id'])
        # Trigger Celery task to send confirmation email
        send_booking_confirmation_mail.delay(
            booking_id=booking.id,
            user_email=booking.user.email,
            user_name=booking.user.first_name,
            booking_date=str(booking.start_date),
            service_name=booking.listing.title
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


# key for payment transactions
chapa_secret_key = settings.CHAPA_SECRET_KEY

#TODO: This is implenentation needs polishing:
# [ ] i need to setup the serializer for payments
# [ ] i need to setup phone numeber verification to match Chapa's requirements
# [ ]  the return url should be made dynamic later. what is there is just for development
# [ ]  the callback url should be made dynamic later as well
# [x]  the payment initiation should be made atomic, so that on any fail, the whole transaction is rolled back. VERY important for payments
# [ ] i need to implement  sending email on paymnent confirmation  to user with Celery
# [ ]  sandbocx  testing with ChapaAPI and  save screenshots of the responses
class InitiatePaymentView(views.APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # get the booking id from the request data ( the user at fronted that wants to make a payment)
        booking_id = request.data.get('booking_id')
        if not booking_id:
            return Response({"error": "Booking ID is required, make a booking before payment"}, status=400)
        
        #verify the booking exists by  retieving the matching data from the database
        try: 
            booking = Booking.objects.get(booking_id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)
        
        # if booking exists
        # 1- create a payment object and generate trx ref
        # 2-  send the post request with payment amount to ChapaAPI
        with transaction.atomic():
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.total_price,
                status='Pending',
            )

            trx_ref = payment.generate_trx_ref()
            

            payload = {
                "amount": str(booking.total_price),
                "currency": "ETB",
                "email": str(booking.user.email),
                "first_name":str(booking.user.first_name),
                "last_name": str(booking.user.last_name),
                "phone_number": str(booking.user.phone_number),
                "tx_ref": trx_ref,
                "callback_url": "http://127.0.0.1:8000/api/bookings/verify/",
                "return_url": "http://127.0.0.1:8000/api/bookings/"
            }

            #ChapaAPI requires a secret key for authentication so we put it in the headers
            
            headers = {
                "Authorization": f"Bearer {chapa_secret_key}",
                "Content-Type": "application/json"
            }

            try:
                chapa_response = requests.post("https://api.chapa.co/v1/transaction/initialize",
                        json=payload,
                        headers=headers
                )
                chapa_data = chapa_response.json().get('data', {})

                # check for success in status_code and retrieve the checkout URL
            
                if chapa_response.status_code == 200 and chapa_data.get('status') == 'success':
                    
                    # if sucessful, get the checkout url
                    
                    checkout_url = chapa_data.get('checkout_url')
                    
                    if checkout_url:
                
                    # 1- save the trx_ref
                    # 2- Return a json response to the frontend.
                    #    They will redirect the user to the payment gateway's checkout url
                    
                        payment.trx_ref = trx_ref
                        payment.save()
                        return Response({
                            "payment_id": payment.payment_id,
                            "amount": str(booking.total_price),
                            "checkout_url": checkout_url,
                            "trx_ref": trx_ref,
                            })
                    else:
                        return Response({'Error: No checkout URL gotten from Chapa'},status=500)
                else:
                    # if failed, set status to failed
                    payment.status = 'Failed'
                    payment.save()
                    return Response({"error": "Payment initiation failed"},
                                    status=chapa_response.status_code)
            except requests.RequestException as e:
                payment.status = 'Failed'
                payment.save()
                return Response({"error": "Failed to connect to Chapa API",},
                                status=500)        


class PaymentCallbackView(views.APIView):
    """ this is to recieve the callback data
      from ChapaAPI after the user has completed the payment."""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, args, **kwargs):
        #reteieve callback data
        status = request.query_params.get('status')
        trx_ref = request.query_params.get('tx_ref')
        ref_id = request.query_params.get('ref_id')

        if not all([status, trx_ref, ref_id]):
            return Response({"error": "Missing required parameters"}, status=400)
        # get the payment with the matching trx_ref
        try:
            payment = Payment.objects.get(trx_ref=trx_ref, chapa_trx_ref=ref_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)
        
        # dave the chapa_trx_ref and update the status
        payment.chapa_trx_ref = ref_id
    

class VerifyPaymentView(views.APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # get chapas trx ref from request 
        chapa_trx_ref = request.query_params.get('trx_ref')
        if not chapa_trx_ref:
            return Response({"error": "Transaction reference is required"}, status=400)
        
        # get the payment with the matching chapa_trx_ref
        try:
            payment = Payment.objects.get(trx_ref=trx_ref, chapa_trx_ref=ref_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)
        
        # conacatenate verification url with the transaction reference
        verification_url = f"https://api.chapa.co/v1/transaction/verify/{chapa_trx_ref}"
        
        # put  chapa secret key in the headers
        headers= {
            'Authorization': "f Bearer {chapa_secret_key}"
        }
        # send verification request
        try:
            response = requests.get(verification_url, headers=headers)

            if chapa_response.status_code == 200 and chapa_data.get('status') == 'success':
            # if successful, update the payment status
                payment.status = 'Completed'
                payment.save()
                return Response({"message": "Payment verified successfully",
                                 "payment_id": payment.payment_id,
                                 "status": payment.status}, status=200)
            else:
                # if failed, set status to failed
                payment.status = 'Failed'
                payment.save()
                return Response({"error": "Invalid Transaction or transaction not found"},
                                status=response.status_code)
                
                # there should be some deletion in the db her i think
        
        except requests.RequestException as e:
            payment.status = 'Failed'
            payment.save()
            return Response({"error": "Failed to connect to Chapa API",},
                            status=500)  
        
