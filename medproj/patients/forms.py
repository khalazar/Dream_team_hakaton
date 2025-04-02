from django import forms
from django.contrib.auth import get_user_model  # Используем кастомную модель пользователя
from .models import Person

User = get_user_model()

class PatientForm(forms.ModelForm):
    """Форма для создания и редактирования пациента"""
    class Meta:
        model = Person
        fields = ['full_name', 'male', 'birth_date', 'phone', 'email', 'address']

class TransferPatientForm(forms.Form):
    """Форма для передачи пациента другому врачу"""
    new_doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='doctor'),
        label="Выбрать нового врача"
    )
