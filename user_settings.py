import json

FILE_PATH_USERS = "../users.json"
FILE_PATH_DEVICES = "../devices.json"

class UserSettings:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name


    # Opening users file
    def load_json_user_file(self):
        with open(FILE_PATH_USERS, 'r') as file:
            data = json.load(file)
            return data

    # Saving users file.
    def save_json_user_file(self, data) -> None:
        with open(FILE_PATH_USERS, 'w') as file:
            json.dump(data, file, indent=4)

    # Opening devices file
    def load_json_devices_file(self):
        with open(FILE_PATH_DEVICES, 'r') as file:
            data = json.load(file)
            return data

    # Saving devices file
    def save_json_devices_file(self, data) -> None:
        with open(FILE_PATH_DEVICES, 'w') as file:
            json.dump(data, file, indent=4)


    # Querying list of users
    def get_users_list(self):
        users = self.load_json_user_file()
        if len(users) == 0:
            return "There are no users"
        else:
            return [(user["user_id"], user["name"]) for user in users["users"]]


    # Adding new user
    def add_new_user(self, user_id: int, name: str):
        users = self.load_json_user_file()
       # Verification if the user already exists and adding the user to the list
        if user_id or name in users:
            return "The user already exists"
        else:
            users[user_id, name].append(self.user_id, self.name)

    # Deleting user
    def delete_user(self, user_id: int, name: str):
        users = self.load_json_user_file()
        # Verification and deleting
        if user_id and name in users:
            del users[user_id, name]
        else:
            print("User not found")

    # Updating user's name
    def update_user_name(self, user_id: int, new_name: str):
        users = self.load_json_user_file()
        # Verification if the user exist and changing their name
        if user_id in users:
            self.name = new_name
        else:
            print("User not found")

    # Finding user
    def get_user(self, user_id: int, name: str):
        users = self.load_json_user_file()
        if user_id or name in users:
            return users[user_id, name]
        else:
            return "User not found"

    # Listing devices the user has access to
    def accessed_devices(self, user_id: int):
        devices = self.load_json_devices_file()
        users = self.load_json_user_file()
        # Iterating "devices" file to find ID of the user from "users" list
        for device in devices["devices"]:
            try:
                if self.user_id in device and self.user_id in users:
                    return device
            except:
                pass
