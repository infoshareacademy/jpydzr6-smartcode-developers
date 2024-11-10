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

    def get_current_state(self) -> str:
        """
        Get the current state of the lawn mower.

        Loads the JSON data, searches for the device with the matching device_id,
        and returns the current state as ON or OFF.

        return: The current state as a string, or None if not found.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return str(device['status'].get('current_state', None))
        return None

    def get_target_state(self) -> str:
        """
        Get the target state of the lawn mower.

        Loads the JSON data, searches for the device with the matching device_id,
        and returns the target state as ON or OFF.

        return: The target state as a string, or None if not found.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return str(device['status'].get('target_state', None))
        return None

    def get_grass_height(self) -> float:
        """
        Get the current grass cutting height of the lawn mower.

        Loads the JSON data, searches for the device with the matching device_id,
        and returns the current grass height.

        return: The current grass cutting height setting as a float, or None if not found.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return float(device['status'].get('grass_height', None))
        return None

    def turn_on_off(self, state: str) -> None:
        """
        Turn the lawn mower on or off and update both its current and target state.

        state: Desired state, "on" or "off".
        """
        if state.lower() not in ["on", "off"]:
            raise ValueError("State must be 'on' or 'off'")

        # Load JSON data
        json_data = load_json()

        # Find the device in JSON data and update states
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device['status']['current_state'] = state.upper()  # Update current state
                device['status']['target_state'] = state.upper()  # Update target state too
                break

        # Save the updated JSON data 
        save_json(json_data)

        print(f"Lawn Mower {self.device_id} turned {state}")


if __name__ == "__main__":
    lawn_mower_device = LawnMower("mower98765", "LawnMower")
    lawn_mower_device.connect_to_device()
    print("Current State:", lawn_mower_device.get_current_state())
    print("Target State:", lawn_mower_device.get_target_state())
    print("Grass cutting height:", lawn_mower_device.get_grass_height())
    lawn_mower_device.turn_on_off("off")
