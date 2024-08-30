import tkinter as tk
from modules.setup_env import setup_environment  # Import the setup script
from modules.db_operations import DatabaseOperations
from modules.application_gui import ApplicationGUI
from modules.system_log import SystemLog
import configparser

class NetworkMonitorApp:
    def __init__(self, root):
        self.root = root
        self.config_path = 'config/config.ini'
        self.config = self.load_config()
        self.db_ops = DatabaseOperations()
        self.logger = SystemLog(self.config['Database']['path'])
        setup_environment(self.logger)  # Run setup with logging
        self.logger.log("INFO", "Application started")
        self.gui = ApplicationGUI(self.root, self)

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        return config

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.root.mainloop()

    def on_exit(self):
        self.logger.log("INFO", "Application exited")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitorApp(root)
    app.run()