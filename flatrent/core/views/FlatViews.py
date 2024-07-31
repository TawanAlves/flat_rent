from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from core import models
from ..serializer import FlatSerializer, BookingSerializer


from django.utils import timezone
# from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError


class FlatViewSet(viewsets.ViewSet):
    # def list(self, request):
    #     """
    #     GET /flats/
    #     List all flats.
    #     """
    #     flats = models.Flat.objects.all()
    #     serializer = FlatSerializer(flats,  many=True)
    #     return Response(serializer.data)
    def list(self, request):
        """
        GET /flats/
        """
        bookings = models.Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """"
        GET /flats/{pk}
        """
        try:
            booking = models.Booking.objects.get(pk=pk)
        except models.Booking.DoesNotExist:
            return Response(status=status.HTTP_400_NOT_FOUND)

        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    def create(self, request):
        """
        POST /flats

        -tudo certo - ok
        -mesmo dia- ok, erro aparecendo
        -data aterior - ok, erro aparecendo
        -data passada - ok, erro aparecendo


        """
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        PUT /flats/{pk}/
        """
        try:
            booking = models.Booking.objects.get(pk=pk)
        except models.Booking.DoesNotExist:
            return Response(status=status.HTTP_400_NOT_FOUND)

        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        DELETE /flats/{pk}/
        """
        try:
            booking = models.Booking.objects.get(pk=pk)
        except models.Booking.DoesNotExist:
            return Response(status=status.HTTP_400_NOT_FOUND)

        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
