# Version: 1.1.3.1
# Description: Module to handle device file operations.

import csv, os
from pathlib import Path
from modules.log_manager import LogManager

class DeviceFileHandler:
    def __init__(self, filepath):
        """Initialize the DeviceFileHandler with a filepath and LogManager instance."""
        try:
            self.filepath = Path(filepath)
            self.logger = LogManager.get_instance()
            self.initialize_device_file()
        except Exception as e:
            self.logger.log_error(f"Failed to initialize DeviceFileHandler: {e}")
            raise e

    def initialize_device_file(self):
        """Initialize the device file with a header if it doesn't exist."""
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            if not self.filepath.exists():
                with open(self.filepath, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=["Key", "Location", "Name", "IP", "Type", "Status", "Acknowledge"])
                    writer.writeheader()
                self.logger.log_info("Device file created with header.")
            else:
                # Check file integrity upon initialization
                if not self.check_file_integrity():
                    # Log and raise an exception if file integrity check fails
                    self.logger.log_warning("Device file integrity check failed upon initialization.")
                    raise IOError("Device file integrity check failed.")
        except IOError as e:
            self.logger.log_error(f"Failed to create or access device file: {e}")
            raise e

    def check_file_integrity(self):
        """Check if the device file has the required fields in the header."""
        try:
            with open(self.filepath, mode='r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader)
                required_fields = ["Key", "Location", "Name", "IP", "Type", "Status"]
                # Check if header contains all required fields
                if not all(field in header for field in required_fields):
                    return False
            return True
        except Exception as e:
            self.logger.log_error(f"Error while checking device file integrity: {e}")
            return False

    def read_devices(self):
        """Read the devices from the device file and return as a list of dictionaries."""
        try:
            with open(self.filepath, mode='r', newline='') as file:
                return list(csv.DictReader(file))
        except IOError as e:
            self.logger.log_error(f"Failed to read device file: {e}")
            raise e

    def write_devices(self, devices):
        """Write the list of devices to the device file."""
        try:
            with open(self.filepath, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["Key", "Location", "Name", "IP", "Type", "Status", "Acknowledge"])
                writer.writeheader()
                writer.writerows(devices)
            self.logger.log_debug("Device file updated successfully.")
        except IOError as e:
            self.logger.log_error(f"Failed to write to device file: {e}")
            raise

    def update_csv(self, ip, status):
        data = []
        with open(os.path.join('config', 'equipment.csv'), 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 7:
                    row.append('False')
                    LogManager.get_instance().log_error("Row list was too short, added missing acknowledgement field: " + str(row))
                if row[3] == ip:
                    row[5] = status
                    if status.startswith('Online') and row[6] == 'False':
                        self.logger.log_info(f"Device with IP {ip} status reset to 'Online'")
                    elif status.startswith('Offline') and row[6] == 'True':
                        self.logger.log_info(f"Device with IP {ip} status set to 'Offline' and Acknowledge set to 'True'")
                data.append(row)
        with open(os.path.join('config', 'equipment.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)