from .device import NotCompatibleDevice, Device, load_json, save_json


class LawnMower(Device):
    def __init__(self, device_id: str, device_type: str):
        super().__init__(device_id, device_type)

    def get_power(self) -> str | None:
        """
        Get the current power status of the lawn mower (on or off).
        """
        return self.load_device_info().get('status', {}).get('power', None)

    def get_battery_percent(self) -> int | None:
        """
        Get the battery percentage of the lawn mower.
        """
        return self.load_device_info().get('status', {}).get('battery_percent', None)

    def get_cutting_mode(self) -> str | None:
        """
        Get the cutting mode of the lawn mower (e.g., auto or manual).
        """
        return self.load_device_info().get('status', {}).get('cutting_mode', None)

    def get_cutting_height(self) -> int | None:
        """
        Get the cutting height of the lawn mower in millimeters.
        """
        return self.load_device_info().get('status', {}).get('cutting_height_mm', None)

    def get_current_area(self) -> float | None:
        """
        Get the current area being mowed in square meters.
        """
        return self.load_device_info().get('status', {}).get('current_area_m2', None)

    def get_total_cutting_time(self) -> int | None:
        """
        Get the total cutting time in minutes.
        """
        return self.load_device_info().get('status', {}).get('total_cutting_time_minutes', None)

if __name__ == "__main__":
    lawn_mower_device = LawnMower("mower98765", "LawnMower")
    lawn_mower_device.connect_to_device()

    print("Power:", lawn_mower_device.get_power())
    print("Battery Percentage:", lawn_mower_device.get_battery_percent())
    print("Cutting Mode:", lawn_mower_device.get_cutting_mode())
    print("Cutting Height (mm):", lawn_mower_device.get_cutting_height())
    print("Current Area (m²):", lawn_mower_device.get_current_area())
    print("Total Cutting Time (minutes):", lawn_mower_device.get_total_cutting_time())

    lawn_mower_device.turn_on_off("off")
