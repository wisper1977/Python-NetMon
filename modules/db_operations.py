import sqlite3
import threading
import csv

class DatabaseOperations:
    def __init__(self, db_path='database/network_monitor.db'):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.create_tables()
        self.ensure_google_device()

    def create_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.execute('PRAGMA journal_mode=WAL;')
        return conn, conn.cursor()

    def execute_query(self, query, params=None):
        with self.lock:
            conn, cursor = self.create_connection()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if query.strip().upper().startswith("SELECT"):
                    result = cursor.fetchall()
                    return result

                conn.commit()
            except sqlite3.DatabaseError as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()

    def create_tables(self):
        conn, cursor = self.create_connection()
        
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

    def ensure_google_device(self):
        # Check if the devices table is empty
        query = "SELECT COUNT(*) FROM devices"
        result = self.execute_query(query)
        if result[0][0] == 0:  # If the count is 0, the table is empty
            # Insert the Google device
            self.execute_query(
                "INSERT INTO devices (name, ip_address, location, type) VALUES (?, ?, ?, ?)",
                ('Google', '8.8.8.8', 'Internet', 'DNS')
            )

    def get_all_devices(self):
        query = "SELECT * FROM devices"
        return self.execute_query(query)

    def update_status(self, device_id, snmp_status, ping_status, overall_status):
        query = '''
            UPDATE devices SET snmp_status = ?, ping_status = ?, last_status = ?, last_checked = datetime('now')
            WHERE id = ?
        '''
        self.execute_query(query, (snmp_status, ping_status, overall_status, device_id))

    def log_event(self, message):
        query = "INSERT INTO program_logs (log_message, timestamp) VALUES (?, datetime('now'))"
        self.execute_query(query, (message,))

    def import_devices(self, file_path):
        """Imports devices from a CSV file."""
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row.get('Name')
                ip_address = row.get('IP Address')
                location = row.get('Location')
                device_type = row.get('Type')

                if name and ip_address:
                    try:
                        self.execute_query('''
                            INSERT INTO devices (name, ip_address, location, type) VALUES (?, ?, ?, ?)
                        ''', (name, ip_address, location, device_type))
                    except sqlite3.IntegrityError as e:
                        print(f"Failed to import device {name} ({ip_address}): {e}")
                        continue