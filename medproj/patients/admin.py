from django.contrib import admin
from .models import Person, MedCard, Diagnosis, Visit

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'male', 'birth_date', 'phone')
    search_fields = ('full_name', 'email')

@admin.register(MedCard)
class MedCardAdmin(admin.ModelAdmin):
    list_display = ('number', 'person')
    search_fields = ('number',)

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'archived')
    search_fields = ('patient__full_name', 'doctor__username')
    list_filter = ('archived', 'date')
