import sys
import tkinter as tk
from ui_terminal import menu
from ui_gui import update_ui, load_devices as load_devices_gui


def main():
    print("SmartCode Developers")
    print("Choose interface:")
    print("1. Terminal")
    print("2. Graphical User Interface")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        print("Starting terminal UI...")
        menu()

    elif choice == "2":
        print("Starting graphical UI...")
        devices_data = load_devices_gui()
        root = tk.Tk()
        root.title("Device Manager")
        update_ui(devices_data, root)
        root.mainloop()

    else:
        print("Invalid choice. Exiting...")
        sys.exit(1)
  

if __name__ == "__main__":
    main()
    