from django.shortcuts import render, get_object_or_404, redirect
from .models import Device, BulbStatus
from .forms import DeviceForm, BulbStatusForm


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

# BULB
def bulb_list(request):
    bulbs = BulbStatus.objects.all()
    return render(request, 'bulbs/bulb_list.html', {'bulbs': bulbs})

def bulb_detail(request, pk):
    bulb = get_object_or_404(BulbStatus, pk=pk)
    return render(request, 'bulbs/bulb_detail.html', {'bulb': bulb})

def bulb_create(request):
    if request.method == "POST":
        form = BulbStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bulb_list')
    else:
        form = BulbStatusForm()
    return render(request, 'bulbs/bulb_form.html', {'form': form})

def bulb_update(request, pk):
    bulb = get_object_or_404(BulbStatus, pk=pk)
    if request.method == "POST":
        form = BulbStatusForm(request.POST, instance=bulb)
        if form.is_valid():
            form.save()
            return redirect('bulb_list')
    else:
        form = BulbStatusForm(instance=bulb)
    return render(request, 'bulbs/bulb_form.html', {'form': form})

def bulb_delete(request, pk):
    bulb = get_object_or_404(BulbStatus, pk=pk)
    if request.method == "POST":
        bulb.delete()
        return redirect('bulb_list')
    return render(request, 'bulbs/bulb_confirm_delete.html', {'bulb': bulb})
