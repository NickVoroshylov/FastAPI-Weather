import os
from logging.config import dictConfig

from app.core.config import LOGGING_DIR, LOGGING_FILE_PATH


def setup_logging():
    if not os.path.exists(LOGGING_DIR):
        os.makedirs(LOGGING_DIR)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": LOGGING_FILE_PATH,
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
    }
    dictConfig(logging_config)
