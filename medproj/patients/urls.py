from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('visits/', views.visit_list, name='visit_list'),
    path('visit/archive/<int:visit_id>/', views.visit_archive, name='visit_archive'),
    path('visit/create/', views.visit_create, name='visit_create'),
    path('visit/update/<int:visit_id>/', views.visit_update, name='visit_update'),
]
