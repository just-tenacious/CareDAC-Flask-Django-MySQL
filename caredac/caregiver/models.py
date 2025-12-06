from django.db import models


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
    address = models.TextField()
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pincode = models.CharField(max_length=20)
    acc_status = models.IntegerField(default=0)

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

    caregiver = models.ForeignKey(
        CaregiverInfo,
        on_delete=models.CASCADE,
        db_column='caregiver_id'
    )

    class Meta:
        db_table = "caregiver_documents"


# -------------------------------
# Caregiver Details
# -------------------------------
class CaregiverDetails(models.Model):
    detail_id = models.AutoField(primary_key=True)

    resume = models.IntegerField(default=0)
    disability_support_worker = models.IntegerField(default=0)
    hours_cnt = models.IntegerField()
    experience = models.CharField(max_length=255)
    police_chk_status = models.CharField(max_length=255)
    qualifications = models.TextField()
    wcc = models.IntegerField(default=0)
    ndis = models.IntegerField(default=0)
    first_aid_training = models.IntegerField(default=0)
    preferred_work_area = models.CharField(max_length=255)
    services_offered = models.TextField()  # CSV IDs
    languages = models.CharField(max_length=255)

    caregiver = models.ForeignKey(
        CaregiverInfo,
        on_delete=models.CASCADE,
        db_column='caregiver_id'
    )

    class Meta:
        db_table = "caregiver_details"


# -------------------------------
# Caregiver Language
# -------------------------------
class CaregiverLanguage(models.Model):
    caregiver_language_id = models.AutoField(primary_key=True)

    language_id = models.ForeignKey(
        'caredac_admin.SystemLanguage',
        on_delete=models.CASCADE,
        db_column='language_id'
    )

    caregiver_id = models.ForeignKey(
        CaregiverInfo,
        on_delete=models.CASCADE,
        db_column='caregiver_id'
    )

    class Meta:
        db_table = 'caregiver_language'

    def __str__(self):
        return f"{self.caregiver_id.full_name}"


# -------------------------------
# Caregiver Payments
# -------------------------------
class CaregiverPayments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)
    set_primary = models.BooleanField(default=False)

    caregiver_id = models.ForeignKey(
        CaregiverInfo,
        on_delete=models.CASCADE,
        db_column='caregiver_id'
    )

    class Meta:
        db_table = 'caregiver_payments'

    def __str__(self):
        return f"Payment method for {self.caregiver_id.full_name}"
