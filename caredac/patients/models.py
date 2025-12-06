from django.db import models


# ---------------------------------------------------
# Patient Master
# ---------------------------------------------------
class PatientMaster(models.Model):
    patient_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=20)

    class Meta:
        db_table = "patient_master"

    def __str__(self):
        return self.full_name


# ---------------------------------------------------
# Patient Language
# ---------------------------------------------------
class PatientLanguage(models.Model):
    patient_language_id = models.AutoField(primary_key=True)

    language = models.ForeignKey(
        'caredac_admin.SystemLanguage',
        on_delete=models.CASCADE,
        db_column='language_id'
    )

    patient = models.ForeignKey(
        PatientMaster,
        on_delete=models.CASCADE,
        db_column='patient_id'
    )

    class Meta:
        db_table = "patient_language"

    def __str__(self):
        return f"{self.patient.full_name}"


# ---------------------------------------------------
# Member Details
# ---------------------------------------------------
class MemberDetails(models.Model):
    RELATION_CHOICES = [
        ('self', 'Self'),
        ('child', 'Child'),
        ('partner', 'Partner'),
        ('client', 'Client'),
        ('other', 'Other'),
    ]

    member_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=20)
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES)

    patient = models.ForeignKey(
        PatientMaster,
        on_delete=models.CASCADE,
        db_column='patient_id'
    )

    class Meta:
        db_table = "member_details"

    def __str__(self):
        return f"{self.full_name} ({self.relation})"


# ---------------------------------------------------
# Patient Payments
# ---------------------------------------------------
class PatientPayments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)
    set_primary = models.BooleanField(default=False)

    patient = models.ForeignKey(
        PatientMaster,
        on_delete=models.CASCADE,
        db_column='patient_id'
    )

    class Meta:
        db_table = "patient_payments"

    def __str__(self):
        return f"Payment method for {self.patient.full_name}"


# ---------------------------------------------------
# Patient Help
# ---------------------------------------------------
class PatientHelp(models.Model):
    patient_help_id = models.AutoField(primary_key=True)

    patient = models.ForeignKey(
        PatientMaster,
        on_delete=models.CASCADE,
        db_column='patient_id',
        null = True,
        blank = True
    )

    help = models.ForeignKey(   # NEW COLUMN
        'caredac_admin.NeedHelp',
        on_delete=models.CASCADE,
        db_column='help_id',
        null = True
    )

    class Meta:
        db_table = "patient_help"

    def __str__(self):
        return f"Help for {self.patient.full_name}"



# ---------------------------------------------------
# Patient Service
# ---------------------------------------------------
class PatientService(models.Model):
    patient_service_id = models.AutoField(primary_key=True)

    patient = models.ForeignKey(
        PatientMaster,
        on_delete=models.CASCADE,
        db_column='patient_id'
    )

    services = models.TextField()  # CSV list of service IDs

    class Meta:
        db_table = "patient_service"

    def __str__(self):
        return f"Services for {self.patient.full_name}"


# ---------------------------------------------------
# Patient Condition
# ---------------------------------------------------
class PatientCondition(models.Model):
    condition_id = models.AutoField(primary_key=True)
    condition = models.TextField()

    patient = models.ForeignKey(
        PatientMaster,
        on_delete=models.CASCADE,
        db_column='patient_id'
    )

    class Meta:
        db_table = "patient_condition"

    def __str__(self):
        return f"Condition for {self.patient.full_name}"


# ---------------------------------------------------
# Special Needs
# ---------------------------------------------------
class SpecialNeeds(models.Model):
    special_need_id = models.AutoField(primary_key=True)
    needs = models.TextField()

    patient = models.ForeignKey(
        PatientMaster,
        on_delete=models.CASCADE,
        db_column='patient_id'
    )

    class Meta:
        db_table = "special_needs"

    def __str__(self):
        return f"Special Needs for {self.patient.full_name}"
