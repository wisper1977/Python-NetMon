# Version: 1.1.3.1
# Description: Module to create a dialog window for adding or editing device details.

import tkinter as tk
from tkinter import simpledialog, Label, Entry
from modules.log_manager import LogManager

class DeviceDialog(simpledialog.Dialog):
    def __init__(self, master, existing_details=None, action=None):
        """DeviceDialog constructor to initialize the dialog window."""
        self.logger = LogManager.get_instance()
        try:
            self.existing_details = existing_details or {'Key': '', 'Location': '', 'Name': '', 'IP': '', 'Type': '', 'Status': 'Unknown'}
            self.action = action
            super().__init__(master, title="Edit Device Details" if existing_details else "Add Device Details")
            self.logger.log_info("DeviceDialog initialized successfully")
        except Exception as e:
            self.logger.log_error("Failed to initialize DeviceDialog: " + str(e))
            raise e

    def body(self, master):
        """Build the body of the dialog with input fields for device details."""
        try:
            Label(master, text="Key:").grid(row=0, column=0)
            Label(master, text="Location:").grid(row=1, column=0)
            Label(master, text="Name:").grid(row=2, column=0)
            Label(master, text="IP:").grid(row=3, column=0)
            Label(master, text="Type:").grid(row=4, column=0)
            self.key_var = tk.StringVar(master, self.existing_details['Key'])
            self.location_var = tk.StringVar(master, self.existing_details['Location'])
            self.name_var = tk.StringVar(master, self.existing_details['Name'])
            self.ip_var = tk.StringVar(master, self.existing_details['IP'])
            self.type_var = tk.StringVar(master, self.existing_details['Type'])
            key_entry = Entry(master, textvariable=self.key_var, state='readonly')
            key_entry.grid(row=0, column=1)
            location_entry = Entry(master, textvariable=self.location_var)
            location_entry.grid(row=1, column=1)
            name_entry = Entry(master, textvariable=self.name_var)
            name_entry.grid(row=2, column=1)
            ip_entry = Entry(master, textvariable=self.ip_var)
            ip_entry.grid(row=3, column=1)
            type_entry = Entry(master, textvariable=self.type_var)
            type_entry.grid(row=4, column=1)
            return key_entry
        except Exception as e:
            self.logger.log_error("Failed to create body for DeviceDialog: " + str(e))
            raise e

    def apply(self):
        """Apply the changes made in the dialog to the device details."""
        try:
            details = {
                'Key': self.key_var.get(),
                'Location': self.location_var.get(),
                'Name': self.name_var.get(),
                'IP': self.ip_var.get(),
                'Type': self.type_var.get(),
                'Status': 'Unknown'
            }
            if self.action:
                self.action(details)
            self.result = details
        except Exception as e:
            self.logger.log_error("Failed to apply changes in DeviceDialog: " + str(e))
            raise e