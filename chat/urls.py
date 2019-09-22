from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('send_one/', views.send_to_one, name='send_to_one'),
    path('send_group/', views.send_to_group, name='send_to_group'),
    path('create_group/', views.create_group, name='create_group'),
    path('create_reply/', views.create_reply, name='create_reply'),
    path('delete_message/<int:id>', views.DestroyUpdateMessageView.as_view(), name='delete_message'),
    path('delete_group/<int:id>', views.DestroyUpdateGroupView.as_view(), name='delete_group'),
    path('delete_reply/<int:id>', views.DestroyUpdateReplyView.as_view(), name='delete_reply'),
    path('edit_message/', views.edit_message, name='edit_message'),
    path('edit_reply/', views.edit_Reply, name='edit_reply'),
    path('get_message/<int:id>', views.RetrieveMessageView.as_view(), name='get_message'),
    path('get_reply/<int:id>', views.RetrieveMessageView.as_view(), name='get_reply'),
]
