from django.urls import path
from . import views

urlpatterns = [
    path('', views.caregiver_home, name='caregiver_home'),
    path('caregiver_info/', views.caregiverInfo, name='caregiver_info'),
    path('caregiver_info/documents/', views.caregiverDocuments, name='caregiver_documents_list'), 
    path('caregiver_info/documents/<int:pk>/', views.caregiverDocuments, name='caregiver_documents'), 
]
