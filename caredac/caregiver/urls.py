from django.urls import path
from . import views

urlpatterns = [
    path('', views.caregiver_home, name='caregiver_home'),
    # path('list/', views.caregiver_list, name='caregiver_list'),
    path('caregiver_info/',views.caregiverInfo, name='caregiver_info'),
]
