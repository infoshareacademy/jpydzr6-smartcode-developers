import json
import os
from typing import Dict, Any
import itertools
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from types import FunctionType
from Devices.device import Device
from Devices.bulb import Bulb
from Devices.curtain import Curtain
from Devices.LawnMower import LawnMower
from Devices.plug import Plug
from Devices.thermostat import Thermostat
from Devices.WeatherStation import WeatherStation



def save_devices(devices: Dict[str, Any]) -> None:
    file_path = os.path.join(os.path.dirname(__file__), "devices.json")
    with open(file_path, "w") as file:
        json.dump(devices, file, indent=4)


def load_devices() -> Dict[str, Any]:
    try:
        with open(os.path.join(os.path.dirname(__file__), "devices.json"), "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return {"devices": []}
    except json.JSONDecodeError:
        print("Error reading the file.")
        return {"devices": []}


def toggle_device(index: int, devices_data: Dict[str, Any]) -> None:
    device = devices_data["devices"][index]
    if "status" not in device:
        device["status"] = {"power": "off"}

    if device["status"]["power"] == "on":
        device["status"]["power"] = "off"
    else:
        device["status"]["power"] = "on"

    save_devices(devices_data)


def print_devices(devices_data: Dict[str, Any]) -> None:
    if not devices_data["devices"]:
        print("No devices in the system.")
        return
    print("\n")
    for index, device in enumerate(devices_data["devices"]):
        power_status = device['status'].get('power', 'unknown')
        print(f"{index + 1}. Name :{device['name']} ({device['location']}) - Device id: {device['device_id']}, device type: {device['type']}, power: {power_status}")


def add_device(devices_data: Dict[str, Any]) -> None:
    name = input("Enter device name: ")
    location = input("Enter device location: ")
    new_device = {"name": name, "location": location, "status": {"power": "off"}}
    devices_data["devices"].append(new_device)
    save_devices(devices_data)
    print(f"Device '{name}' added successfully.")


def remove_device(devices_data: Dict[str, Any]) -> None:
    print_devices(devices_data)
    try:
        device_number = int(input("Enter the device number to remove: ")) - 1
        if 0 <= device_number < len(devices_data["devices"]):
            removed_device = devices_data["devices"].pop(device_number)
            save_devices(devices_data)
            print(f"Device '{removed_device['name']}' removed successfully.")
        else:
            print("Invalid device number.")
    except ValueError:
        print("Enter a valid number.")


def create_device_object(device_id: str, device_type: str):
    match device_type:
        case "plug":
            return Plug(device_id, device_type)
        case "bulb":
            return Bulb(device_id, device_type)
        case "curtain":
            return Curtain(device_id, device_type)
        case "lawnmower":
            return LawnMower(device_id, device_type)
        case "thermostat":
            return Thermostat(device_id, device_type)
        case "weather_station":
            return WeatherStation(device_id, device_type)
        case _:
            print("Unsupported device type")
            return None

def get_specific_operations(device):
    return [
        x for x, y in type(device).__dict__.items()
        if isinstance(y, (FunctionType, classmethod, staticmethod)) and x != "__init__"
    ]

def loop_specific_operations(device, specific_operations):
    specific_operations.append("Return")
    while True:
        for index, element in enumerate(specific_operations):
            print(f"{index}: {element}")

        specific_operation = int(input("\nChoose an option number: "))
        if hasattr(device, specific_operations[specific_operation]):
            method = getattr(device, specific_operations[specific_operation])
            print(f"\n{method()}\n")
        elif specific_operations[specific_operation] == "Return":
            return        
        else:
            print(f"Method does not exist.")

def interact_with_device():
    device_id = input("Enter device id: ")
    device_type = input("Enter device type: ")
    device = create_device_object(device_id, device_type)
    if device is None:
        return
    device.connect_to_device()
    while True:
        print("\nChoose an option:")
        print("1. Get device Status")
        print("2. Display all device info")
        print("3. Turn on")
        print("4. Turn off")
        print("5. Reboot")
        print("6. Change device name")
        print("7. Change device password")
        print("8. Specific operations")
        print("9. Return to menu")
        option = input("Choose an option number: ")
        match option:
            case "1":
                print(device.get_status())
            case "2":
                device.display_device_info()
            case "3":
                device.turn_on_off("on")
            case "4":
                device.turn_on_off("off")
            case "5":
                device.reboot()
            case "6":
                new_name = input("Enter new device name ")
                device.change_device_name(new_name)
            case "7":
                device.change_device_password()
            case "8":
                specific_operations = get_specific_operations(device)
                loop_specific_operations(device, specific_operations)
            case "9":
                device.disconnect_from_device()
                return
            case _:
                print("Unsupported operation")

def menu() -> None:
    

    while True:
        devices_data = load_devices()
        print("\nChoose an option:")
        print("1. Show devices")
        print("2. Toggle device")
        print("3. Add device")
        print("4. Remove device")
        print("5. Interact with device")
        print("6. Save and exit")

        option = input("Choose an option number: ")

        if option == "1":
            print_devices(devices_data)

        elif option == "2":
            print_devices(devices_data)
            try:
                device_number = int(input("Enter the device number to toggle: ")) - 1
                if 0 <= device_number < len(devices_data["devices"]):
                    toggle_device(device_number, devices_data)
                    print("Device state has been changed.")
                else:
                    print("Invalid device number.")
            except ValueError:
                print("Enter a valid number.")

        elif option == "3":
            add_device(devices_data)

        elif option == "4":
            remove_device(devices_data)

        elif option == "5":
            interact_with_device()            

        elif option == "6":
            save_devices(devices_data)
            print("Data has been saved.")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    print("Starting menu...")
    menu()
    print("Current working directory:", os.getcwd())
