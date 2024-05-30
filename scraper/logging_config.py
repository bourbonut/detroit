import logging
import logging.config

GREY = "\x1b[38;20m"
YELLOW = "\x1b[33;20m"
RED = "\x1b[31;20m"
BOLD_RED = "\x1b[31;1m"
RESET = "\x1b[0m"
FORMAT = (
    "%(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
)

class ColoredFormatter(logging.Formatter):

    FORMATS = {
        logging.DEBUG: GREY + FORMAT + RESET,
        logging.INFO: GREY + FORMAT + RESET,
        logging.WARNING: YELLOW + FORMAT + RESET,
        logging.ERROR: RED + FORMAT + RESET,
        logging.CRITICAL: BOLD_RED + FORMAT + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {"class": "scrapper.logging_config.ColoredFormatter"},
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "colored",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["default"],
    },
}

def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
