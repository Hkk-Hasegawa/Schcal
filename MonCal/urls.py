from django.contrib.auth.views import LoginView, LogoutView 
from django.urls import path
from . import views

app_name = 'MonCal'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home_page'),
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('setting/Time', views.TimeListView.as_view(), name='Booking_time_list'),
    path('setting/Time/<int:pk>', views.TimeUpdate.as_view(), name='time_update'),

    path('property/<int:pk>/', views.PropertyList.as_view(), name='property_list'),
    path('property/<int:pk>/calendar/', views.PropertyCalendar.as_view(), name='calendar'),
    path('property/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', views.PropertyCalendar.as_view(), name='calendar'),
    path('property/<int:subject_pk>/detail/<int:pk>/',views.PropertyDetail.as_view(), name='Property_detail'),
    path('property/<int:subject_pk>/detail/<int:pk>/edit',views.PropertyEdit.as_view(), name='Property_edit'),
    path('property/<int:subject_pk>/detail/<int:pk>/edit/<int:year>/<int:month>/<int:day>/',views.PropertyEdit.as_view(), name='Property_edit'),
    path('property/<int:subject_pk>/detail/<int:pk>/delete/', views.PropertyDelete.as_view(), name='Property_delete'),
    
    path('event/<int:pk>/', views.EventList.as_view(), name='event_list'),
    path('event/<int:pk>/calendar/', views.EventCalendar.as_view(), name='eventcalendar'),
    path('event/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', views.EventCalendar.as_view(), name='eventcalendar'),
    path('event/<int:event_pk>/detail/<int:pk>/',views.EventDetail.as_view(), name='Event_detail'),
    path('event/<int:event_pk>/detail/edit/<int:pk>/',views.EventEdit.as_view(), name='Event_edit'),
    path('event/<int:event_pk>/detail/edit/<int:pk>/<int:year>/<int:month>/<int:day>/',views.EventEdit.as_view(), name='Event_edit'),
    path('event/<int:event_pk>/detail/<int:pk>/delete/', views.EventDelete.as_view(), name='Event_delete'),
]