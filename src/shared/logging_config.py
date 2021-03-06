import os

LOGGING_ROOT_DIR = f'{os.getcwd()}/logs'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s (%(name)s) '
                      '[%(filename)s:%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[%(asctime)s] [%(filename)s] %(levelname)s: %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'handlers': {

        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },

        'main_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOGGING_ROOT_DIR, 'MCPL.log'),
            'formatter': 'verbose'
        },

    },
    'loggers': {
        'src': {
            'handlers': ['main_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
