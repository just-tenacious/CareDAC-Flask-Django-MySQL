from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view , parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializer import CaregiverInfoSerializer, CaregiverDocumentsSerializer , CaregiverLanguageSerializer , CaregiverDetailsSerializer , CaregiverPaymentSerializer
from .models import CaregiverInfo, CaregiverDocuments , CaregiverDetails, CaregiverLanguage , CaregiverPayments
import os
from django.utils.crypto import get_random_string
from django.core.mail import send_mail  

@api_view(['GET','POST'])
def caregiver_home(request):
    status = {'message': ''}
    if request.method == 'GET':
        status['message'] = "This is GET method"
        return Response(status)
    elif request.method == 'POST':
        status['message'] = "This is POST method"
        return Response(status)


@api_view(['POST'])
def caregiver_login(request):

    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        caregiver = CaregiverInfo.objects.get(email=email)
    except CaregiverInfo.DoesNotExist:
        return Response(
            {"error": "Invalid email or password."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # If password is stored as plain text (not recommended)
    if caregiver.password != password:
        return Response(
            {"error": "Invalid email or password."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Optionally, you could use a serializer to return caregiver info
    serializer = CaregiverInfoSerializer(caregiver)
    return Response({
        "message": "Login successful",
        "caregiver": serializer.data
    })

@api_view(['POST'])
def caregiver_forgot_password(request):
    """
    Send a temporary password to caregiver email.
    """
    email = request.data.get('email')
    
    if not email:
        return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        caregiver = CaregiverInfo.objects.get(email=email)
    except CaregiverInfo.DoesNotExist:
        return Response({"error": "No account found with this email."}, status=status.HTTP_404_NOT_FOUND)
    
    # Generate a temporary password
    temp_password = get_random_string(length=8)  # e.g., "aB3dE9hJ"
    
    # Update caregiver password (plain text for now, but can hash if using hashed passwords)
    caregiver.password = temp_password
    caregiver.save()
    
    # Send email
    subject = "Password Reset Request"
    message = f"Hello {caregiver.full_name},\n\nYour temporary password is: {temp_password}\nPlease login and change your password immediately."
    from_email = None  # uses DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({"message": "Temporary password sent to your email."})


@api_view(['GET', 'POST', 'PUT'])
@parser_classes([MultiPartParser, FormParser]) 
def caregiverInfo(request):
    if request.method == 'GET':
        objs = CaregiverInfo.objects.all()
        serializer = CaregiverInfoSerializer(objs, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        caregiver_id = request.query_params.get('id')
        if not caregiver_id:
            return Response(
                {"error": "ID is required for PUT update."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            doc = CaregiverInfo.objects.get(id=caregiver_id)
        except CaregiverInfo.DoesNotExist:
            return Response(
                {"error": "Object not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CaregiverInfoSerializer(doc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:  # POST
        data = request.data
        print("FILES =>", request.FILES)  
        print("DATA  =>", request.data)

        serializer = CaregiverInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET', 'POST'])
def caregiverDocumentsList(request):    
    if request.method == 'GET':
        docs = CaregiverDocuments.objects.all()
        serializer = CaregiverDocumentsSerializer(docs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print("FILES =>", request.FILES)  
        print("DATA  =>", request.data)
        serializer = CaregiverDocumentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
def caregiverDocuments(request, pk):    
    try:
        doc = CaregiverDocuments.objects.get(pk=pk)
    except CaregiverDocuments.DoesNotExist:
        return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CaregiverDocumentsSerializer(doc)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CaregiverDocumentsSerializer(doc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = CaregiverDocumentsSerializer(doc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET','POST','PUT'])
# def caregiverDetails(request):
#     if request.method == 'GET':
#         details = CaregiverDetails.objects.all()
#         serializer = CaregiverDetailsSerializer(details, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         data = request.data
#         serializer = CaregiverDetailsSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
#     elif request.method == 'PUT':
#         data = request.data
#         serializer = CaregiverDetailsSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

@api_view(['GET', 'POST', 'PUT'])
def caregiverDetails(request, caregiver_id=None):
    """
    GET: Fetch caregiver details. If caregiver_id is provided, fetch only for that caregiver.
    POST: Add new caregiver details
    PUT: Update existing caregiver details by caregiver_id
    """
    if request.method == 'GET':
        if caregiver_id:
            try:
                details = CaregiverDetails.objects.get(caregiver_id=caregiver_id)
                serializer = CaregiverDetailsSerializer(details)
            except CaregiverDetails.DoesNotExist:
                return Response({"error": "Caregiver details not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            details = CaregiverDetails.objects.all()
            serializer = CaregiverDetailsSerializer(details, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CaregiverDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not caregiver_id:
            return Response({"error": "caregiver_id is required for PUT"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            details = CaregiverDetails.objects.get(caregiver_id=caregiver_id)
        except CaregiverDetails.DoesNotExist:
            return Response({"error": "Caregiver details not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CaregiverDetailsSerializer(details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','PUT','DELETE'])
def caregiverLanguage(request):
    status = {'message': ''}
    if request.method == 'GET':
        languages = CaregiverLanguage.objects.all()
        serializer = CaregiverLanguageSerializer(languages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = CaregiverLanguageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        serializer = CaregiverLanguageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        status['message'] = "This is DELETE method for Caregiver Language"
        return Response(status)

@api_view(['GET','POST','PUT','DELETE'])
def caregiverPayments(request):
    status = {'message': ''}
    if request.method == 'GET':
        payment = CaregiverPayments.objects.all()
        serializer = CaregiverPaymentSerializer(payment, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = CaregiverPaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        serializer = CaregiverPaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        data = request.data
        obj = CaregiverPayments.get(pk=data['payment_id'])
        obj.delete()
        status['message'] = "Payment method deleted successfully"
        
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def specificCaregiverPayment(request, caregiver_id):
    try:
        # Get all payments for this caregiver
        payments = CaregiverPayments.objects.filter(caregiver_id=caregiver_id)
        if not payments.exists():
            return Response({"error": "No payment methods found for this caregiver"}, 
                            status=status.HTTP_404_NOT_FOUND)
    except CaregiverPayments.DoesNotExist:
        return Response({"error": "No payment methods found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CaregiverPaymentSerializer(payments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CaregiverPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # If you want to update a specific payment, you should pass payment_id in request.data
        payment_id = request.data.get('payment_id')
        if not payment_id:
            return Response({"error": "payment_id is required to update a payment"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payment = CaregiverPayments.objects.get(pk=payment_id, caregiver_id=caregiver_id)
        except CaregiverPayments.DoesNotExist:
            return Response({"error": "Payment method not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CaregiverPaymentSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete all payments for this caregiver
        payments.delete()
        return Response({"message": "All payment methods deleted successfully"}, status=status.HTTP_204_NO_CONTENT)