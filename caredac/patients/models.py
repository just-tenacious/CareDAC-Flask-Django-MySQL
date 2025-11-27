from django.db import models
from caredac_admin.models import SystemLanguage

# Choices for member relationship
relationship_choices = (
    ('Self', 'Self'),
    ('Child', 'Child'),
    ('Partner', 'Partner'),
    ('Client', 'Client'),
    ('Other', 'Other')
)

# User master table
class UserMaster(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=150)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    emergency_no = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    acc_status = models.IntegerField(default=0)

    class Meta:
        db_table = "user_master"

    def __str__(self):
        return self.full_name


# User languages
class UserLanguage(models.Model):
    user_lang_id = models.AutoField(primary_key=True)
    lang = models.ForeignKey(SystemLanguage, on_delete=models.CASCADE)
    user = models.ForeignKey("patients.UserMaster", on_delete=models.CASCADE)

    class Meta:
        db_table = "user_language"


# User payments
class UserPayments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=10)  # Example: MM/YY or MM/YYYY
    cvv = models.CharField(max_length=4)
    set_primary = models.IntegerField(default=0)  # 0 or 1

    user = models.ForeignKey(
        UserMaster,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='payments'
    )

    class Meta:
        db_table = "user_payments"

    def __str__(self):
        return f"{self.card_name} - {self.card_number[-4:]}"


# Member details with relation field
class MemberDetails(models.Model):
    member_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=150)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    emergency_no = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    acc_status = models.IntegerField(default=0)
    relation = models.CharField(
        max_length=20,
        choices=relationship_choices,
        default='Self'
    )

    # Foreign key to UserMaster
    user = models.ForeignKey(
        UserMaster,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='member_details'
    )

    class Meta:
        db_table = "member_detail"

    def __str__(self):
        return f"{self.full_name} ({self.relation})"


# from django.db import models
# from caredac_admin.models import SystemLanguage

# relationship_choices = (
#     ('Self', 'Self'),
#     ('Child', 'Child'),
#     ('Partner', 'Partner'),
#     ('Client', 'Client'),
#     ('Other', 'Other')
# )

# class UserMaster(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     full_name = models.CharField(max_length=150)
#     dob = models.DateField(null=True, blank=True)
#     email = models.EmailField(unique=True)
#     phone_no = models.CharField(max_length=15)
#     emergency_no = models.CharField(max_length=15, null=True, blank=True)
#     password = models.CharField(max_length=255)
#     gender = models.CharField(max_length=10)
#     address = models.TextField()
#     country = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=10)
#     acc_status = models.IntegerField(default=0)

#     class Meta:
#         db_table = "user_master"

#     def __str__(self):
#         return self.full_name


# class UserLanguage(models.Model):
#     user_lang_id = models.AutoField(primary_key=True)
#     lang = models.ForeignKey(SystemLanguage, on_delete=models.CASCADE)
#     user = models.ForeignKey("patients.UserMaster", on_delete=models.CASCADE)

#     class Meta:
#         db_table = "user_language"

# class UserPayments(models.Model):
#     payment_id = models.AutoField(primary_key=True)
#     card_name = models.CharField(max_length=255)
#     card_number = models.CharField(max_length=20)
#     expiry_date = models.CharField(max_length=10)  # Example: MM/YY or MM/YYYY
#     cvv = models.CharField(max_length=4)
#     set_primary = models.IntegerField(default=0)  # 0 or 1

#     user = models.ForeignKey(
#         UserMaster,
#         on_delete=models.CASCADE,
#         db_column='user_id',
#         related_name='payments'
#     )

#     class Meta:
#         db_table = "user_payments"

#     def __str__(self):
#         return f"{self.card_name} - {self.card_number[-4:]}"

# class MemberDetails(models.Model):
#     member_id = models.AutoField(primary_key=True)
#     full_name = models.CharField(max_length=150)
#     dob = models.DateField(null=True, blank=True)
#     email = models.EmailField(unique=True)
#     phone_no = models.CharField(max_length=15)
#     emergency_no = models.CharField(max_length=15, null=True, blank=True)
#     password = models.CharField(max_length=255)
#     gender = models.CharField(max_length=10)
#     address = models.TextField()
#     country = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=10)
#     acc_status = models.IntegerField(default=0)

#     # Foreign key to UserMaster
#     user = models.ForeignKey(
#         UserMaster,
#         on_delete=models.CASCADE,
#         db_column='user_id',
#         related_name='member_details'
#     )

#     class Meta:
#         db_table = "member_detail"

#     def __str__(self):
#         return self.full_name
