import os


PROJECT_PATH = os.getcwd()
DATA_PATH = f'{PROJECT_PATH}/data'
RAW_DATA_PATH = f'{DATA_PATH}/01_raw'

# Endpoints
ENDPOINT_URL = 'http://127.0.0.1:8000/api/v1/'
MCPL_ENDPOINT_NAME = 'max_char_per_line_train_data'

# Get training data
MCPL_TEST_SPLIT = 0.33
MCPL_DATASET_NAME = 'Data_test'
EXPERIMENT_ID = 0

RMSE_THRESOLD = 20
HYPER_PARAMETER_EXP_NAME = 'Hyperparameter Search'
HYPEROPT_MAX_EVALS = 50
TRAIN_MODEL_EXP_NAME = 'Model training'
VERSION = 'v1'

ARTIFACT_LOCAL_PATH = 'pipeline'
ARTIFACTS_URI = ('/home/lenovo/Documents/projects/MCPL_prediction/mlruns/2/ca63e9'
                 f'5ea1f0426c835d94c8f29334e2/artifacts')

MODEL_PATH = f'{ARTIFACTS_URI}/{ARTIFACT_LOCAL_PATH}/model.pkl'
# MODEL_PATH = './mlruns/0/cba6098fa7bc45bfb0f3eea60fa15a98/artifacts/pipeline/model.pkl'
