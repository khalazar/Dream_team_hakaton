from django.db import models
from django.conf import settings

class DocumentTemplate(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()  # Здесь может быть шаблон с плейсхолдерами

    def __str__(self):
        return self.title

class GeneratedDocument(models.Model):
    template = models.ForeignKey(DocumentTemplate, on_delete=models.CASCADE)
    patient = models.ForeignKey('patients.Person', on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content_filled = models.TextField()

    def __str__(self):
        return f"{self.template.title} - {self.patient.full_name} ({self.created_at})"
