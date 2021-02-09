
import logging.config
from src.logging_config import LOGGING_CONFIG

from src.data.download_raw_data import download_raw_data
from src.data_validation.schema_validation import validate_data_schema


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("controller")

logger.info('Controller....')

# download_raw_data(data_name='Data_test2')
validate_data_schema(data_name='Data_test')
