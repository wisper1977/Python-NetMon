# Network Monitor App
# settings_manager.py
# version: 1.2
# description: Handles the loading and saving of application settings from a configuration file.

import configparser
from tkinter import Toplevel, Label, Entry, Button, messagebox
from modules.system_log import SystemLog

class SettingsManager:
    def __init__(self, config_path='config/config.ini'):
        self.config = configparser.ConfigParser()
        self.config_path = config_path
        self.load_settings()
        self.logger = SystemLog(self.config.get('Database', 'path', fallback='database/network_monitor.db'))

    def load_settings(self):
        """Load settings from the config file."""
        self.config.read(self.config_path)

    def get_snmp_community_string(self):
        return self.config.get('SNMP', 'community_string', fallback='public')
    
    def save_settings(self):
        """Save the current settings to the config file."""
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

    def open_settings_dialog(self, root):
        dialog = Toplevel(root)
        dialog.title("Settings")

        # Network Settings
        Label(dialog, text="Network Refresh Interval (seconds):").grid(row=0, column=0, padx=10, pady=5)
        refresh_interval_entry = Entry(dialog)
        refresh_interval_entry.grid(row=0, column=1, padx=10, pady=5)
        refresh_interval_entry.insert(0, self.config.get('Network', 'refreshinterval', fallback='180'))

        # Ping Settings
        Label(dialog, text="Ping Attempts:").grid(row=1, column=0, padx=10, pady=5)
        ping_attempts_entry = Entry(dialog)
        ping_attempts_entry.grid(row=1, column=1, padx=10, pady=5)
        ping_attempts_entry.insert(0, self.config.get('PING', 'attempts', fallback='5'))

        Label(dialog, text="Ping Timeout (seconds):").grid(row=2, column=0, padx=10, pady=5)
        ping_timeout_entry = Entry(dialog)
        ping_timeout_entry.grid(row=2, column=1, padx=10, pady=5)
        ping_timeout_entry.insert(0, self.config.get('PING', 'timeout', fallback='40'))

        # SNMP Settings
        Label(dialog, text="SNMP Community String:").grid(row=3, column=0, padx=10, pady=5)
        snmp_entry = Entry(dialog)
        snmp_entry.grid(row=3, column=1, padx=10, pady=5)
        snmp_entry.insert(0, self.config.get('SNMP', 'community_string', fallback='public'))

        # Database Settings
        Label(dialog, text="Database Path:").grid(row=4, column=0, padx=10, pady=5)
        db_path_entry = Entry(dialog)
        db_path_entry.grid(row=4, column=1, padx=10, pady=5)
        db_path_entry.insert(0, self.config.get('Database', 'path', fallback='database/network_monitor.db'))

        def save_settings():
            # Save each setting to the config
            self.config.set('Network', 'refreshinterval', refresh_interval_entry.get())
            self.config.set('PING', 'attempts', ping_attempts_entry.get())
            self.config.set('PING', 'timeout', ping_timeout_entry.get())
            self.config.set('SNMP', 'community_string', snmp_entry.get())
            self.config.set('Database', 'path', db_path_entry.get())

            # Save the updated config to the file
            self.save_settings()

            # Log the update
            self.logger.log("INFO", f"Settings updated: Refresh interval: {refresh_interval_entry.get()}, Ping attempts: {ping_attempts_entry.get()}, Ping timeout: {ping_timeout_entry.get()}, SNMP community: {snmp_entry.get()}")

            # Close the dialog
            dialog.destroy()
            messagebox.showinfo("Settings", "Settings saved successfully.")

        Button(dialog, text="Save", command=save_settings).grid(row=5, column=0, columnspan=2, pady=10)