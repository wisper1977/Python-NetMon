# Network Monitor App
# application_gui.py
# version: 1.2
# description: Contains the main GUI logic for the Network Monitor application, including the setup of menus, the device treeview, and the refresh clock.

import pygame
import queue
import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from modules.plugin_manager import PluginManager
from modules.system_log_gui import SystemLogGUI
from modules.network_monitor import NetworkMonitor 
from modules.device_manager_gui import DeviceManagerGUI
from modules.gui_utils import GUIUtils
from modules.refresh_clock import RefreshClock
from modules.update_program import ProgramUpdater  # Import the RefreshClock class

class ApplicationGUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.update_queue = queue.Queue()
        self.device_manager_gui = DeviceManagerGUI(app)
        self.network_monitor = NetworkMonitor(app, self.update_queue, self.device_manager_gui)
        
        # Initialize other components that rely on app's settings
        self.settings_manager = app.settings_manager
        self.system_log_gui = SystemLogGUI(self.root, self.app, self.app.logger)

        # Load version and developer information from config
        self.version = self.settings_manager.config.get('DEFAULT', 'version')
        self.developer = self.settings_manager.config.get('DEFAULT', 'developer')
        self.help_url = self.settings_manager.config.get('DEFAULT', 'hyperlink')
        
        # Initialize the plugins list
        self.plugins = []

        # Set window title and icon
        self.root.title("NetMon - Network Monitoring Tool")
        GUIUtils.set_icon(self.root)

        self.setup_menu()
        self.setup_treeview()

        # Initialize the refresh clock
        self.refresh_clock = RefreshClock(self.root, self.network_monitor, self.network_monitor.start_monitoring)
        
        self.timer_running = False  # Control flag for the countdown timer

        # Start processing the queue and monitoring devices after initialization
        self.root.after(100, self.process_queue)
        self.root.after(200, self.network_monitor.start_monitoring)

        # Explicitly load devices into the Treeview
        self.update_treeview_with_devices(self.device_manager_gui.device_manager.get_all_devices())

        # Dynamically load and initialize plugins using PluginManager
        self.plugin_manager = PluginManager('plugins')
        self.plugin_manager.load_plugins(self)

        # Set up the processing of the UI task queue after GUI initialization
        self.root.after(100, self.device_manager_gui.process_ui_queue)

    def add_tool_menu(self, label, command):
        """Add a command to the Tools menu."""
        self.toolsmenu.add_command(label=label, command=command)

    def setup_menu(self):
        menubar = Menu(self.root)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Settings", command=lambda: self.app.settings_manager.open_settings_dialog(self.root))
        filemenu.add_command(label="Import Devices", command=lambda: GUIUtils.import_devices(self.app, self.update_treeview_with_devices, self.device_manager_gui.device_manager))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=lambda: GUIUtils.on_exit(self.root))
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Add Device", command=self.device_manager_gui.add_device_dialog)
        editmenu.add_command(label="Edit Device", command=self.device_manager_gui.edit_device_dialog)
        editmenu.add_command(label="Delete Device", command=self.device_manager_gui.delete_device_dialog)
        menubar.add_cascade(label="Edit", menu=editmenu)

        viewmenu = Menu(menubar, tearoff=0)
        viewmenu.add_command(label="System Log", command=self.system_log_gui.view_system_log)
        menubar.add_cascade(label="View", menu=viewmenu)

        self.toolsmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=self.toolsmenu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Online Help", accelerator="Ctrl+H", command=lambda: GUIUtils.open_online_help(self.help_url))
        help_menu.add_command(label="About Python NetMon", command=lambda: GUIUtils.show_about(self.version, self.developer))
        help_menu.add_command(label="Check for Updates", command=lambda: ProgramUpdater.check_for_update())
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def setup_treeview(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "IP", "Location", "Type", "SNMP Status", "Ping Status", "Status"), show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("IP", text="IP Address")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Type", text="Type")
        self.tree.heading("SNMP Status", text="SNMP Status")
        self.tree.heading("Ping Status", text="Ping Status")
        self.tree.heading("Status", text="Overall Status")

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("IP", width=150)
        self.tree.column("Location", width=100)
        self.tree.column("Type", width=100)
        self.tree.column("SNMP Status", width=100)
        self.tree.column("Ping Status", width=100)
        self.tree.column("Status", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_double_click)

    def update_device_status(self, device_id, snmp_status, ping_status, overall_status):
        """Updates the status of a device in the Treeview."""
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if str(values[0]) == str(device_id):
                self.tree.item(item, values=(device_id, values[1], values[2], values[3], values[4], snmp_status, ping_status, overall_status))
                break
            
    def update_treeview_with_devices(self, devices):
        """Update the Treeview with the loaded devices, sorting unreachable ones to the top and highlighting their rows."""
        if devices is None:
            print("No devices to display")
            return
        
        # Clear the Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Sort devices so that unreachable ones are at the top
        devices.sort(key=lambda x: x[7] != "Unreachable")

        # Insert devices into the Treeview
        for device in devices:
            device_id, name, ip_address, location, device_type, snmp_status, ping_status, last_status = [
                val if val is not None else '' for val in device[:8]
            ]
            
            # Determine the color based on status and acknowledgment
            if last_status == "Unreachable":
                if device_id in self.network_monitor.acknowledged_devices:
                    self.tree.insert("", "end", values=(device_id, name, ip_address, location, device_type, snmp_status, ping_status, last_status), tags=('acknowledged',))
                else:
                    self.tree.insert("", "end", values=(device_id, name, ip_address, location, device_type, snmp_status, ping_status, last_status), tags=('unreachable',))
            else:
                self.tree.insert("", "end", values=(device_id, name, ip_address, location, device_type, snmp_status, ping_status, last_status))

        # Configure the Treeview tags for different statuses
        self.tree.tag_configure('unreachable', background='red')
        self.tree.tag_configure('acknowledged', background='yellow')

    def process_queue(self):
        """Process tasks in the update queue."""
        try:
            while not self.update_queue.empty():
                task = self.update_queue.get_nowait()
                task()
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)  # Continue processing
         
    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            device_id = self.tree.item(item, "values")[0]
            if device_id:
                device_id = int(device_id)
                self.network_monitor.acknowledged_devices.add(device_id)
                self.update_treeview_with_devices(self.device_manager_gui.device_manager.get_all_devices())
