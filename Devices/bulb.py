from device import NotCompatibleDevice, Device, load_json, save_json


class Bulb(Device):
    def __init__(self, device_id: str, device_type: str):
        super().__init__(device_id, device_type)

    def connect_to_device(self) -> None:
        """
        Connect to the bulb device.
        """
        if self.device_type != "Bulb":
            raise NotCompatibleDevice("Device type is not compatible.")
        else:
            print(f"Connected to Bulb {self.device_id}")

    def load_device_info(self) -> dict:
        """
        Load the JSON data and retrieve the information for this specific bulb.

        A dictionary containing the device's information, or an empty dictionary if not found.
        """
        json_data = load_json()
        for device in json_data.get('devices', []):
            if device['device_id'] == self.device_id:
                return device
        return {}

    def get_name(self) -> str:
        """
        Get the name of the bulb.

        The name of the bulb as a string, or None if not found.
        """
        return self.load_device_info().get('name', None)

    def get_brand(self) -> str:
        """
        Get the brand of the bulb.

        The brand of the bulb as a string, or None if not found.
        """
        return self.load_device_info().get('brand', None)

    def get_model(self) -> str:
        """
        Get the model of the bulb.

        The model of the bulb as a string, or None if not found.
        """
        return self.load_device_info().get('model', None)

    def get_power(self) -> str:
        """
        Get the current power status of the bulb (on or off).

        The power status as a string, or None if not found.
        """
        return self.load_device_info().get('status', {}).get('power', None)

    def get_brightness(self) -> int:
        """
        Get the current brightness level of the bulb.

        The brightness level as an integer, or None if not found.
        """
        return self.load_device_info().get('status', {}).get('brightness', None)

    def get_color_temp(self) -> int:
        """
        Get the color temperature of the bulb.

        The color temperature as an integer, or None if not found.
        """
        return self.load_device_info().get('status', {}).get('color_temp', None)

    def get_rgb(self) -> dict:
        """
        Get the RGB color settings of the bulb.

        A dictionary with 'red', 'green', 'blue' values, or None if not found.
        """
        return self.load_device_info().get('status', {}).get('rgb', None)

    def turn_on_off(self, state: str) -> None:
        """
        Turn the bulb on or off and update the power state in the JSON data.

        state: Desired state, "on" or "off".
        """
        if state.upper() not in ["on", "off"]:
            raise ValueError("State must be 'ON' or 'OFF'")

        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device['status']['power'] = state.lower()  # Update power state
                break
        save_json(json_data)
        print(f"Bulb {self.device_id} turned {state}")


if __name__ == '__main__':
    bulb_device = Bulb("1234567890abcdef", "Bulb")
    bulb_device.connect_to_device()
    print("Name:", bulb_device.get_name())
    print("Brand:", bulb_device.get_brand())
    print("Model:", bulb_device.get_model())
    print("Power:", bulb_device.get_power())
    print("Brightness:", bulb_device.get_brightness())
    print("Color Temperature:", bulb_device.get_color_temp())
    print("RGB:", bulb_device.get_rgb())
    bulb_device.turn_on_off("OFF")
