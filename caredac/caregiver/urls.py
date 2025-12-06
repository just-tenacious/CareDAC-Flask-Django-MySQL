from django.urls import path
from . import views

urlpatterns = [
    path('', views.caregiver_home, name='caregiver_home'),
    path('caregiver_login/', views.caregiver_login, name='caregiver_login'),
    path('caregiver_forgot_password/', views.caregiver_forgot_password, name='caregiver_forgot_password'),
    path('caregiver_info/', views.caregiverInfo, name='caregiver_info'),
    path('caregiver_info/documents/', views.caregiverDocuments, name='caregiver_documents_list'), 
    path('caregiver_info/documents/<int:pk>/', views.caregiverDocuments, name='caregiver_documents'), 
    path('caregiver_info/caregiver_details/', views.caregiverDetails, name='caregiver_details'),
    path('caregiver_info/caregiver_details/<int:caregiver_id>/', views.caregiverDetails, name='caregiver_details_by_id'),
    path('caregiver_info/caregiver_language/', views.caregiverLanguage, name='caregiver_language'),
    path('caregiver_info/caregiver_payments/', views.caregiverPayments, name = 'caregiver_payments'),
    path('caregiver_info/caregiver_payments/<int:caregiver_id>/',views.specificCaregiverPayment,name='specific_caregiver_payment'),
]
