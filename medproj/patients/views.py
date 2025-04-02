from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Person, Visit
from django import forms
from django.shortcuts import render
from .forms import PatientForm, TransferPatientForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'patients/index.html')

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

# Определим форму для модели Visit
class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['date', 'time', 'doctor', 'patient', 'diagnosis', 'notes']

def visit_create(request):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients:visit_list')
    else:
        form = VisitForm()
    return render(request, 'patients/visit_form.html', {'form': form, 'visit': None})

def visit_update(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            return redirect('patients:visit_list')
    else:
        form = VisitForm(instance=visit)
    return render(request, 'patients/visit_form.html', {'form': form, 'visit': visit})


@login_required
def add_patient(request):
    """Представление для создания нового пациента без создания приёма."""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients:patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/add_patient.html', {'form': form})

@login_required
def select_transfer_patient(request):
    """
    Представление для выбора пациента, которого необходимо передать.
    Здесь можно вывести список пациентов с кнопкой "Передать" для каждого.
    """
    patients = Person.objects.all()
    return render(request, 'patients/select_transfer_patient.html', {'patients': patients})

@login_required
def transfer_patient(request, patient_id):
    """Представление для передачи пациента от одного врача другому."""
    patient = get_object_or_404(Person, id=patient_id)
    if request.method == 'POST':
        form = TransferPatientForm(request.POST)
        if form.is_valid():
            new_doctor = form.cleaned_data['new_doctor']
            # Например, можно добавить новое поле в Person, которое хранит лечащего врача.
            # Предположим, что в модели Person есть поле doctor:
            patient.doctor = new_doctor
            patient.save()
            return redirect('patients:patient_list')
    else:
        form = TransferPatientForm()
    return render(request, 'patients/transfer_patient.html', {'form': form, 'patient': patient})

