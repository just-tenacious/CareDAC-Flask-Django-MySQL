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
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=20)

    class Meta:
        db_table = "caregiver_info"

    def __str__(self):
        return self.full_name


# -------------------------------
# Helper function for file paths
# -------------------------------
def caregiver_document_path(instance, filename, folder_name):
    """
    Store files in media/caregiver/<docx_id>/<folder_name>/<filename>
    """
    return f'caregiver/{instance.docx_id}/{folder_name}/{filename}'


# -------------------------------
# Upload functions (serializable for migrations)
# -------------------------------
def covid_19_upload_to(instance, filename):
    return caregiver_document_path(instance, filename, 'covid_19')

def first_aid_upload_to(instance, filename):
    return caregiver_document_path(instance, filename, 'first_aid')

def ndis_upload_to(instance, filename):
    return caregiver_document_path(instance, filename, 'ndis')

def police_upload_to(instance, filename):
    return caregiver_document_path(instance, filename, 'police')

def child_chk_upload_to(instance, filename):
    return caregiver_document_path(instance, filename, 'child_chk')

def visa_upload_to(instance, filename):
    return caregiver_document_path(instance, filename, 'visa')

def resume_upload_to(instance, filename):
    return caregiver_document_path(instance, filename, 'resume')


# -------------------------------
# Caregiver Documents
# -------------------------------
class CaregiverDocuments(models.Model):
    docx_id = models.AutoField(primary_key=True)

    covid_19 = models.FileField(upload_to=covid_19_upload_to, blank=True, null=True)
    first_aid = models.FileField(upload_to=first_aid_upload_to, blank=True, null=True)
    ndis = models.FileField(upload_to=ndis_upload_to, blank=True, null=True)
    police = models.FileField(upload_to=police_upload_to, blank=True, null=True)
    child_chk = models.FileField(upload_to=child_chk_upload_to, blank=True, null=True)
    visa = models.FileField(upload_to=visa_upload_to, blank=True, null=True)
    resume = models.FileField(upload_to=resume_upload_to, blank=True, null=True)

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


# # from django.db import models

# # # Create your models here.

# from django.db import models

# # -------------------------------
# # Caregiver Info
# # -------------------------------
# class CaregiverInfo(models.Model):
#     caregiver_id = models.AutoField(primary_key=True)
#     full_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     phone_no = models.CharField(max_length=20)
#     password = models.CharField(max_length=255)
#     dob = models.DateField()
#     profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#     gender = models.CharField(max_length=20)

#     class Meta:
#         db_table = "caregiver_info"

#     def __str__(self):
#         return self.full_name


# # -------------------------------
# # Caregiver Documents
# # -------------------------------
# class CaregiverDocuments(models.Model):
#     docx_id = models.AutoField(primary_key=True)

#     covid_19 = models.FileField(upload_to='documents/covid_19/', blank=True, null=True)
#     first_aid = models.FileField(upload_to='documents/first_aid/', blank=True, null=True)
#     ndis = models.FileField(upload_to='documents/ndis/', blank=True, null=True)
#     police = models.FileField(upload_to='documents/police/', blank=True, null=True)
#     child_chk = models.FileField(upload_to='documents/child_chk/', blank=True, null=True)
#     visa = models.FileField(upload_to='documents/visa/', blank=True, null=True)
#     resume = models.FileField(upload_to='documents/resume/', blank=True, null=True)

#     caregiver = models.ForeignKey(
#         CaregiverInfo,
#         on_delete=models.CASCADE,
#         db_column='caregiver_id'
#     )

#     class Meta:
#         db_table = "caregiver_documents"


# # -------------------------------
# # Caregiver Details
# # -------------------------------
# class CaregiverDetails(models.Model):
#     detail_id = models.AutoField(primary_key=True)
#     resume = models.IntegerField(default=0)  # 0 or 1
#     disability_support_worker = models.IntegerField(default=0)
#     hours_cnt = models.IntegerField()  # 1/2/3/4
#     experience = models.CharField(max_length=255)
#     police_chk_status = models.CharField(max_length=255)
#     qualifications = models.TextField()
#     wcc = models.IntegerField(default=0)
#     ndis = models.IntegerField(default=0)
#     first_aid_training = models.IntegerField(default=0)
#     preferred_work_area = models.CharField(max_length=255)
#     services_offered = models.TextField()
#     languages = models.CharField(max_length=255)

#     caregiver = models.ForeignKey(
#         CaregiverInfo,
#         on_delete=models.CASCADE,
#         db_column='caregiver_id'
#     )

#     class Meta:
#         db_table = "caregiver_details"
