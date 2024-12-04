import json
import os
from typing import Dict, Any


def save_devices(devices: Dict[str, Any]) -> None:
    try:
        file_path = os.path.join(os.path.dirname(__file__), "devices.json")
        with open(file_path, "w") as file:
            json.dump(devices, file, indent=4)
        print("Devices have been saved successfully.")
    except IOError as e:
        print(f"Error saving devices: {e}")


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


def set_brightness_and_rgb(device: Dict[str, Any]) -> None:
    try:

        device_type = device.get("type")
        if device_type in ["light"]:

            brightness = int(input("Enter brightness (0-100): "))
            if 0 <= brightness <= 100:
                device["status"]["brightness"] = brightness
            else:
                print("Brightness must be between 0 and 100.")
        
            red = int(input("Enter red color value (0-255): "))
            green = int(input("Enter green color value (0-255): "))
            blue = int(input("Enter blue color value (0-255): "))
        
            if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255:
                device["status"]["rgb"] = {"red": red, "green": green, "blue": blue}
            else:
                print("RGB values must be between 0 and 255.")

        else:
            print(f"Cannot change brightness and RGB settings for {device_type} devices.")
    
    except ValueError:
        print("Invalid value entered. Keeping previous settings.")


def toggle_device(index: int, devices_data: Dict[str, Any]) -> None:
    device = devices_data["devices"][index]
    
    if "status" not in device:
        device["status"] = {"power": "off"}

    if "power" not in device["status"]:
        device["status"]["power"] = "off"

    device["status"]["power"] = "on" if device["status"]["power"] == "off" else "off"

    if device["type"] == "light":
        if device["status"]["power"] == "on":
            print(f"{device['name']} in {device['location']} is now ON.")
            print(f"Brightness: {device['status']['brightness']}%")
            print(f"Color temperature: {device['status']['color_temp']}K")
            print(f"RGB Color: ({device['status']['rgb']['red']}, {device['status']['rgb']['green']}, {device['status']['rgb']['blue']})")
        else:
            print(f"{device['name']} in {device['location']} is now OFF.")

    elif device["type"] == "plug":
        if device["status"]["power"] == "on":
            print(f"{device['name']} in {device['location']} is now ON.")
            print(f"Current power: {device['status']['energy_consumption']['current_power_w']}W")
            print(f"Total energy consumed: {device['status']['energy_consumption']['total_energy_kwh']} kWh")
        else:
            print(f"{device['name']} in {device['location']} is now OFF.")

    elif device["type"] == "thermostat":
        if device["status"]["power"] == "on":
            print(f"{device['name']} in {device['location']} is now ON.")
            print(f"Current temperature: {device['status']['current_temperature_c']}°C")
            print(f"Target temperature: {device['status']['target_temperature_c']}°C")
            print(f"Humidity: {device['status']['humidity']}%")
        else:
            print(f"{device['name']} in {device['location']} is now OFF.")

    elif device["type"] == "curtain":
        if device["status"]["power"] == "on":
            print(f"{device['name']} in {device['location']} is now ON.")
            print(f"Current position: {device['status']['position']}%")
            print(f"Open percentage: {device['status']['open_percent']}%")
        else:
            print(f"{device['name']} in {device['location']} is now OFF.")

    elif device["type"] == "weather_station":
        if device["status"]["power"] == "on":
            print(f"{device['name']} in {device['location']} is now ON.")
            print(f"Temperature: {device['status']['temperature_c']}°C")
            print(f"Humidity: {device['status']['humidity_percent']}%")
            print(f"Pressure: {device['status']['pressure_hpa']} hPa")
            print(f"Wind speed: {device['status']['wind_speed_kmh']} km/h")
            print(f"Rainfall: {device['status']['rainfall_mm']} mm")
        else:
            print(f"{device['name']} in {device['location']} is now OFF.")

    elif device["type"] == "lawn_mower":
        if device["status"]["power"] == "on":
            print(f"{device['name']} in {device['location']} is now ON.")
            print(f"Battery level: {device['status']['battery_percent']}%")
            print(f"Cutting mode: {device['status']['cutting_mode']}")
            print(f"Current area being cut: {device['status']['current_area_m2']} m²")
            print(f"Total cutting time: {device['status']['total_cutting_time_minutes']} minutes")
        else:
            print(f"{device['name']} in {device['location']} is now OFF.")

    else:
        print(f"{device['name']} in {device['location']} is not a recognized device type.") 

    save_devices(devices_data)
    print(f"Device '{device['name']}' has been toggled.")


