# Network Monitor App
# syslog.py
# version: 1.2
# description: Manages the logging of system events and errors to a database, allowing for retrieval and display in the GUI. Supports logging with both local and Zulu (UTC) time formats.

from modules.db_operations import DatabaseOperations
from datetime import datetime, timezone

class SystemLog:
    def __init__(self, db_path='database/network_monitor.db', use_local_time=True):
        self.db_ops = DatabaseOperations(db_path)  # Initialize DatabaseOperations
        self.use_local_time = use_local_time  # Determine if local or Zulu time should be used

    def log(self, level, message):
        log_message = f"{level}: {message}"
        
        # Get either local time or Zulu (UTC) time based on the configuration
        if self.use_local_time:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + 'L'  # Local time with "L" appended
        else:
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S') + 'Z'  # Zulu time with "Z" appended
        
        self.db_ops.execute_query(
            "INSERT INTO program_logs (log_message, timestamp) VALUES (?, ?)",
            (log_message, timestamp)
        )

    def get_logs(self):
        # Create the connection and fetch logs
        conn = self.db_ops.create_connection()  # Get the connection object
        cursor = conn.cursor()  # Create a cursor from the connection
        
        cursor.execute("SELECT log_message, timestamp FROM program_logs ORDER BY timestamp DESC")
        logs = cursor.fetchall()  # Load logs into memory
        
        # Clean up by closing the cursor and connection
        cursor.close()
        conn.close()
        
        return logs
