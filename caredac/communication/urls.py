from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CaregiverAvailabilityViewSet, 
    ChatsList, 
    ReviewList, 
    CaregiverAverageRating, 
    TransactionDetailsList, 
    communication_home,
    caregiver_filter
)

router = DefaultRouter()
router.register("availability", CaregiverAvailabilityViewSet, basename="availability")

urlpatterns = [
    path('', communication_home, name='communication_home'),
    path('chats/', ChatsList, name='chats_list'),
    path('reviews/', ReviewList, name='review_list'),
    path('reviews/caregiver-average/', CaregiverAverageRating, name='caregiver_average_rating'),
    path('transactions/', TransactionDetailsList, name='transaction_details_list'),
    path('caregiver_filter/', caregiver_filter, name='caregiver_filter'),
    # Router handles /api/availability/
    path('api/', include(router.urls)),
]