# # region Imports
import datetime as dt
import os
import sys

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable


sys.path.append(os.getcwd())
from src.data.download_raw_data import download_raw_data
from src.data_validation.schema_validation import validate_data_schema
from src.config_variables import MCPL_DATASET_NAME
# endregion


# Define the general arguments for the DAG (will apply to any of its operators)
default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2021, 2, 22),  # Y, M, D
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=10),
}

# Define the DAG as context manager
with DAG('max_char_per_line',
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
        return download_raw_data(data_name=op_args[0])

    data_ingestion = PythonOperator(task_id='data_ingestion',
                                    python_callable=download_data,
                                    op_args=[MCPL_DATASET_NAME])
    # endregion

    # region Step 2: Data validation
    def validate_data(*op_args):
        return validate_data_schema(data_name=op_args[0])

    data_validation = PythonOperator(task_id='data_validation',
                                     python_callable=validate_data,
                                     op_args=[MCPL_DATASET_NAME])
    # endregion

return_project_path >> data_ingestion >> data_validation
