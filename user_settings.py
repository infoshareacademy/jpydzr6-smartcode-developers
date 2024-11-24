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
        json_data = self.load_json_user_file()
        if len(json_data) == 0:
            return "There are no users"
        else:
            return [(self.user["user_id"], self.user["name"] for self.user in json_data["users"]]


    # Adding new user
    def add_new_user(self, user_id: int, name: str):
        json_data = self.load_json_user_file()
       # Verification if the user already exists and adding the user to the list
        if user_id or name in json_data:
            return "The user already exists"
        else:
            json_data[user_id, name].append(self.user_id, self.name)

    # Deleting user
    def delete_user(self, user_id: int, name: str):
        json_data = self.load_json_user_file()
        # Verification and deleting
        if user_id and name in json_data:
            del json_data[user_id, name]
        else:
            print("User not found")

    # Updating user's name
    def update_user_name(self, user_id: int, new_name: str):
        json_data = self.load_json_user_file()
        # Verification if the user exist and changing their name
        if user_id in json_data:
            self.name = new_name
        else:
            print("User not found")

    # Finding user
    def find_user(self, user_id: int, name: str):
        json_data = self.load_json_user_file()
        if user_id or name in json_data:
            return json_data[user_id, name]
        else:
            return "User not found"

    # Listing devices the user has access to
    def accessed_devices(self, user_id: int):
        json_data_devices = self.load_json_devices_file()
        json_data_users = self.load_json_user_file()
        # Iterating "devices" file to find ID of the user from "users" list
        for device in json_data_devices["devices"]:
            try:
                if self.user_id in device and self.user_id in json_data_users:
                    return device
            except:
                pass



if __name__ == '__main__':
    ...