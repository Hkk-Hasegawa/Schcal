from django.shortcuts import render
from .models import Suresubject

def monthcal(request):
    Suresubjects=Suresubject.objects.all()
    return render(request, 'MonCal/monthcal.html', {'Suresubjects':Suresubjects})
