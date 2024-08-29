# Version: 1.1.3.1
# Description: Module to write to the log file and clear the log file.

import time, logging
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from shutil import move
from datetime import datetime
from modules.log_manager import LogManager
from modules.config_manager import ConfigManager


class LogWriter:
    def __init__(self):
        """Initialize the LogWriter with a path to the log file."""
        self.logger = LogManager.get_instance()
        self.config = ConfigManager()  # Create an instance of ConfigManager
        log_directory = self.config.get_setting('Log', 'log_directory')  # Get the log directory from the config.ini file
        logfile = self.config.get_setting('Log', 'logfile')  # Get the logfile from the config.ini file
        self.log_file_path = Path(log_directory, logfile)  # Construct the log file path
        self.archive_directory = Path('log') / 'archive'

    def clear_logs(self, log_text_widget):
        """Clears the log file and updates the display."""
        try:
            self.logger.log_info("Attempting to archive logs...")
            self.archive_logs()  # Archive the current log file before clearing
            self.logger.log_info("Logs archived successfully.")

            self.logger.log_info("Attempting to clear log file...")
            with open(self.log_file_path, "w") as file:
                file.truncate()  # Clear the file content
            self.logger.log_info("Log file cleared successfully.")

            self.logger.log_info("Attempting to clear log text widget...")
            log_text_widget.delete(1.0, tk.END)  # Clear the text widget
            self.logger.log_info("Log text widget cleared successfully.")

            self.logger.log_info("Log file cleared by user.")
        except PermissionError:
            self.logger.log_error("Permission denied when trying to clear logs.")
            messagebox.showerror("Error", "Permission denied when trying to clear logs.")
        except FileNotFoundError:
            self.logger.log_error("Log file not found when trying to clear logs.")
            messagebox.showerror("Error", "Log file not found when trying to clear logs.")
        except Exception as e:
            self.logger.log_error("Failed to clear log file: " + str(e))
            messagebox.showerror("Error", "Failed to clear logs: " + str(e))

    def archive_logs(self):
        """Archive the current log file."""
        for i in range(3):  # try 3 times
            try:
                self.archive_directory.mkdir(parents=True, exist_ok=True)  # Ensure the archive directory exists
                if self.log_file_path.exists():
                    # Remove the logger
                    logging.shutdown()

                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    archive_file_path = self.archive_directory / f'log_file_{timestamp}.txt'
                    move(self.log_file_path, archive_file_path)

                    # Use the logger from LogManager
                    self.logger = LogManager.get_instance()

                    self.logger.log_info(f"Archived log file to {archive_file_path} by the system")
                    self.last_archive_time = datetime.now()  # Update the last archive time
                break
            except PermissionError as e:
                if i < 2:  # if it's not the last try
                    time.sleep(1)  # wait for 1 second
                else:  # if it's the last try
                    self.logger.log_error(f"Error archiving log file: {e}")
                    raise  # re-raise the last exception
            except FileNotFoundError as e:
                self.logger.log_error(f"Log file not found when trying to archive: {e}")
                raise e
            except Exception as e:
                self.logger.log_error(f"Error archiving log file: {e}")
                raise e