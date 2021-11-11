from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponseNotFound

from zahteve.models import WorkGroup, Demand
from zahteve.forms import RegisterForm

# Create your views here.
def landing(request):
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

    return render(request, 'zahteve/delovna_skupina.html', context={'demands': demands, 'delovna_skupina': delovna_skupina})

def demand(request, demand_id):
    try:
        demand = Demand.objects.get(id=demand_id)
    except:
        Demand.HttpResponseNotFound()

    return render(request, 'zahteve/zahteva.html', context={'demand': demand})

class Registracija(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/registration.html', context={'form': form})

    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username, username, password)
        # TODO send verification email
        return redirect('/')
