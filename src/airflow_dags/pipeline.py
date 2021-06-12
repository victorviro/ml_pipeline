# region Imports
from datetime import datetime, timedelta
from requests import post
from requests.exceptions import ConnectionError
from json import loads, dumps

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from src.shared.infrastructure.mlflow_api_tracker import MlflowApiTracker
from src.shared.constants import (
    TRAIN_MODEL_EXPERIMENT_NAME, DATASET_NAME, RAW_DATA_PATH, VERSION, GIT_REMOTE_NAME,
    GIT_BRANCH_NAME, MODEL_NAME, TRANSFORMER_PIPELINE_NAME, SIZE_TEST_SPLIT,
    TEST_SPLIT_SEED, MODEL_SEED, L1_RATIO_PARAM_MODEL, ALPHA_PARAM_MODEL,
    RMSE_THRESOLD, URL_DATA_MCPL_QUOTES_IMAGE_API,
    URL_GET_DATA_API, URL_VALIDATE_DATA_API, URL_VERSION_DATA_API,
    URL_FIT_DATA_TRANSFORMER_API, URL_TRAIN_MODEL_API, URL_VALIDATE_MODEL_API
)
# endregion


# Define the general arguments for the DAG (it will apply to any of its operators)
default_args = {
    'owner': 'me',
    'start_date': datetime(2021, 4, 7),  # Y, M, D
    'retries': 0,
    'retry_delay': timedelta(minutes=10),
}


def launch_and_manage_api_request(api_url: str, body: dict, description: str) -> dict:
    """Launch a request and catch exceptions and HTTP status codes.

    :param api_url: The url of the API
    :type api_url: str
    :param body: The body for the request
    :type body: dict
    :param description: The description of the step of the pipeline
    :type description: str
    :return: The content of the request response
    :rtype: dict
    """
    try:
        request = post(api_url, data=dumps(body))
    except Exception as err:
        if isinstance(err, ConnectionError):
            msg = (f'Connection error. Check that the api to {description} is'
                   ' running or that the host and port are specified correctly.'
                   f'\nTraceback of error: {str(err)}')
            raise Exception(msg)
        msg = f'Error request the api to {description}.\nTraceback: {err}'
        raise Exception(msg)

    request_content = request.content
    content = loads(request_content.decode('utf-8'))
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
with DAG('Max char per line ML pipeline',
         default_args=default_args,
         description='Max character per line ML pipeline',
         schedule_interval='0 0 * * *',
         ) as dag:

    # region Step 0: Create experiment run
    def create_run(*op_args):
        mlflow_api_tracker = MlflowApiTracker()
        run_id = mlflow_api_tracker.create_run_by_experiment_name(
            experiment_name=op_args[0]
        )
        return run_id
    run_creation = PythonOperator(task_id='create_run', python_callable=create_run,
                                  op_args=[TRAIN_MODEL_EXPERIMENT_NAME])
    # endregion

    # region Step 1: Data ingestion
    def get_data(*op_args):
        body = {
            'data_api_url': op_args[0],
            'data_path': op_args[1],
            'data_name': op_args[2]
        }
        return launch_and_manage_api_request(url_api=URL_GET_DATA_API, body=body,
                                             description='download the data')

    DATA_INGESTION_ARGS = [URL_DATA_MCPL_QUOTES_IMAGE_API, RAW_DATA_PATH, DATASET_NAME]
    data_ingestion = PythonOperator(task_id='data_ingestion',
                                    python_callable=get_data,
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
    # endregion

    # region Step 3: Data versioning
    def version_data(*op_args, **context):
        body = {
            'data_path': op_args[0],
            'data_name': op_args[1],
            'data_version': op_args[2],
            'git_remote_name': op_args[3],
            'git_branch_name': op_args[4],
            'mlflow_run_id': context['ti'].xcom_pull(task_ids='create_run')
        }
        return launch_and_manage_api_request(url_api=URL_VERSION_DATA_API, body=body,
                                             description='version the data')
    DATA_VERSIONING_ARGS = [
        RAW_DATA_PATH, DATASET_NAME, VERSION, GIT_REMOTE_NAME,
        GIT_BRANCH_NAME
    ]
    data_versioning = PythonOperator(task_id='data_versioning',
                                     python_callable=version_data,
                                     op_args=DATA_VERSIONING_ARGS,
                                     provide_context=True)
    # endregion

    # region Step 4: Preprocessing fitter
    def fit_data_transformer(*op_args, **context):
        body = {
            'data_path': op_args[0],
            'data_name': op_args[1],
            'size_test_split':  op_args[2],
            'test_split_seed':  op_args[3],
            'mlflow_run_id': context['ti'].xcom_pull(task_ids='create_run')
        }
        return launch_and_manage_api_request(url_api=URL_FIT_DATA_TRANSFORMER_API,
                                             body=body, description='transform the data')
    PREPROCESSING_FITTER_ARGS = [
        RAW_DATA_PATH, DATASET_NAME, SIZE_TEST_SPLIT, TEST_SPLIT_SEED
    ]
    preprocessing_fitter = PythonOperator(task_id='preprocessing_fitter',
                                          python_callable=fit_data_transformer,
                                          op_args=PREPROCESSING_FITTER_ARGS,
                                          provide_context=True)
    # endregion

    # region Step 5: Model training
    def train_model(*op_args, **context):
        body = {
            'raw_data_path': op_args[0],
            'data_name': op_args[1],
            'alpha': op_args[2],
            'l1_ratio': op_args[3],
            'transformer_name': op_args[4],
            'model_name': op_args[5],
            'size_test_split': op_args[6],
            'test_split_seed': op_args[7],
            'model_seed': op_args[8],
            'mlflow_run_id': context['ti'].xcom_pull(task_ids='create_run')
        }
        return launch_and_manage_api_request(url_api=URL_TRAIN_MODEL_API, body=body,
                                             description='train the model')
    MODEL_TRAINING_ARGS = [
        RAW_DATA_PATH, DATASET_NAME, L1_RATIO_PARAM_MODEL, ALPHA_PARAM_MODEL,
        TRANSFORMER_PIPELINE_NAME, MODEL_NAME, SIZE_TEST_SPLIT, TEST_SPLIT_SEED,
        MODEL_SEED
    ]
    model_training = PythonOperator(task_id='model_training',
                                    python_callable=train_model,
                                    op_args=MODEL_TRAINING_ARGS,
                                    provide_context=True)
    # endregion

    # region Step 5: Model validation
    def validate_model(*op_args, **context):
        body = {
            'raw_data_path': op_args[0],
            'data_name': op_args[1],
            'size_test_split': op_args[2],
            'test_split_seed': op_args[3],
            'rmse_threshold': op_args[4],
            'mlflow_run_id': context['ti'].xcom_pull(task_ids='create_run')
        }
        return launch_and_manage_api_request(url_api=URL_VALIDATE_MODEL_API, body=body,
                                             description='validate the model')
    MODEL_VALIDATION_ARGS = [
        RAW_DATA_PATH, DATASET_NAME, SIZE_TEST_SPLIT, TEST_SPLIT_SEED, RMSE_THRESOLD
    ]
    model_validation = PythonOperator(task_id='model_validation',
                                      python_callable=validate_model,
                                      op_args=MODEL_VALIDATION_ARGS,
                                      provide_context=True)
    # endregion

(run_creation >> data_ingestion >> data_validation >> data_versioning
    >> preprocessing_fitter >> model_training >> model_validation)
