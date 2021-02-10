
import logging.config
from src.logging_config import LOGGING_CONFIG

from src.config_variables import MCPL_DATASET_NAME
from src.data.download_raw_data import download_raw_data
from src.data_validation.schema_validation import validate_data_schema


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("controller")


# download_raw_data(data_name=MCPL_DATASET_NAME)
validate_data_schema(data_name=MCPL_DATASET_NAME)
