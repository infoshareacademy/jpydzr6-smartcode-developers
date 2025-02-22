from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Device, BulbStatus, PlugStatus, ThermostatStatus, CurtainStatus, WeatherStationStatus, LawnMowerStatus
from .forms import DeviceForm, BulbStatusForm, PlugStatusForm, ThermostatStatusForm, CurtainStatusForm, WeatherStationStatusForm, LawnMowerStatusForm


# from models import *


@login_required(login_url='login')
def devices(request):
    return render(request, 'devices.html')

@login_required(login_url='login')
def device_list(request):
    user = request.user
    devices = Device.objects.filter(owner=user)
    # print(devices)
    return render(request, 'device_list.html', {'devices': devices})

@login_required(login_url='login')
def device_detail(request, device_id):
    # device = Device.objects.get(id=id)
    user = request.user
    device = get_object_or_404(Device, id=device_id, owner=user)
    return render(request, 'device_detail.html', {'device': device})

@login_required(login_url='login')
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

@login_required(login_url='login')
def device_update(request, pk):
    user = request.user
    device = get_object_or_404(Device, pk=pk, owner=user)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_list')
    else:
        form = DeviceForm(instance=device)
    return render(request, 'device_form.html', {'form': form})

@login_required(login_url='login')
def device_delete(request, pk):
    user = request.user
    device = get_object_or_404(Device, pk=pk, owner=user)
    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    return render(request, 'device_confirm_delete.html', {'device': device})

# Create your views here.

# bulb
@login_required(login_url='login')
def bulb_list(request):
    user = request.user
    bulbs = BulbStatus.objects.filter(device_id__owner=user)
    return render(request, 'bulbs/bulb_list.html', {'bulbs': bulbs})

@login_required(login_url='login')
def bulb_detail(request, pk):
    user = request.user
    bulb = get_object_or_404(BulbStatus, pk=pk, device_id__owner=user)
    return render(request, 'bulbs/bulb_detail.html', {'bulb': bulb})

@login_required(login_url='login')
def bulb_create(request):
    if request.method == "POST":
        form = BulbStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bulb_list')
    else:
        form = BulbStatusForm()
    return render(request, 'bulbs/bulb_form.html', {'form': form})

@login_required(login_url='login')
def bulb_update(request, pk):
    user = request.user
    bulb = get_object_or_404(BulbStatus, pk=pk, device_id__owner=user)
    if request.method == "POST":
        form = BulbStatusForm(request.POST, instance=bulb)
        if form.is_valid():
            form.save()
            return redirect('bulb_list')
    else:
        form = BulbStatusForm(instance=bulb)
    return render(request, 'bulbs/bulb_form.html', {'form': form})

@login_required(login_url='login')
def bulb_delete(request, pk):
    user = request.user
    bulb = get_object_or_404(BulbStatus, pk=pk, device_id__owner=user)
    if request.method == "POST":
        bulb.delete()
        return redirect('bulb_list')
    return render(request, 'bulbs/bulb_confirm_delete.html', {'bulb': bulb})

# plug
@login_required(login_url='login')
def plug_list(request):
    user = request.user
    plugs = PlugStatus.objects.filter(device_id__owner=user)
    return render(request, 'plugs/plug_list.html', {'plugs': plugs})

@login_required(login_url='login')
def plug_detail(request, plug_id):
    user = request.user
    plug = get_object_or_404(PlugStatus, pk=plug_id, device_id__owner=user)
    return render(request, 'plugs/plug_detail.html', {'plug': plug})

@login_required(login_url='login')
def plug_create(request):
    if request.method == 'POST':
        form = PlugStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plug_list')
    else:
        form = PlugStatusForm()
    return render(request, 'plugs/plug_form.html', {'form': form})

@login_required(login_url='login')
def plug_update(request, plug_id):
    user = request.user
    plug = get_object_or_404(PlugStatus, pk=plug_id, device_id__owner=user)
    if request.method == 'POST':
        form = PlugStatusForm(request.POST, instance=plug)
        if form.is_valid():
            form.save()
            return redirect('plug_list')
    else:
        form = PlugStatusForm(instance=plug)
    return render(request, 'plugs/plug_form.html', {'form': form})

@login_required(login_url='login')
def plug_delete(request, plug_id):
    user = request.user
    plug = get_object_or_404(PlugStatus, pk=plug_id, device_id__owner=user)
    if request.method == 'POST':
        plug.delete()
        return redirect('plug_list')
    return render(request, 'plugs/plug_confirm_delete.html', {'plug': plug})

# thermostat
@login_required(login_url='login')
def thermostat_list(request):
    user = request.user
    thermostats = ThermostatStatus.objects.filter(device_id__owner=user)
    return render(request, 'thermostats/thermostat_list.html', {'thermostats': thermostats})

@login_required(login_url='login')
def thermostat_detail(request, pk):
    user = request.user
    thermostat = get_object_or_404(ThermostatStatus, pk=pk, device_id__owner=user)
    return render(request, 'thermostats/thermostat_detail.html', {'thermostat': thermostat})

@login_required(login_url='login')
def thermostat_create(request):
    if request.method == 'POST':
        form = ThermostatStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thermostat_list')
    else:
        form = ThermostatStatusForm()
    return render(request, 'thermostats/thermostat_form.html', {'form': form})

