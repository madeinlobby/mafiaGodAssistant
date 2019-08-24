from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

from MGA import views

urlpatterns = [
    #    path('admin/', admin.site.urls, name='admin'),
    path('api/token/', obtain_jwt_token, name='token_obtain_pair'),
    path('admin/', admin.site.urls, name='admin'),
    path('mga/', include('MGA.urls'), name='MGA'),

    path('resetPassword/', views.reset_password, name='reset_password'),
    path('changPassword/', views.change_password, name='change_password'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup')
]
