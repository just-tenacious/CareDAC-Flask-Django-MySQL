from django.db import models
from caredac_admin.models import SystemLanguage


class CaregiverInfo(models.Model):
    caregiver_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pincode = models.IntegerField(max_length=255)

    class Meta:
        db_table = "caregiver_info"

    def __str__(self):
        return self.full_name


class CaregiverDocuments(models.Model):
    docx_id = models.AutoField(primary_key=True)
    covid_19 = models.FileField(upload_to='documents/covid_19/', blank=True, null=True)
    first_aid = models.FileField(upload_to='documents/first_aid/', blank=True, null=True)
    ndis = models.FileField(upload_to='documents/ndis/', blank=True, null=True)
    police = models.FileField(upload_to='documents/police/', blank=True, null=True)
    child_chk = models.FileField(upload_to='documents/child_chk/', blank=True, null=True)
    visa = models.FileField(upload_to='documents/visa/', blank=True, null=True)
    resume = models.FileField(upload_to='documents/resume/', blank=True, null=True)

    caregiver = models.ForeignKey(
        CaregiverInfo,
        on_delete=models.CASCADE,
        db_column='caregiver_id',
        related_name='documents'
    )

    class Meta:
        db_table = "caregiver_documents"


class CaregiverDetails(models.Model):
    detail_id = models.AutoField(primary_key=True)
    resume = models.IntegerField(default=0)  # 0 or 1
    disability_support_worker = models.IntegerField(default=0)
    hours_cnt = models.IntegerField()  # 1/2/3/4
    experience = models.CharField(max_length=255)
    police_chk_status = models.CharField(max_length=255)
    qualifications = models.TextField()
    wcc = models.IntegerField(default=0)
    ndis = models.IntegerField(default=0)
    first_aid_training = models.IntegerField(default=0)
    preferred_work_area = models.CharField(max_length=255)
    services_offered = models.TextField()
    languages = models.CharField(max_length=255)

    caregiver = models.ForeignKey(
        CaregiverInfo,
        on_delete=models.CASCADE,
        db_column='caregiver_id',
        related_name='details'
    )

    class Meta:
        db_table = "caregiver_details"


class CaregiverLanguage(models.Model):
    cg_lang_id = models.AutoField(primary_key=True)
    lang = models.ForeignKey(SystemLanguage, on_delete=models.CASCADE)

    caregiver = models.ForeignKey(
        CaregiverInfo,
        on_delete=models.CASCADE,
        db_column='caregiver_id',
        related_name='languages'
    )

    class Meta:
        db_table = "caregiver_language"

class CaregiverPayments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=10)  # Example: MM/YY or MM/YYYY
    cvv = models.CharField(max_length=4)
    set_primary = models.IntegerField(default=0)  # 0 or 1

    caregiver = models.ForeignKey(
        CaregiverInfo,
        on_delete=models.CASCADE,
        db_column='caregiver_id',
        related_name='payments'
    )

    class Meta:
        db_table = "caregiver_payments"

    def __str__(self):
        return f"{self.card_name} - {self.card_number[-4:]}"
