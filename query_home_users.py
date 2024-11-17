import json
FILE_PATH_USERS = "../users.json"

def load_json_users(file_path_users = FILE_PATH_USERS) -> dict:
    with open(file_path_users, 'r') as file:
        data = json.load(file)
    return data

def get_users_list() -> list:

    """
    List of all users with their ID
    """

    json_data = load_json_users()
    users_in_network = []
    for user in json_data['users']:
        users_list = user['user_id'], user['name']
        users_in_network.append(users_list)
    return users_in_network


if __name__ == '__main__':

    print("List of users:\n")
    print(get_users_list())
