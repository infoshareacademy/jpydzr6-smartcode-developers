from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .models import Bulb, Plug, Thermostat, Curtain, WeatherStation, LawnMower, BaseDevice
from .forms import BulbForm, PlugForm, ThermostatForm, CurtainForm, WeatherStationForm, LawnMowerForm, BaseDeviceForm
from django import forms


class DeviceCreateView(LoginRequiredMixin, FormView):
    template_name = 'device_form.html'
    success_url = "/devices/create/success/"  # Redirect on success

    def get_form_class(self):
        """
        Dynamically returns the specific form class depending on the device type.
        """
        device_type = self.kwargs.get('device_type')
        form_classes = {
            'bulb': BulbForm,
            'plug': PlugForm,
            'thermostat': ThermostatForm,
            'curtain': CurtainForm,
            'weatherstation': WeatherStationForm,
            'lawnmower': LawnMowerForm
        }

        self.specific_form_class = form_classes.get(device_type)
        if not self.specific_form_class:
            raise ValueError("Invalid device type.")
        return self.specific_form_class

    def get_form(self, form_class=None):
        """
        Create and return the forms (base form and specific form).
        """
        if form_class is None:
            form_class = self.get_form_class()

        specific_form = form_class(self.request.POST or None)
        return {'specific_form': specific_form}

    def get_context_data(self, **kwargs):
        """
        Pass the specific form to the template.
        """
        context = super().get_context_data(**kwargs)
        forms = self.get_form()
        context.update(forms)  # Add the specific form to the context
        return context

    def post(self, request, *args, **kwargs):
        forms = self.get_form()
        specific_form = forms['specific_form']

        if specific_form.is_valid():
            specific_form.instance.owner = request.user  # set logged user as owner
            specific_form.save()

            return redirect(self.success_url)

        print(specific_form.errors)
        return self.form_invalid(specific_form)


