import json
import os

def write_user_to_file(user_data):
    file_path = 'users.json'

    # Extract only the required fields
    user_data_to_save = {
        'name': user_data.get('name'),
        'email': user_data.get('email'),
        'age': user_data.get('age')
    }

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(user_data_to_save)

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)
