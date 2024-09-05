# Network Monitor App
# ftp_plugin.py
# version: 1.2
# description: Plugin that provides FTP server functionality, allowing users to start and stop an FTP server through the Network Monitor application.

import tkinter as tk
from tkinter import messagebox, filedialog
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from modules.gui_utils import GUIUtils
import threading
import configparser
import os

class FTPServerPlugin:
    CONFIG_FILE = 'config.ini'  # The name of the config file
    server = None  # Class-level server to keep it independent of the window
    is_running = False  # Class-level state to track server running status
    server_thread = None  # Class-level thread to handle server in background

    def __init__(self, root):
        self.root = root

        # Create the config parser
        self.config = configparser.ConfigParser()

        # Ensure config file and section exist
        self.check_config_file()

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame, text="Port:").grid(row=0, column=0, padx=10, pady=10)
        self.port_entry = tk.Entry(self.frame)
        self.port_entry.grid(row=0, column=1, padx=10, pady=10)
        self.port_entry.insert(0, "21")

        tk.Label(self.frame, text="Username:").grid(row=1, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame, text="Password:").grid(row=2, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.frame, text="Root Directory:").grid(row=3, column=0, padx=10, pady=10)
        self.root_dir_entry = tk.Entry(self.frame)
        self.root_dir_entry.grid(row=3, column=1, padx=10, pady=10)
        self.browse_button = tk.Button(self.frame, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=3, column=2, padx=10, pady=10)

        # Load saved root directory if it exists
        if self.config.has_option('FTP', 'root_dir'):
            self.root_dir_entry.insert(0, self.config.get('FTP', 'root_dir'))

        self.start_button = tk.Button(self.frame, text="Start FTP Server", command=self.start_server)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.stop_button = tk.Button(self.frame, text="Stop FTP Server", command=self.stop_server)
        self.stop_button.grid(row=4, column=2, padx=10, pady=10)

        # Disable stop button initially if the server is not running
        if not FTPServerPlugin.is_running:
            self.stop_button.config(state=tk.DISABLED)
        else:
            self.start_button.config(state=tk.DISABLED)

    def check_config_file(self):
        """Ensure that the config file exists and contains the necessary FTP section."""
        if not os.path.exists(self.CONFIG_FILE):
            # Create the config file if it doesn't exist
            with open(self.CONFIG_FILE, 'w') as configfile:
                self.config.add_section('FTP')
                self.config.set('FTP', 'root_dir', '')
                self.config.write(configfile)
        else:
            # Read existing config file
            self.config.read(self.CONFIG_FILE)

            # Check if 'FTP' section exists, if not, add it
            if not self.config.has_section('FTP'):
                self.config.add_section('FTP')

            # If 'root_dir' doesn't exist, create an empty entry for it
            if not self.config.has_option('FTP', 'root_dir'):
                self.config.set('FTP', 'root_dir', '')

            # Write any changes to the config file
            with open(self.CONFIG_FILE, 'w') as configfile:
                self.config.write(configfile)

    def browse_directory(self):
        """Open a directory selection dialog and save the selected directory to the config file."""
        directory = filedialog.askdirectory()
        if directory:
            self.root_dir_entry.delete(0, tk.END)
            self.root_dir_entry.insert(0, directory)

            # Save the selected directory to the config file
            self.config.set('FTP', 'root_dir', directory)
            with open(self.CONFIG_FILE, 'w') as configfile:
                self.config.write(configfile)

    def start_server(self):
        if FTPServerPlugin.is_running:
            messagebox.showinfo("FTP Server", "Server is already running.")
            return

        port = int(self.port_entry.get())
        root_dir = self.root_dir_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not root_dir:
            messagebox.showerror("Error", "Please select a root directory")
            return

        if not username or not password:
            messagebox.showerror("Error", "Please enter a username and password")
            return

        # Set up the FTP server with user authentication
        authorizer = DummyAuthorizer()
        authorizer.add_user(username, password, root_dir, perm="elradfmw")

        handler = FTPHandler
        handler.authorizer = authorizer

        FTPServerPlugin.server = FTPServer(("0.0.0.0", port), handler)

        # Start the server in a separate thread to avoid freezing the GUI
        FTPServerPlugin.server_thread = threading.Thread(target=self.run_server, daemon=True)
        FTPServerPlugin.server_thread.start()

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        FTPServerPlugin.is_running = True
        messagebox.showinfo("FTP Server", f"FTP server started on port {port}")

    def run_server(self):
        """Run the FTP server in a separate thread."""
        if FTPServerPlugin.server:
            FTPServerPlugin.server.serve_forever()

    def stop_server(self):
        if FTPServerPlugin.server and FTPServerPlugin.is_running:
            FTPServerPlugin.server.close_all()
            FTPServerPlugin.is_running = False
            FTPServerPlugin.server = None
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            messagebox.showinfo("FTP Server", "FTP server stopped")
        else:
            messagebox.showinfo("FTP Server", "Server is not running.")

def init_plugin(application):
    """Initialize the plugin and add it to the Tools menu."""
    application.add_tool_menu(
        label="FTP Server",
        command=lambda: open_ftp_server_window(application.root)
    )

def open_ftp_server_window(root):
    """Open the FTP Server Plugin GUI in a new Toplevel window."""
    ftp_window = tk.Toplevel(root)
    ftp_window.title("FTP Server")
    ftp_window.geometry("400x250")  # Adjusted size for added fields
    
    # Set the custom icon
    GUIUtils.set_icon(ftp_window)
    
    FTPServerPlugin(ftp_window)
