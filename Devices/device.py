from abc import ABC
import json
import sys
import os
from datetime import datetime
from colorama import Fore, init

sys.path.append(os.path.abspath('..'))
from logging_config import get_logger

FILE_PATH = "../devices.json"
MAX_ATTEMPTS = 3
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

class CantConnectToDevice(Exception):
    """
    Exception raised when device can't connect
    """

class ToManyAttempts(Exception):
    """
    Exception raised when too many attempts are made
    """

class Device(ABC):
    """
    Abstract class for all devices
    """

    def __init__(self, device_id: str, device_type: str):
        self.device_id = device_id
        self.device_type = device_type
        self.connected = False
        self.logger = get_logger()

    def connect_to_device(self) -> None:
        """
        Connects to the device if compatible with the current class.
        """
        print(f"{Fore.YELLOW}Connecting to device {self.device_id}...")
        self.logger.info(f"Connecting to device {self.device_id}...")

        if self.device_type != self.__class__.__name__.lower():
            print(f"{Fore.RED}Connection error: Device {self.device_id} is not compatible.")
            self.logger.error(f"Connection error: Device {self.device_id} is not compatible.")
            raise NotCompatibleDevice
        if self.__login_to_device():
            self.connected = True
            print(f"{Fore.GREEN}Successfully connected to device {self.device_id}.")
            self.logger.info(f"Successfully connected to device {self.device_id}.")
        else:
            print(f"{Fore.RED}Wrong password, failed to connect to device {self.device_id}.")
            self.logger.error(f"Wrong password, failed to connect to device {self.device_id}.")
            raise CantConnectToDevice

    def __login_to_device(self) -> bool:
        """
        Logs in to the device during connection process.
        """
        password = input(f"Enter password for device {self.device_id}: ")
        device_secret_key = self.__get_device_secret_key()

        if device_secret_key == password:
            return True
        return False

    def __get_device_secret_key(self) -> str | None:
        """
        Retrieves the device secret key from the JSON data.
        """
        device_secret_key = None
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device_secret_key = device['device_secret_key']
                break
        return device_secret_key

    def change_device_password(self) -> bool:
        """
        Changes the password for the device if connected.
        """
        if not self.connected:
            print(f"{Fore.RED}Cannot change password. Device {self.device_id} is not connected.")
            self.logger.error(f"Cannot change password. Device {self.device_id} is not connected.")
            return False

        counter = 0
        prompt = f"Enter current password for device {self.device_id}: "
        current_password = self.__get_device_secret_key()
        while input(prompt) != current_password:
            counter += 1
            if counter >= MAX_ATTEMPTS:
                raise ToManyAttempts
            print(f"{Fore.RED}Incorrect password. Please try again.")

        counter = 0
        prompt_new_password = f"Enter new password for device {self.device_id}: "
        prompt_confirm_password = f"Confirm new password for device {self.device_id}: "
        while (new_password:= input(prompt_new_password)) != input(prompt_confirm_password):
            counter += 1
            if counter > MAX_ATTEMPTS:
                print(f"{Fore.RED}Too many attempts. Please try again later.")
                return False
            print(f"{Fore.RED}Incorrect password. Please try again.")

        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device['device_secret_key'] = new_password
                save_json(json_data)
                print(f"{Fore.GREEN}Password changed successfully for device {self.device_id}.")
                self.logger.info(f"Password changed for device {self.device_id}.")
                return True
        print(f"{Fore.RED}Failed to change password for device {self.device_id}.")
        self.logger.error(f"Failed to change password for device {self.device_id}.")
        return False


    def disconnect_from_device(self) -> None:
        """
        Disconnects from the device if currently connected.
        """
        print(f"{Fore.YELLOW}Disconnecting from device {self.device_id}...")

        if self.connected:
            self.connected = False
            print(f"{Fore.GREEN}Successfully disconnected from device {self.device_id}.")
            self.logger.info(f"disconnected from device {self.device_id}.")
        else:
            print(f"{Fore.YELLOW}Device {self.device_id} was not connected.")

    def turn_on_off(self, new_state: str) -> None:
        """
        Updates the device's power status to the specified state.

        Loads the JSON data, finds the device by `device_id`, updates its 'power' status,
        modifies the 'last_updated' timestamp, and saves the updated JSON data.

        Args:
            new_state (str): The new power state to set for the device ('on' or 'off').
        """
        json_data = load_json()

        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device['status']['power'] = new_state
                self.modify_last_updated(json_data)
                print(f"{Fore.GREEN}Device {self.device_id} power set to {new_state}.")
                self.logger.info(f"Device {self.device_id} power set to {new_state}.")
                break

    def reboot(self) -> bool:
        """
        Reboots the device by turning it off and then on, updating the 'last_updated' timestamp.

        Returns:
            bool: True if reboot was successful, False otherwise.
        """
        if not self.connected:
            print(f"{Fore.RED}Cannot perform reboot. Device {self.device_id} is not connected.")
            return False

        print(f"{Fore.YELLOW}Rebooting device {self.device_id}...")
        self.logger.info(f"Rebooting device {self.device_id}...")
        
        self.turn_on_off("off")
        self.turn_on_off("on")
        
        print(f"{Fore.GREEN}Device {self.device_id} is back online.")
        self.logger.info(f"Device {self.device_id} is back online.")
        return True

    def get_status(self) -> str | None:
        """
        Retrieves the status of the device if connected.

        Returns:
            str | None: The status of the device in JSON format if connected, None otherwise.
        """
        if not self.connected:
            print(f"{Fore.RED}Cannot get status. Device {self.device_id} is not connected.")
            self.logger.error(f"Cannot get status. Device {self.device_id} is not connected.")
            return None

        print(f"{Fore.GREEN}Getting status for device {self.device_id}")
        self.logger.info(f"Getting status for device {self.device_id}")

        json_data = load_json()
        device_status = next(
            (device['status'] for device in json_data['devices'] if device['device_id'] == self.device_id),
            None
        )

        if device_status is not None:
            return f"{Fore.BLUE}{json.dumps(device_status, indent=4)}"
        else:
            print(f"{Fore.RED}Status not found for device {self.device_id}.")
            self.logger.error(f"Status not found for device {self.device_id}.")
            return None

    def change_device_name(self, name: str) -> bool:
        """
        Changes the name of the device if connected.

        This method checks if the user is connected to the device, then loads the JSON data, finds the device by ID,
        and updates the 'name' attribute. It also updates the 'last_updated' timestamp and saves the modified JSON data.

        Args:
            name (str): The new name for the device.

        Returns:
            bool: True if the name was successfully changed, False otherwise.
        """
        if not self.connected:
            print(f"{Fore.RED}Cannot change device name. Device {self.device_id} is not connected.")
            self.logger.error(f"Cannot change device name. Device {self.device_id} is not connected.")
            return False

        json_data = load_json()
        
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device['name'] = name
                self.modify_last_updated(json_data)
                print(f"{Fore.GREEN}Device name changed successfully. New name: {name}")
                self.logger.info(f"Device name changed successfully. New name: {name}")
                return True

        print(f"{Fore.RED}Failed to change device name. Device {self.device_id} not found.")
        self.logger.error(f"Failed to change device name. Device {self.device_id} not found.")
        return False

    def modify_last_updated(self, json_data) -> None:
        """
        Updates the 'last_updated' timestamp for the device in the JSON data.

        Finds the device with the matching `device_id` and updates its 'last_updated' 
        field with the current date and time, then saves the updated JSON data.

        Args:
            json_data (dict): The JSON data containing device information.
        """
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_json(json_data, FILE_PATH)
                break

