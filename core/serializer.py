from rest_framework import serializers
from .models import Flat, Booking


class FlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flat
        fields = ['id', 'nome']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'flat', 'checkin', 'checkout']
