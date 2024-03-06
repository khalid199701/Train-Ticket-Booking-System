from django.db import models
from passenger.models import Passenger
from train.models import Train, SeatNumber
# Create your models here.

class SeatBooking(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat_number = models.OneToOneField(SeatNumber, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.passenger.user.username} - {self.train.train_name} - Seat {self.seat_number}"
