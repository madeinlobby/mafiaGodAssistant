from django.urls import path

from logic import views

app_name = 'logic'

urlpatterns = [
    path('creat_game/', views.create_game, name='create_game'),
    path('get_roles/', views.get_all_roles, name='get_all_roles'),
    path('set_roles/', views.set_game_role, name='set_game_role'),
    path('day_to_night/', views.day_to_night, name='day_to_night'),
    path('set_night_aim/', views.set_night_aims, name='set_night_aim'),
    path('night_to_day/', views.night_to_day, name='night_to_day'),
    path('speech/', views.speech_for_start_game, name='speech_for_start'),
    path('get_players_except_role', views.get_players_except_one, name='get_all_except_one_role'),
    path('ask_q/', views.ask_god, name='ask_god'),

]
