from django.core.management.base import BaseCommand
from django.utils import timezone
from yourapp.models import DeviceSchedule

class Command(BaseCommand):
    help = 'Turns devices off and deletes schedules'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired = DeviceSchedule.objects.filter(end_time__lte=now)

        for schedule in expired:
            device = schedule.device
            device.power = False
            device.save()
            self.stdout.write(f"Device {device.name} has been turned off")
            schedule.delete()
            self.stdout.write(f"Schedule of device {device.name} has been deleted")
