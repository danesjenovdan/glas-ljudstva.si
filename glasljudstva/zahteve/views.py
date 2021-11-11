from django.shortcuts import render

from zahteve.models import WorkGroup, Demand

# Create your views here.
def landing(request):
    demands = Demand.objects.all()
    return render(request, 'zahteve/landing.html', context={'demands': demands})

def delovna_skupina(request, delovna_skupina_id):
    delovna_skupina = WorkGroup.objects.get_or_none(id=delovna_skupina_id)
    return render(request, 'zahteve/delovna_skupina.html', context={'demands': demands, 'id': delovna_skupina_id})
