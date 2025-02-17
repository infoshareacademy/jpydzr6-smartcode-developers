from django import forms
from .models import Device, BulbStatus, PlugStatus


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_secret_key', 'name', 'type_id', 'brand', 'model', 'location', 'connected']

class BulbStatusForm(forms.ModelForm):
    class Meta:
        model = BulbStatus
        fields = ['power', 'brightness', 'color_temp', 'red_temp', 'green_temp', 'blue_temp', 'device_id']

class PlugStatusForm(forms.ModelForm):
    class Meta:
        model = PlugStatus
        fields = ['power', 'current_power_w', 'total_energy_kwh', 'device_id']