class DeviceUpdateView(LoginRequiredMixin, FormView):
    template_name = 'device_update_form.html'
    success_url = "/devices/update/success/"  # Redirect on success

    def get_object(self):
        """
        Retrieve the device object to be updated.
        """
        device_type = self.kwargs.get('device_type')
        device_id = self.kwargs.get('pk')

        # Fetch the base device
        base_device = BaseDevice.objects.get(pk=device_id, owner=self.request.user)

        # Get the specific device type instance
        specific_device = device_type.lower()
        device_model = {
            'bulb': Bulb,
            'plug': Plug,
            'thermostat': Thermostat,
            'curtain': Curtain,
            'weatherstation': WeatherStation,
            'lawnmower': LawnMower
        }

        specific_device_class = device_model.get(device_type.lower())
        if not specific_device_class:
            raise ValueError("Invalid device type.")

        # Fetch the specific device instance based on the base device
        specific_device_instance = specific_device_class.objects.get(basedevice_ptr_id=base_device.id)
        return base_device, specific_device_instance

    def get_form_class(self):
        """
        Dynamically returns the specific form class depending on the device type.
        """
        device_type = self.kwargs.get('device_type')
        form_classes = {
            'bulb': BulbForm,
            'plug': PlugForm,
            'thermostat': ThermostatForm,
            'curtain': CurtainForm,
            'weatherstation': WeatherStationForm,
            'lawnmower': LawnMowerForm
        }

        self.specific_form_class = form_classes.get(device_type)
        if not self.specific_form_class:
            raise ValueError("Invalid device type.")
        return self.specific_form_class

    def get_form(self, form_class=None):
        """
        Create and return the forms (base form and specific form).
        """
        if form_class is None:
            form_class = self.get_form_class()

        base_device, specific_device = self.get_object()

        # Exclude device_secret_key and owner fields from the form
        base_device_form = BaseDeviceForm(self.request.POST or None, instance=base_device)
        specific_form = form_class(self.request.POST or None, instance=specific_device)

        # Exclude 'owner' and 'device_secret_key' from the fields to be shown/modified
        return {'base_device_form': base_device_form, 'specific_form': specific_form}

    def get_context_data(self, **kwargs):
        """
        Pass both forms (base and specific) to the template.
        """
        context = super().get_context_data(**kwargs)
        forms = self.get_form()
        context.update(forms)  # Add both forms to the context
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle form submission for both base and specific device forms.
        """
        forms = self.get_form()
        base_device_form = forms['base_device_form']
        specific_form = forms['specific_form']

        if base_device_form.is_valid() and specific_form.is_valid():
            print(base_device_form.cleaned_data)
            base_device = base_device_form.save(commit=False)
            specific_device = specific_form.save(commit=False)

            # Set the owner to the logged-in user
            specific_device.owner = request.user  # Ensure owner is set to the logged-in user

            # Save the updated base device and specific device

            base_device.save()
            specific_device.save()

            return redirect(self.success_url)
        print("LIPA")
        print(specific_form.errors)  # Print/Log validation errors for debugging
        print(base_device_form.errors, specific_form.errors)  # Print/Log validation errors for debugging
        return self.form_invalid(base_device_form)



@login_required(login_url='login')
def device_create_success(request):
    return render(request, 'device_added.html')

@login_required(login_url='login')
def device_update_success(request):
    return render(request, 'device_updated.html')


@login_required(login_url='login')
def devices(request):
    return render(request, 'devices.html')

@login_required(login_url='login')
def device_list(request):
    user = request.user
    devices = BaseDevice.objects.filter(owner=user)
    # print(devices)
    return render(request, 'device_list.html', {'devices': devices})


# bulb
@login_required(login_url='login')
def bulb_list(request):
    user = request.user
    bulbs = Bulb.objects.filter(basedevice_ptr__owner=user)
    return render(request, 'bulbs/bulb_list.html', {'bulbs': bulbs})

@login_required(login_url='login')
def bulb_detail(request, pk):
    user = request.user
    bulb = get_object_or_404(Bulb, pk=pk, basedevice_ptr__owner=user)
    return render(request, 'bulbs/bulb_detail.html', {'bulb': bulb})

@login_required(login_url='login')
def bulb_create(request):
    if request.method == "POST":
        form = BulbForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bulb_list')
    else:
        form = BulbForm()
    return render(request, 'bulbs/bulb_form.html', {'form': form})

@login_required(login_url='login')
def bulb_update(request, pk):
    user = request.user
    bulb = get_object_or_404(Bulb, pk=pk, basedevice_ptr__owner=user)
    if request.method == "POST":
        form = BulbForm(request.POST, instance=bulb)
        if form.is_valid():
            form.save()
            return redirect('bulb_list')
    else:
        form = BulbForm(instance=bulb)
    return render(request, 'bulbs/bulb_form.html', {'form': form})

@login_required(login_url='login')
def bulb_delete(request, pk):
    user = request.user
    bulb = get_object_or_404(Bulb, pk=pk, basedevice_ptr__owner=user)
    if request.method == "POST":
        bulb.delete()
        return redirect('bulb_list')
    return render(request, 'bulbs/bulb_confirm_delete.html', {'bulb': bulb})

# plug
@login_required(login_url='login')
def plug_list(request):
    user = request.user
    plugs = Plug.objects.filter(basedevice_ptr__owner=user)
    return render(request, 'plugs/plug_list.html', {'plugs': plugs})

@login_required(login_url='login')
def plug_detail(request, plug_id):
    user = request.user
    plug = get_object_or_404(Plug, pk=plug_id, basedevice_ptr__owner=user)
    return render(request, 'plugs/plug_detail.html', {'plug': plug})

@login_required(login_url='login')
def plug_create(request):
    if request.method == 'POST':
        form = PlugForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plug_list')
    else:
        form = PlugForm()
    return render(request, 'plugs/plug_form.html', {'form': form})

@login_required(login_url='login')
def plug_update(request, plug_id):
    user = request.user
    plug = get_object_or_404(Plug, pk=plug_id, basedevice_ptr__owner=user)
    if request.method == 'POST':
        form = PlugForm(request.POST, instance=plug)
        if form.is_valid():
            form.save()
            return redirect('plug_list')
    else:
        form = PlugForm(instance=plug)
    return render(request, 'plugs/plug_form.html', {'form': form})

@login_required(login_url='login')
def plug_delete(request, plug_id):
    user = request.user
    plug = get_object_or_404(Plug, pk=plug_id, basedevice_ptr__owner=user)
    if request.method == 'POST':
        plug.delete()
        return redirect('plug_list')
    return render(request, 'plugs/plug_confirm_delete.html', {'plug': plug})

# thermostat
@login_required(login_url='login')
def thermostat_list(request):
    user = request.user
    thermostats = Thermostat.objects.filter(basedevice_ptr__owner=user)
    return render(request, 'thermostats/thermostat_list.html', {'thermostats': thermostats})

@login_required(login_url='login')
def thermostat_detail(request, pk):
    user = request.user
    thermostat = get_object_or_404(Thermostat, pk=pk, basedevice_ptr__owner=user)
    return render(request, 'thermostats/thermostat_detail.html', {'thermostat': thermostat})

@login_required(login_url='login')
def thermostat_create(request):
    if request.method == 'POST':
        form = ThermostatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thermostat_list')
    else:
        form = ThermostatForm()
    return render(request, 'thermostats/thermostat_form.html', {'form': form})

@login_required(login_url='login')
def thermostat_update(request, pk):
    user = request.user
    thermostat = get_object_or_404(Thermostat, pk=pk, basedevice_ptr__owner=user)
    if request.method == 'POST':
        form = ThermostatForm(request.POST, instance=thermostat)
        if form.is_valid():
            form.save()
            return redirect('thermostat_list')
    else:
        form = ThermostatForm(instance=thermostat)
    return render(request, 'thermostats/thermostat_form.html', {'form': form})

@login_required(login_url='login')
def thermostat_delete(request, pk):
    user = request.user
    thermostat = get_object_or_404(Thermostat, pk=pk, basedevice_ptr__owner=user)
    if request.method == 'POST':
        thermostat.delete()
        return redirect('thermostat_list')
    return render(request, 'thermostats/thermostat_confirm_delete.html', {'thermostat': thermostat})

# curtain
@login_required(login_url='login')
def curtain_list(request):
    user = request.user
    curtains = Curtain.objects.filter(basedevice_ptr__owner=user)
    return render(request, 'curtains/curtain_list.html', {'curtains': curtains})

@login_required(login_url='login')
def curtain_detail(request, pk):
    user = request.user
    curtain = get_object_or_404(Curtain, pk=pk, basedevice_ptr__owner=user)
    return render(request, 'curtains/curtain_detail.html', {'curtain': curtain})

@login_required(login_url='login')
def curtain_create(request):
    if request.method == 'POST':
        form = CurtainForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('curtain_list')
    else:
        form = CurtainForm()
    return render(request, 'curtains/curtain_form.html', {'form': form})

@login_required(login_url='login')
def curtain_update(request, pk):
    user = request.user
    curtain = get_object_or_404(Curtain, pk=pk, basedevice_ptr__owner=user)
    if request.method == "POST":
        form = CurtainForm(request.POST, instance=curtain)
        if form.is_valid():
            form.save()
            return redirect('curtain_list')
    else:
        form = CurtainForm(instance=curtain)
    return render(request, 'curtains/curtain_form.html', {'form': form})

@login_required(login_url='login')
def curtain_delete(request, pk):
    user = request.user
    curtain = get_object_or_404(Curtain, pk=pk, basedevice_ptr__owner=user)
    if request.method == 'POST':
        curtain.delete()
        return redirect('curtain_list')
    return render(request, 'curtains/curtain_confirm_delete.html', {'curtain': curtain})

# weather station
@login_required(login_url='login')
def weather_station_list(request):
    user = request.user
    stations = WeatherStation.objects.filter(basedevice_ptr__owner=user)
    return render(request, "weather_stations/weatherstation_list.html", {"stations": stations})

@login_required(login_url='login')
def weather_station_detail(request, pk):
    user = request.user
    station = get_object_or_404(WeatherStation, pk=pk, basedevice_ptr__owner=user)
    return render(request, "weather_stations/weatherstation_detail.html", {"station": station})

@login_required(login_url='login')
def weather_station_create(request):
    if request.method == "POST":
        form = WeatherStationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("weather_station_list")
    else:
        form = WeatherStationForm()
    return render(request, "weather_stations/weatherstation_form.html", {"form": form})

@login_required(login_url='login')
def weather_station_update(request, pk):
    user = request.user
    station = get_object_or_404(WeatherStation, pk=pk, basedevice_ptr__owner=user)
    if request.method == "POST":
        form = WeatherStationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return redirect("weather_station_list")
    else:
        form = WeatherStationForm(instance=station)
    return render(request, "weather_stations/weatherstation_form.html", {"form": form})

@login_required(login_url='login')
def weather_station_delete(request, pk):
    user = request.user
    station = get_object_or_404(WeatherStation, pk=pk, basedevice_ptr__owner=user)
    if request.method == "POST":
        station.delete()
        return redirect("weather_station_list")
    return render(request, "weather_stations/weatherstation_confirm_delete.html", {"station": station})

# lawn mower
@login_required(login_url='login')
def lawn_mower_list(request):
    user = request.user
    lawn_mowers = LawnMower.objects.filter(basedevice_ptr__owner=user)
    return render(request, "lawn_mowers/lawnmower_list.html", {"statusy": lawn_mowers})

@login_required(login_url='login')
def lawn_mower_detail(request, pk):
    user = request.user
    lawn_mower = get_object_or_404(LawnMower, pk=pk, basedevice_ptr__owner=user)
    return render(request, "lawn_mowers/lawnmower_detail.html", {"status": lawn_mower})

@login_required(login_url='login')
def lawn_mower_create(request):
    if request.method == "POST":
        form = LawnMowerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lawnmower_list")
    else:
        form = LawnMowerForm()
    return render(request, "lawn_mowers/lawnmower_form.html", {"form": form})

@login_required(login_url='login')
def lawn_mower_update(request, pk):
    user = request.user
    lawn_mower = get_object_or_404(LawnMower, pk=pk, basedevice_ptr__owner=user)
    if request.method == "POST":
        form = LawnMowerForm(request.POST, instance=lawn_mower)
        if form.is_valid():
            form.save()
            return redirect("lawn_mower_list")
    else:
        form = LawnMowerForm(instance=lawn_mower)
    return render(request, "lawn_mowers/lawnmower_form.html", {"form": form})

@login_required(login_url='login')
def lawn_mower_delete(request, pk):
    user = request.user
    lawn_mower = get_object_or_404(LawnMower, pk=pk, basedevice_ptr__owner=user)
    if request.method == "POST":
        lawn_mower.delete()
        return redirect("lawn_mower_list")
    return render(request, "lawn_mowers/lawnmower_confirm_delete.html", {"status": lawn_mower})

