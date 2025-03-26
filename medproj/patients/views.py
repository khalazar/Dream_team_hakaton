from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Person, Visit

def patient_list(request):
    query = request.GET.get('q')
    if query:
        patients = Person.objects.filter(full_name__icontains=query)
    else:
        patients = Person.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})

def visit_list(request):
    q_name = request.GET.get('name')
    q_medcard = request.GET.get('medcard')
    q_diag = request.GET.get('diag')

    visits = Visit.objects.all()

    if q_name:
        visits = visits.filter(patient__full_name__icontains=q_name)
    if q_medcard:
        visits = visits.filter(patient__medcard__number__icontains=q_medcard)
    if q_diag:
        visits = visits.filter(diagnosis__name__icontains=q_diag)

    return render(request, 'patients/visit_list.html', {'visits': visits})

def visit_archive(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    visit.archived = True
    visit.save()
    return redirect('patients:visit_list')

def visit_create(request):
    # Здесь можно реализовать логику создания приёма
    # Либо использовать ModelForm
    pass

def visit_update(request, visit_id):
    # Логика обновления
    pass
