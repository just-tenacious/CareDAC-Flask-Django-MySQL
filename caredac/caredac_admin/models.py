from django.db import models

class SystemLanguage(models.Model):
    lang_id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=100)

    class Meta:
        db_table = "system_language"

    def __str__(self):
        return self.language
