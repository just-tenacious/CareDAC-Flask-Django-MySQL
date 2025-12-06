from rest_framework import serializers
from communication.models import Chats, Review, TransactionDetails, CaregiverAvailability
from caregiver.models import CaregiverInfo
from caredac_admin.models import ServicesOffered
from .models import Skill, Preference, Language

# -----------------------------
# COMMUNICATION SERIALIZERS
# -----------------------------
class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class TransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetails
        fields = '__all__'


# -----------------------------
# SUPPORT SERIALIZERS
# -----------------------------
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ["id", "name"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name"]


class ServiceOfferedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesOffered
        fields = ["services_id", "services"]


class CaregiverAvailabilitySerializer(serializers.ModelSerializer):

    # Use CharField for text input
    skills = serializers.ListField(child=serializers.CharField(), write_only=True)
    preferences_accepted = serializers.ListField(child=serializers.CharField(), write_only=True)
    languages_known = serializers.ListField(child=serializers.CharField(), write_only=True)
    services_offering = serializers.ListField(child=serializers.CharField(), write_only=True)

    # For read/display
    skills_display = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', source='skills')
    preferences_display = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', source='preferences_accepted')
    languages_display = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', source='languages_known')
    services_display = serializers.SlugRelatedField(many=True, read_only=True, slug_field='services', source='services_offering')

    class Meta:
        model = CaregiverAvailability
        fields = [
            'availability_id', 'date', 'start_time', 'end_time', 'child_count', 
            'child_age_service', 'time_offering', 'caregiver',
            'skills', 'preferences_accepted', 'languages_known', 'services_offering',
            'skills_display', 'preferences_display', 'languages_display', 'services_display'
        ]

    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])
        preferences_data = validated_data.pop('preferences_accepted', [])
        languages_data = validated_data.pop('languages_known', [])
        services_data = validated_data.pop('services_offering', [])

        # Create availability instance
        availability = CaregiverAvailability.objects.create(**validated_data)

        # Map text to actual objects
        for skill_name in skills_data:
            skill_obj, _ = Skill.objects.get_or_create(name=skill_name)
            availability.skills.add(skill_obj)

        for pref_name in preferences_data:
            pref_obj, _ = Preference.objects.get_or_create(name=pref_name)
            availability.preferences_accepted.add(pref_obj)

        for lang_name in languages_data:
            lang_obj, _ = Language.objects.get_or_create(name=lang_name)
            availability.languages_known.add(lang_obj)

        for service_name in services_data:
            service_obj = ServicesOffered.objects.get(services=service_name)
            availability.services_offering.add(service_obj)

        return availability

