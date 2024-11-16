import logging
from functools import partial
import sys

from app.core.config import Settings


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def _instantiate_project_logger(logger: logging.Logger, log_level: int, log_format):
    logger.setLevel(log_level)
    
    # Avoid duplicate handlers
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        # Create handlers for logging to the standard output
        stdoutHandler = logging.StreamHandler(stream=sys.stdout)
        stdoutHandler.setLevel(log_level)
        stdoutHandler.setFormatter(CustomFormatter(log_format)) # Set the log format

        # Add handler to the Logger object
        logger.addHandler(stdoutHandler)

    logger.error = partial(logger.error, exc_info=True)


def setup_logging(settings: Settings):
    log_level = logging.DEBUG if settings.debug else logging.INFO
    log_format = "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
    
    # # Configure the root logger - Causing duplicate logs
    # logging.basicConfig(
    #     stream=sys.stdout,
    #     level=log_level,
    #     format=log_format,
    # )

    # Configure the project-specific logger
    project_logger = logging.getLogger(settings.project_name)
    _instantiate_project_logger(
        logger=project_logger,
        log_level=log_level,
        log_format=log_format,
    )

    return project_logger