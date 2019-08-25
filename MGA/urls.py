from django.urls import path

from MGA import views
from MGA.view import UserViews, EventViews

app_name = 'MGA'

urlpatterns = [
    path('confirm/<int:id>/', views.confirm_email, name='confirm'),
    path('allUsers/', UserViews.UserList.as_view(), name="users"),
    path('friendRequest/', views.send_friendship_request, name='send_friend_request'),
    path('friendAccept/', views.accept_friendship_request, name='accept_friend_request'),
    path('notifications/', views.get_not_read_notification, name='getNotification'),

    path('events/', EventViews.EventList.as_view(), name='event_list'),
    path('events/<int:pk>', EventViews.event_details, name='event_details'),
    path('organizations/', EventViews.OrganizationList.as_view(), name='organizations_list')
]
