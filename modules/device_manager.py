from modules.db_operations import DatabaseOperations
from modules.system_log import SystemLog

class DeviceManager:
    def __init__(self):
        self.db_ops = DatabaseOperations()
        self.logger = SystemLog()

    def update_status(self, device_id, snmp_status, ping_status, overall_status):
        query = '''
            UPDATE devices SET snmp_status = ?, ping_status = ?, last_status = ?, last_checked = datetime('now')
            WHERE id = ?
        '''
        self.db_ops.execute_query(query, (snmp_status, ping_status, overall_status, device_id))

    def add_device(self, name, ip_address, location, device_type):
        try:
            query = '''
                INSERT INTO devices (name, ip_address, location, type, last_status, last_checked) 
                VALUES (?, ?, ?, ?, 'Unknown', datetime('now'))
            '''
            self.db_ops.execute_query(query, (name, ip_address, location, device_type))
            self.logger.log("INFO", f"Device added: {name} ({ip_address})")
        except Exception as e:
            self.logger.log("ERROR", f"Failed to add device: {name} ({ip_address}) - {str(e)}")
            raise

    def edit_device(self, device_id, new_name, new_ip_address, new_location, new_type):
        try:
            # Retrieve the current values
            query = "SELECT name, ip_address, location, type FROM devices WHERE id = ?"
            current_values = self.db_ops.execute_query(query, (device_id,))
            
            if not current_values:
                raise Exception("Device not found")

            current_values = current_values[0]  # fetchone returns a list of tuples

            changes = []
            if current_values[0] != new_name:
                changes.append(f"Name changed from '{current_values[0]}' to '{new_name}'")
            if current_values[1] != new_ip_address:
                changes.append(f"IP Address changed from '{current_values[1]}' to '{new_ip_address}'")
            if current_values[2] != new_location:
                changes.append(f"Location changed from '{current_values[2]}' to '{new_location}'")
            if current_values[3] != new_type:
                changes.append(f"Type changed from '{current_values[3]}' to '{new_type}'")

            # Update the device
            query = '''
                UPDATE devices SET name = ?, ip_address = ?, location = ?, type = ? WHERE id = ?
            '''
            self.db_ops.execute_query(query, (new_name, new_ip_address, new_location, new_type, device_id))

            # Log the changes
            if changes:
                change_summary = "; ".join(changes)
                self.logger.log("INFO", f"Device ID {device_id} edited: {change_summary}")
            else:
                self.logger.log("INFO", f"Device ID {device_id} edited with no changes")

        except Exception as e:
            self.logger.log("ERROR", f"Failed to edit device: ID {device_id} - {str(e)}")
            raise

    def delete_device(self, device_id):
        try:
            query = "DELETE FROM devices WHERE id = ?"
            self.db_ops.execute_query(query, (device_id,))
            self.logger.log("INFO", f"Device deleted: ID {device_id}")
        except Exception as e:
            self.logger.log("ERROR", f"Failed to delete device: ID {device_id} - {str(e)}")
            raise

    def get_device(self, device_id):
        # Retrieve a single device's details
        query = "SELECT * FROM devices WHERE id = ?"
        result = self.db_ops.execute_query(query, (device_id,))
        return result[0] if result else None

    def get_all_devices(self):
        query = '''
            SELECT id, name, ip_address, location, type, snmp_status, ping_status, last_status 
            FROM devices
        '''
        result = self.db_ops.execute_query(query)
        return result if result else []