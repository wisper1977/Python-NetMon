# Network Monitor App
# system_log.py
# version: 1.2
# description: Manages the logging of system events and errors to a database, allowing for retrieval and display in the GUI.

from modules.db_operations import DatabaseOperations

class SystemLog:
    def __init__(self, db_path='database/network_monitor.db'):
        self.db_ops = DatabaseOperations(db_path)  # Initialize DatabaseOperations

    def log(self, level, message):
        log_message = f"{level}: {message}"
        self.db_ops.execute_query(
            "INSERT INTO program_logs (log_message, timestamp) VALUES (?, datetime('now'))",
            (log_message,)
        )

    def get_logs(self):
        conn, cursor = self.db_ops.create_connection()  # Use the method from DatabaseOperations to create connection
        cursor.execute("SELECT log_message, timestamp FROM program_logs ORDER BY timestamp DESC")
        logs = cursor.fetchall()  # Load logs into memory
        cursor.close()
        conn.close()  # Close the connection immediately after fetching logs
        return logs
