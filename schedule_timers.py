import json
import os
from typing import Dict, Any

from datetime import timedelta, datetime

class ScheduleUpdate:
    def __init__(self, turn_on_time, turn_off_time, working_duration, current_time = str(datetime.now()), task_list = []):
        self.turn_on_time = turn_on_time ("%Y-%m-%d-%H-%M")
        self.turn_off_time = turn_off_time ("%Y-%m-%d-%H-%M")
        self.working_duration = working_duration("%M")
        self.current_time = current_time
        self.task_list = task_list

    def load_devices(self) -> Dict[str, Any]:
        try:
            with open(os.path.join(os.path.dirname(__file__), "devices.json"), "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("File not found.")
            return {"devices": []}
        except json.JSONDecodeError:
            print("Error reading the file.")
            return {"devices": []}

    def print_devices(self, devices_data: Dict[str, Any]) -> None:
        if not devices_data["devices"]:
            print("No devices in the system.")
            return

        for index, device in enumerate(devices_data["devices"]):
            power_status = device['status'].get('power', 'unknown')
            print(f"{index + 1}. {device['name']} ({device['location']}) - Power: {power_status}")

    # Adding turn-on and turn-off time
    def add_turn_on_off_time(self, devices_data: Dict[str, Any]):
        self.print_devices(devices_data)
        device_number = int(input("Enter the device number to set working time schedule: "))
        if device_number not in devices_data:
            return "Device is not available."
        else:
            # Setting turn-on time
            self.turn_on_time = input("Enter time for turning on the device: ")

            # Setting turn-off time
            self.turn_off_time = input("Enter time for turning off the device: ")

            # Verification of dates and adding them to the task list
            if self.turn_on_time <= self.current_time < self.turn_off_time:
                self.task_list.append(self.turn_on_time)

            else:
                return "Incorrect device turn-on time entered."

            if self.current_time >= self.turn_off_time:
                self.task_list.append(self.turn_off_time)

            else:
                return "Incorrect device turn-off time entered."

        return f"Device's working schedule time has been set: {self.turn_on_time} - {self.turn_off_time}."

    # Setting a time period when (starting from now) the device is going to work
    def add_working_time(self, index: int, devices_data: Dict[str, Any]):
        self.device = devices_data["devices"][index]
        self.print_devices(devices_data)
        device_number = int(input("Enter the device number to set working time schedule: "))

        if device_number not in devices_data:
            return "Device is not available."

        # Setting the device's operating time
        else:
            self.working_duration = input(int("Enter for how long the device is to be turned on in minutes: "))
            if self.working_duration > 0:
                self.turn_off_time = self.current_time + timedelta(minutes=self.working_duration)
                self.task_list.append(self.current_time, self.turn_off_time)

            else:
                return "Wrong operating time for the device."

    # Verification if there's any schedule for any device and turning it on/off if conditions are met
    def check_schedule_time(self, scheduled_devices: [str, Any]) -> None:
        self.device = scheduled_devices["task_list"]

        for self.device in self.task_list:
            if self.turn_on_time <= self.current_time < self.turn_off_time:
                if self.device["status"]["power"] == "off":
                    self.device["status"]["power"] = "on"
                else:
                    self.device["status"]["power"] = "on"

            elif self.current_time >= self.turn_off_time:
                if self.device["status"]["power"] == "on":
                    self.device["status"]["power"] = "off"
                else:
                    self.device["status"]["power"] = "off"

            else:
                pass


"""
Adding to the menu:

def menu() -> None:
    devices_data = load_devices()

    while True:
        print("\nChoose an option:")
        print("1. Show devices")
        print("2. Toggle device")
        print("3. Add device")
        print("4. Remove device")
        print("5. Set working schedule time for a device")
        print("6. Save and exit")

        # Checking if there are any time schedules set and activating them if conditions are met
        ScheduleUpdate.check_schedule_time(scheduled_devices["task_list"])        
           
        elif option == "5":
            print("\nChoose an option:")
            print("a. Set time for turning on and turning off the device")
            print("b. Set working duration time for the device")

            option_time = input("Choose an option: ")
            if option_time == "a":
                ScheduleUpdate.add_turn_on_off_time(devices_list)
            if option_time == "b":
                ScheduleUpdate.add_working_time(devices_data)
"""
