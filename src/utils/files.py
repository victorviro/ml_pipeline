import json


# Json utils
def get_json_from_file_path(file_path: str) -> dict:

    try:
        with open(file_path) as f:
            data = json.load(f)

    except Exception as e:
        print(f'Error trying to load the json file.\nMessage: {e}')

    return data


def save_json_file(file_path: str, content: dict):

    try:
        with open(file_path, 'w') as output_file:
            json.dump(content, output_file, default=str)

    except Exception as e:
        print(f'Error trying to save the output json.\nMessage: {e}')
