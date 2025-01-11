import json

FILE_PATH_USERS = "../users.json"
FILE_PATH_DEVICES = "../devices.json"

class UserSettings:
    def __init__(self, user_id: int, name: str, controlled_devices_ids: [int]):
        self.user_id = user_id
        self.name = name
        self.controlled_devices_ids = controlled_devices_ids

    def load_json_user_file(self):
        # Opening users file
        with open(FILE_PATH_USERS, 'r') as file:
            data = json.load(file)
            return data

    def save_json_user_file(self, data) -> None:
        # Saving users file.
        with open(FILE_PATH_USERS, 'w') as file:
            json.dump(data, file, indent=4)

    def load_json_devices_file(self):
        # Opening devices file
        with open(FILE_PATH_DEVICES, 'r') as file:
            data = json.load(file)
            return data

    def save_json_devices_file(self, data) -> None:
        # Saving devices file
        with open(FILE_PATH_DEVICES, 'w') as file:
            json.dump(data, file, indent=4)

    def get_users_list(self):
        users = self.load_json_user_file()
        # Querying list of users
        if len(users) == 0:
            return "There are no users"
        else:
            return [(user["user_id"], user["user_name"], user["controlled_devices_ids"]) for user in users["users"]]

    # Adding new user
    def add_new_user(self, user_id: int, name: str):
        users = self.load_json_user_file()
       # Verification if the user already exists and adding the user to the list
        if user_id or name in users:
            return "The user already exists"
        else:
            users[user_id, name].append(self.user_id, self.name)

    # Deleting user
    def delete_user(self, user_id: int, name: str, controlled_devices_ids):
        users = self.load_json_user_file()
        # Verification and deleting user
        if user_id or name in users:
            del users[user_id, name, controlled_devices_ids]
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


    def get_user(self, user_id: int, name: str, controlled_devices_ids):
        users = self.load_json_user_file()
        # Finding user
        if user_id or name in users:
            return users[user_id, name, controlled_devices_ids]
        else:
            return "User not found"

    def users_by_controlled_devices(self, user_id: int, name, controlled_devices_ids):
        users = self.load_json_user_file()
        #Listing users who have access to particular device
        for user in users["users"]:
            try:
                if controlled_devices_ids in user["controlled_devices_ids"]:
                    return user[user_id, name]
            except:
                pass

    def add_device(self, user_id: int, name: str):
        users = self.load_json_user_file()
        # Adding devices to users
        for user in users["users"]:
            if user_id == user["user_id"] or name in users["users"]:
                self.controlled_devices_ids.append(user["controlled_devices_ids"])
            else:
                print("User not found")
