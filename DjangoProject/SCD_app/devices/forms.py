from django import forms
from .models import BaseDevice, Bulb, Plug, Thermostat, Curtain, WeatherStation, LawnMower, DeviceSchedule, DeviceType


class BaseDeviceForm(forms.ModelForm):
    class Meta:
        model = BaseDevice
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use PasswordInput widget for device_secret_key
        self.fields['device_secret_key'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        # Optionally, add a custom help text if necessary


        self.fields['device_secret_key'].help_text = "Enter a secure device secret key."
        if self.instance and self.instance.pk:
            del self.fields['device_secret_key']

        # Remove owner field from form
        if 'owner' in self.fields:
            del self.fields['owner']
            

class BulbForm(BaseDeviceForm):
    brightness = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 100})
    )
    color_temp = forms.IntegerField(
        min_value=2000, max_value=6500,
        widget=forms.NumberInput(attrs={'min': 2000, 'max': 6500})
    )
    red_temp = forms.IntegerField(
        min_value=0, max_value=255,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 255})
    )
    green_temp = forms.IntegerField(
        min_value=0, max_value=255,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 255})
    )
    blue_temp = forms.IntegerField(
        min_value=0, max_value=255,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 255})
    )
    class Meta:
        model = Bulb
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'brightness', 'color_temp', 'red_temp', 'green_temp', 'blue_temp']


class PlugForm(BaseDeviceForm):
    current_power_w = forms.FloatField(
        min_value=0, widget=forms.NumberInput(attrs={'min': 0})
    )
    total_energy_kwh = forms.FloatField(
        min_value=0, widget=forms.NumberInput(attrs={'min': 0})
    )
    class Meta:
        model = Plug
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'current_power_w', 'total_energy_kwh']


class ThermostatForm(BaseDeviceForm):
    target_temperature = forms.FloatField(
        min_value=10, max_value=30,
        widget=forms.NumberInput(attrs={'min': 10, 'max': 30})
    )
    current_temperature = forms.FloatField(
        min_value=-50, max_value=50,
        widget=forms.NumberInput(attrs={'min': -50, 'max': 50})
    )
    humidity = forms.FloatField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 100})
    )
    class Meta:
        model = Thermostat
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'target_temperature', 'current_temperature', 'humidity']


class CurtainForm(BaseDeviceForm):
    open_percent = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 100})
    )
    class Meta:
        model = Curtain
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'position', 'open_percent']


class WeatherStationForm(BaseDeviceForm):
    temperature_c = forms.FloatField(
        min_value=-50, max_value=50,
        widget=forms.NumberInput(attrs={'min': -50, 'max': 50})
    )
    humidity_percent = forms.FloatField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 100})
    )
    pressure_hpa = forms.FloatField(
        min_value=900, max_value=1100,
        widget=forms.NumberInput(attrs={'min': 900, 'max': 1100})
    )
    wind_speed_kmh = forms.FloatField(
        min_value=0, max_value=200,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 200})
    )
    rainfall = forms.FloatField(
        min_value=0, widget=forms.NumberInput(attrs={'min': 0})
    )
    class Meta:
        model = WeatherStation
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'temperature_c', 'humidity_percent', 'pressure_hpa', 'wind_speed_kmh', 'rainfall']


class LawnMowerForm(BaseDeviceForm):
    battery_percent = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 100})
    )
    cutting_height_mm = forms.IntegerField(
        min_value=10, max_value=100,
        widget=forms.NumberInput(attrs={'min': 10, 'max': 100})
    )
    current_area_m2 = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={'min': 0})
    )
    total_cutting_time_minutes = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={'min': 0})
    )
    class Meta:
        model = LawnMower
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'battery_percent', 'cutting_mode', 'cutting_height_mm',
                  'current_area_m2', 'total_cutting_time_minutes']

class DeviceScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['device'].queryset = BaseDevice.objects.filter(owner=user)

    class Meta:
        model = DeviceSchedule
        fields = ['device', 'start_time', 'end_time', 'duration']
        widgets = {
            "start_time": forms.TimeInput(attrs={'type': 'time'}),
            "end_time": forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('end_time') and not cleaned_data.get('duration'):
            raise forms.ValidationError('Provide the device shutdown time or device operation time.')
        if cleaned_data.get('end_time') and cleaned_data.get('duration'):
            raise forms.ValidationError('Provide either device shutdown time or operation time.')
        return cleaned_data
