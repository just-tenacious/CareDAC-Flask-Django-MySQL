from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg , Q
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from communication.models import Chats, Review, TransactionDetails
from communication.serializers import ChatsSerializer, ReviewSerializer, TransactionDetailsSerializer

from .models import CaregiverAvailability, Skill, Preference, Language
from .serializers import CaregiverAvailabilitySerializer, SkillSerializer, PreferenceSerializer, LanguageSerializer
from caregiver.models import CaregiverInfo


# ----------------------------
# Function-Based Views
# ----------------------------
@api_view(['GET'])
def communication_home(request):
    return Response({"message": "Welcome to the Communication API Root"})


@api_view(['GET', 'POST'])
def ChatsList(request):
    if request.method == 'GET':
        serializer = ChatsSerializer(Chats.objects.all(), many=True)
        return Response(serializer.data)
    serializer = ChatsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def ReviewList(request):
    reviews = Review.objects.all()
    caregiver_id = request.GET.get('caregiver_id')
    patient_id = request.GET.get('patient_id')

    if caregiver_id:
        caregiver_ct = ContentType.objects.get(app_label='caregiver', model='caregiverinfo')
        reviews = reviews.filter(to_content_type=caregiver_ct, to_object_id=caregiver_id)
    if patient_id:
        patient_ct = ContentType.objects.get(app_label='patients', model='patientmaster')
        reviews = reviews.filter(from_content_type=patient_ct, from_object_id=patient_id)

    if request.method == 'GET':
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def CaregiverAverageRating(request):
    caregiver_id = request.GET.get('caregiver_id')
    if not caregiver_id:
        return Response({"error": "caregiver_id is required"}, status=400)

    caregiver_ct = ContentType.objects.get(app_label='caregiver', model='caregiverinfo')
    reviews = Review.objects.filter(to_content_type=caregiver_ct, to_object_id=caregiver_id)
    avg_rating = round(reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0, 1)

    return Response({"caregiver_id": caregiver_id, "average_rating": avg_rating})


@api_view(['GET', 'POST'])
def TransactionDetailsList(request):
    if request.method == 'GET':
        serializer = TransactionDetailsSerializer(TransactionDetails.objects.all(), many=True)
        return Response(serializer.data)

    serializer = TransactionDetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# ----------------------------
# Support ViewSets
# ----------------------------
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]


class PreferenceViewSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
    permission_classes = [AllowAny]


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [AllowAny]


# ----------------------------
# Caregiver Availability ViewSet
# ----------------------------
# class CaregiverAvailabilityViewSet(viewsets.ModelViewSet):
#     permission_classes = [AllowAny]

#     def retrieve(self, request, pk=None):
#         """
#         GET /api/availability/<caregiver_id>/
#         Returns all availability for a caregiver with skills, preferences, languages, and services.
#         """
#         caregiver = CaregiverInfo.objects.filter(caregiver_id=pk).first()
#         if not caregiver:
#             return Response({"error": "Invalid caregiver ID"}, status=404)

#         availability_qs = CaregiverAvailability.objects.filter(caregiver_id=pk).prefetch_related(
#             "skills", "preferences_accepted", "languages_known", "services_offering"
#         )

#         serializer = CaregiverAvailabilitySerializer(availability_qs, many=True)
#         return Response({
#             "caregiver": {
#                 "id": caregiver.caregiver_id,
#                 "name": f"{caregiver.full_name}"
#             },
#             "availability_count": availability_qs.count(),
#             "availability": serializer.data
#         })

class CaregiverAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = CaregiverAvailability.objects.all().prefetch_related(
        "skills", "preferences_accepted", "languages_known", "services_offering"
    )
    serializer_class = CaregiverAvailabilitySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        """GET /api/availability/?caregiver_id=2"""
        caregiver_id = request.query_params.get("caregiver_id")
        queryset = self.queryset
        if caregiver_id:
            queryset = queryset.filter(caregiver_id=caregiver_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import CaregiverAvailability
from .serializers import CaregiverAvailabilitySerializer

# This is the filter view
class CaregiverAvailabilityFilterView(generics.ListAPIView):
    queryset = CaregiverAvailability.objects.all()
    serializer_class = CaregiverAvailabilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'date',
        'child_count',
        'child_age_service',
        'time_offering',
        'caregiver',
        'skills',
        'preferences_accepted',
        'languages_known',
        'services_offering',
    ]
    