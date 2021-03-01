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
from src.config_variables import (DATASET_NAME, URL_DATA_MCPL_QUOTES_IMAGE_API,
                                  RAW_DATA_PATH, TRANSFORMED_DATA_PATH,
                                  URL_VALIDATE_DATA_API, RELATIVE_RAW_DATA_PATH,
                                  VERSION, GIT_REMOTE_NAME, GIT_BRANCH_NAME,
                                  URL_VERSION_DATA, TRANSFORMED_DATA_PATH,
                                  URL_DOWNLOAD_DATA_API)
# endregion


# Define the general arguments for the DAG (will apply to any of its operators)
default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2021, 2, 26),  # Y, M, D
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

    data_ingestion = PythonOperator(task_id='data_ingestion',
                                    python_callable=download_data,
                                    op_args=[URL_DATA_MCPL_QUOTES_IMAGE_API, RAW_DATA_PATH,
                                             DATASET_NAME])
    # endregion

    # region Step 2: Data validation
    def validate_data(*op_args):
        body = {
            'data_path': op_args[0],
            'data_name': op_args[1]
        }
        return launch_and_manage_api_request(url_api=URL_VALIDATE_DATA_API, body=body,
                                             description='validate the data schema')

    data_validation = PythonOperator(task_id='data_validation',
                                     python_callable=validate_data,
                                     op_args=[RAW_DATA_PATH, DATASET_NAME])
    # endregion

return_project_path >> data_ingestion >> data_validation
