from device import NotCompatibleDevice, Device, load_json

class Thermostat(Device):
    def __init__(self, device_id: str, device_type: str):
        super().__init__(device_id, device_type)

    def connect_to_device(self) -> None:
        """
        Connect to the thermostat device.
        """
        if self.device_type != "thermostat":
            raise NotCompatibleDevice
        else:
            print(f"Connected to thermostat {self.device_id}")

    def get_current_temperature(self) -> float:
        """
        Get the current temperature of the thermostat.

        This method loads the JSON data from the file, iterates through the devices,
        and returns the current temperature in Celsius for the device with the matching device_id.

        :return: The current temperature in Celsius as a string. If the device is not found,
                 it returns None.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return float(device['status'].get('current_temperature_c', None))
        return None

    def get_target_temperature(self) -> float:
        """
        Get the target temperature of the thermostat.

        This method loads the JSON data from the file, iterates through the devices,
        and returns the target temperature in Celsius for the device with the matching device_id.

        :return: The target temperature in Celsius as a string. If the device is not found,
                 it returns None.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return float(device['status'].get('target_temperature_c', None))
        return None

    def get_humidity(self) -> float:
        """
        Get the current humidity level of the thermostat.

        This method loads the JSON data from the file, iterates through the devices,
        and returns the current humidity percentage for the device with the matching device_id.

        :return: The current humidity percentage as a string. If the device is not found,
                 it returns None.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return float(device['status'].get('humidity', None))
        return None


if __name__ == "__main__":
    thermostat = Thermostat("abcdef1234563298", "thermostat")
    thermostat.connect_to_device()
    print("Current Temperature:", thermostat.get_current_temperature())
    print("Target Temperature:", thermostat.get_target_temperature())
    print("Humidity:", thermostat.get_humidity())
    thermostat.turn_on_off("off")
