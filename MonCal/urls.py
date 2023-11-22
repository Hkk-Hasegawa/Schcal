from django.contrib.auth.views import LoginView, LogoutView 
from django.urls import path
from . import views

app_name = 'MonCal'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home_page'),
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('Sure/<int:pk>/property/calendar/', views.PropertyCalendar.as_view(), name='calendar'),
    path('Sure/<int:pk>/property/calendar/<int:year>/<int:month>/<int:day>/', views.PropertyCalendar.as_view(), name='calendar'),
    path('Sure/<int:pk>/property/', views.PropertyList.as_view(), name='property_list'),
    
    path('Sure/<int:pk>/event/calendar/', views.EventCalendar.as_view(), name='eventcalendar'),
    path('Sure/<int:pk>/event/calendar/<int:year>/<int:month>/<int:day>/', views.EventCalendar.as_view(), name='eventcalendar'),
    path('Sure/<int:pk>/event/', views.EventList.as_view(), name='event_list'),

    path('Property/<int:pk>/detail',views.PropertyDetail.as_view(), name='Property_detail'),
    path('Property/<int:pk>/detail/edit',views.PropertyEdit.as_view(), name='Property_edit'),
    path('Property/<int:pk>/detail/edit/<int:year>/<int:month>/<int:day>/',views.PropertyEdit.as_view(), name='Property_edit'),
    path('Property/<int:pk>/delete/', views.PropertyDelete.as_view(), name='Property_delete'),
    
]