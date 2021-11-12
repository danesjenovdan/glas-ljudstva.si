from django import forms
from django.forms import widgets
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    email = forms.CharField(widget=widgets.EmailInput, label='E-naslov')
    password = forms.CharField(widget=widgets.PasswordInput, label='Geslo')
    newsletter_permission = forms.BooleanField(
        label="Če želiš, da Danes je nov dan tvoj e-naslov hrani, da ti občasno pošlje elektronsko sporočilo z vsebino vezano na Glas ljudstva pusti kljukico v spodnji škatli. Tvojega e-naslova ne bomo izdali nikomur (niti drugim sodelujočim organizacijam).",
        label_suffix='',
        required=False
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            'newsletter_permission'
        ]


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

