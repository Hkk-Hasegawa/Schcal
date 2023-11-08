from django.urls import path
from . import views

app_name = 'MonCal'

urlpatterns = [
    path('', views.Surelist.as_view(), name='suresubject_list'),
    path('Sure/<int:pk>/calendar/', views.SureCalendar.as_view(), name='calendar'),
    path('Sure/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', views.SureCalendar.as_view(), name='calendar'),
    path('Sure/<int:pk>/booking/<int:year>/<int:month>/<int:day>/<str:time>/', views.Booking.as_view(), name='booking'),
]