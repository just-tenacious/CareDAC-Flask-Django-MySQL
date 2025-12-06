from caredac_admin.models import SystemLanguage , ServicesOffered , NeedHelp , LanguageOptions
from rest_framework import serializers

class SystemLanguageSerializer(serializers.ModelSerializer):
  class Meta:
    model = SystemLanguage
    fields = ['language_id', 'language']

class ServicesOfferedSerializer(serializers.ModelSerializer):
  class Meta:
    model = ServicesOffered
    fields = ['services_id', 'services']

class NeedHelpSerializer(serializers.ModelSerializer):
  class Meta:
    model = NeedHelp
    fields = ['help_id', 'help_name']

class LanguageOptionsSerializer(serializers.ModelSerializer):
  class Meta:
    model = LanguageOptions
    fields = ['option_id', 'languages_known']