from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from .models import Bulb, Plug, Thermostat, Curtain, WeatherStation, LawnMower, BaseDevice, SharedDevice
from .forms import BulbForm, PlugForm, ThermostatForm, CurtainForm, WeatherStationForm, LawnMowerForm, BaseDeviceForm, ShareDeviceForm
from django.forms.models import model_to_dict
from django.contrib import messages
from django.http import Http404
from django.core.exceptions import PermissionDenied

User = get_user_model()

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
        Allow access to both owned devices and devices shared with the user.
        """
        device_type = self.kwargs.get('device_type')
        device_id = self.kwargs.get('pk')
        user = self.request.user

        # Get base device without owner restriction
        base_device = get_object_or_404(BaseDevice, pk=device_id)

        # Check if user is the owner or has shared access
        is_owner = (base_device.owner == user)

        if not is_owner:
            # Check if device is shared with this user
            shared_access = SharedDevice.objects.filter(
                device_id=base_device.id,
                shared_with=user
            ).exists()

            if not shared_access:
                raise Http404("Device not found")

        # Store ownership status for use in other methods
        self.is_owner = is_owner

        # Get the specific device instance
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

        specific_device_instance = device_model.objects.get(basedevice_ptr_id=base_device.id)

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

        return {'base_device_form': base_device_form, 'specific_form': specific_form}

    def get_context_data(self, **kwargs):
        """
        Pass both forms (base and specific) to the template.
        """
        context = super().get_context_data(**kwargs)
        forms = self.get_form()
        context.update(forms)
        context['is_owner'] = self.is_owner
        context['device_type'] = self.kwargs.get('device_type').lower()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle form submission for both base and specific device forms.
        Preserve owner information for shared devices.
        """
        forms = self.get_form()
        base_device_form = forms['base_device_form']
        specific_form = forms['specific_form']

        if base_device_form.is_valid() and specific_form.is_valid():
            base_device = base_device_form.save(commit=False)
            specific_device = specific_form.save(commit=False)

            # Only update owner if current user is the owner
            if not self.is_owner:
                # For shared devices, preserve the original owner
                original_base_device = BaseDevice.objects.get(pk=self.kwargs.get('pk'))
                base_device.owner = original_base_device.owner
                specific_device.owner = original_base_device.owner
            else:
                base_device.owner = request.user
                specific_device.owner = request.user

            base_device.save()
            specific_device.save()

            return redirect(self.success_url)

        return self.form_invalid(base_device_form)


class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'device_confirm_delete.html'
    success_url = "/devices/delete/success/"

    def get_object(self):
        device_type = self.kwargs.get('device_type')
        device_id = self.kwargs.get('device_id')
        user = self.request.user

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

        # Get the device
        device = get_object_or_404(device_model, pk=device_id)

        # Store the device instance and owner status for use in other methods
        self.device = device
        self.is_owner = (device.owner == user)

        # Check if user has access to the device
        if not self.is_owner:
            shared_access = SharedDevice.objects.filter(
                device_id=device.basedevice_ptr_id,
                shared_with=user
            ).exists()
            if not shared_access:
                raise PermissionDenied("You don't have access to this device.")

        return device

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.is_owner
        context['device_type'] = self.kwargs.get('device_type')
        return context

    def form_valid(self, form):
        """Override to prevent actual deletion for non-owners"""
        if not self.is_owner:
            # For shared users, don't call super().form_valid()
            # which would delete the device
            SharedDevice.objects.filter(
                device_id=self.device.basedevice_ptr_id,
                shared_with=self.request.user
            ).delete()
            messages.success(self.request, f"Device '{self.device.name}' has been removed from your shared devices.")
            return redirect(self.success_url)
        else:
            # Only owners can actually delete the device
            messages.success(self.request, f"Device '{self.device.name}' has been deleted.")
            return super().form_valid(form)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    template_name = "device_detail.html"
    context_object_name = "device"

    def get_object(self):
        """
        Retrieve the device object dynamically based on type and ID.
        Allow access to both owned devices and devices shared with the user.
        """
        device_type = self.kwargs.get('device_type')
        device_id = self.kwargs.get('device_id')
        user = self.request.user

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

        # Get the device first without filtering by owner
        device = get_object_or_404(device_class, basedevice_ptr_id=device_id)

        # Check if the user is the owner or has shared access
        is_owner = device.owner == user

        if not is_owner:
            # Check if device is shared with this user
            shared_access = SharedDevice.objects.filter(
                device_id=device.basedevice_ptr_id,
                shared_with=user
            ).exists()

            if not shared_access:
                raise Http404("Device not found")

        # Store ownership status for use in context
        self.is_owner = is_owner

        return device

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.get_object()

        device_fields = model_to_dict(device)

        # Add calculated color field for bulbs
        if self.kwargs.get('device_type') == 'bulb':
            # Calculate hex color from RGB components
            r = getattr(device, 'red_temp', 255)
            g = getattr(device, 'green_temp', 255)
            b = getattr(device, 'blue_temp', 255)

            # Add the calculated color to device fields
            device_fields['color'] = f'#{r:02x}{g:02x}{b:02x}'

        excluded_fields = ["id", "device_secret_key", "owner", "basedevice_ptr"]

        for field in excluded_fields:
            device_fields.pop(field, None)

        context["device_fields"] = device_fields
        context["device_type"] = self.kwargs.get('device_type')
        context["is_owner"] = self.is_owner

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

