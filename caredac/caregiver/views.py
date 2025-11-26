from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view , parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
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
@parser_classes([MultiPartParser, FormParser]) 
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


@api_view(['GET', 'POST'])
def caregiverDocumentsList(request):
    """List all caregiver documents or create new one."""
    
    if request.method == 'GET':
        docs = CaregiverDocuments.objects.all()
        serializer = CaregiverDocumentsSerializer(docs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CaregiverDocumentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
def caregiverDocuments(request, pk):
    """Retrieve, update (PUT), or partial update (PATCH) a document record."""
    
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