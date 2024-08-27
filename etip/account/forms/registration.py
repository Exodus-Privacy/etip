from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=('Email'), widget=forms.EmailInput(),)

    first_name = forms.CharField(label=('first-name'), widget=forms.TextInput(),)
    last_name = forms.CharField(label=('last-name'), widget=forms.TextInput(),)
    
    class Meta():
        model = User
        fields = ("username", "first_name", "last_name", "email",)

