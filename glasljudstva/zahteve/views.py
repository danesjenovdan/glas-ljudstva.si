from django.shortcuts import render
from django.http import HttpResponseNotFound

from zahteve.models import WorkGroup, Demand

# Create your views here.
def landing(request):
    demands = Demand.objects.all()
    return render(request, 'zahteve/landing.html', context={'demands': demands})

def delovna_skupina(request, delovna_skupina_id):
    try:
        delovna_skupina = WorkGroup.objects.get(id=delovna_skupina_id)
    except WorkGroup.DoesNotExist:
        return HttpResponseNotFound()
    
    demands = Demand.objects.filter(workgroup=delovna_skupina)

    return render(request, 'zahteve/delovna_skupina.html', context={'demands': demands, 'id': delovna_skupina_id})
