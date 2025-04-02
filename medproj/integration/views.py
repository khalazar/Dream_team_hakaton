import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import LabResult
from patients.models import Person
from django.conf import settings



API_ADDR_LABS = settings.API_ADDR_LABS
API_ADDR_MEDICINES = settings.API_ADDR_MEDICINES
TOKEN = settings.TOKEN
CACHE_TIMEOUT = settings.CACHE_TIMEOUT


# Страница по умолчанию
def index(request):
    return render(request, 'integration/index.html')


def get_medicines():
    url = f"{settings.API_ADDR_MEDICINES}/medicines"
    headers = {'Authorization': f'Bearer {settings.TOKEN}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200 and 'application/json' in response.headers.get(
            'Content-Type', ''):
        return response.json()  # Возвращаем список медикаментов в виде JSON
    return None  # Если что-то пошло не так, возвращаем None


def fetch_medicines(request):
    medicines = get_medicines()

    if not medicines:
        return render(request, 'integration/error.html',
                      {"message": "Не удалось загрузить список медикаментов."})

    return render(request, 'integration/medicines_list.html',
                  {'medicines': medicines})

# Функция для получения лабораторных результатов по пациенту
def fetch_lab_results(request, patient_id):
    patient = Person.objects.get(id=patient_id)

    # Получаем sessionId для доступа к API
    session_id = get_session_id(settings.API_ADDR_LABS)
    if not session_id:
        return JsonResponse({"error": "Не удалось получить sessionId для API"},
                            status=400)

    # Получаем результаты лабораторных исследований через API
    lab_results = get_api(settings.API_ADDR_LABS, "/labReserchInfo", "",
                          {'Cookie': f'sessionId={session_id}'})
    if not lab_results:
        return JsonResponse(
            {"error": "Не удалось получить лабораторные результаты"},
            status=400)

    # Для каждого лабораторного результата сохраняем его в базу данных
    for lab_result in lab_results:
        if lab_result[
            'patientLocalId'] == patient.id:  # Проверяем, что это результаты для нужного пациента
            LabResult.objects.create(
                patient=patient,
                result_data=str(lab_result)
                # Преобразуем результат в строку для хранения
            )

    # Получаем все результаты для пациента
    lab_results_db = LabResult.objects.filter(patient=patient)

    # Рендерим шаблон с результатами
    return render(request, 'integration/lab_results.html',
                  {'patient': patient, 'lab_results': lab_results_db})


# Функция для получения данных с API
def get_api(uri, path="", command="", headers={}):
    url = f"{uri}{path}{command}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and 'application/json' in response.headers.get(
            'Content-Type', ''):
        return response.json()
    return None


# Функция для получения sessionId с API
def get_session_id(api_addr):
    response = get_api(api_addr, "/", "auth",
                       {'Authorization': f'Bearer {settings.TOKEN}'})
    if response and response.get('errorCode') == 0:
        return response.get('sessionId')
    return None
