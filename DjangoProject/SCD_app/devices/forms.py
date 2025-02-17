from django import forms
from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_secret_key', 'name', 'type_id', 'brand', 'model', 'location', 'connected']