@login_required(login_url='login')
def thermostat_update(request, pk):
    user = request.user
    thermostat = get_object_or_404(ThermostatStatus, pk=pk, device_id__owner=user)
    if request.method == 'POST':
        form = ThermostatStatusForm(request.POST, instance=thermostat)
        if form.is_valid():
            form.save()
            return redirect('thermostat_list')
    else:
        form = ThermostatStatusForm(instance=thermostat)
    return render(request, 'thermostats/thermostat_form.html', {'form': form})

@login_required(login_url='login')
def thermostat_delete(request, pk):
    user = request.user
    thermostat = get_object_or_404(ThermostatStatus, pk=pk, device_id__owner=user)
    if request.method == 'POST':
        thermostat.delete()
        return redirect('thermostat_list')
    return render(request, 'thermostats/thermostat_confirm_delete.html', {'thermostat': thermostat})

# curtain
@login_required(login_url='login')
def curtain_list(request):
    user = request.user
    curtains = CurtainStatus.objects.filter(device_id__owner=user)
    return render(request, 'curtains/curtain_list.html', {'curtains': curtains})

@login_required(login_url='login')
def curtain_detail(request, pk):
    user = request.user
    curtain = get_object_or_404(CurtainStatus, pk=pk, device_id__owner=user)
    return render(request, 'curtains/curtain_detail.html', {'curtain': curtain})

@login_required(login_url='login')
def curtain_create(request):
    if request.method == 'POST':
        form = CurtainStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('curtain_list')
    else:
        form = CurtainStatusForm()
    return render(request, 'curtains/curtain_form.html', {'form': form})

@login_required(login_url='login')
def curtain_update(request, pk):
    user = request.user
    curtain = get_object_or_404(CurtainStatus, pk=pk, device_id__owner=user)
    if request.method == "POST":
        form = CurtainStatusForm(request.POST, instance=curtain)
        if form.is_valid():
            form.save()
            return redirect('curtain_list')
    else:
        form = CurtainStatusForm(instance=curtain)
    return render(request, 'curtains/curtain_form.html', {'form': form})

@login_required(login_url='login')
def curtain_delete(request, pk):
    user = request.user
    curtain = get_object_or_404(CurtainStatus, pk=pk, device_id__owner=user)
    if request.method == 'POST':
        curtain.delete()
        return redirect('curtain_list')
    return render(request, 'curtains/curtain_confirm_delete.html', {'curtain': curtain})

# weather station
@login_required(login_url='login')
def weather_station_list(request):
    user = request.user
    stations = WeatherStationStatus.objects.filter(device_id__owner=user)
    return render(request, "weather_stations/weatherstation_list.html", {"stations": stations})

@login_required(login_url='login')
def weather_station_detail(request, pk):
    user = request.user
    station = get_object_or_404(WeatherStationStatus, pk=pk, device_id__owner=user)
    return render(request, "weather_stations/weatherstation_detail.html", {"station": station})

@login_required(login_url='login')
def weather_station_create(request):
    if request.method == "POST":
        form = WeatherStationStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("weather_station_list")
    else:
        form = WeatherStationStatusForm()
    return render(request, "weather_stations/weatherstation_form.html", {"form": form})

@login_required(login_url='login')
def weather_station_update(request, pk):
    user = request.user
    station = get_object_or_404(WeatherStationStatus, pk=pk, device_id__owner=user)
    if request.method == "POST":
        form = WeatherStationStatusForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return redirect("weather_station_list")
    else:
        form = WeatherStationStatusForm(instance=station)
    return render(request, "weather_stations/weatherstation_form.html", {"form": form})

@login_required(login_url='login')
def weather_station_delete(request, pk):
    user = request.user
    station = get_object_or_404(WeatherStationStatus, pk=pk, device_id__owner=user)
    if request.method == "POST":
        station.delete()
        return redirect("weather_station_list")
    return render(request, "weather_stations/weatherstation_confirm_delete.html", {"station": station})

# lawn mower
@login_required(login_url='login')
def lawn_mower_list(request):
    user = request.user
    lawn_mowers = LawnMowerStatus.objects.filter(device_id__owner=user)
    return render(request, "lawn_mowers/lawnmower_list.html", {"statusy": lawn_mowers})

@login_required(login_url='login')
def lawn_mower_detail(request, pk):
    user = request.user
    lawn_mower = get_object_or_404(LawnMowerStatus, pk=pk, device_id__owner=user)
    return render(request, "lawn_mowers/lawnmower_detail.html", {"status": lawn_mower})

@login_required(login_url='login')
def lawn_mower_create(request):
    if request.method == "POST":
        form = LawnMowerStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lawnmower_list")
    else:
        form = LawnMowerStatusForm()
    return render(request, "lawn_mowers/lawnmower_form.html", {"form": form})

@login_required(login_url='login')
def lawn_mower_update(request, pk):
    user = request.user
    lawn_mower = get_object_or_404(LawnMowerStatus, pk=pk, device_id__owner=user)
    if request.method == "POST":
        form = LawnMowerStatusForm(request.POST, instance=lawn_mower)
        if form.is_valid():
            form.save()
            return redirect("lawn_mower_list")
    else:
        form = LawnMowerStatusForm(instance=lawn_mower)
    return render(request, "lawn_mowers/lawnmower_form.html", {"form": form})

@login_required(login_url='login')
def lawn_mower_delete(request, pk):
    user = request.user
    lawn_mower = get_object_or_404(LawnMowerStatus, pk=pk, device_id__owner=user)
    if request.method == "POST":
        lawn_mower.delete()
        return redirect("lawn_mower_list")
    return render(request, "lawn_mowers/lawnmower_confirm_delete.html", {"status": lawn_mower})

