from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.create_scientist),
    path('success/', views.success_registration),
    path('map/', views.map_scientists),
]