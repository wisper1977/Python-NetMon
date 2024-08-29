# Version: 1.1.3.1
# Description: Module to manage devices and their details.

import csv
from modules.device_file_handler import DeviceFileHandler
from modules.log_manager import LogManager

class DeviceManager:
    def __init__(self, filepath='config/equipment.csv'):
        """Initialize the DeviceManager with a DeviceFileHandler and LogManager."""
        try:
            self.filepath = filepath  # store filepath as an instance variable
            self.file_handler = DeviceFileHandler(filepath)
            self.logger = LogManager.get_instance()
            self.devices = self.load_devices_from_file()
        except Exception as e:
            self.logger.log_error(f"Failed to initialize DeviceManager: {e}")
            raise e

    def load_devices_from_file(self):
        """Load the devices from the device file."""
        try:
            return self.file_handler.read_devices()
        except Exception as e:
            self.logger.log_error(f"Failed to load devices: {e}")
            return []

    def save_device(self, device):
        """Save a new device to the device file."""
        try:
            devices = self.load_devices_from_file()
            # Ensure uniqueness of keys
            new_key = self.generate_new_key(devices)
            device['Key'] = str(new_key)
            devices.append(device)
            self.file_handler.write_devices(devices)
        except Exception as e:
            self.logger.log_error(f"Failed to save device: {e}")

    def delete_device(self, device_key):
        """Delete a device with the given key from the device file."""
        try:
            devices = self.load_devices_from_file()
            original_count = len(devices)
            devices = [device for device in devices if device['Key'] != str(device_key)]
            if len(devices) == original_count:
                self.logger.log_warning(f"No device found with Key: {device_key} to delete.")
            else:
                self.logger.log_info(f"Device with Key: {device_key} deleted.")
                self.file_handler.write_devices(devices)
                self.load_devices_from_file()  # Reload devices after deleting
        except Exception as e:
            self.logger.log_error(f"Failed to delete device: {e}")
            raise e

    def add_device(self, new_device):
        """Add a new device and save it to the device file."""
        try:
            new_key = self.generate_new_key()
            new_device['Key'] = str(new_key)
            self.save_device(new_device)
            self.load_devices_from_file()  # Reload devices after adding
        except Exception as e:
            self.logger.log_error(f"Failed to add device: {e}")
            raise e
    
    def edit_device(self, device_key, new_details):
        """Edit an existing device and save the changes to the device file."""
        try:
            devices = self.load_devices_from_file()
            for device in devices:
                if device['Key'] == device_key:
                    # If the IP has changed, update the device with the new details
                    if new_details['IP'] != device['IP']:
                        device.update(new_details)
                    else:
                        # If the IP has not changed, update the device without changing the status
                        new_details['Status'] = device['Status']
                        device.update(new_details)
                    self.file_handler.write_devices(devices)
                    self.lload_devices_from_file()  # Reload devices after editing
                    break
            else:
                self.logger.log_warning(f"No device found with Key: {device_key} to edit.")
        except Exception as e:
            self.logger.log_error(f"Failed to edit device: {e}")
            raise e

    def update_device(self, device_key, new_details):
        """Update the details of a device with the given key."""
        try:
            devices = self.load_devices_from_file()
            for device in devices:
                if device['Key'] == str(device_key):
                    device.update(new_details)
            self.file_handler.write_devices(devices)
        except Exception as e:
            self.logger.log_error(f"Failed to update device: {e}")

    def update_acknowledge_status(self, device_key, status):
        """Update the acknowledge status of a device."""
        try:
            # Read the CSV file into a list of rows
            with open(self.filepath, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)

            # Find the row with the device key and update the status
            for row in data:
                if row[0] == device_key:  # assuming the device key is in the 1st column
                    row[6] = status  # assuming the acknowledge status is in the 7th column
                    self.logger.log_info(f"Device with Key {device_key} acknowledged.")
                    break  # exit the loop once the device key is found

            # Write the updated data back to the CSV file
            with open(self.filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
                self.logger.log_info(f"Acknowledge status updated for device with Key: {device_key} in CSV file.")

            self.logger.log_info(f"Acknowledge status updated for device with Key: {device_key}")
        except Exception as e:
            self.logger.log_error(f"Failed to update acknowledge status: {e}")
            return e

    def generate_new_key(self, devices=None):
        """Generate a new unique key for a device based on existing keys."""
        try:
            max_key = max((int(device['Key']) for device in devices), default=0)
            return max_key + 1
        except Exception as e:
            self.logger.log_error(f"Failed to generate new key: {e}")
            return 1  # Default to 1 if key generation fails
