import os
import subprocess
import sys
import platform
import sqlite3

def ensure_package_installed(package_name, logger):
    """Ensures that a package is installed, installs it if missing."""
    try:
        __import__(package_name)
    except ImportError:
        logger.log("INFO", f"Package '{package_name}' is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        logger.log("INFO", f"Package '{package_name}' installed successfully.")

def setup_environment(logger):
    """Sets up the environment by ensuring required packages are installed and configuring firewall rules."""
    # Ensure required packages are installed
    required_packages = ["pyasn1", "pysmi", "snmpclitools", "pysnmp", "pygame", "speedtest-cli", "pyftpdlib","paramiko"]  # Add any other packages you need
    for package in required_packages:
        ensure_package_installed(package, logger)

    # Platform-specific setup
    if platform.system() == "Linux":
        setup_linux_firewall(logger)
    elif platform.system() == "Windows":
        setup_windows_firewall(logger)

    # Ensure the config.ini file and database exist
    ensure_config_file_exists(logger)
    ensure_database_exists(logger)

def ensure_config_file_exists(logger):
    """Ensures that the config.ini file exists with default settings."""
    config_folder = "config"
    config_file_path = os.path.join(config_folder, "config.ini")

    # Create the config folder if it doesn't exist
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
        logger.log("INFO", f"Created config folder at {config_folder}")

    # Create the config.ini file with default settings if it doesn't exist
    if not os.path.isfile(config_file_path):
        with open(config_file_path, 'w') as config_file:
            config_file.write(
                "[DEFAULT]\n"
                "version = 1.1.4\n"
                "hyperlink = https://github.com/wisper1977/Python-NetMon/wiki\n"
                "developer = Chris Collins\n\n"
                "[Network]\n"
                "refreshinterval = 180\n\n"
                "[PING]\n"
                "attempts = 5\n"
                "timeout = 40\n\n"
                "[SNMP]\n"
                "community_string = public\n\n"
                "[Database]\n"
                "path = database/network_monitor.db\n"
            )
        logger.log("INFO", f"Created default config.ini at {config_file_path}")

def ensure_database_exists(logger):
    """Ensures that the SQLite database file exists."""
    database_folder = "database"
    database_file_path = os.path.join(database_folder, "network_monitor.db")

    # Create the database folder if it doesn't exist
    if not os.path.exists(database_folder):
        os.makedirs(database_folder)
        logger.log("INFO", f"Created database folder at {database_folder}")

    # Create an empty database file if it doesn't exist
    if not os.path.isfile(database_file_path):
        open(database_file_path, 'a').close()  # Create an empty file
        logger.log("INFO", f"Created an empty SQLite database file at {database_file_path}")

def setup_linux_firewall(logger):
    """Configures firewall rules for Linux."""
    logger.log("INFO", "Setting up Linux firewall rules...")
    subprocess.run(["sudo", "ufw", "allow", "514/udp"])  # Syslog default port
    logger.log("INFO", "Linux firewall rules set.")

def setup_windows_firewall(logger):
    """Configures firewall rules for Windows."""
    logger.log("INFO", "Setting up Windows firewall rules...")
    subprocess.run([
        "netsh", "advfirewall", "firewall", "add", "rule",
        "name=Allow Syslog", "dir=in", "action=allow", "protocol=UDP", "localport=514"
    ])
    logger.log("INFO", "Windows firewall rules set.")

# Example usage:
# if __name__ == "__main__":
#     logger = YourLoggerClass()  # Replace with your logger implementation
#     setup_environment(logger)