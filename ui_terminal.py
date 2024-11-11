import json
import os
from typing import Dict, Any


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

    for index, device in enumerate(devices_data["devices"]):
        power_status = device['status'].get('power', 'unknown')
        print(f"{index + 1}. {device['name']} ({device['location']}) - Power: {power_status}")


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


def menu() -> None:
    devices_data = load_devices()

    while True:
        print("\nChoose an option:")
        print("1. Show devices")
        print("2. Toggle device")
        print("3. Add device")
        print("4. Remove device")
        print("5. Save and exit")

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
            save_devices(devices_data)
            print("Data has been saved.")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    print("Starting menu...")
    menu()
    print("Current working directory:", os.getcwd())
