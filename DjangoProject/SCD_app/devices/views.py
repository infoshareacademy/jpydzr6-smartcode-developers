from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .models import Bulb, Plug, Thermostat, Curtain, WeatherStation, LawnMower, BaseDevice, DeviceSchedule
from .forms import BulbForm, PlugForm, ThermostatForm, CurtainForm, WeatherStationForm, LawnMowerForm, BaseDeviceForm, DeviceScheduleForm, DeviceType
from django.forms.models import model_to_dict
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse


class DeviceCreateView(LoginRequiredMixin, FormView):
    template_name = 'device_form.html'
    success_url = "/devices/create/success/"

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
            specific_form.instance.owner = request.user
            specific_form.save()

            return redirect(self.success_url)

        print(specific_form.errors)
        return self.form_invalid(specific_form)


class DeviceUpdateView(LoginRequiredMixin, FormView):
    template_name = 'device_update_form.html'
    success_url = "/devices/update/success/"

    def get_object(self):
        """
        Retrieve the device object to be updated.
        """
        device_type = self.kwargs.get('device_type')
        device_id = self.kwargs.get('pk')

        base_device = BaseDevice.objects.get(pk=device_id, owner=self.request.user)

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
        context.update(forms)
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

            specific_device.owner = request.user

            base_device.save()
            specific_device.save()

            return redirect(self.success_url)

        print(base_device_form.errors, specific_form.errors)
        return self.form_invalid(base_device_form)

class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'device_confirm_delete.html'
    success_url = "/devices/delete/success/"

    def get_object(self):
        """
        Retrieve the specific device to be deleted.
        """
        device_type = self.kwargs.get('device_type')
        device_id = self.kwargs.get('device_id')

        device_model = {
            'bulb': Bulb,
            'plug': Plug,
            'thermostat': Thermostat,
            'curtain': Curtain,
            'weatherstation': WeatherStation,
            'lawnmower': LawnMower
        }.get(device_type.lower())

        if not device_model:
            raise ValueError("Invalid device type.")

        # Retrieve the object ensuring that only the owner can delete it
        return get_object_or_404(device_model, pk=device_id, owner=self.request.user)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    template_name = "device_detail.html"
    context_object_name = "device"

    def get_object(self):
        """
        Retrieve the device object dynamically based on type and ID.
        """
        device_type = self.kwargs.get('device_type')
        device_id = self.kwargs.get('device_id')

        device_models = {
            'bulb': Bulb,
            'plug': Plug,
            'thermostat': Thermostat,
            'curtain': Curtain,
            'weatherstation': WeatherStation,
            'lawnmower': LawnMower
        }

        device_class = device_models.get(device_type.lower())
        if not device_class:
            raise ValueError("Invalid device type.")

        device = get_object_or_404(device_class, basedevice_ptr_id=device_id, owner=self.request.user)
        return device



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.get_object()

        device_fields = model_to_dict(device)
        print(device_fields)

        excluded_fields = ["id", "device_secret_key", "owner", "basedevice_ptr"]

        for field in excluded_fields:
            device_fields.pop(field, None)

        context["device_fields"] = device_fields
        context["device_type"] = self.kwargs.get('device_type')
        return context

@login_required(login_url='login')
def device_create_success(request):
    return render(request, 'device_added.html')

@login_required(login_url='login')
def device_update_success(request):
    return render(request, 'device_updated.html')

@login_required(login_url='login')
def device_delete_success(request):
    return render(request, 'device_updated.html')


@login_required(login_url='login')
def devices(request):
    return render(request, 'devices.html')

@login_required(login_url='login')
def device_list(request):
    user = request.user
    devices = BaseDevice.objects.filter(owner=user)
    return render(request, 'device_list.html', {'devices': devices})


# bulb
@login_required(login_url='login')
def bulb_list(request):
    user = request.user
    bulbs = Bulb.objects.filter(basedevice_ptr__owner=user)
    return render(request, 'bulbs/bulb_list.html', {'bulbs': bulbs})


# plug
@login_required(login_url='login')
def plug_list(request):
    user = request.user
    plugs = Plug.objects.filter(basedevice_ptr__owner=user)
    return render(request, 'plugs/plug_list.html', {'plugs': plugs})


# thermostat
@login_required(login_url='login')
def thermostat_list(request):
    user = request.user
    thermostats = Thermostat.objects.filter(basedevice_ptr__owner=user)
    return render(request, 'thermostats/thermostat_list.html', {'thermostats': thermostats})


# curtain
@login_required(login_url='login')
def curtain_list(request):
    user = request.user
    curtains = Curtain.objects.filter(basedevice_ptr__owner=user)
    return render(request, 'curtains/curtain_list.html', {'curtains': curtains})


# weather station
@login_required(login_url='login')
def weather_station_list(request):
    user = request.user
    stations = WeatherStation.objects.filter(basedevice_ptr__owner=user)
    return render(request, "weather_stations/weatherstation_list.html", {"stations": stations})


# lawn mower
@login_required(login_url='login')
def lawn_mower_list(request):
    user = request.user
    lawn_mowers = LawnMower.objects.filter(basedevice_ptr__owner=user)
    return render(request, "lawn_mowers/lawnmower_list.html", {"statusy": lawn_mowers})

@login_required
def device_schedule(request, device_type=None, device_id=None):
    current_time = timezone.now()
    expired_schedules = DeviceSchedule.objects.filter(end_time__lt=current_time)
    expired_schedules.delete()

    if request.method == "POST":
        print("form valid")
        form = DeviceScheduleForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_device_schedule')
        else:
            print(form.errors)
    else:
        form = DeviceScheduleForm(user=request.user)

        if device_type and device_id:
            try:
                device = BaseDevice.objects.get(id=device_id, owner=request.user)
                form.fields['device'].initial = device
            except BaseDevice.DoesNotExist:
                pass
    schedules = DeviceSchedule.objects.filter(device__owner=request.user)
    return render(request, 'device_schedule.html', {'form': form, 'schedules': schedules})

@login_required
def list_device_schedule(request):
    schedules = DeviceSchedule.objects.filter(device__owner=request.user)
    return render(request, 'list_device_schedule.html', {'schedules': schedules})

# @login_required
# def delete_schedule(request, schedule_id):
#     schedule = get_object_or_404(DeviceSchedule, id=schedule_id)
#
#     if request.user != schedule.device.owner:
#         messages.error(request, "You are not authorized to perform this action.")
#         return redirect('device_list')
#     schedule.delete()
#     messages.success(request, f"Schedule for the device has been deleted.")
#     return redirect('device_list')


