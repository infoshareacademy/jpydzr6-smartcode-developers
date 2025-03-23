from django import forms
from .models import BaseDevice, Bulb, Plug, Thermostat, Curtain, WeatherStation, LawnMower


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

        # Remove owner field from form
        if 'owner' in self.fields:
            del self.fields['owner']

class BulbForm(BaseDeviceForm):
    class Meta:
        model = Bulb
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'brightness', 'color_temp', 'red_temp', 'green_temp', 'blue_temp']


class PlugForm(BaseDeviceForm):
    class Meta:
        model = Plug
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'current_power_w', 'total_energy_kwh']

class ThermostatForm(BaseDeviceForm):
    class Meta:
        model = Thermostat
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'target_temperature', 'current_temperature', 'humidity']

class CurtainForm(BaseDeviceForm):
    class Meta:
        model = Curtain
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'position', 'open_percent']

class WeatherStationForm(BaseDeviceForm):
    class Meta:
        model = WeatherStation
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'temperature_c', 'humidity_percent', 'pressure_hpa', 'wind_speed_kmh', 'rainfall']

class LawnMowerForm(BaseDeviceForm):
    class Meta:
        model = LawnMower
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected', 'battery_percent', 'cutting_mode', 'cutting_height_mm',
                  'current_area_m2', 'total_cutting_time_minutes']