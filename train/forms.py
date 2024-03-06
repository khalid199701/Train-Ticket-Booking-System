from django import forms
from .models import Train, Review

class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'body']