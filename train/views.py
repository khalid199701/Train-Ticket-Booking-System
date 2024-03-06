from django.shortcuts import render, redirect
from . import forms
from . import models
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.
@login_required
def seatBook(request, id):
    seat_no = models.SeatNumber.objects.get(id = id)
    passenger = request.user.account
    train = seat_no.train
    if not seat_no.passenger:
        if passenger.balance >= train.seat_fair:  # Access seat_fair from the train object
            m = passenger.balance
            passenger.balance -= train.seat_fair  # Deduct fare from passenger's balance
            passenger.save()
            seat_no.passenger = passenger
            seat_no.is_taken = True
            seat_no.save()
            messages.success(request, "Seat booked successfully.")
        else:
            messages.error(request, "Insufficient balance to book the seat.")
    else:
        messages.error(request, "Seat already booked.")

    return redirect('profile')

class DetailTrainView(View):
    template_name = 'train_details.html'

    def get_object(self):
        train_id = self.kwargs.get('id')
        return get_object_or_404(models.Train, id=train_id)

    def get(self, request, *args, **kwargs):
        train_id = self.kwargs.get('id')
        train = models.Train.objects.get(id=train_id)
        seat_numbers = train.seatnumber_set.all()
        review_form = forms.ReviewForm()
        reviews = train.reviews.all()

        context = {
            'train': train,
            'seat_numbers': seat_numbers,
            'review_form': review_form,
            'reviews': reviews,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data=self.request.POST)
        train = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            user_account = request.user.account
            if models.SeatNumber.objects.filter(passenger = user_account):
                new_review.passenger = user_account
                new_review.name = user_account.user.first_name
                new_review.email = user_account.user.email

                new_review.train = train  
                new_review.save()
            else:
                messages.warning("You have to be a passenger to review")
            
        return self.get(request, *args, **kwargs)
    
