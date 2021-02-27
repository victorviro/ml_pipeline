# # region Imports
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
from src.config_variables import (MCPL_DATASET_NAME, ENDPOINT_PATH, RAW_DATA_PATH,
                                  TRANSFORMED_DATA_PATH, URL_DOWNLOAD_DATA_API,
                                  URL_VALIDATE_DATA_API)
# endregion


# Define the general arguments for the DAG (will apply to any of its operators)
default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2021, 2, 26),  # Y, M, D
    'retries': 0,
    'retry_delay': dt.timedelta(minutes=10),
}

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
            'endpoint_path': op_args[0],
            'data_path': op_args[1],
            'data_name': op_args[2]
        }
        try:
            request = requests.post(URL_DOWNLOAD_DATA_API, data=json.dumps(body))
        except Exception as err:
            if isinstance(err, requests.exceptions.ConnectionError):
                msg = ('Connection error. Check that the api for downloading the data is'
                       ' running or that the host and port are specified correctly.'
                       f'\nTraceback of error: {str(err)}')
                raise Exception(msg)
            msg = f'Error request the api for downloading the data.\nTraceback: {err}'
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

    data_ingestion = PythonOperator(task_id='data_ingestion',
                                    python_callable=download_data,
                                    op_args=[ENDPOINT_PATH, RAW_DATA_PATH,
                                             MCPL_DATASET_NAME])
    # endregion

    # region Step 2: Data validation
    def validate_data(*op_args):
        body = {
            'data_path': op_args[0],
            'data_name': op_args[1]
        }
        try:
            request = requests.post(URL_VALIDATE_DATA_API, data=json.dumps(body))
        except Exception as err:
            if isinstance(err, requests.exceptions.ConnectionError):
                msg = ('Connection error. Check that the api to validate the data schema'
                       ' is running or that the host and port are specified correctly.'
                       f'\nTraceback of error: {str(err)}')
                raise Exception(msg)
            msg = f'Error request the api to validate the data schema.\nTraceback: {err}'
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

    data_validation = PythonOperator(task_id='data_validation',
                                     python_callable=validate_data,
                                     op_args=[RAW_DATA_PATH, MCPL_DATASET_NAME])
    # endregion

return_project_path >> data_ingestion >> data_validation
