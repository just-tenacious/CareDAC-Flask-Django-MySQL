from .models import CaregiverInfo , CaregiverDocuments , CaregiverDetails , CaregiverLanguage , CaregiverPayments
from rest_framework import serializers

class CaregiverInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model = CaregiverInfo
    fields = '__all__'

class CaregiverDocumentsSerializer(serializers.ModelSerializer):
  class Meta:
    model = CaregiverDocuments
    fields = '__all__'

# class CaregiverDetailsSerializer(serializers.ModelSerializer):
#   class Meta:
#     model: CaregiverDetails
#     fields = '__all__'

class CaregiverDetailsSerializer(serializers.ModelSerializer):
    LANGUAGE_CHOICES = {
        '0': 'English',
        '1': 'French',
        '2': 'Hindi'
    }

    languages_display = serializers.SerializerMethodField()

    class Meta:
        model = CaregiverDetails
        fields = '__all__'

    def get_languages_display(self, obj):
        """
        Convert stored numeric language codes into readable text.
        """
        codes = obj.languages.split(',') if obj.languages else []
        return [self.LANGUAGE_CHOICES.get(code.strip(), 'Unknown') for code in codes]

class CaregiverLanguageSerializer(serializers.ModelSerializer):
  class Meta:
    model = CaregiverLanguage
    fields = '__all__'

class CaregiverPaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = CaregiverPayments
    fields = '__all__'