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
from src.models.train_model import data_transformation_and_training
from src.config_variables import MCPL_DATASET_NAME, VERSION
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

    # region Step 3: Data versioning
    data_versioning_command = """
    cd {{ ti.xcom_pull(task_ids='return_project_path') }};
    dvc add data/01_raw/{{ params.data_name }}.json;
    dvc push;
    git add data/raw/{{ params.data_name }}.json.dvc;
    git commit -m 'ref #410 Added raw data {{ params.data_name }} version \
        {{ params.version }}';
    git push master master
    """
    # data_versioning = BashOperator(task_id='data_versioning',
    #                                bash_command=data_versioning_command_test,
    #                                params={"data_name": MCPL_DATASET_NAME,
    #                                        "version": VERSION})
    # endregion

    # region Step 4: Data transformation and training
    def transformation_and_training(*op_args):
        return data_transformation_and_training(data_name=op_args[0], alpha=op_args[1],
                                                l1_ratio=op_args[2])
    # return ./models/19e6f5ff3e214460a2adbfca75d25682/artifacts
    # data_trans_and_train = PythonOperator(task_id='data_trans_and_train',
    #                                       python_callable=transformation_and_training,
    #                                       op_args=[MCPL_DATASET_NAME,
    #                                                0.1,
    #                                                0.1])
    # endregion

return_project_path >> data_ingestion >> data_validation
