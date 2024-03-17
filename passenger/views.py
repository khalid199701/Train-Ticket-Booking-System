from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import UserRegistrationForm, UserUpdateForm, ChangeUserForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, update_session_auth_hash, logout
from .models import Passenger, Transaction
from django.views.generic import CreateView, ListView
from passenger.forms import DepositForm, TransactionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView
from train.models import SeatNumber
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

def profile(request):
    try:
        user = Passenger.objects.get(user=request.user)
        booked_seats = SeatNumber.objects.filter(passenger = user)
        balance = user.balance
    except Passenger.DoesNotExist:
        user = None
        booked_seats = None
        balance = None
    
    context = {
        'user': user,
        'booked_seats': booked_seats,
        'balance': balance,
    }
    return render(request, 'profile.html', context)

class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')


    def form_valid(self, form):
        user = form.save()
        user.is_active = False  
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        current_site = get_current_site(self.request)
        confirm_link = f"http://127.0.0.1:8000/passenger/active/{uid}/{token}"

        email_subject = "Confirm Your Email"
        email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
        to_email = form.cleaned_data.get('email')
        email = EmailMultiAlternatives(email_subject, email_body, to=[to_email])
        email.send()
        message = "Check your mail for confirmation"
        return HttpResponseRedirect("http://127.0.0.1:8000/passenger/login/")


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        Passenger.objects.create(user=user, balance = 0)
        return redirect('login') 
    else:
        return redirect('register')

class UserLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('login')
    
class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user
        })
        return kwargs

class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        user = get_object_or_404(User, user=self.request.user)
        passenger = get_object_or_404(Passenger, user=user)
        transaction = Transaction.objects.create(account=passenger, amount=amount)
        passenger.balance += amount
        passenger.save(
            update_fields=[
                'balance'
            ]
        )
        return super().form_valid(form)
    
class EditProfile(UpdateView):
    form_class = ChangeUserForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'
    def get_object(self, queryset=None):
        return self.request.user
    
def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    
    else:
        form = PasswordChangeForm(user = request.user)
    return render(request, 'pass_change.html', {'form': form})