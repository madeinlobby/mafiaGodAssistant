from django.urls import path

from logic import views

app_name = 'logic'

urlpatterns = [
    path('createGame/', views.create_game, name='create_game'),
    path('getRoles/', views.get_all_roles, name='get_all_roles'),
    path('setRoles/', views.set_game_role, name='set_game_role'),
    path('dayToNight/', views.day_to_night, name='day_to_night'),
    path('setNightAim/', views.set_night_aims, name='set_night_aim'),
    path('nightToDay/', views.night_to_day, name='night_to_day'),

]
