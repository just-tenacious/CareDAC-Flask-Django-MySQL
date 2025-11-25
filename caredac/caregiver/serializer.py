from .models import CaregiverInfo , CaregiverDocuments , CaregiverDetails
from rest_framework import serializers

class CaregiverInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model = CaregiverInfo
    fields = '__all__'