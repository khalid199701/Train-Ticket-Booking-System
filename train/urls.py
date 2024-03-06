from django.urls import path
from . import views

urlpatterns = [
    path('details/<int:id>/', views.DetailTrainView.as_view(), name='detail_train'),
    path('details/book/<int:id>/', views.seatBook, name='seatBook'),
]
