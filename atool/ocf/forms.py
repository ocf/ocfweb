from django import forms
from django.forms import widgets

class LoginForm(forms.Form):
    username = forms.CharField(label="OCF Username",
        min_length=3,
        max_length=8)
    password = forms.CharField(widget=forms.PasswordInput,
        label="Password",
        min_length=8,
        max_length=64)
