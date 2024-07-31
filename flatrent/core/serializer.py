from rest_framework import serializers
from .models import Flat, Booking
from django.core.exceptions import ValidationError
from datetime import datetime


class FlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flat
        fields = ['id', 'nome']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'flat', 'checkin', 'checkout']

    def validate(self, data):

        checkin = data.get('checkin')
        checkout = data.get('checkout')

        if checkin and checkout and checkin >= checkout:
            raise serializers.ValidationError(
                "Cheking have to be before checkout")

        if checkin and checkin < datetime.now().date():
            raise serializers.ValidationError(
                "Invalid date, we cannot go back to past ... yet")

        if checkin and checkout:
            two_bookings = Booking.objects.filter(
                flat=data['flat'],
                checkin__lt=checkout,
                checkout__gt=checkin,
            )
            if two_bookings.exists():
                raise serializers.ValidationError("Flat is already occupied")

        return data
