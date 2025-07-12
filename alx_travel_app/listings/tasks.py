from celery import shared_task
from django .core.mail import send_mail
from django.conf import settings


# shared tasks are not tied to a specific app,
# this means that you can call a task "foo.delay(bar)" from anywhere and celery will handle tha task
@shared_task
def send_booking_confirmation_mail(booking_id, user_email,
                               user_name, booking_date, listing_name):
    
    subject = f'Booking Confirmation - {booking_id}'
    message = f"""
    Dear {user_name},

    You've successfully booked a stay at {listing_name}!

    Booking Details:
    - Booking ID: {booking_id}
    - Listing: {listing_name}
    - Date: {booking_date}

    We'll send you a reminder closer to the date. If you need to cancel or modify your booking,
    please contact us at {settings.DEFAULT_FROM_EMAIL}.

    Best regards,
    Your App Team
    """"

    send_mail(
           subject=subject,
           message=message,
           from_email=settings.DEFAULT_FROM_EMAIL,
           recipient_list=[user_email],
           fail_silently=False,
       )
    return f"Confirmation email sent for booking {booking_id} to {user_email}"


