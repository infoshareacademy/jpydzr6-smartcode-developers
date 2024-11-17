import json
FILE_PATH_DEVICES = "../devices.json"
FILE_PATH_USERS = "../users.json"

"""
Loading list of users and list of devices.
"""

def load_json_users(file_path_users = FILE_PATH_USERS) -> dict:
    with open(file_path_users, 'r') as file:
        data = json.load(file)
    return data

def load_json_devices(file_path_devices = FILE_PATH_DEVICES) -> dict:
    with open(file_path_devices, 'r') as file:
        data = json.load(file)
    return data

"""Creating User class"""

class User:
    def __init__(self, user_id: int, name, accessed_devices: []):
        self.user_id = user_id
        self.name = name

        """List of devices user has access to"""
        self.accessed_devices = accessed_devices

    def __str__(self) -> str:
        return f"{self.user_id}, {self.name}, {self.accessed_devices()}"

    def accessed_devices(self):
        for device in self.accessed_devices:
            try:
                if self.user_id in device:
                    return device
            except:
                pass










