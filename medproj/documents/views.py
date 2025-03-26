from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DocumentTemplate, GeneratedDocument
from patients.models import Person

@login_required
def generate_document(request, template_id, patient_id):
    template = get_object_or_404(DocumentTemplate, id=template_id)
    patient = get_object_or_404(Person, id=patient_id)

    # Допустим, у нас в шаблоне есть плейсхолдеры {patient_name}, {doctor_name}
    content = template.content
    content = content.replace('{patient_name}', patient.full_name)
    content = content.replace('{doctor_name}', request.user.username)

    generated = GeneratedDocument.objects.create(
        template=template,
        patient=patient,
        doctor=request.user,
        content_filled=content
    )

    return render(request, 'documents/generated.html', {'document': generated})
