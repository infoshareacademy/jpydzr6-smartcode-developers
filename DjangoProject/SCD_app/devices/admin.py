from django.contrib import admin
from .models import Bulb, Plug, Thermostat, Curtain, WeatherStation, LawnMower

admin.site.register(Bulb)
admin.site.register(Plug)
admin.site.register(Thermostat)
admin.site.register(Curtain)
admin.site.register(WeatherStation)
admin.site.register(LawnMower)

