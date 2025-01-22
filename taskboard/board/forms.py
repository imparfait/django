from django import forms
from .models import Task, TaskList,Profile, TaskGroup
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'event_date', 'is_completed','list', 'group']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),}
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['list'].queryset = TaskList.objects.filter(user=user)
            self.fields['group'].queryset = TaskGroup.objects.filter(members=user)
        else:
            self.fields['list'].queryset = TaskList.objects.none()
            self.fields['group'].queryset = TaskGroup.objects.none()


class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['name', 'description', 'color']
        widgets = {
            'color': forms.RadioSelect(choices=TaskList.COLOR_CHOICES),
        }

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)  
    last_name = forms.CharField(max_length=30, required=False) 
    email= forms.EmailField(required=False)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']
    
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)    
    class Meta:
        model = User
        fields = ['username', 'email']
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
class TaskGroupForm(forms.ModelForm):
    class Meta:
        model = TaskGroup
        fields = ['name', 'description', 'members']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].widget = forms.CheckboxSelectMultiple()