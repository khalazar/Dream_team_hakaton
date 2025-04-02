from django.urls import path
from . import views

app_name = 'integration'

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('lab_results/<int:patient_id>/', views.fetch_lab_results, name='fetch_lab_results'),  # Путь для получения лабораторных результатов
    path('medicines/', views.fetch_medicines, name='fetch_medicines'),  # Путь для списка медикаментов
]
