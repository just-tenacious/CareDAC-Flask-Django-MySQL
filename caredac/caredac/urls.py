from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from caredac.views import home , caregiver_login , patient_login , admin_login , otp_verification

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Routes
    path('', home),  
    path('caregiver_login/',caregiver_login, name='caregiver_login'),
    path('patient_login/',patient_login, name='patient_login'),
    path('admin_login/',admin_login, name='admin_login'),
    path('otp_verification/',otp_verification, name='otp_verification'),
    path('caregiver/', include('caregiver.urls')),
    path('patients/', include('patients.urls')),
    path('caredac_admin/', include('caredac_admin.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
