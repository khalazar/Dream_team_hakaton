from django.shortcuts import render, redirect
from .models import LabResult
from patients.models import Person


def index(request):
    return render(request, 'integration/index.html')


def fetch_lab_results(request, patient_id):
    patient = Person.objects.get(id=patient_id)
    # Здесь вместо заглушки получаем/обрабатываем реальные данные
    fake_result = "Hb: 140 g/L, RBC: 4.5x10^12/L"
    LabResult.objects.create(patient=patient, result_data=fake_result)
    lab_results = LabResult.objects.filter(patient=patient)
    return render(request, 'integration/lab_results.html', {'patient': patient, 'lab_results': lab_results})
