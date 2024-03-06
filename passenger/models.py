from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Passenger(models.Model):
    user = models.OneToOneField(User, related_name = 'account', on_delete = models.CASCADE)
    nid = models.IntegerField(unique = True, null = True, blank = True)
    balance = models.DecimalField(default = 0, decimal_places = 2, max_digits = 12)
    def __str__(self):
        return self.user.first_name
    
class Transaction(models.Model):
    account = models.ForeignKey(Passenger, on_delete= models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12, null = True)
    timestamp = models.DateTimeField(auto_now_add = True)
    class Meta:
        ordering = ['timestamp']