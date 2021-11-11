from django.shortcuts import render
from django.http import HttpResponseNotFound

from zahteve.models import WorkGroup, Demand

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