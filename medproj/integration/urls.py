from django.urls import path
from . import views

app_name = 'integration'

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-lab-results/<int:patient_id>/', views.fetch_lab_results, name='fetch_lab_results'),
]
