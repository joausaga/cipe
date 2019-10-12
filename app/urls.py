from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
    path('success/', views.success_registration),
    path('map/', views.map_scientists, name='map'),
    path('map/filter_map/', views.filter_map, name='filter_map')
]