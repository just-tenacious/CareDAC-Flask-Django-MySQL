# from django.shortcuts import render

# # Create your views here.

from django.http import JsonResponse

def admin_home(request):
    return JsonResponse({"message": "Caredac Admin API Root"})

def admin_stats(request):
    return JsonResponse({"message": "Admin stats (sample API)"})
