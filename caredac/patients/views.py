# from django.shortcuts import render

# # Create your views here.

from django.http import JsonResponse

def patients_home(request):
    return JsonResponse({"message": "Patients API Root"})

def patients_list(request):
    return JsonResponse({"message": "List of patients (sample API)"})
