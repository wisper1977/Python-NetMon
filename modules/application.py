# Version: 1.1.3.1
# Description: Module to manage the main application window and setup the GUI.

import os, threading, pygame, logging
import tkinter as tk
from pathlib import Path
from logging.handlers import RotatingFileHandler
from modules.device_file_handler import DeviceFileHandler
from modules.device_manager import DeviceManager
from modules.application_gui import ApplicationGUI
from modules.log_manager import LogManager
from modules.network_operations import NetworkOperations

class Application(tk.Frame):
    def __init__(self, master=None, config_manager=None, log_manager=None):
        """Initialize the main application with the root window and setup the GUI."""
        try:
            super().__init__(master)
            self.master = master
            self.master.title("Python NetMon")
            self.master.state('zoomed')
            
            self.config_manager = config_manager
            self.logger = log_manager
            self.setup_logging()
            self.device_manager = DeviceManager(filepath='config/equipment.csv')
            self.gui = ApplicationGUI(master, self)
            self.network_ops = NetworkOperations(config=self.config_manager, update_callback=self.update_callback)
            self.device_file_handler = DeviceFileHandler(filepath='config/equipment.csv')

            self.gui.load_devices()
            self.gui.initiate_refresh_cycle()
        except Exception as e:
            self.logger.log_error("Failed to initialize application: " + str(e))
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
            self.log_manager.log_error(f"Error setting up logging: {e}")
            raise e

    def setup_gui(self):
        """Setup the GUI for the application."""
        try:
            self.create_menu()
            self.create_widgets()
            self.pack(fill='both', expand=True)
        except Exception as e:
            self.logger.log_error("Failed to setup GUI: " + str(e))
            raise e

    def update_callback(self, ip, message):
        """Callback method for network operations updates."""
        try:
            self.update_device_status(ip, message)
        except Exception as e:
            self.logger.log_error("Failed to update device status: " + str(e))
            raise e
        
    def update_device_status(self, ip, status, acknowledge=''):
        def update():
            try:
                for item in self.gui.tree.get_children():
                    device = self.gui.tree.item(item)['values']
                    if len(device) < 7:
                        device.append('False')
                        LogManager.get_instance().log_error("Device list was too short, added missing acknowledgement field: " + str(device))
                    if device[3] == ip:
                        self.gui.update_tree_view(ip, status, device, item)
                        self.gui.play_alert_sound(status, device)
                        self.device_file_handler.update_csv(ip, status)
                        self.gui.update_gui(ip, status)
            except Exception as e:
                LogManager.get_instance().log_error("Failed to update device status: " + str(e))
                return e

        self.master.after(0, update)