from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

from caregiver.models import CaregiverInfo
from caredac_admin.models import ServicesOffered


# =============================
# ENUM CHOICES
# =============================
SKILL_CHOICES = [
    ("cr_training", "CR Training"),
    ("first_aid_training", "First Aid Training"),
    ("special_need_care", "Special Need Care"),
]

PREFERENCE_CHOICES = [
    ("comfort_with_pets", "Comfort with Pets"),
    ("has_own_transport", "Has Own Transport"),
    ("non_smoker", "Non-Smoker"),
]

LANGUAGE_CHOICES = [
    ("hindi", "Hindi"),
    ("french", "French"),
    ("english", "English"),
]


# =============================
# CHAT MODEL
# =============================
class Chats(models.Model):
    chat_id = models.AutoField(primary_key=True)

    from_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='chat_from_type'
    )
    from_object_id = models.PositiveIntegerField()
    chat_from = GenericForeignKey('from_content_type', 'from_object_id')

    to_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='chat_to_type'
    )
    to_object_id = models.PositiveIntegerField()
    chat_to = GenericForeignKey('to_content_type', 'to_object_id')

    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chats"

    def __str__(self):
        return f"Chat {self.chat_id}"


# =============================
# REVIEW MODEL
# =============================
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)

    from_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='review_from_type'
    )
    from_object_id = models.PositiveIntegerField()
    review_from = GenericForeignKey('from_content_type', 'from_object_id')

    to_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='review_to_type'
    )
    to_object_id = models.PositiveIntegerField()
    review_to = GenericForeignKey('to_content_type', 'to_object_id')

    review = models.TextField()
    rating = models.IntegerField(default=0)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reviews"

    def __str__(self):
        return f"Review {self.review_id}"


# =============================
# TRANSACTION DETAILS MODEL
# =============================
class TransactionDetails(models.Model):
    transaction_id = models.AutoField(primary_key=True)

    transaction_from = models.ForeignKey(
        'patients.PatientMaster',
        on_delete=models.CASCADE,
        db_column='patient_id',
        related_name='transactions_from'
    )

    transaction_to = models.ForeignKey(
        'caregiver.CaregiverInfo',
        on_delete=models.CASCADE,
        db_column='caregiver_id',
        related_name='transactions_to'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transaction_details"

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.amount}"


# ==============================================================================
#                NEW MODELS ADDED BELOW (CARETAKER AVAILABILITY SYSTEM)
# ==============================================================================

# =======================================
# SKILL TABLE
# =======================================
class Skill(models.Model):
    name = models.CharField(
        max_length=50,
        choices=SKILL_CHOICES,
        unique=True
    )

    class Meta:
        db_table = "caregiver_skills"

    def __str__(self):
        return self.get_name_display()


# =======================================
# PREFERENCE TABLE
# =======================================
class Preference(models.Model):
    name = models.CharField(
        max_length=50,
        choices=PREFERENCE_CHOICES,
        unique=True
    )

    class Meta:
        db_table = "caregiver_preferences"

    def __str__(self):
        return self.get_name_display()


# =======================================
# LANGUAGE TABLE
# =======================================
class Language(models.Model):
    name = models.CharField(
        max_length=50,
        choices=LANGUAGE_CHOICES,
        unique=True
    )

    class Meta:
        db_table = "caregiver_languages"

    def __str__(self):
        return self.get_name_display()


# =======================================
# MAIN CAREGIVER AVAILABILITY TABLE
# =======================================
class CaregiverAvailability(models.Model):

    CHILD_AGE_CHOICES = [ 
        ("0-11 months", "0-11 months"),
        ("1-3 years", "1-3 years"),
        ("4-5 years", "4-5 years"),
        ("10+ years", "10+ years"),
    ]

    class Meta:
        db_table = "caregiver_availability"   # REQUIRED TABLE NAME

    availability_id = models.AutoField(primary_key=True)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    child_count = models.PositiveIntegerField()
    # child_age_service = models.CharField(max_length=255, blank=True, null=True)

    child_age_service = models.CharField(
        max_length=20,
        choices=CHILD_AGE_CHOICES,
        blank=True,
        null=True
    )

    TIME_CHOICES = [
        (0, "Part-Time"),
        (1, "Full-Time"),
    ]
    time_offering = models.IntegerField(choices=TIME_CHOICES)

    caregiver = models.ForeignKey(
        CaregiverInfo,
        on_delete=models.CASCADE,
        related_name="availabilities"
    )

    # Many-to-many fields
    services_offering = models.ManyToManyField(
        ServicesOffered,
        related_name="availability_services",
        blank=True
    )

    skills = models.ManyToManyField(
        Skill,
        related_name="availability_skills",
        blank=True
    )

    preferences_accepted = models.ManyToManyField(
        Preference,
        related_name="availability_preferences",
        blank=True
    )

    languages_known = models.ManyToManyField(
        Language,
        related_name="availability_languages",
        blank=True
    )

    # Validation
    def clean(self):
        if self.date <= date.today():
            raise ValidationError("Date must be after the current date.")

        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start_time.")

    def __str__(self):
        return f"Availability {self.availability_id} - {self.caregiver}"

