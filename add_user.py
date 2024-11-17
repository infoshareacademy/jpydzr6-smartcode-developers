import json

FILE_PATH_USERS = "../users.json"

def add_json_user(file_path_users = FILE_PATH_USERS):

    """
    Opening json file
    """
    with open(file_path_users, 'r') as file:
        data = json.load(file)

        """
        Adding new user.
        """
        temp = data["users"]
        y = {}
        if y in temp:
            print("User already exists")
        else:
            temp.append(y)
    """
    Updating json file.
    """
    with open(file_path_users, 'w') as file:
        json.dump(data, file)
        return data



if __name__ == '__main__':
    ...