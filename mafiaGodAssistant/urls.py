from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

from MGA import views
from MGA.view import UserViews

urlpatterns = [
    #    path('admin/', admin.site.urls, name='admin'),
    path('api/token/', obtain_jwt_token, name='token_obtain_pair'),
    path('admin/', admin.site.urls, name='admin'),
    path('mga/', include('MGA.urls'), name='MGA'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', UserViews.post_user, name='signup')
]
