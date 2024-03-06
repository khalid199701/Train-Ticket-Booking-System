from django.db import models
from passenger.models import Passenger
from django.db.models.signals import post_save
from station.models import Station
from django.dispatch import receiver
# Create your models here.
class Train(models.Model):
    train_name = models.CharField(max_length = 100)
    description = models.TextField(blank=True, null=True)
    seat_count = models.IntegerField()
    seat_fair = models.IntegerField()
    station = models.ForeignKey(Station, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    
    def __str__(self):
        return self.train_name
    

@receiver(post_save, sender=Train)
def create_seat_numbers(sender, instance, created, **kwargs):
    if created:
        # Create SeatNumber instances for each seat in the train
        for seat_number in range(1, instance.seat_count + 1):
            SeatNumber.objects.create(train=instance, seat_number=seat_number)

class SeatNumber(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    is_taken = models.BooleanField(default = False)
    passenger = models.OneToOneField(Passenger, on_delete=models.CASCADE, null = True, blank = True)
    def __str__(self):
        return f"{self.train.train_name} - Seat {self.seat_number}"
    
    
class Review(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name = 'reviews')
    passenger = models.ForeignKey(Passenger, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return f"Reviewed by {self.name}"