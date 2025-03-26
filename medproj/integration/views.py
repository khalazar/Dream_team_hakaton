from django.shortcuts import render, redirect
from .models import LabResult
from patients.models import Person

def fetch_lab_results(request, patient_id):
    # Заглушка: допустим, мы делаем запрос к внешней системе
    patient = Person.objects.get(id=patient_id)
    # Получаем какие-то результаты (заглушка)
    fake_result = "Hb: 140 g/L, RBC: 4.5x10^12/L"
    LabResult.objects.create(patient=patient, result_data=fake_result)
    return redirect('patients:patient_list')
