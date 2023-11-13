from django.contrib.auth.views import LoginView, LogoutView 
from django.urls import path
from . import views

app_name = 'MonCal'

urlpatterns = [
    path('', views.Surelist.as_view(), name='suresubject_list'),
    path('Sure/<int:pk>/calendar/', views.SureCalendar.as_view(), name='calendar'),
    path('Sure/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', views.SureCalendar.as_view(), name='calendar'),
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mypage/', views.MyPage.as_view(), name='my_page'),
    path('mypage/<int:pk>/', views.MyPageWithPk.as_view(), name='my_page_with_pk'),
    path('Event/<int:pk>/detail',views.EventDetail.as_view(), name='Event_detail'),
    path('Event/<int:pk>/detail/edit',views.EventEdit.as_view(), name='Event_edit'),
    path('Event/<int:pk>/detail/edit/<int:year>/<int:month>/<int:day>/',views.EventEdit.as_view(), name='Event_edit'),
    path('Event/<int:pk>/delete/', views.EventDelete.as_view(), name='Event_delete'),
]