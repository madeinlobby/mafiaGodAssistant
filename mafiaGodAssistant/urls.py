from django.contrib import admin
from django.urls import path, include

from MGA import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('mga/', include('MGA.urls'), name='MGA'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup_user, name='signup')
]
