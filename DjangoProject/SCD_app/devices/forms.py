from django import forms
from .models import Device, BulbStatus, PlugStatus, ThermostatStatus, CurtainStatus, WeatherStationStatus, LawnMowerStatus


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_secret_key', 'name', 'type', 'brand', 'model', 'location', 'connected']

class BulbStatusForm(forms.ModelForm):
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
        model = BulbStatus
        fields = ['power', 'brightness', 'color_temp', 'red_temp', 'green_temp', 'blue_temp', 'device_id']

class PlugStatusForm(forms.ModelForm):
    current_power_w = forms.FloatField(
        min_value=0, widget=forms.NumberInput(attrs={'min': 0})
    )
    total_energy_kwh = forms.FloatField(
        min_value=0, widget=forms.NumberInput(attrs={'min': 0})
    )
    class Meta:
        model = PlugStatus
        fields = ['power', 'current_power_w', 'total_energy_kwh', 'device_id']

class ThermostatStatusForm(forms.ModelForm):
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
        model = ThermostatStatus
        fields = ['power', 'target_temperature', 'current_temperature', 'humidity', 'device_id']

class CurtainStatusForm(forms.ModelForm):
    open_percent = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 100})
    )
    class Meta:
        model = CurtainStatus
        fields = ['power', 'position', 'open_percent', 'device_id']

class WeatherStationStatusForm(forms.ModelForm):
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
        model = WeatherStationStatus
        fields = ['temperature_c', 'humidity_percent', 'pressure_hpa', 'wind_speed_kmh', 'rainfall', 'device_id']

class LawnMowerStatusForm(forms.ModelForm):
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
        model = LawnMowerStatus
        fields = ['power', 'battery_percent', 'cutting_mode', 'cutting_height_mm',
                  'current_area_m2', 'total_cutting_time_minutes', 'device_id']