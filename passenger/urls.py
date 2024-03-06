from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/edit', views.EditProfile.as_view(), name='edit_profile'),
    path('profile/pass_change/', views.pass_change, name='pass_change'),
    path('deposit/', views.DepositMoneyView.as_view(), name='deposit_money'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
]
