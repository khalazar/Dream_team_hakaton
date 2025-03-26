from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('my-schedule/', views.my_schedule, name='my_schedule'),
    path('task/done/<int:task_id>/', views.task_done, name='task_done'),
]
