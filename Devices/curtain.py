from device import NotCompatibleDevice, Device, load_json

class Curtain(Device):
    def __init__(self, device_id: str, device_type: str):
        super().__init__(device_id, device_type)

    def connect_to_device(self) -> None:
        """
        Connect to the device
        :return:
        """
        if self.device_type != "curtain":
            raise NotCompatibleDevice
        else:
            print(f"Connected to device {self.device_id}")

    def get_current_position(self) -> float:
        """
        Get the current position of the curtain.

        This method loads the JSON data from the file, iterates through the devices,
        and returns the current position for the curtain with the matching device_id.

        :return: The current position of the curtain as a string. If the device is not found,
                 it returns None.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return float(device['status'].get('position', None))
        return None

    def get_open_percentage(self) -> float:
        """
        Get the open percentage of the curtain.

        This method loads the JSON data from the file, iterates through the devices,
        and returns the open percentage for the curtain with the matching device_id.

        :return: The open percentage of the curtain as a string. If the device is not found,
                 it returns None.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return float(device['status'].get('open_percent'))
        return None


if __name__ == "__main__":
    curtain = Curtain("curtain12345", "curtain")
    curtain.connect_to_device()
    print("Current Position:", curtain.get_current_position())
    print("Open Percentage:", curtain.get_open_percentage())