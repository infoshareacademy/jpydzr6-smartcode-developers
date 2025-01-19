from django.shortcuts import render
from django.http import HttpResponse
from .models import Device

def index(request):
    qs = Device.objects.all()
    device = qs.first()
    response = ""

    for device in qs:
        response += f"{device.name}, {device.brand}, {device.connected}, {device.last_updated}"

    return HttpResponse(response)

# Create your views here.
