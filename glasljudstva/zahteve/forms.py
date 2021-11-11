from django import forms
from django.forms import widgets
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    email = forms.CharField(widget=widgets.EmailInput)
    password = forms.CharField(widget=widgets.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password"]
