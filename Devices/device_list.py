import json
from pprint import pprint
FILE_PATH = "../devices.json"

def load_json(file_path = FILE_PATH) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def get_device_list() -> list:
    """
    This method loads the JSON data from the file, iterates through the devices, and returns the list of them
    """

    json_data = load_json()
    devices_in_network = []
    for device in json_data['devices']:
        device_list = device['device_id'], device['name']
        devices_in_network.append(device_list)
    return devices_in_network

if __name__ == '__main__':

    print('====List of devices====\n')

    pprint(get_device_list())

