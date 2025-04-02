from django.db import models
from django.conf import settings

class Person(models.Model):
    full_name = models.CharField(max_length=255)
    male = models.BooleanField()  # Обязательное поле, True - мужской, False - женский
    birth_date = models.DateField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')

    def __str__(self):
        return self.full_name

class MedCard(models.Model):
    number = models.IntegerField(unique=True)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='medcard')

    def __str__(self):
        return f"Медкарта №{self.number} ({self.person.full_name})"

class Diagnosis(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Visit(models.Model):
    date = models.DateField()
    time = models.TimeField()
    doctor = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'doctor'})
    patient = models.ForeignKey(Person, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient.full_name} - {self.date} {self.time}"
