from django.urls import path

from MGA import views
from MGA.view import UserViews

app_name = 'MGA'

urlpatterns = [
    path('confirm/<int:id>/', views.confirm_email, name='confirm'),
    path('allUsers/', UserViews.UserList.as_view(), name="users"),

    path('events/', views.EventList.as_view(), name='event_list'),
    path('events/<int:pk>', views.event_details, name='event_details'),
    path('organizations/', views.OrganizationList.as_view(), name='organizations_list')
]
