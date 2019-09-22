from django.urls import path

from MGA import views
from MGA.view import UserViews, EventViews, CafeViews

app_name = 'MGA'

urlpatterns = [
    path('confirm/<int:id>/', views.confirm_email, name='confirm'),
    path('all_users/', UserViews.UserList.as_view(), name="users"),
    path('friend_request/', views.send_friendship_request, name='send_friend_request'),
    path('friend_accept/', views.accept_friendship_request, name='accept_friend_request'),
    path('notifications/', views.get_not_read_notification, name='getNotification'),
    path('create_org/', EventViews.add_organization, name='create_organization'),
    path('add_admin/', EventViews.add_admins, name='add_admin'),
    path('add_event/', EventViews.add_event, name='add_event'),
    path('cafe/', CafeViews.create_cafe, name='create_cafe'),
    path('public_events', EventViews.get_public_events, name="public_events"),
    path('join_event/<int:id>', EventViews.join_event, name='join_event'),
    path('add_member/', EventViews.add_member, name='add_member'),
    path('get_public_events/', EventViews.get_public_events, name='get_public_event'),
    path('get_authenticated_orgs/', EventViews.get_authenticated_organization, name='get_authenticated_orgs'),
    path('get_org_events/', EventViews.get_all_events_for_organization, name='get_org_events'),
    path('get_user_fields/', UserViews.get_user_fields, name='get_user_fields'),
    path('get_event_fields/', EventViews.get_event_fields, name='get_event_fields'),
    path('get_org_fields/', EventViews.get_organization_fields, name='get_org_fields'),
    path('search_event/', EventViews.search_event, name='search_event'),

    path('events/', EventViews.EventList.as_view(), name='event_list'),
    path('events/<int:pk>', EventViews.event_details, name='event_details'),
    path('organizations/', EventViews.OrganizationList.as_view(), name='organizations_list')
]
