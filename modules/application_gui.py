import tkinter as tk
from tkinter import filedialog
import webbrowser
import pygame
import queue
from tkinter import Menu, Label, messagebox
from tkinter import ttk
from modules.plugin_manager import PluginManager
from modules.system_log_gui import SystemLogGUI
from modules.network_monitor import NetworkMonitor 
from modules.device_manager_gui import DeviceManagerGUI

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
        self.root.iconbitmap('media/NetMon.ico')  # Ensure this path is correct

        self.setup_menu()
        self.setup_treeview()
        self.setup_refresh_clock()
        
        self.timer_running = False  # Control flag for the countdown timer

        # Start processing the queue and monitoring devices after initialization
        self.root.after(100, self.process_queue)
        self.root.after(200, self.start_monitoring_thread)

        # Explicitly load devices into the Treeview
        self.update_treeview_with_devices(self.device_manager_gui.device_manager.get_all_devices())

        pygame.mixer.init()  # Initialize the mixer for sound playback

        # Dynamically load and initialize plugins using PluginManager
        self.plugin_manager = PluginManager('plugins')
        self.plugin_manager.load_plugins(self)

    def add_tool_menu(self, label, command):
        """Add a command to the Tools menu."""
        self.toolsmenu.add_command(label=label, command=command)

    def start_monitoring_thread(self):
        """Start the thread that will monitor devices."""
        self.network_monitor.start_monitoring()

    def set_icon(self, window):
        window.iconbitmap('media/NetMon.ico')

    def setup_menu(self):
        menubar = Menu(self.root)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Settings", command=lambda: self.app.settings_manager.open_settings_dialog(self.root))
        filemenu.add_command(label="Import Devices", command=self.import_devices)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_exit)
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
        help_menu.add_command(label="Online Help", accelerator="Ctrl+H", command=self.open_online_help)
        help_menu.add_command(label="About Python NetMon", command=self.show_about)
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

    def update_treeview_with_devices(self, devices):
        """Update the Treeview with the loaded devices, sorting unreachable ones to the top and highlighting their rows."""
        if devices is None:
            print("No devices to display")
            return
        
        # Clear the Treeview
        #print("Clearing Treeview")
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Sort devices so that unreachable ones are at the top
        devices.sort(key=lambda x: x[7] != "Unreachable")

        # Insert devices into the Treeview
        for device in devices:
            device_id, name, ip_address, location, device_type, snmp_status, ping_status, last_status = [
                val if val is not None else '' for val in device[:8]
            ]
            
            #print(f"Inserting into Treeview: {device_id}, {name}, {ip_address}, {location}, {device_type}, {snmp_status}, {ping_status}, {last_status}")
            
            # Determine the color based on status and acknowledgment
            if last_status == "Unreachable":
                if device_id in self.network_monitor.acknowledged_devices:  # Ensure this uses the correct reference to acknowledged devices
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

    def schedule_next_check(self):
        """Schedule the next device monitoring check."""
        self.root.after(self.network_monitor.refresh_interval, self.start_monitoring_thread)

    def play_alert_sound(self):
        if not pygame.mixer.music.get_busy():
            alert_sound = 'media/alert.wav'
            pygame.mixer.music.load(alert_sound)
            pygame.mixer.music.play()
            
    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            device_id = self.tree.item(item, "values")[0]
            if device_id:
                device_id = int(device_id)
                self.network_monitor.acknowledged_devices.add(device_id)
                self.update_treeview_with_devices(self.device_manager_gui.device_manager.get_all_devices())

    def setup_refresh_clock(self):
        self.refresh_label = Label(self.root, text="Next refresh in:")
        self.refresh_label.pack()

        self.progress_bar = ttk.Progressbar(self.root, maximum=self.network_monitor.refresh_interval // 1000, length=300)
        self.progress_bar.pack()
        self.progress_bar['value'] = self.network_monitor.remaining_time

        self._run_refresh_clock()

    def _run_refresh_clock(self):
        if self.network_monitor.remaining_time <= 0:
            self.network_monitor.remaining_time = self.network_monitor.refresh_interval // 1000
            # Trigger the actual refresh
            self.start_monitoring_thread()
        
        self.network_monitor.remaining_time -= 1
        self.refresh_label.config(text=f"Next refresh in: {self.network_monitor.remaining_time} seconds")
        self.progress_bar['value'] = self.network_monitor.remaining_time

        self.root.after(1000, self._run_refresh_clock)
        
    def update_device_status(self, device_id, snmp_status, ping_status, overall_status):
        """Updates the status of a device in the Treeview."""
        #print(f"Updating device {device_id} in Treeview GUI: SNMP={snmp_status}, Ping={ping_status}, Overall={overall_status}")
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if str(values[0]) == str(device_id):
                self.tree.item(item, values=(device_id, values[1], values[2], values[3], values[4], snmp_status, ping_status, overall_status))
                break

    def update_refresh_clock_display(self, remaining_time):
        """Update the refresh clock display."""
        self.refresh_label.config(text=f"Next refresh in: {remaining_time} seconds")
        self.progress_bar['value'] = remaining_time

    def import_devices(self):
        """Handle the import devices action from the File menu."""
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            self.app.db_ops.import_devices(file_path)
            self.update_treeview_with_devices(self.device_manager_gui.device_manager.get_all_devices())

    def show_about(self):
        try:
            messagebox.showinfo("About Python NetMon", f"Version: {self.version}\nDeveloped by: {self.developer}\nA simple network monitoring tool built with Python and Tkinter.")
        except Exception as e:
            print(f"Failed to show about dialog: {str(e)}")

    def open_online_help(self):
        try:
            webbrowser.open(self.help_url)
        except Exception as e:
            print(f"Failed to open online help: {str(e)}")
            messagebox.showerror("Error", "Unable to open the online help link.")

    def on_exit(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.root.destroy()
