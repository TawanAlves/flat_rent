from django.db import models


class Booking(models.Model):
    flat = models.ForeignKey(
        'Flat', on_delete=models.CASCADE, related_name='booking')
    checkin = models.DateField(null=True, blank=True)
    checkout = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self. flat}'
