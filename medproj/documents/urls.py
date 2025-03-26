from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('generate/<int:template_id>/<int:patient_id>/', views.generate_document, name='generate_document'),
]
