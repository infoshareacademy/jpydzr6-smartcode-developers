from abc import ABC
import json
from datetime import datetime
from colorama import Fore, init

FILE_PATH = "../devices.json"
# Initialize Colorama (necessary for Windows compatibility)
init(autoreset=True)

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

class Device(ABC):
    """
    Abstract class for all devices
    """

    def __init__(self, device_id: str, device_type: str):
        self.device_id = device_id
        self.device_type = device_type
        self.connected = False

    def connect_to_device(self):
        """
        Connect to the device
        :return:
        """
        print(f"{Fore.YELLOW}Connecting to device_id {self.device_id}")
        if self.device_type != self.__class__.__name__.lower():
            print(f"{Fore.RED}Error while connecting to device_id {self.device_id}")
            raise NotCompatibleDevice
        else:
            print(f"{Fore.GREEN}Connected to device_id {self.device_id}")
            self.connected = True
        

    def disconnect_from_device(self):
        """
        Disconnect from the device
        :return:
        """
        print(f"Disconnecting from device_id {self.device_id}")
        if self.connected:
            self.connected = False
            print(f"{Fore.GREEN}Succesfully disconected from device_id {self.device_id}")
        else:
            print(f"{Fore.YELLOW}device_id {self.device_id} was not connected")

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
        self.modify_last_updated(json_data)

    def reboot(self) -> bool:
        """
        Reboot the device.

        This method turns the device off and then back on, updating the 'last_updated' timestamp.
        """
        if not self.connected:
            print(f"{Fore.RED}Cant perform reboot. Not connected to device_id {self.device_id}")
            return False
        print(f"{Fore.YELLOW}Rebooting device_id {self.device_id}")
        self.turn_on_off("off")
        self.turn_on_off("on")
        print(f"{Fore.GREEN}device_id {self.device_id} back online")
        return True

    def get_status(self) -> str | None:
        if not self.connected:
            print(f"{Fore.RED}Cant get status. Not connected to device_id {self.device_id}")
            return
        print(f"{Fore.GREEN}Getting status for device_id {self.device_id}")
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return f"{Fore.BLUE}{json.dumps(device['status'], indent=4)}"

    def change_device_name(self, name: str) -> bool:
        """
        Change device name

        This checks if user is connected to device if so, method loads the JSON data from the file, iterates through the devices,
        and updates the 'name' parameter of the device with the matching device_id.
        It also updates the 'last_updated' timestamp for the device and saves the modified JSON data back to the file.
        If user is not connected to device, 


        :param name: New name for the device.

        :return: bool True if name was changed, otherwise False
        """
        if not self.connected:
            print(f"{Fore.RED}Cant perform change_device_name. Not connected to device_id {self.device_id}")
            return False
        changed = False
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device['name'] = name
                changed = True
                break
        if changed:      
            self.modify_last_updated(json_data)
            print(f"{Fore.GREEN}Changing name of device_id {self.device_id} succeeded, new {name = }")
            return True
        else:
            print(f"{Fore.RED}Changing name of device_id {self.device_id} failed")
            return False

    def modify_last_updated(self, json_data) -> None:
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
        save_json(json_data, FILE_PATH)

