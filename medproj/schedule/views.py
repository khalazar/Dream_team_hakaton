from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Shift, Task
from django.shortcuts import render

def index(request):
    return render(request, 'schedule/index.html')

@login_required
def my_schedule(request):
    shifts = Shift.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user, done=False)
    return render(request, 'schedule/my_schedule.html', {'shifts': shifts, 'tasks': tasks})

@login_required
def task_done(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.done = True
    task.save()
    return redirect('schedule:my_schedule')
