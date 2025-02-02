from django.contrib import admin
from .models import Device, BulbStatus, PlugStatus, ThermostatStatus, CurtainStatus, WeatherStationStatus, LawnMowerStatus

admin.site.register(Device)
admin.site.register(BulbStatus)
admin.site.register(PlugStatus)
admin.site.register(ThermostatStatus)
admin.site.register(CurtainStatus)
admin.site.register(WeatherStationStatus)
admin.site.register(LawnMowerStatus)

