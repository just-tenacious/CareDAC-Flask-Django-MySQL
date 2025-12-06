from rest_framework import serializers
from .models import PatientMaster , PatientCondition, PatientHelp, PatientService , PatientLanguage , PatientPayments , MemberDetails , SpecialNeeds
from caredac_admin.models import ServicesOffered


class PatientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PatientMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMaster
        fields = '__all__'

class PatientConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientCondition
        fields = '__all__'


class PatientHelpSerializer(serializers.ModelSerializer):
    help_name = serializers.CharField(source='help.help_name', read_only=True)

    class Meta:
        model = PatientHelp
        fields = ['patient_help_id', 'patient', 'help', 'help_name']
        # 'help' is writable (ID), help_name is read-only



class PatientServiceSerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField()

    class Meta:
        model = PatientService
        fields = ['patient_service_id', 'patient', 'services']

    def get_services(self, obj):
        import json

        try:
            service_ids = json.loads(obj.services)
        except:
            service_ids = obj.services.split(',')

        service_ids = [int(s) for s in service_ids]

        names = ServicesOffered.objects.filter(
            services_id__in=service_ids
        ).values_list('services', flat=True)

        return list(names)


# class PatientLanguageSerializer(serializers.ModelSerializer):
#     language_name = serializers.CharField(source='language.language_name', read_only=True)
#     patient_name = serializers.CharField(source='patient.full_name', read_only=True)

#     class Meta:
#         model = PatientLanguage
#         fields = ['patient_language_id', 'patient', 'patient_name', 'language', 'language_name']
#         # 'language' and 'patient' are writable (IDs), names are read-only


class PatientLanguageSerializer(serializers.ModelSerializer):
    # Read-only fields for GET
    language_name = serializers.CharField(source='language.language', read_only=True)
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)

    class Meta:
        model = PatientLanguage
        fields = ['patient_language_id', 'patient', 'patient_name', 'language', 'language_name']
        # patient & language are writable



class PatientPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientPayments
        fields = '__all__'

# class MemberDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MemberDetails
#         fields = '__all__'

class MemberDetailsSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)

    class Meta:
        model = MemberDetails
        fields = [
            'member_id', 'full_name', 'dob', 'email', 'phone', 'password',
            'gender', 'address', 'city', 'state', 'country', 'pincode',
            'relation', 'patient', 'patient_name'
        ]


class SpecialNeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialNeeds
        fields = '__all__'