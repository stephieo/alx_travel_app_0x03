from django.db import models
import uuid
from datetime import datetime
# Create your models here.


class User(models.Model):
    USER_TYPES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin')
    ]
    user_id = models.UUIDField(primary_key=True,
                               default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    password_hash = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250, null=True)
    role = models.CharField(max_length=100, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)


class Listing(models.Model):
    listing_id = models.UUIDField(primary_key=True,
                                  default=uuid.uuid4, editable=False)
    host = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    location = models.CharField(max_length=250)
    max_guests = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        Pending = 'pending', 'Pending'
        Confirmed = 'confirmed', 'Confirmed'
        Cancelled = 'cancelled', 'Cancelled'

    booking_id = models.IntegerField(primary_key=True,
                                     default=uuid.uuid4, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=BookingStatus.choices)
    booked_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    class Ratings(models.IntegerChoices):
        """NAME = database_value, "display_value
                NAME: Python identifier (constant name) you use in your code"""
        ONE = 1, '1'
        TWO = 2, '2'
        THREE = 3, '3'
        FOUR = 4, '4'
        FIVE = 5, '5'
    
    review_id = models.IntegerField(primary_key=True,
                                    default=uuid.uuid4, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=Ratings.choices)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'credit_card', 'Credit Card'
        PAYPAL = 'paypal', 'PayPal'
        BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
    
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    payment_id = models.IntegerField(primary_key=True,
                                     default=uuid.uuid4, editable=False)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    trx_ref = models.CharField(max_length=100, unique=True, blank=True, null=True)
    chapa_trx_ref = models.CharField(max_length=100, unique=True, blank=True, null=True)
    payment_status = models.CharField(max_length=100, choices=PaymentStatus.choices)

    def generate_trx_ref(self):
        """Generates a unique transaction reference for the payment."""
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"PAY-{self.payment_id}-{now}-{uuid.uuid4().hex[:8].upper()}"

