from django.urls import path
from . import views
from .views import RegistrationView, LoginView, LogoutView, ProfileView

urlpatterns = [
    path('api/accounts/registration', views.RegistrationView.as_view(), name='RegistrationView'),
    path('api/accounts/login', views.LoginView.as_view(), name='LoginView'),
    path('api/accounts/logout', views.LogoutView.as_view(), name='LogoutView'),
    path('api/accounts/profile', views.ProfileView.as_view(), name='SignupView'),
]