from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('sendOne/', views.send_to_one, name='send_to_one'),
    path('sendGroup/', views.send_to_group, name='send_to_group'),
    path('createGroup/', views.create_group, name='create_group'),
    path('createReply/', views.create_reply, name='create_reply'),
    path('deleteMessage/<int:id>', views.DestroyUpdateMessageView.as_view(), name='delete_message'),
    path('deleteGroup/<int:id>', views.DestroyUpdateGroupView.as_view(), name='delete_group'),
    path('deleteReply/<int:id>', views.DestroyUpdateReplyView.as_view(), name='delete_reply'),
    path('editMessage/', views.edit_message, name='edit_message'),
    path('editReply/', views.edit_Reply, name='edit_reply'),
    path('getMessage/<int:id>', views.RetrieveMessageView.as_view(), name='get_message'),
    path('getReply/<int:id>', views.RetrieveMessageView.as_view(), name='get_reply'),
]
