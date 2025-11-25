from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

# Simple home page view
def home(request):
    return HttpResponse("Welcome to Caredac API! Connected Successfully!!")

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Routes
    path('', home),  
    path('caregiver/', include('caregiver.urls')),
    path('patients/', include('patients.urls')),
    path('caredac_admin/', include('caredac_admin.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
