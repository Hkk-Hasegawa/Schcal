from django.urls import path
from . import views

urlpatterns = [
    path('', views.monthcal, name='monthcal'),
    
]