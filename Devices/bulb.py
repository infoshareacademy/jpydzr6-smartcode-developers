from device import NotCompatibleDevice, Device, load_json, save_json


class Bulb(Device):
    def __init__(self, device_id: str, device_type: str):
        super().__init__(device_id, device_type)

    def connect_to_device(self) -> None:
        """
        Connect to the bulb device.
        """
        if self.device_type != "Bulb":
            raise NotCompatibleDevice("Device type is not compatible.")
        else:
            print(f"Connected to Bulb {self.device_id}")

    def get_current_state(self) -> str:
        """
        Get the current state of the bulb.

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
        Get the target state of the Bulb.

        Loads the JSON data, searches for the device with the matching device_id,
        and returns the target state as ON or OFF.

        return: The target state as a string, or None if not found.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                return str(device['status'].get('target_state', None))
        return None

    def get_light_power(self) -> float:
        """
        Get the current bulb power.

        Loads the JSON data, searches for the device with the matching device_id,
        and returns the bulb power.

        return: The current bulb power setting as a float, or None if not found.
        """
        json_data = load_json()
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                power = device['status'].get('bulb_power', None)
                return float(power) if power is not None else None
        return None

    def set_light_power(self, power: float) -> None:
        """
        Set the power level of the bulb.

        power: The desired power level (e.g., a float between 0.0 and 100.0).
        """
        if not (0.0 <= power <= 100.0):
            raise ValueError("Power level must be between 0.0 and 100.0")

        # Load JSON data
        json_data = load_json()

        # Find the device in JSON data and update the power level
        for device in json_data['devices']:
            if device['device_id'] == self.device_id:
                device['status']['bulb_power'] = power
                break

        # Save the updated JSON data
        save_json(json_data)

        print(f"Bulb {self.device_id} power set to {power}")

    def turn_on_off(self, state: str) -> None:
        """
        Turn the bulb on or off and update both its current and target state.

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

        print(f"Bulb {self.device_id} turned {state}")


if __name__ == "__main__":
    bulb_device = Bulb("abcdef1234569298", "Bulb")
    bulb_device.connect_to_device()
    print("Current State:", bulb_device.get_current_state())
    print("Target State:", bulb_device.get_target_state())
    print("Bulb power:", bulb_device.get_light_power())
    bulb_device.set_light_power(75.0)  # Set the power level to 75%
    bulb_device.turn_on_off("on")
