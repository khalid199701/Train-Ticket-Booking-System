from django.contrib import admin
from .models import Train, Review, SeatNumber
# Register your models here.
admin.site.register(Train)
admin.site.register(SeatNumber)
admin.site.register(Review)