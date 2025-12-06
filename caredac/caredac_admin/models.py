from django.db import models
from django.utils import timezone
from datetime import timedelta

# For generic foreign keys (chats & reviews)
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# -------------------------------
# Email OTP
# -------------------------------
class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.email} - {self.otp}"


# -------------------------------
# System Language
# -------------------------------
class SystemLanguage(models.Model):
    language_id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=255)

    class Meta:
        db_table = 'system_language'

    def __str__(self):
        return self.language


# -------------------------------
# Services Offered
# -------------------------------
class ServicesOffered(models.Model):
    services_id = models.AutoField(primary_key=True)
    services = models.CharField(max_length=255)

    class Meta:
        db_table = 'services_offered'

    def __str__(self):
        return self.services


# -------------------------------
# Need Help
# -------------------------------
class NeedHelp(models.Model):
    help_id = models.AutoField(primary_key=True)
    help_name = models.CharField(max_length=255)

    class Meta:
        db_table = "need_help"

    def __str__(self):
        return self.help_name

# -------------------------------
# Language Options
# -------------------------------
class LanguageOptions(models.Model):
    option_id = models.AutoField(primary_key=True)
    languages_known = models.CharField(max_length=255)

    class Meta:
        db_table = "language_options"

    def __str__(self):
        return self.languages_known
