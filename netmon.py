# Network Monitor App
# netmon.py
# version: 1.2
# description: Entry point for the Network Monitor application. Initializes and runs the main application loop.

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
