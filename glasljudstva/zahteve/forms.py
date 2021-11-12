from django import forms
from django.forms import widgets
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    email = forms.CharField(widget=widgets.EmailInput, label='E-naslov')
    password = forms.CharField(widget=widgets.PasswordInput, label='Geslo')

    class Meta:
        model = User
        fields = ["email", "password"]


class RequestRestorePasswordForm(forms.ModelForm):
    email = forms.CharField(widget=widgets.EmailInput, label='E-naslov')

    class Meta:
        model = User
        fields = ["email"]


class RestorePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=widgets.PasswordInput, label='Geslo')

    class Meta:
        model = User
        fields = ["password"]

