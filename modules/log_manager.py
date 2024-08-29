# Version: 1.1.3.1
# Description: This module contains the LogManager class which is a singleton class that provides logging functionality for the application.

from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from modules.config_manager import ConfigManager

class LogManager:
    _instance = None

    @classmethod
    def get_instance(cls, config_manager=None):
        """Get the singleton instance of LogManager."""
        if cls._instance is None:
            if config_manager is None:
                raise ValueError("config_manager cannot be None when creating the first LogManager instance")
            cls._instance = cls(config_manager)
        return cls._instance

    def __init__(self, config_manager):
        """Initialize the LogManager class."""
        if config_manager is None:
            raise ValueError("config_manager cannot be None")
        self.config_manager = config_manager
        try:
            self.setup_logging()
        except Exception as e:
            logging.error(f"Error setting up logging: {e}")
            raise e

    def setup_logging(self):
        """Setup logging configuration for the application."""
        try:
            log_directory = Path(self.config_manager.get_setting('Logging', 'log_directory', 'log'))
            log_directory.mkdir(exist_ok=True)
            log_file = self.config_manager.get_setting('Logging', 'log_file', 'log_file.txt')
            log_file_path = log_directory / log_file
            archive_directory = Path(self.config_manager.get_setting('Logging', 'archive_directory', 'log/archive'))
            archive_directory.mkdir(parents=True, exist_ok=True)
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5),
                    logging.StreamHandler()
                ]
            )
        except Exception as e:
            logging.error(f"Error setting up logging: {e}")
            raise e
        
    def log_info(self, message):
        """Log an info message."""
        try:
            logging.info(message)
        except Exception as e:
            logging.error(f"Error logging info message: {e}")
            raise e

    def log_debug(self, message):
        """Log a debug message."""
        try:
            logging.debug(message)
        except Exception as e:
            logging.error(f"Error logging debug message: {e}")
            raise e

    def log_warning(self, message):
        """Log a warning message."""
        try:
            logging.warning(message)
        except Exception as e:
            logging.error(f"Error logging warning message: {e}")
            raise e

    def log_error(self, message):
        """Log an error message and raise an exception."""
        try:
            logging.error(message)
        except Exception as e:
            logging.error(f"Error logging error message: {e}")
            raise e

    def log_critical(self, message):
        """Log a critical message and raise an exception."""
        try:
            logging.critical(message)
        except Exception as e:
            logging.error(f"Error logging critical message: {e}")
            raise e