from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import render

def index(request):
    return render(request, 'accounts/index.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patients:patient_list')  # например, на список пациентов
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
