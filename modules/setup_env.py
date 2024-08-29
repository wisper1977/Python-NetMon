# Description: Install required packages and firewall rules
# Version: 1.1.4

import subprocess
import sys
import platform

def ensure_package_installed(package_name):
    """Ensures that a package is installed, installs it if missing."""
    try:
        __import__(package_name)
    except ImportError:
        print(f"Package '{package_name}' is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Package '{package_name}' installed successfully.")

def setup_environment():
    """Sets up the environment by ensuring required packages are installed and configuring firewall rules."""
    # Ensure required packages are installed
    required_packages = ["pygame", "speedtest-cli", "speedtest"]  # Add any other packages you need
    for package in required_packages:
        ensure_package_installed(package)

    # Platform-specific setup
    if platform.system() == "Linux":
        setup_linux_firewall()
    elif platform.system() == "Windows":
        setup_windows_firewall()

def setup_linux_firewall():
    """Configures firewall rules for Linux."""
    print("Setting up Linux firewall rules...")
    # Add your Linux firewall setup code here
    # Example:
    subprocess.run(["sudo", "ufw", "allow", "514/udp"])  # Syslog default port
    print("Linux firewall rules set.")

def setup_windows_firewall():
    """Configures firewall rules for Windows."""
    print("Setting up Windows firewall rules...")
    # Add your Windows firewall setup code here
    # Example:
    subprocess.run([
        "netsh", "advfirewall", "firewall", "add", "rule",
        "name=Allow Syslog", "dir=in", "action=allow", "protocol=UDP", "localport=514"
    ])
    print("Windows firewall rules set.")