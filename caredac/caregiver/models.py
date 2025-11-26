from django.db import models
import os

# -------------------------------
# Caregiver Info
# -------------------------------
class CaregiverInfo(models.Model):
    caregiver_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    profile_pic = models.ImageField(upload_to='caregiver/profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=20)
    acc_status = models.IntegerField(default=0) # 0: not verified, 1: verified

    class Meta:
        db_table = "caregiver_info"

    def __str__(self):
        return self.full_name


# -------------------------------
# Caregiver Documents
# -------------------------------
class CaregiverDocuments(models.Model):
    docx_id = models.AutoField(primary_key=True)

    covid_19 = models.FileField(upload_to='caregiver/covid_19/', blank=True, null=True)
    first_aid = models.FileField(upload_to='caregiver/first_aid/', blank=True, null=True)
    ndis = models.FileField(upload_to='caregiver/ndis/', blank=True, null=True)
    police = models.FileField(upload_to='caregiver/police/', blank=True, null=True)
    child_chk = models.FileField(upload_to='caregiver/child_chk/', blank=True, null=True)
    visa = models.FileField(upload_to='caregiver/visa/', blank=True, null=True)
    resume = models.FileField(upload_to='caregiver/resume/', blank=True, null=True)

    caregiver = models.ForeignKey(CaregiverInfo, on_delete=models.CASCADE, db_column='caregiver_id')

    class Meta:
        db_table = "caregiver_documents"


# -------------------------------
# Caregiver Details
# -------------------------------
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

    caregiver = models.ForeignKey(CaregiverInfo, on_delete=models.CASCADE, db_column='caregiver_id')

    class Meta:
        db_table = "caregiver_details"