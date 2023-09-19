import logging, sys

class Config:
    API_PATH_PREFIX = '/api'
    MODEL_VERSION = 'v1'

class LessThanFilter(logging.Filter):
    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        #non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0

class config_Logger:
    def __init__(self, logger):
        self.logger = logger
    def config_level(self):
        self.logger.setLevel(logging.DEBUG)
        # Create handlers for stdout (INFO, NOTICE, DEBUG) and stderr (WARNING, ERROR, CRITICAL)
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        stderr_handler = logging.StreamHandler(stream=sys.stderr)
        # Set the log level for each handler
        stderr_handler.setLevel(logging.WARNING)  # Log WARNING and above to stderr
        stdout_handler.setLevel(logging.DEBUG)  # Log INFO and above to stdout
        stdout_handler.addFilter(LessThanFilter(logging.WARNING))
        # Define log formats (you can customize these as needed)
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stdout_handler.setFormatter(log_format)
        stderr_handler.setFormatter(log_format)
        # Add the handlers to the logger based on log levels
        self.logger.handlers.clear()
        self.logger.addHandler(stderr_handler)  # WARNING, ERROR, CRITICAL will go to stderr
        self.logger.addHandler(stdout_handler)  # INFO, NOTICE, DEBUG will go to stdout
        return self.logger