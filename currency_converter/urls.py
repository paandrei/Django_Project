
from django.urls import path
from currency_converter import views

urlpatterns = [
    path("exchange", views.show, name='exchange'),
]