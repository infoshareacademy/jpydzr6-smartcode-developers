# Generated by Django 5.2 on 2025-04-09 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_alter_bulb_blue_temp_alter_bulb_brightness_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basedevice',
            name='location',
            field=models.CharField(choices=[('LIVING ROOM', 'Living Room'), ('KITCHEN', 'Kitchen'), ('HALLWAY', 'Hallway'), ('BEDROOM', 'Bedroom'), ('BATHROOM', 'Bathroom'), ('GARDEN', 'Garden'), ('BACKYARD', 'Backyard')], max_length=50),
        ),
    ]
