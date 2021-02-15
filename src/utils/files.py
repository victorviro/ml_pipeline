import logging
import json
import pickle

from sklearn.pipeline import Pipeline

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


def save_json_file(file_path: str, content: dict):

    try:
        with open(file_path, 'w') as output_file:
            json.dump(content, output_file, default=str)

    except Exception as err:
        msg = f'Error saving the json in path {file_path}.\nMessage: {err}'
        logger.error(msg)
        raise Exception(msg)

def load_pickle_file(file_path: str) -> Pipeline:

    try:
        with open(file_path, 'rb') as f:
            file = pickle.load(f)

    except Exception as err:
        msg = f'Error loading the pickle file in path: {file_path}.\nMessage: {err}'
        logger.error(msg)
        raise Exception(msg)

    return file
