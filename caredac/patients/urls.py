from django.urls import path
from . import views

urlpatterns = [
    path('', views.patients_home, name='patients_home'),
    path('list/', views.patients_list, name='patients_list'),
]
