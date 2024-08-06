import os
import subprocess
from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from core import models
from django.utils.dateparse import parse_date
from ..serializer import FlatSerializer, BookingSerializer
from core.services import svc_pdf
from core.task import generate_and_send_pdf_task

from django.utils import timezone
# from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError


class FlatViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        GET /flats/
        """
        bookings = models.Booking.objects.all().order_by('id')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def byorder(self, request):
        """
        GET /flats/byorder/
        """
        bookings = models.Booking.objects.all().order_by('flat_id', 'checkin')
        serialized_data = []
        current_flat_id = None
        current_order = 0
        for booking in bookings:
            if booking.flat_id != current_flat_id:
                current_flat_id = booking.flat_id
                current_order = 1
            else:
                current_order += 1
            booking_data = BookingSerializer(booking).data
            booking_data['ordem'] = current_order
            serialized_data.append(booking_data)
        return Response(serialized_data)

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

    @action(detail=False, methods=["get"])
    def allflats(self, request):
        """
        GET flats/allflats/
        """
        flats = models.Flat.objects.all()
        serializer = FlatSerializer(flats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def available_flats(self, request):
        """
        GET /flats/available_flats/?checkin=YYYY-MM-DD&checkout=YYYY-MM-DD
        """
        # TODO: repeated
        checkin_date = request.GET.get('checkin')
        checkout_date = request.GET.get('checkout')

        if not checkin_date or not checkout_date:
            return Response({'error': 'Por favor, forneça as datas de checkin e checkout.'}, status=status.HTTP_400_BAD_REQUEST)

        checkin_date = parse_date(checkin_date)
        checkout_date = parse_date(checkout_date)

        if not checkin_date or not checkout_date:
            return Response({'error': 'Datas inválidas.'}, status=status.HTTP_400_BAD_REQUEST)

        booked_flats = models.Booking.objects.filter(
            checkin__lt=checkout_date,
            checkout__gt=checkin_date
        ).values_list('flat_id', flat=True)

        available_flats = models.Flat.objects.exclude(id__in=booked_flats)

        serializer = FlatSerializer(available_flats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def send_pdf(self, request):
        """
        POST /flats/send_pdf/
        """
        email = request.data.get('email')
        flatIds = request.data.get('flatIds')

        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not flatIds:
            return Response({'error': 'Flat IDs are required.'}, status=status.HTTP_400_BAD_REQUEST)

        generate_and_send_pdf_task.delay(email, flatIds)

        return Response({'message': 'PDF generation and email sending initiated.'}, status=status.HTTP_200_OK)


# TODO: create pagination, add logic to many data
