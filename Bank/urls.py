from django.contrib import admin
from django.urls import path
from Bank import views

urlpatterns = [
    path("", views.homepage, name='homepage_bank'),
    path("feedback", views.feedback, name='feedback'),
    path("SignUp", views.SignUp, name='SignUp'),
    path("LogIn", views.LogIn, name='LogIn'),
    path('LogIn-Active', views.login_active, name='login-active'),
    path("LogIn-Active/actions", views.deposit, name='deposit'),
    path("LogIn-Active/actions", views.withdraw, name='withdraw'),
    path("LogIn-Active/actions", views.transfer, name='transfer'),
    path("LogIn-Active/register", views.register, name='register'),

]