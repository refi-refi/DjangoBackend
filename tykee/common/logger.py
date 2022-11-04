import logging
from datetime import date
from os import makedirs, path

from tykee import Config


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[38;21m"
    green = "\x1b[38;5;35m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.formats = {
            logging.DEBUG: self.green + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


log_level = Config.LOGGER_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Define LOG_FORMAT for logs
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(module)s - %(funcName)s | %(message)s"

# Create stdout handler for logging to the console (logs all five levels)
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(log_level)
stdout_handler.setFormatter(CustomFormatter(LOG_FORMAT))

# Create file handler for logging to a file (logs all five levels)
makedirs(Config.LOG_DIR, exist_ok=True)
today = date.today()
file_handler = logging.FileHandler(
    path.join(Config.LOG_DIR, f"logs_{today.strftime('%Y_%m_%d')}.log")
)
file_handler.setLevel("DEBUG")
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Add both handlers to the logger
logger.addHandler(stdout_handler)
logger.addHandler(file_handler)
