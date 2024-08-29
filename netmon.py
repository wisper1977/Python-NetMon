# Description: Main entry point for the application.
# Version: 1.1.4

# Import required libraries
import tkinter as tk
from modules.log_manager import LogManager
from modules.application import Application
from modules.config_manager import ConfigManager
from modules.syslog_server import SyslogServer
from modules.setup_env import setup_environment  # Import the setup_environment function

if __name__ == "__main__":
    """Main entry point for the application."""

    # Step 1: Set up the environment
    setup_environment()  # Ensures required packages are installed and firewall rules are set

    # Step 2: Initialize the configuration manager
    config_manager = ConfigManager()  # Create ConfigManager instance first

    # Step 3: Initialize the log manager
    log_manager = LogManager.get_instance(config_manager)  # Pass ConfigManager instance here
    config_manager.set_logger(log_manager)  # Set LogManager instance in ConfigManager
    log_manager.log_info("Application started")

    # Step 4: Start the Syslog Server
    syslog_server = SyslogServer()
    syslog_server.run_in_background()

    # Step 5: Start the GUI Application
    root = tk.Tk()
    app = Application(master=root, config_manager=config_manager, log_manager=log_manager)
    app.mainloop()

    # Step 6: Log the application ending
    log_manager.log_info("Application ended")
