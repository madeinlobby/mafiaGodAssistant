from django.urls import path

from MGA import views
from MGA.view import UserViews

app_name = 'MGA'

urlpatterns = [
    path('confirm/<int:id>/', views.confirm_email, name='confirm'),
    path('getUsers/', UserViews.UserList.as_view(), name="users"),
    path('create/', UserViews.User_G_D.as_view(), name='create'),
    path('events/', views.event_list, name='event_list')
]
