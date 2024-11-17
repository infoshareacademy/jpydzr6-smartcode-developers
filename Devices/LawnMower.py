from device import NotCompatibleDevice, Device, load_json, save_json


class LawnMower(Device):
    def __init__(self, device_id: str, device_type: str):
        super().__init__(device_id, device_type)

    def connect_to_device(self) -> None:
        """
        Connect to the lawn mower device.
        """
        if self.device_type != "LawnMower":
            raise NotCompatibleDevice("Device type is not compatible.")
        else:
            print(f"Connected to Lawn Mower {self.device_id}")

    def load_device_info(self) -> dict:
        """
        Load the JSON data and retrieve the information for this specific lawn mower.

        Returns the device's information as a dictionary, or an empty dictionary if not found.
        """
        json_data = load_json()
        for device in json_data.get('devices', []):
            if device['device_id'] == self.device_id:
                return device
        return {}

    def get_name(self) -> str:
        """
        Get the name of the lawn mower.
        """
        return self.load_device_info().get('name', None)

    def get_brand(self) -> str:
        """
        Get the brand of the lawn mower.
        """
        return self.load_device_info().get('brand', None)

    def get_model(self) -> str:
        """
        Get the model of the lawn mower.
        """
        return self.load_device_info().get('model', None)

    def get_power(self) -> str:
        """
        Get the current power status of the lawn mower (on or off).
        """
        return self.load_device_info().get('status', {}).get('power', None)

    def get_battery_percent(self) -> int:
        """
        Get the battery percentage of the lawn mower.
        """
        return self.load_device_info().get('status', {}).get('battery_percent', None)

    def get_cutting_mode(self) -> str:
        """
        Get the cutting mode of the lawn mower (e.g., auto or manual).
        """
        return self.load_device_info().get('status', {}).get('cutting_mode', None)

    def get_cutting_height(self) -> int:
        """
        Get the cutting height of the lawn mower in millimeters.
        """
        return self.load_device_info().get('status', {}).get('cutting_height_mm', None)

    def get_current_area(self) -> float:
        """
        Get the current area being mowed in square meters.
        """
        return self.load_device_info().get('status', {}).get('current_area_m2', None)

    def get_total_cutting_time(self) -> int:
        """
        Get the total cutting time in minutes.
        """
        return self.load_device_info().get('status', {}).get('total_cutting_time_minutes', None)

    def get_location(self) -> str:
        """
        Get the location of the lawn mower.
        """
        return self.load_device_info().get('location', None)

    def get_last_updated(self) -> str:
        """
        Get the last updated time of the lawn mower.
        """
        return self.load_device_info().get('last_updated', None)

    def turn_on_off(self, state: str) -> None:
        """
        Turn the lawn mower on or off and update its power state in the JSON data.
        """
        if state.upper() not in ["ON", "OFF"]:
            raise ValueError("State must be 'ON' or 'OFF'")

        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device['status']['power'] = state.upper()  # Update power state
                break

        save_json(json_data)
        print(f"Lawn Mower {self.device_id} turned {state}")


if __name__ == "__main__":
    lawn_mower_device = LawnMower("mower98765", "LawnMower")
    lawn_mower_device.connect_to_device()


    print("Name:", lawn_mower_device.get_name())
    print("Brand:", lawn_mower_device.get_brand())
    print("Model:", lawn_mower_device.get_model())
    print("Power:", lawn_mower_device.get_power())
    print("Battery Percentage:", lawn_mower_device.get_battery_percent())
    print("Cutting Mode:", lawn_mower_device.get_cutting_mode())
    print("Cutting Height (mm):", lawn_mower_device.get_cutting_height())
    print("Current Area (m²):", lawn_mower_device.get_current_area())
    print("Total Cutting Time (minutes):", lawn_mower_device.get_total_cutting_time())
    print("Location:", lawn_mower_device.get_location())
    print("Last Updated:", lawn_mower_device.get_last_updated())

    lawn_mower_device.turn_on_off("off")
