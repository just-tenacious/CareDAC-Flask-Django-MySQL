from django.urls import path
from . import views

urlpatterns = [
    path('', views.patients_home, name='patients_home'),
    path('list/', views.patients_list, name='patients_list'),
    path('patients_login/', views.patient_login, name='patient_login'),
    path('patients_forgot_password/', views.forgot_password, name='forgot_password'),
    path('patient_info/', views.patient_info, name='patient_info'),
    path('patient_specific_info/<int:patient_id>/', views.patient_specific_info, name='patient_specific_info'),
    path('patient_conditions/', views.patient_conditions, name='patient_conditions'),
    path('patient_conditions/<int:patient_id>/', views.patient_conditions, name='patient_conditions'),
    path('patient_services/', views.patient_services, name='patient_services'),
    path('patient_services/<int:patient_id>/', views.patient_services, name='patient_services'),
    path('patient_help/', views.patient_help, name='patient_help'),
    path('patient_help/<int:patient_id>/', views.patient_help, name='patient_help'),
    path('patient_languages/', views.patient_languages, name='patient_languages'),
    path('patient_languages/<int:patient_id>/', views.patient_languages, name='patient_languages'),
    path('patient_payments/<int:patient_id>/', views.patient_payments, name='patient_payments'),
    path('member_details/', views.member_details, name='member_details'),
    path('member_details/<int:patient_id>/', views.member_details, name='member_details'),
    path('special_needs/', views.special_needs_list, name='special_needs'),
    path('special_needs/<int:patient_id>/', views.special_needs_by_patient, name='special_needs'),
]