def print_devices(devices_data: Dict[str, Any]) -> None:
    if devices_data["devices"]:
        for index, device in enumerate(devices_data["devices"]):
            print("="*40)
            print(f"{index +1}. Device Name: {device['name']}")
            print(f"   Location: {device['location']}")

            power_status = device['status'].get('power', None)
            if power_status is not None:
                print(f"   Power: {power_status}")

            if device["type"] == "light":
                brightness = device['status'].get('brightness', None)
                if brightness is not None:
                    print(f"   Brightness: {brightness}")

                rgb = device['status'].get('rgb', None)
                if rgb is not None:
                    print(f"   RGB: {rgb}")
            
            is_connected = "Connected" if device.get("connected") else "Disconnected"
            print(f"   Connection: {is_connected}")
            
            print("="*40)
    
    else:
        print("No devices available.")


def print_device_details(devices_data: Dict[str, Any], device_index: int) -> None:
    device = devices_data["devices"][device_index]
    
    print("="*40)
    print(f"Device Name: {device['name']}")
    print(f"Location: {device['location']}")
    
    power_status = device['status'].get('power', None)
    print(f"Power: {power_status if power_status else 'N/A'}")

    if device["type"] == "light":
        brightness = device['status'].get('brightness', None)
        print(f"Brightness: {brightness if brightness else 'N/A'}")
        rgb = device['status'].get('rgb', None)
        if rgb:
            print(f"RGB Color: ({rgb['red']}, {rgb['green']}, {rgb['blue']})")
        else:
            print("RGB: N/A")
        print(f"Color Temperature: {device['status'].get('color_temp', 'N/A')}K")

    elif device["type"] == "plug":
        print(f"Energy Consumption: {device['status']['energy_consumption'].get('current_power_w', 'N/A')}W")
        print(f"Total Energy Consumed: {device['status']['energy_consumption'].get('total_energy_kwh', 'N/A')} kWh")
        
    elif device["type"] == "thermostat":
        print(f"Current Temperature: {device['status'].get('current_temperature_c', 'N/A')}°C")
        print(f"Target Temperature: {device['status'].get('target_temperature_c', 'N/A')}°C")
        print(f"Humidity: {device['status'].get('humidity', 'N/A')}%")
        
    elif device["type"] == "curtain":
        print(f"Position: {device['status'].get('position', 'N/A')}%")
        print(f"Open Percentage: {device['status'].get('open_percent', 'N/A')}%")
        
    elif device["type"] == "weather_station":
        print(f"Temperature: {device['status'].get('temperature_c', 'N/A')}°C")
        print(f"Humidity: {device['status'].get('humidity_percent', 'N/A')}%")
        print(f"Pressure: {device['status'].get('pressure_hpa', 'N/A')} hPa")
        print(f"Wind Speed: {device['status'].get('wind_speed_kmh', 'N/A')} km/h")
        print(f"Rainfall: {device['status'].get('rainfall_mm', 'N/A')} mm")

    elif device["type"] == "lawn_mower":
        print(f"Battery Level: {device['status'].get('battery_percent', 'N/A')}%")
        print(f"Cutting Mode: {device['status'].get('cutting_mode', 'N/A')}")
        print(f"Current Area: {device['status'].get('current_area_m2', 'N/A')} m²")
        print(f"Total Cutting Time: {device['status'].get('total_cutting_time_minutes', 'N/A')} minutes")
        
    else:
        print(f"Device type '{device['type']}' is not recognized.")
        
    print("="*40)


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
        print("\n========================================")
        print("Smart Home Device Manager")
        print("========================================")
        print("\nChoose an option:")
        print("1. Show devices")
        print("2. Toggle device")
        print("3. Set brightness and RGB of device")
        print("4. Add device")
        print("5. Remove device")
        print("6. View device details")
        print("7. Save and exit")

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
            print_devices(devices_data)
            try:
                device_number = int(input("Enter the device number to set brightness and RGB: ")) - 1
                if 0 <= device_number < len(devices_data["devices"]):
                    set_brightness_and_rgb(devices_data["devices"][device_number])
                else:
                    print("Invalid device number.")
            except ValueError:
                print("Enter a valid number.")

        elif option == "4":
            add_device(devices_data)

        elif option == "5":
            remove_device(devices_data)

        elif option == "6":
            print_devices(devices_data)
            try:
                device_number = int(input("Enter the device number to view details: ")) - 1
                if 0 <= device_number < len(devices_data["devices"]):
                    print_device_details(devices_data, device_number)
                else:
                    print("Invalid device number.")
            except ValueError:
                print("Enter a valid number.")

        elif option == "7":
            save_devices(devices_data)
            print("Data has been saved.")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    print("Starting menu...")
    menu()
    print("Current working directory:", os.getcwd())
