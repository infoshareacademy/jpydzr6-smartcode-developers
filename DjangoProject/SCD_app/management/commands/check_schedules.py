from datetime import datetime
from devices.models import DeviceSchedule

def process_schedules():
    now = datetime.now().time()
    schedules = DeviceSchedule.objects.all()

    for sched in schedules:
        start = sched.start_time
        end = sched.get_end_time()
        if start <= now <= end:
            activate_device(sched.device)
        else:
            deactivate_device(sched.device)

def activate_device(device):
    print(f"Turning on device: {device.name} ({device.device_type})")

def deactivate_device(device):
    print(f"Turning off device: {device.name}")
