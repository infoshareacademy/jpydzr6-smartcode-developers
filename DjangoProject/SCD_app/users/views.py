from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def dashboard(request):
    return render(request, 'dashboard.html')

def bulb_manager(request):
    return render(request, 'bulb_manager.html')

def curtain_manager(request):
    return render(request, 'curtain_manager.html')

def lawnmower_manager(request):
    return render(request, 'lawnmower_manager.html')

def plug_manager(request):
    return render(request, 'plug_manager.html')


def thermostat_manager(request):
    return render(request, 'thermostat_manager.html')

def weatherstation_manager(request):
    return render(request, 'weatherstation_manager.html')







