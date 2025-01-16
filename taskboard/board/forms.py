from django import forms
from .models import Task, TaskList,Profile
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'is_completed', 'list']

class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['name', 'description', 'color']

class GroupInviteForm(forms.Form):
    email = forms.EmailField(label="User Email", max_length=255)

class EditProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)  
    first_name = forms.CharField(max_length=30, required=False)  
    last_name = forms.CharField(max_length=30, required=False)  
    email = forms.EmailField(required=False)
    avatar = forms.ImageField(required=False)  
    class Meta:
        model = Profile
        fields = ['avatar']
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            return None 
        return password 