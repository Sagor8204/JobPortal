from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, RecruiterProfile, JobseekerProfile, Job

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('display_name', 'email', 'user_type')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply form-control to password fields which are defined in UserCreationForm
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'company_description', 'website']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }

class JobseekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobseekerProfile
        fields = ['skills', 'resume']
        widgets = {
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django, SQL'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'openings', 'category', 'description', 'required_skills']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'openings': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'required_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django'}),
        }