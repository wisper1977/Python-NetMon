#Syslog Server Plugin
#syslog.py
#version: 1.2
#description:

import threading
import socket
import sqlite3
import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar, VERTICAL, RIGHT, Y, END, Label, Entry, Button
from modules.gui_utils import GUIUtils

class SysLogPlugin:
    def __init__(self, app, db_path='database/network_monitor.db'):
        self.app = app
        self.db_path = db_path
        self.server_thread = None
        self.stop_event = threading.Event()
        self.setup_database()
        self.start_server()

    def setup_database(self):
        """Create the syslog table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS syslog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                host TEXT,
                severity TEXT,
                message TEXT
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()

    def start_server(self):
        """Start the SysLog server in a separate thread."""
        self.server_thread = threading.Thread(target=self.run_server, daemon=True)
        self.server_thread.start()

    def run_server(self):
        """Run the SysLog server."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind(('0.0.0.0', 514))
            while not self.stop_event.is_set():
                try:
                    message, address = server_socket.recvfrom(1024)
                    log_entry = self.parse_syslog_message(message.decode('utf-8'), address[0])
                    self.store_log(log_entry)
                except Exception as e:
                    print(f"Error receiving syslog message: {e}")

    def parse_syslog_message(self, message, host):
        """Parse the SysLog message and return a dictionary."""
        severity = "INFO"  # Default to INFO
        if "<" in message and ">" in message:
            try:
                severity = message.split(">")[0].strip("<>")
                message = message.split(">")[1]
            except IndexError:
                pass

        return {
            'timestamp': self.get_current_timestamp(),
            'host': host,
            'severity': severity,
            'message': message.strip()
        }

    def get_current_timestamp(self):
        """Return the current timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def store_log(self, log_entry):
        """Store the parsed log entry in the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO syslog (timestamp, host, severity, message)
            VALUES (:timestamp, :host, :severity, :message)
        ''', log_entry)
        conn.commit()
        cursor.close()
        conn.close()

    def stop_server(self):
        """Stop the SysLog server."""
        self.stop_event.set()
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join()

    def show_syslog_gui(self):
        """Show the SysLog GUI window with filtering options."""
        log_window = Toplevel(self.app.root)
        log_window.title("SysLog Viewer")
        GUIUtils.set_icon(log_window)

        # Filter frame
        filter_frame = tk.Frame(log_window)
        filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        Label(filter_frame, text="Host:").pack(side=tk.LEFT)
        host_entry = Entry(filter_frame)
        host_entry.pack(side=tk.LEFT, padx=5)

        Label(filter_frame, text="Severity:").pack(side=tk.LEFT, padx=10)
        severity_entry = Entry(filter_frame)
        severity_entry.pack(side=tk.LEFT, padx=5)

        Label(filter_frame, text="Message:").pack(side=tk.LEFT, padx=10)
        message_entry = Entry(filter_frame)
        message_entry.pack(side=tk.LEFT, padx=5)

        # Log display
        scrollbar = Scrollbar(log_window, orient=VERTICAL)
        log_text = Text(log_window, wrap="none", yscrollcommand=scrollbar.set)
        scrollbar.config(command=log_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        log_text.pack(fill="both", expand=True)

        def apply_filters():
            logs = self.fetch_logs(
                host=host_entry.get(),
                severity=severity_entry.get(),
                message=message_entry.get()
            )
            log_text.delete(1.0, END)  # Clear the current logs
            for log in logs:
                log_text.insert(END, f"{log[1]} - {log[2]} - {log[3]} - {log[4]}\n")

        # Filter button
        filter_button = Button(filter_frame, text="Apply Filters", command=apply_filters)
        filter_button.pack(side=tk.LEFT, padx=10)

        # Load initial logs without filters
        apply_filters()

    def fetch_logs(self, host=None, severity=None, message=None):
        """Fetch logs from the SQLite database with optional filtering."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM syslog WHERE 1=1"
        params = {}

        if host:
            query += " AND host LIKE :host"
            params['host'] = f"%{host}%"

        if severity:
            query += " AND severity LIKE :severity"
            params['severity'] = f"%{severity}%"

        if message:
            query += " AND message LIKE :message"
            params['message'] = f"%{message}%"

        query += " ORDER BY timestamp DESC"
        cursor.execute(query, params)
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        return logs

# Plugin initialization
def init_plugin(app):
    syslog_plugin = SysLogPlugin(app)
    app.plugins.append(syslog_plugin)
    app.add_tool_menu("SysLog Viewer", syslog_plugin.show_syslog_gui)