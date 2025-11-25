from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CaregiverInfoSerializer, CaregiverDocumentsSerializer
from .models import CaregiverInfo, CaregiverDocuments
import os

@api_view(['GET','POST'])
def caregiver_home(request):
    status = {'message': ''}
    if request.method == 'GET':
        status['message'] = "This is GET method"
        return Response(status)
    elif request.method == 'POST':
        status['message'] = "This is POST method"
        return Response(status)

@api_view(['GET','POST'])
def caregiverInfo(request):
    if request.method == 'GET':
        objs = CaregiverInfo.objects.all()
        serializer = CaregiverInfoSerializer(objs, many=True)
        return Response(serializer.data)
    else:
        data = request.data
        serializer = CaregiverInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET','POST','PUT','PATCH'])
def caregiverDocuments(request, pk=None):
    """
    Handles:
    - GET: List all documents
    - POST: Create new documents
    - PUT/PATCH: Update existing documents, replace files if new ones are uploaded
    """
    if request.method == 'GET':
        objs = CaregiverDocuments.objects.all()
        serializer = CaregiverDocumentsSerializer(objs, many=True)
        return Response(serializer.data)

    data = request.data.copy()
    instance = None

    # If pk is provided, try to fetch existing instance
    if pk:
        try:
            instance = CaregiverDocuments.objects.get(pk=pk)
        except CaregiverDocuments.DoesNotExist:
            return Response({"error": "Document not found"}, status=404)

    # Handle file replacement
    file_fields = ['covid_19', 'first_aid', 'ndis', 'police', 'child_chk', 'visa', 'resume']
    if instance:
        for field in file_fields:
            new_file = request.FILES.get(field)
            if new_file:
                # Delete old file if exists
                old_file = getattr(instance, field)
                if old_file and os.path.isfile(old_file.path):
                    os.remove(old_file.path)
                setattr(instance, field, new_file)

        serializer = CaregiverDocumentsSerializer(instance, data=data, partial=True)
    else:
        # Creating new instance
        for field in file_fields:
            if field in request.FILES:
                data[field] = request.FILES[field]
        serializer = CaregiverDocumentsSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# from django.http import JsonResponse

# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# from caregiver.serializer import CaregiverInfoSerializer , CaregiverDocumentsSerializer
# from caregiver.models import CaregiverInfo , CaregiverDocuments

# # def caregiver_home(request):
# #     return JsonResponse({"message": "Caregiver API Root"})

# # def caregiver_list(request):
# #     return JsonResponse({"message": "List of caregivers (sample API)"})

# @api_view(['GET','POST'])
# def caregiver_home(request):
#     status = {'message':''}
#     if request.method == 'GET':
#         status['message']="This is get method"
#         print(status)
#         return Response(status)
#     elif request.method == 'POST':
#         status['message']="This is post method"
#         # data = request.data
#         # print(data)
#         print(status)
#         return Response(status)
    
# @api_view(['GET','POST'])
# def caregiverInfo(request):
#     if request.method == 'GET':
#         objs = CaregiverInfo.objects.all()
#         serializer = CaregiverInfoSerializer(objs, many = True)
#         return Response(serializer.data)
#     else:
#         data = request.data
#         serializer = CaregiverInfoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

# @api_view(['GET','POST','PUT','PATCH'])
# def caregiverDocuments(request):
#     if request.method == 'GET':
#         objs = CaregiverDocuments.objects.all()
#         serializer = CaregiverDocumentsSerializer(objs, many = True)
#         return Response(serializer.data)
#     else:
#         data = request.data
#         serializer = CaregiverDocumentsSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)