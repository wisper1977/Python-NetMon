# Version: 1.1.3.1
# Description: Module to read the contents of a log file.

from pathlib import Path
from modules.log_manager import LogManager
from modules.config_manager import ConfigManager

class LogReader:
    def __init__(self):
        """Initialize the LogReader with a path to the log file."""
        self.logger = LogManager.get_instance()
        self.config = ConfigManager()  # Create an instance of ConfigManager
        log_directory = self.config.get_setting('Log', 'log_directory')  # Get the log directory from the config.ini file
        logfile = self.config.get_setting('Log', 'logfile')  # Get the logfile from the config.ini file
        self.log_file_path = Path(log_directory, logfile)  # Construct the log file path

    def read_log_file(self):
        """Read the log file and return its content."""
        try:
            with open(self.log_file_path, "r") as file:
                return file.readlines()
        except FileNotFoundError:
            self.logger.log_error("Log file not found when trying to read log file.")
            return []
        except PermissionError:
            self.logger.log_error("Permission denied when trying to read log file.")
            return []
        except Exception as e:
            self.logger.log_error("Failed to read log file: " + str(e))
            return []