from typing import List
from device import load_json, save_json
from bulb import Bulb  #Importing bulbs from bulb.py


class BulbNetwork:
    def __init__(self):
        self.bulbs: List[Bulb] = []

    def load_bulbs(self) -> None:
        """
        Load all bulb devices from the JSON data and initialize Bulbs.
        """
        json_data = load_json()
        for device in json_data.get('devices', []):
            if device.get("type") == "light":  #Only devices with "light" are loaded
                bulb = Bulb(device['device_id'], "Bulb")
                self.bulbs.append(bulb)
        print(f"{len(self.bulbs)} bulbs loaded into the network.")

    def find_bulb_by_id(self, device_id: str) -> Bulb:
        """
        Finds a bulb by its device_id.

        device_id: The ID of the bulb to find.
        return: Bulb if found, else None.
        """
        for bulb in self.bulbs:
            if bulb.device_id == device_id:
                return bulb
        print(f"Bulb with ID {device_id} not found.")
        return None

    def turn_all_on_off(self, state: str) -> None:
        """
        Turns all bulbs in the network on or off.

        state: Desired state, "ON" or "OFF".
        """
        if state.upper() not in ["ON", "OFF"]:
            raise ValueError("State must be 'ON' or 'OFF'")

        for bulb in self.bulbs:
            bulb.turn_on_off(state)

    def display_all_statuses(self) -> None:
        """
        Displays the status of each bulb in the network.
        """
        for bulb in self.bulbs:
            print(f"Bulb ID: {bulb.device_id}")
            print(f"  Name: {bulb.get_name()}")
            print(f"  Brand: {bulb.get_brand()}")
            print(f"  Model: {bulb.get_model()}")
            print(f"  Power: {bulb.get_power()}")
            print(f"  Brightness: {bulb.get_brightness()}")
            print(f"  Color Temperature: {bulb.get_color_temp()}")
            print(f"  RGB: {bulb.get_rgb()}")
            print()  #Separator 


if __name__ == "__main__":
   
    bulb_network = BulbNetwork()
    bulb_network.load_bulbs()


    bulb_network.display_all_statuses()

    
    bulb_id = "1234567890abcdef"  
    bulb = bulb_network.find_bulb_by_id(bulb_id)
    if bulb:
        bulb.turn_on_off("ON")

    
    bulb_network.turn_all_on_off("OFF")

    
    bulb_network.display_all_statuses()
