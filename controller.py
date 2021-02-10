
import logging.config
from src.logging_config import LOGGING_CONFIG

from src.config_variables import MCPL_DATASET_NAME, MODEL_PATH
from src.data.download_raw_data import download_raw_data
from src.data_validation.schema_validation import validate_data_schema
from src.models.train_model import data_transformation_and_training
from src.models.model_validation import validate_model
from src.models.hyperparameter_opt import hyper_parameter_search


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("controller")


# download_raw_data(data_name=MCPL_DATASET_NAME)
# validate_data_schema(data_name=MCPL_DATASET_NAME)
# artifact_uri = data_transformation_and_training(data_name=MCPL_DATASET_NAME,
#                                                 alpha=0.1, l1_ratio=0.1)
# validate_model(data_name=MCPL_DATASET_NAME, model_path=MODEL_PATH)
hyper_parameter_search(data_name=MCPL_DATASET_NAME)
