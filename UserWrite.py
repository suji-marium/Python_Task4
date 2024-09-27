import json
import os

def write_user_to_file(user_data):
    file_path = 'users.json'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(user_data)

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)
