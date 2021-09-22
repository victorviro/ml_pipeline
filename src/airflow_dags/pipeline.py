# Imports
from datetime import datetime, timedelta
from json import dumps, loads

from airflow.operators.python_operator import PythonOperator
from mlflow import active_run, end_run, start_run
from requests import post
from requests.exceptions import ConnectionError

from airflow import DAG
from src.shared.constants import (
    ALPHA_PARAM_MODEL,
    DATASET_NAME,
    GIT_BRANCH_NAME,
    GIT_REMOTE_NAME,
    L1_RATIO_PARAM_MODEL,
    MODEL_SEED,
    RAW_DATA_PATH,
    RMSE_THRESOLD,
    SIZE_TEST_SPLIT,
    TEST_SPLIT_SEED,
    URL_DATA_MCPL_QUOTES_IMAGE_API,
    URL_EVALUATE_MODEL_API,
    URL_FIT_DATA_TRANSFORMER_API,
    URL_GET_DATA_API,
    URL_TRAIN_MODEL_API,
    URL_VALIDATE_DATA_API,
    URL_VALIDATE_MODEL_API,
    URL_VERSION_DATA_API,
    VERSION,
)

# Define the general arguments for the DAG (it will apply to any of its operators)
default_args = {
    "owner": "me",
    "start_date": datetime(2021, 6, 16),  # Y, M, D
    "retries": 0,
    "retry_delay": timedelta(minutes=10),
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
    except ConnectionError as err:
        msg = (
            f"Connection error. Check that the api to {description} is running or that"
            f" the host and port are specified correctly. Error description: {err}."
        )
        raise ConnectionError(msg)
    except Exception as err:
        msg = (
            f"Unknown error when request the api to {description}. Error: "
            f"{err.__class__.__name__}:{err}."
        )
        raise Exception(msg)

    request_content = request.content
    content = loads(request_content.decode("utf-8"))
    content["status_code"] = request.status_code
    if request.status_code == 200:
        return content
    elif request.status_code == 500:
        raise Exception(content)
    elif request.status_code == 404:
        message = "Endpoint not found. Check that the path of the endpoint is correct"
        content["message"] = message
        raise Exception(content)
    raise Exception(content)


# Define the DAG as context manager
with DAG(
    "Max_char_per_line_ML_pipeline",
    default_args=default_args,
    description="Max character per line ML pipeline",
    schedule_interval="0 0 * * *",
) as dag:

    # Step 0: Create experiment run
    def create_run():
        start_run()
        run = active_run()
        run_id = run.info.run_id
        end_run()
        return run_id

    run_creation = PythonOperator(task_id="create_run", python_callable=create_run)

    # Step 1: Data ingestion
    def get_data(**kwargs):
        body = {
            "data_api_url": kwargs["data_api_url"],
            "data_path": kwargs["data_path"],
            "data_name": kwargs["data_name"],
        }
        return launch_and_manage_api_request(
            api_url=URL_GET_DATA_API, body=body, description="download the data"
        )

    DATA_INGESTION_ARGS = {
        "data_api_url": URL_DATA_MCPL_QUOTES_IMAGE_API,
        "data_path": RAW_DATA_PATH,
        "data_name": DATASET_NAME,
    }
    data_ingestion = PythonOperator(
        task_id="data_ingestion",
        python_callable=get_data,
        op_kwargs=DATA_INGESTION_ARGS,
    )

    # Step 2: Data validation
    def validate_data(**kwargs):
        body = {
            "data_path": kwargs["data_path"],
            "data_name": kwargs["data_name"],
        }
        return launch_and_manage_api_request(
            api_url=URL_VALIDATE_DATA_API,
            body=body,
            description="validate the data schema",
        )

    DATA_VALIDATION_ARGS = {
        "data_path": RAW_DATA_PATH,
        "data_name": DATASET_NAME,
    }
    data_validation = PythonOperator(
        task_id="data_validation",
        python_callable=validate_data,
        op_kwargs=DATA_VALIDATION_ARGS,
    )

    # Step 3: Data versioning
    def version_data(**kwargs):
        body = {
            "data_path": kwargs["data_path"],
            "data_name": kwargs["data_name"],
            "data_version": kwargs["data_version"],
            "git_remote_name": kwargs["git_remote_name"],
            "git_branch_name": kwargs["git_branch_name"],
            "mlflow_run_id": kwargs["ti"].xcom_pull(task_ids="create_run"),
        }
        return launch_and_manage_api_request(
            api_url=URL_VERSION_DATA_API, body=body, description="version the data"
        )

    DATA_VERSIONING_ARGS = {
        "data_path": RAW_DATA_PATH,
        "data_name": DATASET_NAME,
        "data_version": VERSION,
        "git_remote_name": GIT_REMOTE_NAME,
        "git_branch_name": GIT_BRANCH_NAME,
    }
    data_versioning = PythonOperator(
        task_id="data_versioning",
        python_callable=version_data,
        op_kwargs=DATA_VERSIONING_ARGS,
        provide_context=True,
    )

    # Step 4: Preprocessing fitter
    def fit_data_transformer(**kwargs):
        body = {
            "data_path": kwargs["data_path"],
            "data_name": kwargs["data_name"],
            "size_test_split": kwargs["size_test_split"],
            "test_split_seed": kwargs["test_split_seed"],
            "mlflow_run_id": kwargs["ti"].xcom_pull(task_ids="create_run"),
        }
        return launch_and_manage_api_request(
            api_url=URL_FIT_DATA_TRANSFORMER_API,
            body=body,
            description="transform the data",
        )

    PREPROCESSING_FITTER_ARGS = {
        "data_path": RAW_DATA_PATH,
        "data_name": DATASET_NAME,
        "size_test_split": SIZE_TEST_SPLIT,
        "test_split_seed": TEST_SPLIT_SEED,
    }
    preprocessing_fitter = PythonOperator(
        task_id="preprocessing_fitter",
        python_callable=fit_data_transformer,
        op_kwargs=PREPROCESSING_FITTER_ARGS,
        provide_context=True,
    )

    # Step 5: Model training
    def train_model(**kwargs):
        body = {
            "raw_data_path": kwargs["raw_data_path"],
            "data_name": kwargs["data_name"],
            "alpha": kwargs["alpha"],
            "l1_ratio": kwargs["l1_ratio"],
            "size_test_split": kwargs["size_test_split"],
            "test_split_seed": kwargs["test_split_seed"],
            "model_seed": kwargs["model_seed"],
            "mlflow_run_id": kwargs["ti"].xcom_pull(task_ids="create_run"),
        }
        return launch_and_manage_api_request(
            api_url=URL_TRAIN_MODEL_API, body=body, description="train the model"
        )

    MODEL_TRAINING_ARGS = {
        "raw_data_path": RAW_DATA_PATH,
        "data_name": DATASET_NAME,
        "l1_ratio": L1_RATIO_PARAM_MODEL,
        "alpha": ALPHA_PARAM_MODEL,
        "size_test_split": SIZE_TEST_SPLIT,
        "test_split_seed": TEST_SPLIT_SEED,
        "model_seed": MODEL_SEED,
    }
    model_training = PythonOperator(
        task_id="model_training",
        python_callable=train_model,
        op_kwargs=MODEL_TRAINING_ARGS,
        provide_context=True,
    )

    # Step 6: Model evaluation
    def evaluate_model(**kwargs):
        body = {
            "raw_data_path": kwargs["raw_data_path"],
            "data_name": kwargs["data_name"],
            "size_test_split": kwargs["size_test_split"],
            "test_split_seed": kwargs["test_split_seed"],
            "mlflow_run_id": kwargs["ti"].xcom_pull(task_ids="create_run"),
        }
        return launch_and_manage_api_request(
            api_url=URL_EVALUATE_MODEL_API, body=body, description="evaluate the model"
        )

    MODEL_EVALUATION_ARGS = {
        "raw_data_path": RAW_DATA_PATH,
        "data_name": DATASET_NAME,
        "size_test_split": SIZE_TEST_SPLIT,
        "test_split_seed": TEST_SPLIT_SEED,
    }
    model_evaluation = PythonOperator(
        task_id="model_evaluation",
        python_callable=evaluate_model,
        op_kwargs=MODEL_EVALUATION_ARGS,
        provide_context=True,
    )

    # Step 7: Model validation
    def validate_model(**kwargs):
        body = {
            "rmse_threshold": kwargs["rmse_threshold"],
            "mlflow_run_id": kwargs["ti"].xcom_pull(task_ids="create_run"),
        }
        return launch_and_manage_api_request(
            api_url=URL_VALIDATE_MODEL_API, body=body, description="validate the model"
        )

    MODEL_VALIDATION_ARGS = {"rmse_threshold": RMSE_THRESOLD}
    model_validation = PythonOperator(
        task_id="model_validation",
        python_callable=validate_model,
        op_kwargs=MODEL_VALIDATION_ARGS,
        provide_context=True,
    )


(
    run_creation
    >> data_ingestion
    >> data_validation
    >> data_versioning
    >> preprocessing_fitter
    >> model_training
    >> model_evaluation
    >> model_validation
)
