from tkinter import Tk
import tkinter as tk
import json
# from functools import partial
import os
from typing import Dict, Any


def save_devices(devices: Dict[str, Any]) -> None:
    file_path = os.path.join(os.path.dirname(__file__), "devices.json")
    with open(file_path, "w") as file:
        json.dump(devices, file, indent=4)


def load_devices() -> Dict[str, Any]:
    file_path = os.path.join(os.path.dirname(__file__), "devices.json")
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"devices": []}


def toggle_device(index: int, devices_data: Dict[str, Any], root: tk.Tk) -> None:
    device = devices_data["devices"][index]
    if device["status"]["power"] == "on":
        device["status"]["power"] = "off"
    else:
        device["status"]["power"] = "on"
    update_ui(devices_data, root)
    save_devices(devices_data)


def update_ui(devices_data: Dict[str, Any], root: tk.Tk) -> None:
    for widget in root.winfo_children():
        widget.destroy()

    for index, device in enumerate(devices_data["devices"]):
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=5, fill="x")

        power_status = device['status'].get('power', 'unknown')

        label = tk.Label(
            frame,
            text=f"{device['name']} ({device['location']}) - Power: {power_status}"
        )
        label.pack(side="left")

        button = tk.Button(
            frame,
            text="Toggle",
            command=lambda idx=index: toggle_device(idx, devices_data, root)
        )
        button.pack(side="right")

    print("UI updated.")


if __name__ == "__main__":
    print("Starting main...")
    devices_data = load_devices()
    root = tk.Tk()
    root.title("Device Manager")
    update_ui(devices_data, root)
    root.mainloop()
