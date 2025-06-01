from rest_framework import serializers
from .models import Listing, Booking

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        ''' this  identifies which model the serializer is tied to and the fields  to (de)serialize'''
        model = Listing
        fields = '__all__'
        read_only_fields = ['listing_id', 'user_id','created_at']
    
    # def validate_title(self, value):
    #     if not value.strip():
    #         raise serializers.ValidationError("Title cannot be empty")

    # def validate_description(self, value):
    #     if not value.strip():
    #         raise serializers.ValidationError("Description cannot be empty")

    # def validate_destination(self, value):
    #     if not value.strip():
    #         raise serializers.ValidationError("Destination cannot be empty")

    # def validate_price(self, value):
    #     if value < 0:
    #         raise serializers.ValidationError("price  must be greater than 0")

    # def validate(self, data):
    #     if data['end_date'] < data['start_date']:
    #         raise serializers.ValidationError("Start date must occur before end date")


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = [ 'user_id', 'listing_id', 'booked_at']

    # def validate_totalprice(self, value):
        # if value < 0:
            # raise serializers.ValidationError("price  must be greater than 0")

