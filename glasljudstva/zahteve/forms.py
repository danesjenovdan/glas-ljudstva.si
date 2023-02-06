from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from .models import DemandAnswer, VoterQuestion, MonitoringReport, StateBody, WorkGroup, DemandState


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
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)

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


class MonitoringReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        election_id = kwargs.pop('election_id')
        super(MonitoringReportForm, self).__init__(*args, **kwargs)
        self.fields['working_body'] = forms.ModelChoiceField(queryset=WorkGroup.objects.filter(election=election_id), required=False)

    # working_body = forms.ModelChoiceField(queryset=WorkGroup.objects.filter(election=election_id), required=False)
    
    is_priority_demand = forms.BooleanField(label="Prioritetna zaveza", required=False)
    
    sort_by = forms.ChoiceField(required=False, choices=(
        ('workgroup', 'Področje dela'),
        ('state', 'Napredek'),
    ))

    sort_dir = forms.ChoiceField(required=False, choices=(
        ('asc', 'Naraščujoče'),
        ('desc', 'Padajoče'),
    ))
    
    responsible_state_bodies = forms.ModelMultipleChoiceField(
        queryset=StateBody.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    state = forms.ModelChoiceField(queryset=DemandState.objects.all(), required=False)

    class Meta:
        model = MonitoringReport
        fields = ['present_in_coalition_treaty', 'responsible_state_bodies', 'cooperative', 'state', 'is_priority_demand']

    