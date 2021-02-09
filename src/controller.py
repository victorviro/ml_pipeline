
import logging.config
from src.logging_config import LOGGING_CONFIG

from src.data.download_raw_data import download_raw_data


logging.config.dictConfig(LOGGING_CONFIG)
# logger = logging.getLogger("controller")
logger = logging.getLogger(__name__)

logger.info('Controller....')

download_raw_data(data_name='Data_test', version=1)
