from django.shortcuts import render
from train.models import Train
from station.models import Station

def home(request, station_slug = None):
    data = Train.objects.all()
    if station_slug is not None:
        station = Station.objects.get(slug = station_slug)
        data = Train.objects.filter(station = station)
    stations = Station.objects.all()
    return render(request, 'home.html', {'data': data, 'station': stations})