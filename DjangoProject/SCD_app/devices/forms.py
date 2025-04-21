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
        if self.instance and self.instance.pk:
            del self.fields['device_secret_key']

        # Remove owner field from form
        if 'owner' in self.fields:
            del self.fields['owner']


class BulbForm(BaseDeviceForm):
    brightness = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 100, 'class': 'form-control'})
    )
    color_temp = forms.IntegerField(
        min_value=2000, max_value=6500,
        widget=forms.NumberInput(attrs={'min': 2000, 'max': 6500, 'class': 'form-control'})
    )
    color_picker = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        required=False,
        label="Bulb Color"
    )

    class Meta:
        model = Bulb
        fields = ['device_secret_key', 'name', 'brand', 'model', 'location', 'power', 'connected',
                  'brightness', 'color_temp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        # If we're editing an existing bulb, set the initial color picker value
        if instance:
            r = getattr(instance, 'red_temp', 255)
            g = getattr(instance, 'green_temp', 255)
            b = getattr(instance, 'blue_temp', 255)
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            self.fields['color_picker'].initial = hex_color

    def clean(self):
        cleaned_data = super().clean()
        color_hex = cleaned_data.get('color_picker')

        if color_hex:
            # Remove the '#' and convert to RGB
            color_hex = color_hex.lstrip('#')
            cleaned_data['red_temp'] = int(color_hex[0:2], 16)
            cleaned_data['green_temp'] = int(color_hex[2:4], 16)
            cleaned_data['blue_temp'] = int(color_hex[4:6], 16)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set RGB values from color_picker
        cleaned_data = self.cleaned_data
        if 'red_temp' in cleaned_data:
            instance.red_temp = cleaned_data['red_temp']
            instance.green_temp = cleaned_data['green_temp']
            instance.blue_temp = cleaned_data['blue_temp']

        if commit:
            instance.save()
        return instance

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

class ShareDeviceForm(forms.Form):
    email = forms.EmailField(label="Email to share with")