import json

import requests

from src.shared.constants import (
    DATASET_NAME,
    DATASET_VERSION,
    RMSE_THRESOLD,
    URL_DATA_MCPL_QUOTES_IMAGE_API,
)

RAW_DATA_PATH = "/mcpl_prediction/data/01_raw"
MLFLOW_RUN_ID = "2b847d74310142ae906f457afc5b4732"


def test_services():

    # # Download data
    body = {
        "data_api_url": URL_DATA_MCPL_QUOTES_IMAGE_API,
        "data_path": RAW_DATA_PATH,
        "data_name": DATASET_NAME,
    }
    # Request to Fast API to get dataset
    url_api = "http://0.0.0.0:1213/api/get_data"
    request = requests.post(url_api, data=json.dumps(body))
    print(request.content)

    # Validate data schema
    body = {"data_path": RAW_DATA_PATH, "data_name": DATASET_NAME}
    # Request to Fast API to validate the shema of the dataset
    # url_api = 'http://0.0.0.0:1214/api/validate_data_schema'
    url_api = "http://validate_data:1214/api/validate_data_schema"
    request = requests.post(url_api, data=json.dumps(body))
    print(request.content)

    # # Transform data
    # Fit transformer
    body = {
        "data_path": RAW_DATA_PATH,
        "data_name": DATASET_NAME,
        "size_test_split": 0.33,
        "test_split_seed": 1,
        "mlflow_run_id": MLFLOW_RUN_ID,
    }
    # Request to Fast API to transform the data
    # url_api = 'http://0.0.0.0:1215/api/fit_transformer_pipeline'
    url_api = "http://transform_data:1215/api/fit_transformer_pipeline"
    request = requests.post(url_api, data=json.dumps(body))
    print(request.content)

    # Train model
    body = {
        "raw_data_path": RAW_DATA_PATH,
        "data_name": DATASET_NAME,
        "alpha": 0.1,
        "l1_ratio": 0.1,
        "size_test_split": 0.33,
        "test_split_seed": 1,
        "model_seed": 42,
        "mlflow_run_id": MLFLOW_RUN_ID,
    }
    # Request to Fast API to train the model
    # url_api = 'http://0.0.0.0:1216/api/train_model'
    url_api = "http://train_model:1216/api/train_model"
    request = requests.post(url_api, data=json.dumps(body))
    print(request.content)

    # Version data
    body = {
        "data_path": RAW_DATA_PATH,
        "data_name": "data",
        "data_version": DATASET_VERSION,
        "git_remote_name": "origin",
        "git_branch_name": "master",
        "mlflow_run_id": MLFLOW_RUN_ID,
    }
    # Request to Fast API to train the model
    # url_api = 'http://0.0.0.0:1217/api/version_data'
    url_api = "http://version_data:1217/api/version_data"
    request = requests.post(url_api, data=json.dumps(body))
    print(request.content)

    # Evaluate model
    body = {
        "raw_data_path": RAW_DATA_PATH,
        "data_name": DATASET_NAME,
        "size_test_split": 0.33,
        "test_split_seed": 1,
        "mlflow_run_id": MLFLOW_RUN_ID,
    }
    # Request to Fast API to train the model
    # url_api = 'http://0.0.0.0:1220/api/evaluate_model'
    url_api = "http://evaluate_model:1220/api/evaluate_model"
    request = requests.post(url_api, data=json.dumps(body))
    print(request.content)

    # Validate model
    body = {"rmse_threshold": RMSE_THRESOLD, "mlflow_run_id": MLFLOW_RUN_ID}
    # Request to Fast API to train the model
    # url_api = 'http://0.0.0.0:1218/api/validate_model'
    url_api = "http://validate_model:1218/api/validate_model"
    request = requests.post(url_api, data=json.dumps(body))
    print(request.content)

    # Serve model
    body = {"mlflow_run_id": MLFLOW_RUN_ID}
    # Request to Fast API to train the model
    # url_api = 'http://0.0.0.0:1219/api/served_model'
    url_api = "http://serve_model:1219/api/served_model"
    request = requests.post(url_api, data=json.dumps(body))
    print(request.content)


if __name__ == "__main__":
    test_services()
