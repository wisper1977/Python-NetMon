# Network Monitor App
# netmon.py
# version: 1.2
# description: Entry point for the Network Monitor application. Initializes and runs the main application loop.
#
# Features:
# - Loads configuration settings from 'config/config.ini', including database paths and network settings.
# - Initializes database operations, system logging, and network monitoring services (ping, SNMP).
# - Sets up the main graphical user interface (GUI) to interact with the user.
# - Logs application events such as startup, shutdown, and key operations to the system log.
#
# Configuration:
# - Requires a configuration file located at 'config/config.ini' with database path, SNMP, and ping settings.
# - Uses a SQLite database for storing device statuses, logs, and network monitoring data.
#
# Requirements:
# - tkinter: For the main application GUI.
# - sqlite3: For database operations.
# - configparser: For reading configuration files.
# - Custom modules:
#     - setup_env: Initializes the environment and prepares logging.
#     - db_operations: Handles SQLite database operations.
#     - application_gui: Manages the GUI components.
#     - system_log: Logs events and errors in the system.
#     - net_ops_ping: Executes ping operations for network monitoring.
#     - net_ops_snmp: Handles SNMP queries for network devices.
#     - settings_manager: Manages application settings.
#     - gui_utils: Utility functions for the GUI.
#
# Usage:
# - The script is the main entry point for the Network Monitor application.
# - Simply run this script to launch the full application with its network monitoring and GUI components.


import configparser
import os
import tkinter as tk
from modules.setup_env import setup_environment  # Import the setup script
from modules.db_operations import DatabaseOperations  # Import the DatabaseOperations class
from modules.application_gui import ApplicationGUI   # Import the ApplicationGUI class
from modules.system_log import SystemLog  # Import the SystemLog class
from modules.net_ops_ping import NetOpsPing  # Import the NetOpsPing class
from modules.net_ops_snmp import NetOpsSNMP  # Import the NetOpsSNMP class
from modules.settings_manager import SettingsManager  # Import SettingsManager class
from modules.gui_utils import GUIUtils  # Import GUIUtils class

class NetworkMonitorApp:
    def __init__(self, root):
        self.root = root
        self.config_path = 'config/config.ini'
        self.config = self.load_config()

        try:
            # Load the database path from the configuration
            db_path = self.config['Database']['path']
        except KeyError as e:
            raise KeyError(f"Missing key in configuration file: {e}")

        # Ensure the database path exists
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database path does not exist: {db_path}")

        # Initialize DatabaseOperations with the correct path
        self.db_ops = DatabaseOperations(db_path=db_path)

        # Initialize SystemLog with the correct path
        self.logger = SystemLog(db_path)

        # Initialize SettingsManager
        self.settings_manager = SettingsManager(self.config_path)

        # Initialize Network Operations
        self.ping = NetOpsPing(attempts=self.settings_manager.config.getint('PING', 'attempts'),
                               timeout=self.settings_manager.config.getint('PING', 'timeout'))
        self.snmp = NetOpsSNMP(community_string=self.settings_manager.config.get('SNMP', 'community_string'))

        setup_environment(self.logger)  # Run setup with logging
        self.logger.log("INFO", "Application started")

        # Initialize the GUI and pass db_ops
        self.gui = ApplicationGUI(self.root, self, self.db_ops)

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)

        if 'Database' not in config or 'path' not in config['Database']:
            raise KeyError("The 'Database' section or 'path' key is missing in the config file.")

        return config

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.root.mainloop()

    def on_exit(self):
        self.logger.log("INFO", "Application exited")
        GUIUtils.on_exit(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitorApp(root)
    app.run()
