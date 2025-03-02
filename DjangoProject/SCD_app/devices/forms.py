from django import forms
from .models import Device, BulbStatus, PlugStatus, ThermostatStatus, CurtainStatus, WeatherStationStatus, LawnMowerStatus


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_secret_key', 'name', 'type', 'brand', 'model', 'location', 'connected']

class BulbStatusForm(forms.ModelForm):
    class Meta:
        model = BulbStatus
        fields = ['power', 'brightness', 'color_temp', 'red_temp', 'green_temp', 'blue_temp', 'device_id']

class PlugStatusForm(forms.ModelForm):
    class Meta:
        model = PlugStatus
        fields = ['power', 'current_power_w', 'total_energy_kwh', 'device_id']

class ThermostatStatusForm(forms.ModelForm):
    class Meta:
        model = ThermostatStatus
        fields = ['power', 'target_temperature', 'current_temperature', 'humidity', 'device_id']

class CurtainStatusForm(forms.ModelForm):
    class Meta:
        model = CurtainStatus
        fields = ['power', 'position', 'open_percent', 'device_id']

class WeatherStationStatusForm(forms.ModelForm):
    class Meta:
        model = WeatherStationStatus
        fields = ['temperature_c', 'humidity_percent', 'pressure_hpa', 'wind_speed_kmh', 'rainfall', 'device_id']

class LawnMowerStatusForm(forms.ModelForm):
    class Meta:
        model = LawnMowerStatus
        fields = ['power', 'battery_percent', 'cutting_mode', 'cutting_height_mm',
                  'current_area_m2', 'total_cutting_time_minutes', 'device_id']