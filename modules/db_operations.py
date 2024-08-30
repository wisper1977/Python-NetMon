import sqlite3
import threading

class DatabaseOperations:
    def __init__(self, db_path='database/network_monitor.db'):
        self.db_path = db_path
        self.lock = threading.Lock()  # Create a lock for serializing database access
        self.create_tables()

    def create_connection(self):
        """Create a new database connection for the current thread."""
        conn = sqlite3.connect(self.db_path, timeout=10)  # Use a timeout to wait for locks to clear
        conn.execute('PRAGMA journal_mode=WAL;')  # Enable WAL mode
        return conn, conn.cursor()

    def execute_query(self, query, params=None):
        with self.lock:  # Lock access to the database
            conn, cursor = self.create_connection()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # If it's a SELECT query, return the fetched results
                if query.strip().upper().startswith("SELECT"):
                    result = cursor.fetchall()
                    return result

                conn.commit()
            except sqlite3.DatabaseError as e:
                conn.rollback()  # Rollback on error
                raise e
            finally:
                cursor.close()
                conn.close()

    def create_tables(self):
        """Create tables if they don't exist."""
        conn, cursor = self.create_connection()
        
        # Create the devices table with Location and Type fields
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                ip_address TEXT UNIQUE,
                location TEXT,
                type TEXT,
                last_status TEXT,
                last_checked TIMESTAMP,
                snmp_status TEXT,
                ping_status TEXT
            )
        ''')

        # Create the status_log table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS status_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                status TEXT,
                method TEXT,
                timestamp TIMESTAMP,
                FOREIGN KEY(device_id) REFERENCES devices(id)
            )
        ''')

        # Create the program_logs table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS program_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_message TEXT,
                timestamp TIMESTAMP
            )
        ''')

        conn.commit()
        cursor.close()
        conn.close()

    def get_all_devices(self):
        with self.lock:
            conn, cursor = self.create_connection()
            cursor.execute("SELECT id, name, ip_address, location, type, snmp_status, ping_status, last_status FROM devices")
            devices = cursor.fetchall()
            cursor.close()
            conn.close()
            return devices

    def update_status(self, device_id, snmp_status, ping_status, overall_status):
        """Update the status of a device."""
        query = '''
            UPDATE devices SET snmp_status = ?, ping_status = ?, last_status = ?, last_checked = datetime('now')
            WHERE id = ?
        '''
        self.execute_query(query, (snmp_status, ping_status, overall_status, device_id))

    def log_event(self, message):
        """Log an event to the program_logs table."""
        self.execute_query("INSERT INTO program_logs (log_message, timestamp) VALUES (?, datetime('now'))", (message,))