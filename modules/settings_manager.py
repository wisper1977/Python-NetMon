# Version: 1.1.3.1
# Description: Module to manage the settings dialog for the application.

import tkinter as tk
from tkinter import simpledialog, Label, Entry, messagebox, Frame, X, W
from modules.log_manager import LogManager   

class SettingsManager(simpledialog.Dialog):
    def __init__(self, master, config_manager):
        """SettingsManager constructor to initialize the dialog window."""
        self.logger = LogManager.get_instance()
        try:
            self.config_manager = config_manager
            self.num_attempts = int(self.config_manager.get_setting('PING', 'attempts', '5'))
            self.timeout_duration = int(self.config_manager.get_setting('PING', 'timeout', '15'))
            super().__init__(master, title="Ping Settings")
            self.logger.log_info("SettingsManager initialized successfully")
        except Exception as e:
            self.logger.log_error("Failed to initialize SettingsManager: " + str(e))
            raise e

    def body(self, master):
        """Build the body of the dialog with input fields for settings."""
        try:
            network_frame = tk.Frame(master)
            network_frame.pack(fill=tk.X, padx=5, pady=5)

            tk.Label(network_frame, text="Network Settings", font=("Arial", 12), anchor=tk.W).pack(fill=tk.X)
            self.refreshinterval_var = tk.StringVar(value=self.config_manager.get_setting('Network', 'refreshinterval'))
            tk.Label(network_frame, text="Refresh Interval:").pack(anchor=tk.W)
            tk.Entry(network_frame, textvariable=self.refreshinterval_var).pack(fill=tk.X)

            ping_frame = tk.Frame(master)
            ping_frame.pack(fill=tk.X, padx=5, pady=5)

            tk.Label(ping_frame, text="Ping Settings", font=("Arial", 12), anchor=tk.W).pack(fill=tk.X)
            self.attempts_var = tk.StringVar(value=self.config_manager.get_setting('PING', 'attempts'))
            tk.Label(ping_frame, text="Attempts:").pack(anchor=tk.W)
            tk.Entry(ping_frame, textvariable=self.attempts_var).pack(fill=tk.X)

            self.timeout_var = tk.StringVar(value=self.config_manager.get_setting('PING', 'timeout'))
            tk.Label(ping_frame, text="Timeout:").pack(anchor=tk.W)
            tk.Entry(ping_frame, textvariable=self.timeout_var).pack(fill=tk.X)

            return network_frame
        except Exception as e:
            self.logger.log_error("Failed to build dialog body: " + str(e))
            raise e

    def apply(self):
        """Apply the changes made in the dialog to the configuration file."""
        try:
            attempts = int(self.attempts_var.get())
            timeout = int(self.timeout_var.get())
            refreshinterval = int(self.refreshinterval_var.get())
            if attempts > 10:
                messagebox.showerror("Invalid Input", "Number of attempts cannot exceed 10.")
                self.logger.log_error("Number of attempts cannot exceed 10.")
                return
            # Save settings using the new method
            self.config_manager.save_settings('PING', 'attempts', str(attempts))
            self.config_manager.save_settings('PING', 'timeout', str(timeout))
            self.config_manager.save_settings('Network', 'refreshinterval', refreshinterval)
            self.logger.log_info("Ping and Network settings updated from settings dialog.")
        except Exception as e:
            self.logger.log_error("Failed to apply changes in SettingsManager: " + str(e))
            raise e