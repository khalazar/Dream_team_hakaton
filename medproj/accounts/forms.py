from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('doctor', 'Врач'),
        ('nurse', 'Медсестра'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Роль")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Добавляем пользователя в нужную группу в зависимости от выбранной роли
            if self.cleaned_data['role'] == 'doctor':
                group, created = Group.objects.get_or_create(name='doctor')
                user.groups.add(group)
            elif self.cleaned_data['role'] == 'nurse':
                group, created = Group.objects.get_or_create(name='nurse')
                user.groups.add(group)
        return user
