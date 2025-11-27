from django.db import models

class SystemLanguage(models.Model):
    language_id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=255)

    class Meta:
        db_table = 'system_language'

    def __str__(self):
        return self.language


class ServiceOffered(models.Model):
    service_id = models.AutoField(primary_key=True)
    services = models.CharField(max_length=255)

    class Meta:
        db_table = 'service_offered'

    def __str__(self):
        return self.services

class NeedHelp(models.Model):
    help_id = models.AutoField(primary_key=True)
    help_name = models.CharField(max_length=255)

    class Meta:
        db_table = "need_help"

    def __str__(self):
        return self.help_name