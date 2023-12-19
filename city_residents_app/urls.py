from django.urls import path
from .views import city_list, person_list, index, list_cities_and_users, add_person, add_city, add_relationship

app_name = 'city_residents_app'

urlpatterns = [
    path('', index, name='index'),
    path('cities/', city_list, name='city_list'),
    path('people/', person_list, name='person_list'),
    path('list_cities_and_users/', list_cities_and_users, name='list_cities_and_users'),
    path('add_person/', add_person, name='add_person'),
    path('add_city/', add_city, name='add_city'),
    path('add_relationship/', add_relationship, name='add_relationship'),
]