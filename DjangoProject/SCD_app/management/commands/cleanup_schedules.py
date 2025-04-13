from django.core.management.base import BaseCommand
from django.utils import timezone
from yourapp.models import DeviceSchedule

class Command(BaseCommand):
    help = 'Turns devices off and deletes schedules'
    def handle(self, *args, **kwargs):
        now = timezone.now()
        deleted, _ = DeviceSchedule.objects.filter(end_time__lt=now).delete()
        self.stdout.write(f'Successfully deleted {deleted} expired device schedule(s).')
