from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponseNotFound
from django.contrib.auth import login

from zahteve.models import WorkGroup, Demand, EmailVerification
from zahteve.forms import RegisterForm

# Create your views here.
def landing(request):
    print(request.user)
    work_groups = WorkGroup.objects.all()
    for wg in work_groups:
        wg.demands = Demand.objects.filter(workgroup=wg)

    return render(request, 'zahteve/landing.html', context={'work_groups': work_groups})

def delovna_skupina(request, delovna_skupina_id):
    try:
        delovna_skupina = WorkGroup.objects.get(id=delovna_skupina_id)
    except WorkGroup.DoesNotExist:
        return HttpResponseNotFound()

    demands = Demand.objects.filter(workgroup=delovna_skupina)

    og_title = delovna_skupina.og_title
    og_description = delovna_skupina.og_description

    return render(request, 'zahteve/delovna_skupina.html', context={'demands': demands, 'delovna_skupina': delovna_skupina, 'og_title': og_title, 'og_description': og_description})

def demand(request, demand_id):
    form = RegisterForm()
    try:
        demand = Demand.objects.get(id=demand_id)
    except Demand.DoesNotExist:
        return HttpResponseNotFound()

    return render(request, 'zahteve/zahteva.html', context={'demand': demand, 'form': form})

def verify_email(request, token):
    verification = get_object_or_404(EmailVerification, verification_key=token)
    user = verification.user
    user.is_active = True
    login(request, user)
    return redirect('/')


class Registracija(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/registration.html', context={'form': form})

    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        redirect_path = request.META.get('HTTP_REFERER', '\\')
        user = User.objects.create_user(username, username, password, is_active=False)
        # TODO send verification email
        return redirect('/')
