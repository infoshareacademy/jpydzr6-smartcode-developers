from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    name = models.CharField(blank=True, max_length=20)
    email = models.EmailField(blank=True, max_length=50)
