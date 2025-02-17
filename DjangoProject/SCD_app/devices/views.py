from django.shortcuts import render, get_object_or_404
from .models import Device
from .forms import DeviceForm
# from models import *


def devices(request):
    return render(request, 'devices.html')

def device_list(request):
    devices = Device.objects.all()
    # print(devices)
    return render(request, 'device_list.html', {'devices': devices})


def device_detail(request, device_id):
    # device = Device.objects.get(id=id)
    device = get_object_or_404(Device, id=device_id)
    return render(request, 'device_detail.html', {'device': device})


def add_device(request):
    if request.method == "POST":
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.owner = request.user
            device.save()
            return redirect('device_list')
    else:
        form = DeviceForm()

    return render(request, 'device_form.html', {'form': form})
# Create your views here.
