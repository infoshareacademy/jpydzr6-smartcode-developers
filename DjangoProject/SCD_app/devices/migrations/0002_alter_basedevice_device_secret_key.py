# Generated by Django 5.1.6 on 2025-03-23 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("devices", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basedevice",
            name="device_secret_key",
            field=models.CharField(max_length=100),
        ),
    ]
