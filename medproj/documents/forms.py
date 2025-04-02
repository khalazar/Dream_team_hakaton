from django import forms
from patients.models import Person

class DocumentGenerationForm(forms.Form):
    patient = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        label="Выберите пациента"
    )
    DIAGNOSIS_CHOICES = [
        ('простуда', 'Простуда'),
        ('перелом ноги', 'Перелом ноги'),
        ('воспаление лёгких', 'Воспаление лёгких'),
        ('вывих плеча', 'Вывих плеча'),
    ]
    diagnosis = forms.ChoiceField(
        choices=DIAGNOSIS_CHOICES,
        label="Выберите диагноз"
    )
