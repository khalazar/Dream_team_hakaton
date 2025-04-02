from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa  # Убедитесь, что библиотека установлена: pip install xhtml2pdf
from .forms import DocumentGenerationForm
from patients.models import Person

# Рекомендации по диагнозам (можно вынести в настройки или базу данных)
RECOMMENDATIONS = {
    'простуда': "Пейте много жидкости, отдыхайте, принимайте парацетамол.",
    'перелом ноги': "Обратитесь к ортопеду, возможно, потребуется гипс.",
    'воспаление лёгких': "Антибиотики, постельный режим, обильное питьё.",
    'вывих плеча': "Обратитесь к травматологу, иммобилизация сустава.",
}

@login_required
def index(request):
    return render(request, 'documents/index.html')

@login_required
def generate_document(request):
    """
    Представление для вывода формы генерации документа.
    После отправки формы выводится страница с предварительным просмотром.
    """
    if request.method == 'POST':
        form = DocumentGenerationForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            diagnosis = form.cleaned_data['diagnosis']
            recommendation = RECOMMENDATIONS.get(diagnosis, "Рекомендации не заданы.")
            content = (
                f"Пациент: {patient.full_name}\n"
                f"Диагноз: {diagnosis}\n"
                f"Рекомендации: {recommendation}"
            )
            # Для передачи в шаблон передаём также id пациента и выбранный диагноз
            context = {
                'content': content,
                'patient': patient,
                'diagnosis': diagnosis,
                'recommendation': recommendation
            }
            return render(request, 'documents/document_preview.html', context)
    else:
        form = DocumentGenerationForm()
    return render(request, 'documents/document_form.html', {'form': form})

@login_required
def download_pdf(request):
    """
    Представление генерирует PDF по данным, переданным через GET-параметры.
    Для простоты данные передаются через URL: patient_id и diagnosis.
    """
    patient_id = request.GET.get('patient_id')
    diagnosis = request.GET.get('diagnosis')

    if not patient_id or not diagnosis:
        return HttpResponse("Неверные параметры", status=400)

    patient = get_object_or_404(Person, id=patient_id)
    recommendation = RECOMMENDATIONS.get(diagnosis, "Рекомендации не заданы.")

    context = {
        'patient': patient,
        'diagnosis': diagnosis,
        'recommendation': recommendation
    }

    template = get_template('documents/document_pdf.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="document_{patient.id}.pdf"'

    # Принудительное указание кодировки UTF-8 и шрифта
    pisa_status = pisa.CreatePDF(html.encode('utf-8'), dest=response, encoding='utf-8')

    if pisa_status.err:
        return HttpResponse("Ошибка при генерации PDF", status=500)

    return response
