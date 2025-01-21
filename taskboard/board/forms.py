from django import forms
from .models import Task, TaskList,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'event_date', 'is_completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),}
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Забираємо параметр user
        super().__init__(*args, **kwargs)
        if not self.instance.list:
            self.instance.list = TaskList.objects.get_or_create(user=self.user, name="Default List")[0]

class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['name', 'description', 'color']

class GroupInviteForm(forms.Form):
    email = forms.EmailField(label="User Email", max_length=255)

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)  
    last_name = forms.CharField(max_length=30, required=False) 
    email= forms.EmailField(required=False)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']
    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if not password:
    #         return None 
    #     return password 
    
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