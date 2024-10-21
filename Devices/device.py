from abc import ABC, abstractmethod
import json
from datetime import datetime

FILE_PATH = "../devices.json"

def load_json(file_path = FILE_PATH):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json(data, file_path = FILE_PATH):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

class NotCompatibleDevice(Exception):
    """
    Exception raised when device is not compatible
    """
    print("Device is not compatible")

class Device(ABC):
    """
    Abstract class for all devices
    """
    def __init__(self, device_id: str, device_type: str):
        self.device_id = device_id
        self.device_type = device_type

    @abstractmethod
    def connect_to_device(self):
        print(f"Connecting to device {self.device_id}")

    def disconnect(self):
        print(f"Disconnecting from device {self.device_id}")

    def turn_on_off(self, new_state: str) -> None:
        """
        Turn the device on or off.

        This method loads the JSON data from the file, iterates through the devices,
        and updates the 'power' status of the device with the matching device_id to the new state.
        It also updates the 'last_updated' timestamp for the device and saves the modified JSON data back to the file.

        :param new_state: The new power state to set for the device ('on' or 'off').
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device['status']['power'] = new_state
                break
        json_data = self.modify_last_updated(json_data)
        save_json(json_data, FILE_PATH)

    def reboot(self):
        print(f"Rebooting device {self.device_id}")

    def get_status(self):
        print(f"Getting status for device {self.device_id}")

    def modify_last_updated(self, json_data) -> dict:
        """
        Update the 'last_updated' timestamp for the device.

        This method iterates through the devices in the provided JSON data,
        finds the device with the matching device_id, and updates its 'last_updated'
        field with the current date and time.

        :param json_data: The JSON data containing device information.
        :return: The updated JSON data with the modified 'last_updated' field.
        """
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        return json_data


class Plug(Device):
    def __init__(self, device_id: str, device_type: str):
        super().__init__(device_id, device_type)

    def connect_to_device(self) -> None:
        """
        Connect to the device
        :return:
        """
        if self.device_type != "plug":
            raise NotCompatibleDevice
        else:
            print(f"Connected to device {self.device_id}")

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
    print(plug.get_current_power_usage())
    print(plug.get_total_power_usage())
    plug.turn_on_off("on")
