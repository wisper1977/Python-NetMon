import os
import threading
import webbrowser
import importlib.util
import tkinter as tk
import pygame
from tkinter import Menu, Toplevel, Label, Entry, Button, messagebox, Text, Scrollbar, filedialog, VERTICAL, RIGHT, Y, END
from tkinter import ttk
from modules.device_manager import DeviceManager
from modules.settings_manager import SettingsManager
from modules.system_log import SystemLog
from modules.net_ops_ping import NetOpsPing
from modules.net_ops_snmp import NetOpsSNMP
from plugins.syslog_plugin import init_plugin as init_syslog_plugin
from plugins.speedtest_plugin import init_plugin as init_speedtest_plugin

class ApplicationGUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.device_manager = DeviceManager()
        self.settings_manager = SettingsManager(self.app.config_path)
        self.logger = SystemLog(self.app.config['Database']['path'])
        self.ping = NetOpsPing(attempts=self.settings_manager.config.getint('PING', 'attempts'),
                               timeout=self.settings_manager.config.getint('PING', 'timeout'))
        self.snmp = NetOpsSNMP(community_string=self.settings_manager.config.get('SNMP', 'community_string'), logger=self.logger)
        self.refresh_interval = self.settings_manager.config.getint('Network', 'refreshinterval') * 1000  # Convert to milliseconds
        self.remaining_time = self.refresh_interval // 1000  # Initial time in seconds
        
        # Load version and developer information from config
        self.version = self.settings_manager.config.get('DEFAULT', 'version')
        self.developer = self.settings_manager.config.get('DEFAULT', 'developer')
        self.help_url = self.settings_manager.config.get('DEFAULT', 'hyperlink')

        self.acknowledged_devices = set()  # Track acknowledged devices
        self.plugins_folder = 'plugins'
        self.plugins = {}

        self.root.title("NetMon - Network Monitoring Tool")
        self.root.iconbitmap('media/NetMon.ico')  # Set the icon for the main window
        self.setup_menu()
        self.setup_treeview()
        self.setup_refresh_clock()

        self.timer_running = False  # Control flag for the countdown timer

        # Load devices and start monitoring asynchronously
        self.load_devices_async()

        pygame.mixer.init()  # Initialize the mixer for sound playback

        # Initialize plugins
        init_syslog_plugin(self)
        init_speedtest_plugin(self)

    def set_icon(self, window):
        """Sets the application icon for the provided window."""
        window.iconbitmap('media/NetMon.ico')

    def setup_menu(self):
        menubar = Menu(self.root)

        # File Menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Settings", command=lambda: self.settings_manager.open_settings_dialog(self.root))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Edit Menu
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Add Device", command=self.add_device_dialog)
        editmenu.add_command(label="Edit Device", command=self.edit_device_dialog)
        editmenu.add_command(label="Delete Device", command=self.delete_device_dialog)
        menubar.add_cascade(label="Edit", menu=editmenu)

        # View Menu
        viewmenu = Menu(menubar, tearoff=0)
        viewmenu.add_command(label="System Log", command=self.view_system_log)
        menubar.add_cascade(label="View", menu=viewmenu)

        # Tools Menu
        self.toolsmenu = Menu(menubar, tearoff=0)
        self.load_plugins()
        menubar.add_cascade(label="Tools", menu=self.toolsmenu)

        # Help Menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Online Help", accelerator="Ctrl+H", command=self.open_online_help)
        help_menu.add_command(label="About Python NetMon", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def load_plugins(self):
        """Load plugins from the plugins folder."""
        if not os.path.exists(self.plugins_folder):
            os.makedirs(self.plugins_folder)

        for filename in os.listdir(self.plugins_folder):
            if filename.endswith(".py"):
                plugin_name = filename[:-3]
                plugin_path = os.path.join(self.plugins_folder, filename)
                self.add_plugin(plugin_name, plugin_path)

    def add_plugin(self, plugin_name, plugin_path):
        """Add a plugin to the Tools menu."""
        try:
            # Format the plugin name: replace underscores with spaces and capitalize each word
            display_name = plugin_name.replace('_', ' ').title()

            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'run_plugin'):
                self.plugins[plugin_name] = module.run_plugin
                self.toolsmenu.add_command(label=display_name, command=lambda: self.run_plugin(plugin_name))
            else:
                self.logger.log("ERROR", f"Plugin {plugin_name} does not have a 'run_plugin' function.")
        except Exception as e:
            self.logger.log("ERROR", f"Failed to load plugin {plugin_name}: {str(e)}")

    def add_tool_menu(self, label, command):
        """Add a command to the Tools menu."""
        self.toolsmenu.add_command(label=label, command=command)

    def run_plugin(self, plugin_name):
        """Execute the selected plugin."""
        try:
            if plugin_name in self.plugins:
                self.plugins[plugin_name]()
            else:
                messagebox.showerror("Error", f"Plugin {plugin_name} not found.")
        except Exception as e:
            self.logger.log("ERROR", f"Failed to run plugin {plugin_name}: {str(e)}")
            messagebox.showerror("Error", f"Failed to run plugin {plugin_name}. Check the logs for more details.")

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
        self.tree.bind("<Double-1>", self.on_double_click)  # Bind double-click event

    def load_devices_async(self):
        """Load devices and start monitoring asynchronously."""
        threading.Thread(target=self.load_devices_and_start_monitoring, daemon=True).start()

    def load_devices_and_start_monitoring(self):
        """Loads devices and starts monitoring them."""
        devices = self.device_manager.get_all_devices()  # Load devices from the database
        self.root.after(0, self.update_treeview_with_devices, devices)  # Update GUI on the main thread
        self.start_monitoring()  # Begin monitoring after devices are loaded

    def update_treeview_with_devices(self, devices):
        """Update the Treeview with the loaded devices, sorting unreachable ones to the top and highlighting their rows."""
        if devices is None:
            return
        
        # Clear the Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Sort devices so that unreachable ones are at the top
        devices.sort(key=lambda x: x[7] != "Unreachable")

        # Insert devices into the Treeview
        for device in devices:
            device_id, name, ip_address, location, device_type, snmp_status, ping_status, last_status = device
            
            # Determine the color based on status and acknowledgment
            if last_status == "Unreachable":
                if device_id in self.acknowledged_devices:
                    self.tree.insert("", "end", values=(device_id, name, ip_address, location, device_type, snmp_status, ping_status, last_status), tags=('acknowledged',))
                else:
                    self.tree.insert("", "end", values=(device_id, name, ip_address, location, device_type, snmp_status, ping_status, last_status), tags=('unreachable',))
            else:
                self.tree.insert("", "end", values=(device_id, name, ip_address, location, device_type, snmp_status, ping_status, last_status))

        # Configure the Treeview tags for different statuses
        self.tree.tag_configure('unreachable', background='red')
        self.tree.tag_configure('acknowledged', background='yellow')

    def start_monitoring(self):
        threading.Thread(target=self.monitor_devices, daemon=True).start()
        self.schedule_next_check()
        self.update_refresh_clock()

    def monitor_devices(self):
        devices = self.device_manager.get_all_devices()
        if devices is None:
            return

        for device in devices:
            device_id, name, ip_address, location, device_type, snmp_status, ping_status, last_status = device

            # Initialize SNMP and Ping statuses
            snmp_status = "Failed"
            ping_status = "Failed"

            snmp_result = self.snmp.snmp_get(ip_address, '1.3.6.1.2.1.1.1.0')  # Example OID
            if snmp_result:
                snmp_status = "Success"
                self.logger.log("INFO", f"SNMP response from {name}: {snmp_result}")
            else:
                self.logger.log("ERROR", f"SNMP failed for {name} ({ip_address})")

            ping_result = self.ping.ping_device(ip_address)
            if ping_result:
                ping_status = "Success"
                self.logger.log("INFO", f"Ping response from {name}: Reachable")
            else:
                self.logger.log("ERROR", f"No response from {name} ({ip_address})")

            overall_status = "Reachable" if snmp_result or ping_result else "Unreachable"
            
            # Update the status including SNMP and Ping results
            self.update_device_status(device_id, snmp_status, ping_status, overall_status)

            # Play alert sound if the device is unreachable and not acknowledged
            if overall_status == "Unreachable" and device_id not in self.acknowledged_devices:
                self.play_alert_sound()

    def update_device_status(self, device_id, snmp_status, ping_status, overall_status):
        # Assuming `update_status` in `DeviceManager` can handle SNMP and Ping statuses
        self.device_manager.update_status(device_id, snmp_status, ping_status, overall_status)

        # If the device becomes reachable, remove it from acknowledged devices
        if overall_status == "Reachable" and device_id in self.acknowledged_devices:
            self.acknowledged_devices.remove(device_id)

        # Refresh the device list in the GUI asynchronously
        self.root.after(0, self.load_devices_async)

    def play_alert_sound(self):
        if not pygame.mixer.music.get_busy():
            alert_sound = 'media/alert.wav'
            pygame.mixer.music.load(alert_sound)
            pygame.mixer.music.play()

    def on_double_click(self, event):
        """Handle double-click event to acknowledge an unreachable device."""
        item = self.tree.identify_row(event.y)
        if item:
            device_id = self.tree.item(item, "values")[0]
            if device_id:
                device_id = int(device_id)
                self.acknowledged_devices.add(device_id)
                self.update_treeview_with_devices(self.device_manager.get_all_devices())

    def setup_refresh_clock(self):
        self.refresh_label = Label(self.root, text="Next refresh in:")
        self.refresh_label.pack()

        self.progress_bar = ttk.Progressbar(self.root, maximum=self.remaining_time, length=300)
        self.progress_bar.pack()
        self.progress_bar['value'] = self.remaining_time

    def update_refresh_clock(self):
        if not self.timer_running:
            self.timer_running = True
            self._run_refresh_clock()

    def _run_refresh_clock(self):
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.remaining_time = self.refresh_interval // 1000
            # Trigger the actual refresh
            self.start_monitoring()
        self.refresh_label.config(text=f"Next refresh in: {self.remaining_time} seconds")
        self.progress_bar['value'] = self.remaining_time

        if self.remaining_time > 0:
            self.root.after(1000, self._run_refresh_clock)
        else:
            self.timer_running = False  # Reset the flag when countdown finishes

    def schedule_next_check(self):
        self.root.after(self.refresh_interval, self.start_monitoring)

    def add_device_dialog(self):
        self.device_dialog("Add Device", self.device_manager.add_device)

    def edit_device_dialog(self):
        # Step 1: Ask for the Device ID
        device_id = self.ask_for_device_id()
        
        if device_id:
            # Step 2: Fetch the device details from the database
            device = self.device_manager.get_device(device_id)
            
            if device:
                # Step 3: Populate the form with the device information
                self.device_dialog("Edit Device", self.device_manager.edit_device, include_id=True, device_info=device)
            else:
                messagebox.showerror("Edit Device", "Device not found.")
        
    def ask_for_device_id(self):
        dialog = Toplevel(self.root)
        dialog.title("Enter Device ID")
        self.set_icon(dialog)

        Label(dialog, text="Device ID:").grid(row=0, column=0, padx=10, pady=5)
        id_entry = Entry(dialog)
        id_entry.grid(row=0, column=1, padx=10, pady=5)

        def submit():
            dialog.quit()

        Button(dialog, text="Submit", command=submit).grid(row=1, column=0, columnspan=2, pady=10)
        
        dialog.protocol("WM_DELETE_WINDOW", dialog.quit)
        dialog.mainloop()
        device_id = id_entry.get()
        dialog.destroy()

        return device_id if device_id else None

    def delete_device_dialog(self):
        self.device_dialog("Delete Device", self.device_manager.delete_device, include_id=True, only_id=True)

    def device_dialog(self, title, action, include_id=False, only_id=False, device_info=None):
        dialog = Toplevel(self.root)
        dialog.title(title)
        self.set_icon(dialog)

        if include_id:
            Label(dialog, text="Device ID:").grid(row=0, column=0, padx=10, pady=5)
            id_entry = Entry(dialog)
            id_entry.grid(row=0, column=1, padx=10, pady=5)
            id_entry.insert(0, device_info[0] if device_info else "")

        if not only_id:
            Label(dialog, text="Device Name:").grid(row=1 if include_id else 0, column=0, padx=10, pady=5)
            name_entry = Entry(dialog)
            name_entry.grid(row=1 if include_id else 0, column=1, padx=10, pady=5)
            name_entry.insert(0, device_info[1] if device_info else "")

            Label(dialog, text="IP Address:").grid(row=2 if include_id else 1, column=0, padx=10, pady=5)
            ip_entry = Entry(dialog)
            ip_entry.grid(row=2 if include_id else 1, column=1, padx=10, pady=5)
            ip_entry.insert(0, device_info[2] if device_info else "")

            Label(dialog, text="Location:").grid(row=3 if include_id else 2, column=0, padx=10, pady=5)
            location_entry = Entry(dialog)
            location_entry.grid(row=3 if include_id else 2, column=1, padx=10, pady=5)
            location_entry.insert(0, device_info[3] if device_info else "")

            Label(dialog, text="Type:").grid(row=4 if include_id else 3, column=0, padx=10, pady=5)
            type_entry = Entry(dialog)
            type_entry.grid(row=4 if include_id else 3, column=1, padx=10, pady=5)
            type_entry.insert(0, device_info[4] if device_info else "")

        def submit():
            if include_id:
                device_id = id_entry.get()
                if not device_id:
                    messagebox.showerror(title, "Device ID is required")
                    return
                if only_id:
                    action(device_id)
                else:
                    name = name_entry.get()
                    ip_address = ip_entry.get()
                    location = location_entry.get()
                    device_type = type_entry.get()
                    if name and ip_address and location and device_type:
                        action(device_id, name, ip_address, location, device_type)
                    else:
                        messagebox.showerror(title, "All fields are required")
                        return
            else:
                name = name_entry.get()
                ip_address = ip_entry.get()
                location = location_entry.get()
                device_type = type_entry.get()
                if name and ip_address and location and device_type:
                    action(name, ip_address, location, device_type)
                else:
                    messagebox.showerror(title, "All fields are required")
                    return
            dialog.destroy()
            messagebox.showinfo(title, f"{title} completed successfully.")
            self.load_devices_async()  # Reload devices asynchronously to update the Treeview

        Button(dialog, text="Submit", command=submit).grid(row=5 if include_id else 4, column=0, columnspan=2, pady=10)

    def view_system_log(self):
        # Create the log window
        log_window = Toplevel(self.root)
        log_window.title("System Log")
        self.set_icon(log_window)

        # Create filter frame
        filter_frame = tk.Frame(log_window)
        filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Log level filter
        tk.Label(filter_frame, text="Log Level:").pack(side=tk.LEFT)
        log_level_var = tk.StringVar(value="All")
        log_level_options = ["All", "INFO", "ERROR", "DEBUG", "WARNING"]
        log_level_menu = tk.OptionMenu(filter_frame, log_level_var, *log_level_options)
        log_level_menu.pack(side=tk.LEFT, padx=5)

        # Search filter
        tk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=10)
        search_var = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable=search_var)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Refresh button
        refresh_button = tk.Button(filter_frame, text="Refresh", command=lambda: self.refresh_logs(log_text, log_level_var.get(), search_var.get()))
        refresh_button.pack(side=tk.LEFT, padx=10)

        # Save button
        save_button = tk.Button(filter_frame, text="Save to File", command=lambda: self.save_log_to_file(log_text))
        save_button.pack(side=tk.LEFT, padx=10)

        # Create log display
        scrollbar = Scrollbar(log_window, orient=VERTICAL)
        log_text = Text(log_window, wrap="none", yscrollcommand=scrollbar.set)
        scrollbar.config(command=log_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        log_text.pack(fill="both", expand=True)

        # Load and display logs
        self.refresh_logs(log_text, log_level_var.get(), search_var.get())

    def refresh_logs(self, log_text, log_level, search_term):
        log_text.delete(1.0, END)  # Clear the current logs

        # Fetch logs from the database
        logs = self.logger.get_logs()

        # Apply filters
        filtered_logs = []
        for log_message, timestamp in logs:
            # Extract log level from the log message
            message_level = log_message.split(":")[0] if ":" in log_message else "INFO"

            # Check log level filter
            if log_level != "All" and message_level != log_level:
                continue  # Skip logs that don't match the selected log level

            # Check search term filter
            if search_term.lower() not in log_message.lower():
                continue  # Skip logs that don't contain the search term

            filtered_logs.append((log_message, timestamp))

        # Display filtered logs
        for log_message, timestamp in filtered_logs:
            log_text.insert(END, f"{timestamp} - {log_message}\n")

    def save_log_to_file(self, log_text):
        # Open file dialog to save the log
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(log_text.get(1.0, END))

    def show_about(self):
        """Display the 'About' dialog with information about the application."""
        try:
            messagebox.showinfo("About Python NetMon", f"Version: {self.version}\nDeveloped by: {self.developer}\nA simple network monitoring tool built with Python and Tkinter.")
        except Exception as e:
            self.logger.log("ERROR", f"Failed to show about dialog: {str(e)}")
            raise e
        
    def open_online_help(self):
        """Open the online help link in the default web browser."""
        try:
            webbrowser.open(self.help_url)
        except Exception as e:
            self.logger.log("ERROR", f"Failed to open online help: {str(e)}")
            messagebox.showerror("Error", "Unable to open the online help link.")
            raise e

    def on_exit(self):
        """Handle the application exit."""
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.root.destroy()