# from django.shortcuts import render

# # Create your views here.

from django.http import JsonResponse
from rest_framework.decorators import api_view

def patients_home(request):
    return JsonResponse({"message": "Patients API Root"})

def patients_list(request):
    return JsonResponse({"message": "List of patients (sample API)"})

from .models import PatientMaster, PatientCondition, PatientHelp, PatientService, PatientLanguage, PatientPayments, MemberDetails, SpecialNeeds
from .serializers import (
    PatientMasterSerializer, PatientConditionSerializer, PatientHelpSerializer,
    PatientServiceSerializer, PatientLanguageSerializer, PatientPaymentsSerializer,
    MemberDetailsSerializer, SpecialNeedsSerializer , PatientLoginSerializer , ForgotPasswordSerializer )
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail  # Optional: if you want to send email

@api_view(['POST'])
def patient_login(request):
    serializer = PatientLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        try:
            patient = PatientMaster.objects.get(email=email)
        except PatientMaster.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        
        if patient.password == password:  # For testing. In production, use hashed passwords
            return Response({
                "message": "Login successful",
                "patient_id": patient.patient_id,
                "full_name": patient.full_name,
                "email": patient.email
            })
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            patient = PatientMaster.objects.get(email=email)
            # Example: send password via email (Not secure for production)
            # send_mail(
            #     'Your Password',
            #     f'Your password is: {patient.password}',
            #     'from@example.com',
            #     [email],
            #     fail_silently=False,
            # )
            return Response({"message": f"Password recovery email sent to {email}"})
        except PatientMaster.DoesNotExist:
            return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def patient_info(request):
    if request.method == 'GET':
        patients = PatientMaster.objects.all()
        serializer = PatientMasterSerializer(patients, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PatientMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET' , 'PUT' , 'DELETE'])
def patient_specific_info(request, patient_id):
    try:
        patient = PatientMaster.objects.get(pk=patient_id)
    except PatientMaster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientMasterSerializer(patient)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientMasterSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def patient_conditions(request, patient_id=None):
    if patient_id:
        conditions = PatientCondition.objects.filter(patient_id=patient_id)
    else:
        conditions = PatientCondition.objects.all()
    serializer = PatientConditionSerializer(conditions, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def patient_conditions(request, patient_id):
    conditions = PatientCondition.objects.filter(patient_id=patient_id)

    if not conditions.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # NOTE the 'many=True' here
        serializer = PatientConditionSerializer(conditions, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PatientConditionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        return Response({"error": "Bulk update not implemented"}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        conditions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def patient_services(request, patient_id=None):

    # LIST + CREATE
    if patient_id is None:

        # GET all
        if request.method == 'GET':
            services = PatientService.objects.all()
            serializer = PatientServiceSerializer(services, many=True)
            return Response(serializer.data)

        # POST new
        if request.method == 'POST':
            serializer = PatientServiceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # SINGLE RECORD OPERATIONS (GET/PUT/DELETE)
    try:
        service = PatientService.objects.get(pk=patient_id)
    except PatientService.DoesNotExist:
        return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

    # GET by id
    if request.method == 'GET':
        serializer = PatientServiceSerializer(service)
        return Response(serializer.data)

    # PUT update by id
    if request.method == 'PUT':
        serializer = PatientServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE by id
    if request.method == 'DELETE':
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def patient_help(request, patient_id=None):

    # ========================================
    # /patient_help/  → GET LIST + POST
    # ========================================
    if patient_id is None:

        # GET all
        if request.method == 'GET':
            helps = PatientHelp.objects.all()
            serializer = PatientHelpSerializer(helps, many=True)
            return Response(serializer.data)

        # POST create
        if request.method == 'POST':
            serializer = PatientHelpSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ========================================
    # /patient_help/<patient_id>/ → GET+PUT+DELETE
    # ========================================
    try:
        help_entry = PatientHelp.objects.get(patient_id=patient_id)
    except PatientHelp.DoesNotExist:
        return Response({"error": "Help entry not found"}, status=status.HTTP_404_NOT_FOUND)

    # GET single
    if request.method == 'GET':
        serializer = PatientHelpSerializer(help_entry)
        return Response(serializer.data)

    # PUT update
    if request.method == 'PUT':
        serializer = PatientHelpSerializer(help_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    if request.method == 'DELETE':
        help_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def patient_languages(request, patient_id=None):

    # -------------------------------
    # List all or create new
    # /patient_languages/
    # -------------------------------
    if patient_id is None:

        # GET all
        if request.method == 'GET':
            languages = PatientLanguage.objects.all()
            serializer = PatientLanguageSerializer(languages, many=True)
            return Response(serializer.data)

        # POST create
        if request.method == 'POST':
            serializer = PatientLanguageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------
    # Operations for a single patient
    # /patient_languages/<patient_id>/
    # -------------------------------
    try:
        language = PatientLanguage.objects.get(patient_id=patient_id)
    except PatientLanguage.DoesNotExist:
        return Response({"error": "Language entry not found"}, status=status.HTTP_404_NOT_FOUND)

    # GET single
    if request.method == 'GET':
        serializer = PatientLanguageSerializer(language)
        return Response(serializer.data)

    # PUT update
    if request.method == 'PUT':
        serializer = PatientLanguageSerializer(language, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    if request.method == 'DELETE':
        language.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def patient_payments(request, patient_id):
    try:
        payment = PatientPayments.objects.get(patient_id=patient_id)
    except PatientPayments.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientPaymentsSerializer(payment)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PatientPaymentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def member_details(request, patient_id=None):
    # -------------------------
    # GET all members or POST new member
    # -------------------------
    if patient_id is None:
        if request.method == 'GET':
            members = MemberDetails.objects.all()
            serializer = MemberDetailsSerializer(members, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = MemberDetailsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # -------------------------
    # GET all members for a specific patient
    # -------------------------
    else:
        if request.method == 'GET':
            members = MemberDetails.objects.filter(patient_id=patient_id)
            serializer = MemberDetailsSerializer(members, many=True)
            return Response(serializer.data)

        # For PUT/DELETE, we require member_id in the request data
        elif request.method in ['PUT', 'DELETE']:
            member_id = request.data.get('member_id')
            if not member_id:
                return Response({"error": "member_id is required for PUT/DELETE"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                member = MemberDetails.objects.get(member_id=member_id, patient_id=patient_id)
            except MemberDetails.DoesNotExist:
                return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

            if request.method == 'PUT':
                serializer = MemberDetailsSerializer(member, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            elif request.method == 'DELETE':
                member.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
# List all / create new special needs
@api_view(['GET', 'POST'])
def special_needs_list(request):
    if request.method == 'GET':
        needs = SpecialNeeds.objects.all()
        serializer = SpecialNeedsSerializer(needs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SpecialNeedsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get all needs for a specific patient / update / delete a specific need by row id
@api_view(['GET', 'PUT', 'DELETE'])
def special_needs_by_patient(request, patient_id):
    needs = SpecialNeeds.objects.filter(patient_id=patient_id)

    if request.method == 'GET':
        serializer = SpecialNeedsSerializer(needs, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # expects 'id' in request.data to update a specific row
        try:
            need = SpecialNeeds.objects.get(pk=request.data.get('id'), patient_id=patient_id)
        except SpecialNeeds.DoesNotExist:
            return Response({"error": "Special Need not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SpecialNeedsSerializer(need, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # expects 'id' in request.data to delete a specific row
        try:
            need = SpecialNeeds.objects.get(pk=request.data.get('id'), patient_id=patient_id)
        except SpecialNeeds.DoesNotExist:
            return Response({"error": "Special Need not found"}, status=status.HTTP_404_NOT_FOUND)

        need.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
