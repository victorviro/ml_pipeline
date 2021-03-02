# region Imports
import datetime as dt
import os
import sys
import requests
import json

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

sys.path.append(os.getcwd())
from src.config_variables import (DATASET_NAME, RAW_DATA_PATH, TRANSFORMED_DATA_PATH,
                                  RELATIVE_RAW_DATA_PATH, VERSION,
                                  GIT_REMOTE_NAME, GIT_BRANCH_NAME,
                                  MODEL_NAME, MODELS_PATH, SIZE_TEST_SPLIT,
                                  TEST_SPLIT_SEED, MODEL_SEED, RMSE_THRESOLD,
                                  URL_DATA_MCPL_QUOTES_IMAGE_API, URL_DOWNLOAD_DATA_API,
                                  URL_VALIDATE_DATA_API, URL_VERSION_DATA_API,
                                  URL_TRANSFORM_DATA_API, URL_TRAIN_MODEL_API,
                                  URL_VALIDATE_MODEL_API)
# endregion


# Define the general arguments for the DAG (will apply to any of its operators)
default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2021, 3, 1),  # Y, M, D
    'retries': 0,
    'retry_delay': dt.timedelta(minutes=10),
}


def launch_and_manage_api_request(url_api: str, body: dict, description: str):
    try:
        request = requests.post(url_api, data=json.dumps(body))
    except Exception as err:
        if isinstance(err, requests.exceptions.ConnectionError):
            msg = (f'Connection error. Check that the api to {description} is'
                   ' running or that the host and port are specified correctly.'
                   f'\nTraceback of error: {str(err)}')
            raise Exception(msg)
        msg = f'Error request the api to {description}.\nTraceback: {err}'
        raise Exception(msg)

    request_content = request.content
    content = json.loads(request_content.decode('utf-8'))
    content['status_code'] = request.status_code
    if request.status_code == 200:
        return content
    elif request.status_code == 500:
        raise Exception(content)
    elif request.status_code == 404:
        message = 'Endpoint not found. Check that the path of the endpoint is correct'
        content['message'] = message
        raise Exception(content)
    raise Exception(content)


# Define the DAG as context manager
with DAG('max_char_per_line_apis',
         default_args=default_args,
         description='Max character per line ML pipeline',
         schedule_interval='0 0 * * *',
         ) as dag:

    # region Step 0: Helpers
    # Define a python operator that returns the path of the project
    def get_project_path():
        return os.getcwd()
    return_project_path = PythonOperator(task_id='return_project_path',
                                         python_callable=get_project_path)
    # endregion

    # region Step 1: Data ingestion
    def download_data(*op_args):
        body = {
            'url_quotes_image_api_mcpl_data': op_args[0],
            'data_path': op_args[1],
            'data_name': op_args[2]
        }
        return launch_and_manage_api_request(url_api=URL_DOWNLOAD_DATA_API, body=body,
                                             description='download the data')

    DATA_INGESTION_ARGS = [URL_DATA_MCPL_QUOTES_IMAGE_API, RAW_DATA_PATH, DATASET_NAME]
    data_ingestion = PythonOperator(task_id='data_ingestion',
                                    python_callable=download_data,
                                    op_args=DATA_INGESTION_ARGS)
    # endregion

    # region Step 2: Data validation
    def validate_data(*op_args):
        body = {
            'data_path': op_args[0],
            'data_name': op_args[1]
        }
        return launch_and_manage_api_request(url_api=URL_VALIDATE_DATA_API, body=body,
                                             description='validate the data schema')

    DATA_VALIDATION_ARGS = [RAW_DATA_PATH, DATASET_NAME]
    data_validation = PythonOperator(task_id='data_validation',
                                     python_callable=validate_data,
                                     op_args=DATA_VALIDATION_ARGS)
    endregion

    # region Step 3: Data versioning
    def version_data(*op_args):
        body = {
            'relative_data_path': op_args[0],
            'data_name': op_args[1],
            'data_version': op_args[2],
            'git_remote_name': op_args[3],
            'git_branch_name': op_args[4]
        }
        return launch_and_manage_api_request(url_api=URL_VERSION_DATA_API, body=body,
                                             description='version the data')
    DATA_VERSIONING_ARGS = [
        RELATIVE_RAW_DATA_PATH, DATASET_NAME, VERSION, GIT_REMOTE_NAME,
        GIT_BRANCH_NAME
    ]
    data_versioning = PythonOperator(task_id='data_versioning',
                                     python_callable=version_data,
                                     op_args=DATA_VERSIONING_ARGS)
    # endregion

    # region Step 4: Data preprocessing
    def transform_data(*op_args):
        body = {
            'data_path': op_args[0],
            'data_name': op_args[1],
            'data_output_path': op_args[2]
        }
        return launch_and_manage_api_request(url_api=URL_TRANSFORM_DATA_API, body=body,
                                             description='transform the data')
    DATA_PREPROCESSING_ARGS = [
        RAW_DATA_PATH, DATASET_NAME, TRANSFORMED_DATA_PATH
    ]
    data_preprocessing = PythonOperator(task_id='data_preprocessing',
                                        python_callable=transform_data,
                                        op_args=DATA_PREPROCESSING_ARGS)
    # endregion

    # region Step 5: Model training
    def train_model(*op_args):
        body = {
            'transformed_data_path': op_args[0],
            'data_name': op_args[1],
            'alpha': op_args[2],
            'l1_ratio': op_args[3],
            'version': op_args[4],
            'model_path': op_args[5],
            'model_name': op_args[6],
            'size_test_split': op_args[7],
            'test_split_seed': op_args[8],
            'model_seed': op_args[9],
            'raw_data_path': op_args[10]
        }
        return launch_and_manage_api_request(url_api=URL_TRAIN_MODEL_API, body=body,
                                             description='train the model')
    MODEL_TRAINING_ARGS = [
        TRANSFORMED_DATA_PATH, DATASET_NAME, 0.1, 0.1, VERSION,
        MODELS_PATH, MODEL_NAME, SIZE_TEST_SPLIT, TEST_SPLIT_SEED, MODEL_SEED,
        RAW_DATA_PATH
    ]
    model_training = PythonOperator(task_id='model_training',
                                    python_callable=train_model,
                                    op_args=MODEL_TRAINING_ARGS)
    # endregion

    # region Step 5: Model validation
    def validate_model(*op_args):
        body = {
            'transformed_data_path': op_args[0],
            'data_name': op_args[1],
            'model_path': op_args[2],
            'model_name': op_args[3],
            'size_test_split': op_args[4],
            'test_split_seed': op_args[5],
            'rmse_threshold': op_args[6]
        }
        return launch_and_manage_api_request(url_api=URL_VALIDATE_MODEL_API, body=body,
                                             description='validate the model')
    MODEL_VALIDATION_ARGS = [
        TRANSFORMED_DATA_PATH, DATASET_NAME, MODELS_PATH, MODEL_NAME, SIZE_TEST_SPLIT,
        TEST_SPLIT_SEED, RMSE_THRESOLD
    ]
    model_validation = PythonOperator(task_id='model_validation',
                                      python_callable=validate_model,
                                      op_args=MODEL_VALIDATION_ARGS)
    # endregion
