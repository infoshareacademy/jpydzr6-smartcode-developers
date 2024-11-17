import json
FILE_PATH_USERS = "../users.json"

def delete_json_user(file_path_users = FILE_PATH_USERS):
    """
    Opening json file
    """
    with open(file_path_users, 'r') as file:
        data = json.load(file)
        """
        Deleting user.
        """
        temp = data["users"]
        y = {}
        if y in temp:
            del temp[y]
        else:
            print("User not found")

    """
    Updating json file.
    """
    with open(file_path_users, 'w') as file:
        json.dump(data, file)
        return data

if __name__ == "__main__":
    print(delete_json_user())

