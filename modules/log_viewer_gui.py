# Version: 1.1.3.1
# Description: Module to write logs to a log file.

import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from datetime import datetime, timedelta
from pathlib import Path
from modules.log_manager import LogManager
from modules.log_reader import LogReader
from modules.log_writer import LogWriter
from modules.config_manager import ConfigManager

class LogViewerGUI:
    def __init__(self, master, app):
        self.logger = LogManager.get_instance() # Get the singleton instance of LogManager
        self.master = master # Reference to the main application window
        self.app = app # Reference to the main application class to access business logic
        self.config = ConfigManager()  # Create an instance of ConfigManager
        log_directory = self.config.get_setting('Log', 'log_directory')  # Get the log directory from the config.ini file
        logfile = self.config.get_setting('Log', 'logfile')  # Get the logfile from the config.ini file
        self.log_file_path = Path(log_directory, logfile)  # Construct the log file path
        self.log_reader = LogReader()
        self.log_writer = LogWriter()
        self.last_archive_time = datetime.now()  # Initialize the last archive time
     
    def update_log_display(self):
        """Update the log content in the log viewer."""
        try:
            with open(self.log_file_path, 'r') as log_file:
                log_content = log_file.readlines()

            # Filter the logs by the selected log level
            log_level = self.log_level.get()
            if log_level != "ALL":
                log_content = [line for line in log_content if log_level in line]

            self.log_text.delete('1.0', tk.END)  # Clear the current log content
            self.log_text.insert(tk.END, ''.join(log_content))  # Insert the new log content
        except FileNotFoundError:
            self.logger.log_error("Log file not found, creating a new one.")
            with open('log_file.txt', "w") as file:
                pass
        except PermissionError:
            self.logger.log_error("Permission denied when trying to update log display.")
            messagebox.showerror("Error", "Permission denied when trying to update log display.")
        except Exception as e:
            self.logger.log_error("Failed to update log display: " + str(e))
            messagebox.showerror("Error", "Failed to update log display: " + str(e))
             
    def open_log_viewer(self):
        """Open a new window to display logs."""
        try:
            log_window = tk.Toplevel(self.master)
            log_window.attributes('-topmost', True)  # Keep the window on top
            log_window.title("Log Viewer")  # Set the title of the log window

            # Create a menu bar
            menubar = tk.Menu(log_window)
            log_window.config(menu=menubar)

            # Create a log menu and add it to the menu bar
            log_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Logs", menu=log_menu)

            # Add "Refresh Logs" and "Clear Logs" options to the log menu
            log_menu.add_command(label="Refresh Logs", command=self.update_log_display)
            log_menu.add_command(label="Clear Logs", command=lambda: self.clear_log_confirmation(self.log_text))

            # Create a dropdown menu to select the log level
            self.log_level = tk.StringVar(log_window)
            self.log_level.set("ALL")  # default value
            log_level_options = ["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            log_level_dropdown = tk.OptionMenu(log_window, self.log_level, *log_level_options, command=lambda _: self.update_log_display())
            log_level_dropdown.pack()

            # Create a ScrolledText widget for log display in the new window
            self.log_text = scrolledtext.ScrolledText(log_window, height=20, width=80)
            self.log_text.pack(padx=10, pady=10, fill='both', expand=True)

            self.update_log_display()  # Initialize with log content
            self.auto_refresh_log_display()  # Start auto-refresh
        except FileNotFoundError:
            self.logger.log_error("Log file not found when trying to open log viewer.")
            messagebox.showerror("Error", "Log file not found when trying to open log viewer.")
            return
        except PermissionError:
            self.logger.log_error("Permission denied when trying to open log viewer.")
            messagebox.showerror("Error", "Permission denied when trying to open log viewer.")
            return
        except Exception as e:
            self.logger.log_error("Failed to open log viewer: " + str(e))
            messagebox.showerror("Error", "Failed to open log viewer: " + str(e))
            return
        
    def clear_log_confirmation(self, log_text_widget):
        """Ask for confirmation before clearing logs."""
        try:
            if messagebox.askyesno("Clear Logs", "Are you sure you want to clear all logs?"):
                self.log_writer.clear_logs(log_text_widget)
        except PermissionError:
            self.logger.log_error("Permission denied when trying to clear logs.")
            messagebox.showerror("Error", "Permission denied when trying to clear logs.")
        except FileNotFoundError:
            self.logger.log_error("Log file not found when trying to clear logs.")
            messagebox.showerror("Error", "Log file not found when trying to clear logs.")
        except Exception as e:
            self.logger.log_error("Failed to clear logs: " + str(e))
            raise e
                
    def auto_refresh_log_display(self):
        """Auto refresh the log content."""
        try:
            self.update_log_display()
            self.log_text.after(120000, self.auto_refresh_log_display)
            print("Current time: ", datetime.now())
            print("Last archive time: ", self.last_archive_time)
            print("Time delta: ", timedelta(hours=24))
            if datetime.now() - self.last_archive_time >= timedelta(hours=24):  # If it's been 24 hours since the last archive
                self.archive_logs()  # Archive the current log file
            self.logger.log_info("Log display auto-refreshed.")
        except PermissionError:
            self.logger.log_error("Permission denied when trying to auto refresh log display.")
            messagebox.showerror("Error", "Permission denied when trying to auto refresh log display.")
        except FileNotFoundError:
            self.logger.log_error("Log file not found when trying to auto refresh log display.")
            messagebox.showerror("Error", "Log file not found when trying to auto refresh log display.")
        except Exception as e:
            self.logger.log_error("Failed to auto refresh log display: " + str(e))
            raise e