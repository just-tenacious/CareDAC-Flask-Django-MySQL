from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('system_languages/', views.system_languages, name='system_languages'),
    path('system_languages/<int:language_id>/', views.system_language_detail, name='system_language_detail'),
    path('services_offered/', views.services_offered, name='services_offered'),
    path('services_offered/<int:services_id>/', views.services_offered_detail, name='services_offered_detail'),
    path('need_help/', views.need_help, name='need_help'),
    path('need_help/<int:help_id>/', views.need_help_detail, name='need_help_detail'),
    path('language_options/', views.language_options, name='language_options'),
    path('language_options/<int:option_id>/', views.language_options_detail, name='language_options_detail'),
    # path('stats/', views.admin_stats, name='admin_stats'),
]
