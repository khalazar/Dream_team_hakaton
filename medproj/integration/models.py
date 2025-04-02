from django.db import models

class LabResult(models.Model):
    patient = models.ForeignKey('patients.Person', on_delete=models.CASCADE)
    result_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.patient.full_name} - {self.created_at}"
