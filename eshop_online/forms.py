from django import forms
from django.contrib.auth import get_user_model
from django.core import validators

class LoginForm(forms.Form):
    userName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your username'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'enter your passowrd'})
    )


User = get_user_model()


