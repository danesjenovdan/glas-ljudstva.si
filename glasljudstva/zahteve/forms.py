from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from .models import DemandAnswer, VoterQuestion


class RegisterForm(forms.ModelForm):
    email = forms.CharField(widget=widgets.EmailInput, label='E-naslov')
    password = forms.CharField(widget=widgets.PasswordInput, label='Geslo')
    newsletter_permission = forms.BooleanField(
        label="Če želiš, da Danes je nov dan tvoj e-naslov hrani in ti občasno pošlje elektronsko sporočilo z vsebino, vezano na Glas ljudstva, to označi v spodnjem polju. Tvojega e-naslova ne bomo izdali nikomur (niti drugim sodelujočim organizacijam).",
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


class DemandAnswerForm(forms.ModelForm):
    class Meta:
        model = DemandAnswer
        fields = ['agree_with_demand', 'comment', 'demand', 'party']
        widgets = {'agree_with_demand': forms.RadioSelect(choices=[(True, 'da'), (False, 'ne')]), 'demand': forms.HiddenInput(), 'party': forms.HiddenInput()}


class VoterQuestionForm(forms.ModelForm):
    class Meta:
        model = VoterQuestion
        fields = "__all__"
        labels = {
            "name": "Ime:",
            "hometown": "Kraj, iz katerega prihajaš: *",
            "receiver": "Komu želiš zastaviti vprašanje (kateri stranki oz. strankam, ali vsem)? *",
            "question": "Tvoje vprašanje: *"
        }
        widgets = {
            "question": forms.Textarea(attrs={"rows" : 6})
        }
