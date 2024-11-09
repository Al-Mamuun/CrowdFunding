from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.forms import ModelForm
from .models import *

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
            # Create the profile with the additional information
            Profile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
        return user

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        
