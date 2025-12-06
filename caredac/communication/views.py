from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Q, F, Subquery, OuterRef
from django.core.paginator import Paginator
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
class CaregiverAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = CaregiverAvailability.objects.all().prefetch_related(
        "skills", "preferences_accepted", "languages_known", "services_offering"
    )
    serializer_class = CaregiverAvailabilitySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        caregiver_id = request.query_params.get("caregiver_id")
        queryset = self.queryset
        if caregiver_id:
            queryset = queryset.filter(caregiver_id=caregiver_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# ----------------------------
# Caregiver Filter Endpoint
# ----------------------------
@api_view(['GET'])
def caregiver_filter(request):
    qs = (
        CaregiverAvailability.objects
        .select_related("caregiver")
        .prefetch_related(
            "skills",
            "preferences_accepted",
            "languages_known",
            "services_offering"
        )
    )

    # -----------------------------
    # 🔍 FILTERS
    # -----------------------------
    city = request.GET.get("city")
    state = request.GET.get("state")
    country = request.GET.get("country")
    gender = request.GET.get("gender")
    skill = request.GET.getlist("skill")
    preference = request.GET.getlist("preference")
    language = request.GET.getlist("language")
    service = request.GET.getlist("service")
    min_date = request.GET.get("min_date")
    max_date = request.GET.get("max_date")
    min_time = request.GET.get("min_time")
    max_time = request.GET.get("max_time")
    child_age = request.GET.get("child_age")
    child_count = request.GET.get("child_count")

    if city:
        qs = qs.filter(caregiver__city__iexact=city)
    if state:
        qs = qs.filter(caregiver__state__iexact=state)
    if country:
        qs = qs.filter(caregiver__country__iexact=country)
    if gender:
        qs = qs.filter(caregiver__gender__iexact=gender)
    if skill:
        qs = qs.filter(skills__name__in=skill).distinct()
    if preference:
        qs = qs.filter(preferences_accepted__name__in=preference).distinct()
    if language:
        qs = qs.filter(languages_known__name__in=language).distinct()
    if service:
        qs = qs.filter(services_offering__services__in=service).distinct()
    if min_date:
        qs = qs.filter(date__gte=min_date)
    if max_date:
        qs = qs.filter(date__lte=max_date)
    if min_time:
        qs = qs.filter(start_time__gte=min_time)
    if max_time:
        qs = qs.filter(end_time__lte=max_time)
    if child_age:
        qs = qs.filter(child_age_service__icontains=child_age)
    if child_count:
        qs = qs.filter(child_count=child_count)

    # -----------------------------
    # ⭐ SORTING WITH AVERAGE RATING
    # -----------------------------
    sort_by = request.GET.get("sort", "rating_desc")
    caregiver_ct = ContentType.objects.get(app_label='caregiver', model='caregiverinfo')
    reviews_qs = Review.objects.filter(
        to_content_type=caregiver_ct,
        to_object_id=OuterRef('caregiver__caregiver_id')
    ).values('to_object_id').annotate(avg_rating=Avg('rating')).values('avg_rating')
    qs = qs.annotate(avg_rating=Subquery(reviews_qs))

    if sort_by == "rating_desc":
        qs = qs.order_by(F("avg_rating").desc(nulls_last=True))
    elif sort_by == "rating_asc":
        qs = qs.order_by(F("avg_rating").asc(nulls_last=True))
    elif sort_by == "price_asc":
        qs = qs.order_by("time_offering")  # replace with price if available
    elif sort_by == "price_desc":
        qs = qs.order_by("-time_offering")
    elif sort_by == "distance":
        user_lat = request.GET.get("lat")
        user_lng = request.GET.get("lng")
        if user_lat and user_lng:
            qs = qs.annotate(
                distance=((F("caregiver__lat") - float(user_lat))**2 +
                          (F("caregiver__lng") - float(user_lng))**2)
            ).order_by("distance")

    # -----------------------------
    # 📄 PAGINATION
    # -----------------------------
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 10))
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page)

    # -----------------------------
    # 🔄 BUILD RESPONSE
    # -----------------------------
    results = []
    for entry in page_obj:
        caregiver = entry.caregiver
        results.append({
            "caregiver_id": caregiver.caregiver_id,
            "full_name": caregiver.full_name,
            "email": caregiver.email,
            "phone_no": caregiver.phone_no,
            "dob": caregiver.dob,
            "profile_pic": caregiver.profile_pic.url if caregiver.profile_pic else None,
            "gender": caregiver.gender,
            "address": caregiver.address,
            "country": caregiver.country,
            "state": caregiver.state,
            "city": caregiver.city,
            "pincode": caregiver.pincode,
            "acc_status": caregiver.acc_status,
            "avg_rating": entry.avg_rating or 0,
            "availability_id": entry.availability_id,
            "date": entry.date,
            "start_time": entry.start_time,
            "end_time": entry.end_time,
            "child_count": entry.child_count,
            "child_age_service": entry.child_age_service,
            "time_offering": entry.time_offering,
            "skills": ", ".join(sorted([s.name for s in entry.skills.all()])),
            "preferences": ", ".join(sorted([p.name for p in entry.preferences_accepted.all()])),
            "languages": ", ".join(sorted([l.name for l in entry.languages_known.all()])),
            "services": ", ".join(sorted([srv.services for srv in entry.services_offering.all()])),
        })

    return Response({
        "page": page,
        "page_size": page_size,
        "total_pages": paginator.num_pages,
        "total_records": paginator.count,
        "results": results
    })