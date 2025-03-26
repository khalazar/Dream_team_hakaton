from django.db import models

class LabResult(models.Model):
    patient = models.ForeignKey('patients.Person', on_delete=models.CASCADE)
    result_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
