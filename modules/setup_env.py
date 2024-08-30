import subprocess
import sys
import platform

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
    required_packages = ["pysnmp","pygame","speedtest"]  # Add any other packages you need
    for package in required_packages:
        ensure_package_installed(package, logger)

    # Platform-specific setup
    if platform.system() == "Linux":
        setup_linux_firewall(logger)
    elif platform.system() == "Windows":
        setup_windows_firewall(logger)

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