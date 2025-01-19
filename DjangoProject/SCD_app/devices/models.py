from django.db import models

class Device(models.Model):

# Create your models here.
    name = models.CharField(max_length=255, null=False)
    connected = models.BooleanField(default=False)
    brand = models.CharField(max_length=100, null=True)
    last_updated = models.DateTimeField(auto_now=True)