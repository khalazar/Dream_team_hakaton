from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.generate_document, name='generate_document'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),

]
