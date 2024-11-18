from device import NotCompatibleDevice, Device, load_json

class Curtain(Device):
    def __init__(self, device_id: str, device_type: str):
        super().__init__(device_id, device_type)


    def get_current_position(self) -> float:
        """
        Get the current position of the curtain.

        Loads the JSON data, searches for the device with the matching device_id,
        and returns the current position of the curtain.

        :return: The current position of the curtain as a float, or None if not found.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return float(device['status'].get('position', None))
        return None

    def get_open_percentage(self) -> float:
        """
        Get the open percentage of the curtain.

        Loads the JSON data, searches for the device with the matching device_id,
        and returns the open percentage of the curtain.

        :return: The open percentage of the curtain as a float, or None if not found.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return float(device['status'].get('open_percent'))
        return None


if __name__ == "__main__":
    curtain = Curtain("curtain12345", "curtain")
    print("Current Position:", curtain.get_current_position())
    print("Open Percentage:", curtain.get_open_percentage())
