from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from caregiver.serializer import CaregiverInfoSerializer
from caregiver.models import CaregiverInfo

# def caregiver_home(request):
#     return JsonResponse({"message": "Caregiver API Root"})

# def caregiver_list(request):
#     return JsonResponse({"message": "List of caregivers (sample API)"})

@api_view(['GET','POST'])
def caregiver_home(request):
    status = {'message':''}
    if request.method == 'GET':
        status['message']="This is get method"
        print(status)
        return Response(status)
    elif request.method == 'POST':
        status['message']="This is post method"
        # data = request.data
        # print(data)
        print(status)
        return Response(status)
    
@api_view(['GET','POST'])
def caregiverInfo(request):
    if request.method == 'GET':
        objs = CaregiverInfo.objects.all()
        serializer = CaregiverInfoSerializer(objs, many = True)
        return Response(serializer.data)
    else:
        data = request.data
        serializer = CaregiverInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)