from .device import NotCompatibleDevice, Device, load_json

class Plug(Device):
    def __init__(self, device_id: str, device_type: str):
        super().__init__(device_id, device_type)

    def get_current_power_usage(self) -> str:
        """
        Get the total power usage of the device.

        This method loads the JSON data from the file, iterates through the devices,
        and returns the total energy consumption in kWh for the device with the matching device_id.

        :return: The total energy consumption in kWh as a string. If the device is not found,
                 it returns "Power usage not available".
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return device['status']['energy_consumption']['current_power_w']
        return "Power usage not available"

    def get_total_power_usage(self) -> str:
        """
        Get the total power usage of the device.

        This method loads the JSON data from the file, iterates through the devices,
        and returns the total energy consumption in kWh for the device with the matching device_id.

        :return: The total energy consumption in kWh as a string. If the device is not found,
                 it returns "Power usage not available".
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return device['status']['energy_consumption']['total_energy_kwh']
        return "Power usage not available"


if __name__ == "__main__":
    plug = Plug("abcdef1234567999", "plug")
    plug.connect_to_device()
    print(f"Current power usage: {plug.get_current_power_usage()}")
    print(f"Total power usage: {plug.get_total_power_usage()}")
    plug.reboot()
    plug.get_status()
    plug.change_device_name("new_plug_name")
    plug.change_device_password()