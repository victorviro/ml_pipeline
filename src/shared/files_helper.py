import logging
import json
import pickle


logger = logging.getLogger(__name__)


# Json utils
def get_json_from_file_path(file_path: str) -> dict:

    try:
        with open(file_path) as f:
            data = json.load(f)

    except Exception as err:
        msg = f'Error trying to load the json file in path: {file_path}.\nMessage: {err}'
        logger.error(msg)
        raise Exception(msg)

    return data


def load_pickle_file(file_path: str):

    try:
        with open(file_path, 'rb') as f:
            file = pickle.load(f)

    except Exception as err:
        msg = f'Error loading the pickle file in path: {file_path}.\nMessage: {err}'
        logger.error(msg)
        raise Exception(msg)

    return file


def save_pickle_file(file_path: str, file):

    try:
        with open(file_path, 'wb') as f:
            pickle.dump(file, f)

    except Exception as err:
        msg = f'Error saving the pickle file in path: {file_path}.\nMessage: {err}'
        logger.error(msg)
        raise Exception(msg)
