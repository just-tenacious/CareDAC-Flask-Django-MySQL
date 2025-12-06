from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CaregiverAvailabilityViewSet, 
    ChatsList, 
    ReviewList, 
    CaregiverAverageRating, 
    TransactionDetailsList, 
    communication_home, 
    CaregiverAvailabilityFilterView
)

router = DefaultRouter()
router.register("availability", CaregiverAvailabilityViewSet, basename="availability")

urlpatterns = [
    path('', communication_home, name='communication_home'),
    path('chats/', ChatsList, name='chats_list'),
    path('reviews/', ReviewList, name='review_list'),
    path('reviews/caregiver-average/', CaregiverAverageRating, name='caregiver_average_rating'),
    path('transactions/', TransactionDetailsList, name='transaction_details_list'),

    # Router handles /api/availability/
    path('api/', include(router.urls)),

    # Filter endpoint
    path('api/availability/filter/', CaregiverAvailabilityFilterView.as_view(), name='availability-filter'),
]


# from django.urls import path, include 
# from rest_framework.routers import DefaultRouter
# from .views import CaregiverAvailabilityViewSet, ChatsList, ReviewList, CaregiverAverageRating, TransactionDetailsList, communication_home , CaregiverAvailabilityFilterView

# router = DefaultRouter()
# router.register("availability", CaregiverAvailabilityViewSet, basename="availability")

# urlpatterns = [
#     path('', communication_home, name='communication_home'),
#     path('chats/', ChatsList, name='chats_list'),
#     path('reviews/', ReviewList, name='review_list'),
#     path('reviews/caregiver-average/', CaregiverAverageRating, name='caregiver_average_rating'),
#     path('transactions/', TransactionDetailsList, name='transaction_details_list'),

#     path('api/', include(router.urls)),  # router will handle /availability/
#     path('api/availability/filter/', CaregiverAvailabilityFilterView.as_view(), name='availability-filter'),
# ]

# # from django.urls import path
# # from . import views

# # urlpatterns = [
# #     path('', views.communication_home, name='communication_home'),
# #     path('chats/', views.ChatsList, name='chats_list'),
# #     path('reviews/', views.ReviewList, name='review_list'),
# #     path('reviews/caregiver-average/', views.CaregiverAverageRating, name='caregiver_average_rating'),
# #     path('transactions/', views.TransactionDetailsList, name='transaction_details_list'),
# # ]
