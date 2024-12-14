from .device import NotCompatibleDevice, Device, load_json, save_json


class Bulb(Device):
    def __init__(self, device_id: str, device_type: str):
        super().__init__(device_id, device_type)

    def get_power(self) -> str | None:
        """
        Get the current power status of the bulb (on or off).

        The power status as a string, or None if not found.
        """
        return self.load_device_info().get('status', {}).get('power', None)

    def get_brightness(self) -> int | None:
        """
        Get the current brightness level of the bulb.

        The brightness level as an integer, or None if not found.
        """
        return self.load_device_info().get('status', {}).get('brightness', None)

    def get_color_temp(self) -> int | None:
        """
        Get the color temperature of the bulb.

        The color temperature as an integer, or None if not found.
        """
        return self.load_device_info().get('status', {}).get('color_temp', None)

    def get_rgb(self) -> dict | None:
        """
        Get the RGB color settings of the bulb.

        A dictionary with 'red', 'green', 'blue' values, or None if not found.
        """
        return self.load_device_info().get('status', {}).get('rgb', None)

if __name__ == '__main__':
    bulb_device = Bulb("1234567890abcdef", "Bulb")
    bulb_device.connect_to_device()
    print("Power:", bulb_device.get_power())
    print("Brightness:", bulb_device.get_brightness())
    print("Color Temperature:", bulb_device.get_color_temp())
    print("RGB:", bulb_device.get_rgb())
    bulb_device.turn_on_off("OFF")
    bulb_device.display_device_info()
