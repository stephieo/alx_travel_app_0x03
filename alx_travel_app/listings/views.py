from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
# Create your views here.

class ListingViewSet(viewsets.ModelViewSet):
    """This class contains all the varous views connected to the CRUD actions for this model.
    the basic setup is specifying the queryset to use for any returned data and the serializer handling any input/output"""
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """This class contains all the varous views connected to the CRUD actions for this model.
    the basic setup is specifying the queryset to use for any returned data and the serializer handling any input/output"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

