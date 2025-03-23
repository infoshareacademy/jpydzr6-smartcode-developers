from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class DeviceType(models.Model):
    BULB = 1
    PLUG = 2
    THERMOSTAT = 3
    CURTAIN = 4
    WEATHER_STATION = 5
    LAWN_MOWER = 6

    TYPE_CHOICES = [
        (BULB, 'Bulb'),
        (PLUG, 'Plug'),
        (THERMOSTAT, 'Thermostat'),
        (CURTAIN, 'Curtain'),
        (WEATHER_STATION, 'Weather Station'),
        (LAWN_MOWER, 'Lawn Mower'),
    ]

    id = models.PositiveSmallIntegerField(primary_key=True, choices=TYPE_CHOICES)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    device_secret_key = models.CharField(max_length=100, unique=True, null=False)
    name = models.CharField(max_length=255, null=False)
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    connected = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.location}, {self.connected}"


class BulbStatus(models.Model):
    power = models.CharField(max_length=10)
    brightness = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    color_temp = models.IntegerField()
    red_temp = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    green_temp = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    blue_temp = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Bulb Statusses"

    def __str__(self):
        return f"{self.device_id.name}, {self.brightness}, {self.device_id.connected}"


class PlugStatus(models.Model):
    power = models.CharField(max_length=10)
    current_power_w = models.DecimalField(max_digits=10, decimal_places=2)
    total_energy_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Plug Statusses"

    def __str__(self):
        return f"{self.device_id.name}, {self.current_power_w}"


class ThermostatStatus(models.Model):
    power = models.CharField(max_length=10)
    target_temperature = models.DecimalField(max_digits=10, decimal_places=2)
    current_temperature = models.DecimalField(max_digits=10, decimal_places=2)
    humidity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Thermostat Statusses"

    def __str__(self):
        return f"{self.device_id.name}, {self.current_temperature}, {self.target_temperature}, {self.humidity}"


class CurtainStatus(models.Model):
    power = models.CharField(max_length=10)
    position = models.IntegerField()
    open_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Curtain Statusses"

    def __str__(self):
        return f"{self.device_id.name}, {self.position}, {self.open_percent}"


class WeatherStationStatus(models.Model):
    temperature_c = models.DecimalField(max_digits=5, decimal_places=2)
    humidity_percent = models.IntegerField(default=0)
    pressure_hpa = models.DecimalField(max_digits=7, decimal_places=2)
    wind_speed_kmh = models.DecimalField(max_digits=5, decimal_places=2)
    rainfall = models.DecimalField(max_digits=5, decimal_places=2)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Weather Station Statusses"

    def __str__(self):
        return f"{self.device_id.name}, {self.temperature_c}, {self.humidity_percent}"


class LawnMowerStatus(models.Model):
    power = models.CharField(max_length=10)
    battery_percent = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    cutting_mode = models.CharField(max_length=50)
    cutting_height_mm = models.IntegerField(validators=[MinValueValidator(0)])
    current_area_m2 = models.IntegerField(validators=[MinValueValidator(0)])
    total_cutting_time_minutes = models.IntegerField(validators=[MinValueValidator(0)])
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Lawn Mower Statusses"

    def __str__(self):
        return (f"{self.device_id.name}, {self.battery_percent}, {self.cutting_mode}, {self.cutting_height_mm},"
                f"{self.current_area_m2}, {self.total_cutting_time_minutes}")

