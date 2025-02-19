from django.shortcuts import render, get_object_or_404, redirect
from .models import Device, BulbStatus, PlugStatus, ThermostatStatus, CurtainStatus, WeatherStationStatus, LawnMowerStatus
from .forms import DeviceForm, BulbStatusForm, PlugStatusForm, ThermostatStatusForm, CurtainStatusForm, WeatherStationStatusForm, LawnMowerStatusForm


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

def device_update(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_list')  # Upewnij się, że taka nazwa istnieje
    else:
        form = DeviceForm(instance=device)
    return render(request, 'device_form.html', {'form': form})

def device_delete(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    return render(request, 'device_confirm_delete.html', {'device': device})

# Create your views here.

# bulb
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

# plug
def plug_list(request):
    plugs = PlugStatus.objects.all()
    return render(request, 'plugs/plug_list.html', {'plugs': plugs})

def plug_detail(request, plug_id):
    plug = get_object_or_404(PlugStatus, pk=plug_id)
    return render(request, 'plugs/plug_detail.html', {'plug': plug})

def plug_create(request):
    if request.method == 'POST':
        form = PlugStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plug_list')
    else:
        form = PlugStatusForm()
    return render(request, 'plugs/plug_form.html', {'form': form})

def plug_update(request, plug_id):
    plug = get_object_or_404(PlugStatus, pk=plug_id)
    if request.method == 'POST':
        form = PlugStatusForm(request.POST, instance=plug)
        if form.is_valid():
            form.save()
            return redirect('plug_list')
    else:
        form = PlugStatusForm(instance=plug)
    return render(request, 'plugs/plug_form.html', {'form': form})

def plug_delete(request, plug_id):
    plug = get_object_or_404(PlugStatus, pk=plug_id)
    if request.method == 'POST':
        plug.delete()
        return redirect('plug_list')
    return render(request, 'plugs/plug_confirm_delete.html', {'plug': plug})

# thermostat
def thermostat_list(request):
    thermostats = ThermostatStatus.objects.all()
    return render(request, 'thermostats/thermostat_list.html', {'thermostats': thermostats})

def thermostat_detail(request, pk):
    thermostat = get_object_or_404(ThermostatStatus, pk=pk)
    return render(request, 'thermostats/thermostat_detail.html', {'thermostat': thermostat})

def thermostat_create(request):
    if request.method == 'POST':
        form = ThermostatStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thermostat_list')
    else:
        form = ThermostatStatusForm()
    return render(request, 'thermostats/thermostat_form.html', {'form': form})

def thermostat_update(request, pk):
    thermostat = get_object_or_404(ThermostatStatus, pk=pk)
    if request.method == 'POST':
        form = ThermostatStatusForm(request.POST, instance=thermostat)
        if form.is_valid():
            form.save()
            return redirect('thermostat_list')
    else:
        form = ThermostatStatusForm(instance=thermostat)
    return render(request, 'thermostats/thermostat_form.html', {'form': form})

def thermostat_delete(request, pk):
    thermostat = get_object_or_404(ThermostatStatus, pk=pk)
    if request.method == 'POST':
        thermostat.delete()
        return redirect('thermostat_list')
    return render(request, 'thermostats/thermostat_confirm_delete.html', {'thermostat': thermostat})

# curtain
def curtain_list(request):
    curtains = CurtainStatus.objects.all()
    return render(request, 'curtains/curtain_list.html', {'curtains': curtains})


def curtain_detail(request, pk):
    curtain = get_object_or_404(CurtainStatus, pk=pk)
    return render(request, 'curtains/curtain_detail.html', {'curtain': curtain})

def curtain_create(request):
    if request.method == 'POST':
        form = CurtainStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('curtain_list')
    else:
        form = CurtainStatusForm()
    return render(request, 'curtains/curtain_form.html', {'form': form})

def curtain_update(request, pk):
    curtain = get_object_or_404(CurtainStatus, pk=pk)
    if request.method == "POST":
        form = CurtainStatusForm(request.POST, instance=curtain)
        if form.is_valid():
            form.save()
            return redirect('curtain_list')
    else:
        form = CurtainStatusForm(instance=curtain)
    return render(request, 'curtains/curtain_form.html', {'form': form})

def curtain_delete(request, pk):
    curtain = get_object_or_404(CurtainStatus, pk=pk)
    if request.method == 'POST':
        curtain.delete()
        return redirect('curtain_list')
    return render(request, 'curtains/curtain_confirm_delete.html', {'curtain': curtain})

# weather station
def weather_station_list(request):
    stations = WeatherStationStatus.objects.all()
    return render(request, "weather_stations/weatherstation_list.html", {"stations": stations})

def weather_station_detail(request, pk):
    station = get_object_or_404(WeatherStationStatus, pk=pk)
    return render(request, "weather_stations/weatherstation_detail.html", {"station": station})

def weather_station_create(request):
    if request.method == "POST":
        form = WeatherStationStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("weather_station_list")
    else:
        form = WeatherStationStatusForm()
    return render(request, "weather_stations/weatherstation_form.html", {"form": form})

def weather_station_update(request, pk):
    station = get_object_or_404(WeatherStationStatus, pk=pk)
    if request.method == "POST":
        form = WeatherStationStatusForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return redirect("weather_station_list")
    else:
        form = WeatherStationStatusForm(instance=station)
    return render(request, "weather_stations/weatherstation_form.html", {"form": form})

def weather_station_delete(request, pk):
    station = get_object_or_404(WeatherStationStatus, pk=pk)
    if request.method == "POST":
        station.delete()
        return redirect("weather_station_list")
    return render(request, "weather_stations/weatherstation_confirm_delete.html", {"station": station})

# lawn mower
def lawn_mower_list(request):
    lawn_mowers = LawnMowerStatus.objects.all()
    return render(request, "lawn_mowers/lawnmower_list.html", {"statusy": lawn_mowers})

def lawn_mower_detail(request, pk):
    lawn_mower = get_object_or_404(LawnMowerStatus, pk=pk)
    return render(request, "lawn_mowers/lawnmower_detail.html", {"status": lawn_mower})

def lawn_mower_create(request):
    if request.method == "POST":
        form = LawnMowerStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lawnmower_list")
    else:
        form = LawnMowerStatusForm()
    return render(request, "lawn_mowers/lawnmower_form.html", {"form": form})

def lawn_mower_update(request, pk):
    lawn_mower = get_object_or_404(LawnMowerStatus, pk=pk)
    if request.method == "POST":
        form = LawnMowerStatusForm(request.POST, instance=lawn_mower)
        if form.is_valid():
            form.save()
            return redirect("lawn_mower_list")
    else:
        form = LawnMowerStatusForm(instance=lawn_mower)
    return render(request, "lawn_mowers/lawnmower_form.html", {"form": form})

def lawn_mower_delete(request, pk):
    lawn_mower = get_object_or_404(LawnMowerStatus, pk=pk)
    if request.method == "POST":
        lawn_mower.delete()
        return redirect("lawn_mower_list")
    return render(request, "lawn_mowers/lawnmower_confirm_delete.html", {"status": lawn_mower})

