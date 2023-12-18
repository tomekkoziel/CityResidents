from django.urls import path
from .views import city_list, person_list, index, list_cities_and_users

app_name = 'city_residents_app'

urlpatterns = [
    path('', index, name='index'),
    path('cities/', city_list, name='city_list'),
    path('people/', person_list, name='person_list'),
    path('list_cities_and_users/', list_cities_and_users, name='list_cities_and_users'),
]