@login_required(login_url='login')
def devices_by_location(request, location):
    devices = BaseDevice.objects.filter(location=location)
    return render(request, 'devices_by_location.html', {'devices': devices, 'location': location})


# bulb
@login_required(login_url='login')
def bulb_list(request):
    user = request.user
    owned_bulbs = Bulb.objects.filter(owner=user)
    shared_device_ids = SharedDevice.objects.filter(shared_with=user).values_list('device_id', flat=True)
    shared_bulbs = Bulb.objects.filter(basedevice_ptr_id__in=shared_device_ids)

    # Combine the querysets
    bulbs = (owned_bulbs | shared_bulbs).distinct()

    return render(request, 'bulbs/bulb_list.html', {'bulbs': bulbs})


# plug
@login_required(login_url='login')
def plug_list(request):
    user = request.user
    owned_plugs = Plug.objects.filter(owner=user)
    shared_device_ids = SharedDevice.objects.filter(shared_with=user).values_list('device_id', flat=True)
    shared_plugs = Plug.objects.filter(basedevice_ptr_id__in=shared_device_ids)

    # Combine the querysets
    plugs = (owned_plugs | shared_plugs).distinct()

    return render(request, 'plugs/plug_list.html', {'plugs': plugs})


# thermostat
@login_required(login_url='login')
def thermostat_list(request):
    user = request.user
    owned_thermostats = Thermostat.objects.filter(owner=user)
    shared_device_ids = SharedDevice.objects.filter(shared_with=user).values_list('device_id', flat=True)
    shared_thermostats = Thermostat.objects.filter(basedevice_ptr_id__in=shared_device_ids)

    # Combine the querysets
    thermostats = (owned_thermostats | shared_thermostats).distinct()

    return render(request, 'thermostats/thermostat_list.html', {'thermostats': thermostats})


# curtain
@login_required(login_url='login')
def curtain_list(request):
    user = request.user
    owned_curtains = Curtain.objects.filter(owner=user)
    shared_device_ids = SharedDevice.objects.filter(shared_with=user).values_list('device_id', flat=True)
    shared_curtains = Curtain.objects.filter(basedevice_ptr_id__in=shared_device_ids)

    # Combine the querysets
    curtains = (owned_curtains | shared_curtains).distinct()

    return render(request, 'curtains/curtain_list.html', {'curtains': curtains})


# weather station
@login_required(login_url='login')
def weather_station_list(request):
    user = request.user
    owned_stations = WeatherStation.objects.filter(owner=user)
    shared_device_ids = SharedDevice.objects.filter(shared_with=user).values_list('device_id', flat=True)
    shared_stations = WeatherStation.objects.filter(basedevice_ptr_id__in=shared_device_ids)

    # Combine the querysets
    stations = (owned_stations | shared_stations).distinct()

    return render(request, "weather_stations/weatherstation_list.html", {"stations": stations})


# lawn mower
@login_required(login_url='login')
def lawn_mower_list(request):
    user = request.user
    owned_lawn_mowers = LawnMower.objects.filter(owner=user)
    shared_device_ids = SharedDevice.objects.filter(shared_with=user).values_list('device_id', flat=True)
    shared_lawn_mowers = LawnMower.objects.filter(basedevice_ptr_id__in=shared_device_ids)

    # Combine the querysets
    lawn_mowers = (owned_lawn_mowers | shared_lawn_mowers).distinct()

    return render(request, "lawn_mowers/lawnmower_list.html", {"statusy": lawn_mowers})

@login_required
def share_device_view(request, device_id):
    device = get_object_or_404(BaseDevice, id=device_id, owner=request.user)

    if request.method == "POST":
        form = ShareDeviceForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            shared_user = User.objects.filter(email=email).first()

            if shared_user:
                existing_shared_device = SharedDevice.objects.filter(device=device, shared_with=shared_user).first()
                if not existing_shared_device:
                    SharedDevice.objects.create(
                        device=device,
                        shared_by_email=request.user,
                        shared_with=shared_user
                    )
            else:
                pass

            messages.success(request, "Device was shared")

            return redirect('dashboard')

    else:
        form = ShareDeviceForm()

    return render(request, 'share_device.html', {'form': form, 'device': device})