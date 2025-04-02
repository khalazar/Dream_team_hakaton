from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
User = get_user_model()
doctor_group = Group.objects.get(name='doctor')
doctors = User.objects.filter(groups=doctor_group)
print(doctors)