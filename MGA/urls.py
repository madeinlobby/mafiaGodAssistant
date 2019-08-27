from django.urls import path

from MGA import views
from MGA.view import UserViews, EventViews, CafeViews

app_name = 'MGA'

urlpatterns = [
    path('confirm/<int:id>/', views.confirm_email, name='confirm'),
    path('allUsers/', UserViews.UserList.as_view(), name="users"),
    path('friendRequest/', views.send_friendship_request, name='send_friend_request'),
    path('friendAccept/', views.accept_friendship_request, name='accept_friend_request'),
    path('notifications/', views.get_not_read_notification, name='getNotification'),
    path('createOrg/', EventViews.add_organization, name='create_organization'),
    path('add_admin/', EventViews.add_admins, name='add_admin'),
    path('addEvent/', EventViews.add_event, name='add_event'),
    path('cafe/', CafeViews.create_cafe, name='create_cafe'),
    path('publicEvents', EventViews.get_public_events, name="public_events"),
    path('joinEvent/<int:event_id>', EventViews.join_event, name='join_event'),


    path('events/', EventViews.EventList.as_view(), name='event_list'),
    path('events/<int:pk>', EventViews.event_details, name='event_details'),
    path('organizations/', EventViews.OrganizationList.as_view(), name='organizations_list')
]
