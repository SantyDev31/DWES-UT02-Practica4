from django import forms 
from django.core.exceptions import ValidationError

from .models import User, Task

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password', 'password_confirm']

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        password_confirm = cleaned.get('password_confirm')

        if(password != password_confirm):
            raise ValidationError('Passwords dont match.')
        
        return cleaned
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            
        return user


class IndividualTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to']

    def clean(self):
        cleaned = super().clean()

        assigned_to = cleaned.get('assigned_to')

        if assigned_to and not assigned_to.is_student():
            raise ValidationError('Tasks must be assignated to a student')
        
        return cleaned
    
    def save(self, commit=True):
        task = super().save(commit=False)
        task.task_type = Task.TYPE_INDIVIDUAL
        task.created_by = self.initial.get('user')
        if commit:
            task.save()
        return task
    
    
class GroupTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'group']

    def clean(self):
        cleaned = super().clean()
        group = cleaned.get('group')

        if not group:
            raise ValidationError('You must select a group.')
        
        if group.members.count() <= 0:
            raise ValidationError('Group must have atleast 1 member.')

        return cleaned
    
    def save(self, commit=True):
        task = super().save(commit=False)
        task.task_type = Task.TYPE_GROUP
        task.created_by = self.initial.get('user')
        if commit:
            task.save()
        return task
