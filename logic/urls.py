from django.urls import path

from logic import views

app_name = 'logic'

urlpatterns = [
    path('createGame/', views.create_game, name='create_game'),
    path('getRoles/', views.get_all_roles, name='get_all_roles'),
    path('setRoles/', views.set_game_role, name='set_game_role'),


]
