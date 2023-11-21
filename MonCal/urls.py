from django.contrib.auth.views import LoginView, LogoutView 
from django.urls import path
from . import views

app_name = 'MonCal'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home_page'),
    path('Sure/<int:pk>/calendar/', views.SureCalendar.as_view(), name='calendar'),
    path('Sure/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', views.SureCalendar.as_view(), name='calendar'),
    path('Sure/<int:pk>/subject/', views.ScheduleList.as_view(), name='schedule_list'),
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('Property/<int:pk>/detail',views.PropertyDetail.as_view(), name='Property_detail'),
    path('Property/<int:pk>/detail/edit',views.PropertyEdit.as_view(), name='Property_edit'),
    path('Property/<int:pk>/detail/edit/<int:year>/<int:month>/<int:day>/',views.PropertyEdit.as_view(), name='Property_edit'),
    path('Property/<int:pk>/delete/', views.PropertyDelete.as_view(), name='Property_delete'),
    
]