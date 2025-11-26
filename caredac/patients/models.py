from django.db import models
from caredac_admin.models import SystemLanguage

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


class UserLanguage(models.Model):
    user_lang_id = models.AutoField(primary_key=True)
    lang = models.ForeignKey(SystemLanguage, on_delete=models.CASCADE)
    user = models.ForeignKey("patients.UserMaster", on_delete=models.CASCADE)

    class Meta:
        db_table = "user_language"
