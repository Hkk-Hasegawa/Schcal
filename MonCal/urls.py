from django.contrib.auth.views import LoginView, LogoutView 
from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'MonCal'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('', views.HomePage.as_view(), name='home_page'),
    
    path('setting/Time/', views.TimeListView.as_view(), name='Booking_time_list'),
    path('setting/Time/<int:pk>', views.TimeUpdate.as_view(), name='time_update'),

    path('workingday/', views.Workingdaylist.as_view(), name='Working_day_list'),
    path('workingday/set/', views.SetWorkingday.as_view(), name='set_workingday'),
    path('workingday/set/<int:year>/<int:month>', views.SetWorkingday.as_view(), name='set_workingday'),
    path('workingday/<int:pk>/delete/', views.WorkingdayDelete.as_view(), name='delete_working'),

    path('calendar/year', views.Sche_year_calendar.as_view(), name='year_calendar'),
    path('calendar/year/<int:year>/<int:month>/<int:day>/', views.Sche_year_calendar.as_view(), name='year_calendar'),

    path('property/<int:pk>/detail/',views.PropertyDetail.as_view(), name='Property_detail'),
    path('property/<int:pk>/detail/delete/', views.PropertyDelete.as_view(), name='Property_delete'),
    path('property/<int:pk>/list/', views.PropertyList.as_view(), name='property_list'),
    path('property/<int:pk>/calendar/', views.PropertyCalendar.as_view(), name='property_calendar'),
    path('property/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', views.PropertyCalendar.as_view(), name='property_calendar'),
    path('property/<int:pk>/edit/', views.PropertyEdit.as_view(), name='property_edit'),
    path('property/<int:pk>/edit/<int:year>/<int:month>/<int:day>/', views.PropertyEdit.as_view(), name='property_edit'),

    path('event/list/<int:year>/', views.EventList.as_view(), name='event_list'),
    path('event/list/', views.EventList.as_view(), name='event_list'),
    path('event/calendar/', views.EventCalendar.as_view(), name='eventcalendar'),
    path('event/calendar/<int:year>/<int:month>/<int:day>/', views.EventCalendar.as_view(), name='eventcalendar'),
    path('event/detail/<int:pk>/',views.EventDetail.as_view(), name='Event_detail'),
    path('event/detail/edit/<int:pk>/',views.EventEdit.as_view(), name='Event_edit'),
    path('event/detail/edit/<int:pk>/<int:year>/<int:month>/<int:day>/',views.EventEdit.as_view(), name='Event_edit'),
    path('event/detail/<int:pk>/delete/', views.EventDelete.as_view(), name='Event_delete'),
    path('event/cycle/detail/<int:pk>/<int:year>/<int:month>/<int:day>/',views.EventCycleEdit.as_view(), name='event_cycle_edit'),
    path('event/cycle/delete/<int:pk>/',views.EventCycleDelete.as_view(), name='event_cycle_delete'),
    
]