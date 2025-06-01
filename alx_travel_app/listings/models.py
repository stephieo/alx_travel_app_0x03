from django.db import models
import uuid
# Create your models here.


class User(models.Model):
    USER_TYPES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('Admin', 'admin')
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
    host_id = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    location = models.CharField(max_length=250)
    max_guests = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    BOOKING_STATUSES = [
        ('pending', 'pending')
        ('confirmed', 'confirmed')
        ('cancelled', 'cancelled')
    ]
    booking_id = models.IntegerField(primary_key=True,
                                     default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    listing_id = models.ForeignKey('Listing', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=BOOKING_STATUSES)
    booked_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    RATINGS = [(x, x) for x in range(5)]
    review_id = models.IntegerField(primary_key=True,
                                    default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    listing_id = models.ForeignKey('Listing', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATINGS)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
