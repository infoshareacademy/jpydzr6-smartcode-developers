from django.contrib.auth.models import User
from django.db import models

class Device(models.Model):

#Created with Artur:
    name = models.CharField(max_length=255, null=False)
    connected = models.BooleanField(default=False)
    brand = models.CharField(max_length=100, null=True)
    last_updated = models.DateTimeField(auto_now=True)


# New stuff:
    device_secret_key = models.CharField(max_length=100, unique=True, null=False)
    type_id = models.CharField(max_length=255)
    model = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    # References


class BulbStatus(models.Model):
    power = models.CharField(max_length=10)
    brightness = models.CharField(max_length=100)
    color_temp = models.CharField(max_length=10)
    red_temp = models.CharField(max_length=10)
    green_temp = models.CharField(max_length=10)
    blue_temp = models.CharField(max_length=10)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    # References


class PlugStatus(models.Model):
    power = models.CharField(max_length=10)
    current_power_w = models.DecimalField(max_digits=10, decimal_places=2)
    total_energy_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    # References


class ThermostatStatus(models.Model):
    power = models.CharField(max_length=10)
    target_temperature = models.DecimalField(max_digits=10, decimal_places=2)
    current_temperature = models.DecimalField(max_digits=10, decimal_places=2)
    humidity = models.CharField(max_length=10)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    # References


class CurtainStatus(models.Model):
    power = models.CharField(max_length=10)
    position = models.CharField()
    open_percent = models.PositiveIntegerField()
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    # References


class WeatherStationStatus(models.Model):
    temperature_c = models.DecimalField(max_digits=5, decimal_places=2)
    humidity_percent = models.PercentField()
    pressure_hpa = models.DecimalField(max_digits=7, decimal_places=2)
    wind_speed_kmh = models.DecimalField(max_digits=5, decimal_places=2)
    rainfall = models.DecimalField(max_digits=5, decimal_places=2)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    # References


class LawnMowerStatus(models.Model):
    power = models.CharField(max_length=10)
    battery_percent = models.PercentField()
    cutting_mode = models.CharField(max_length=50)
    cutting_height_mm = models.CharField()
    current_area_m2 = models.CharField()
    total_cutting_time_minutes = models.CharField()
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    # References
