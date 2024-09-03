import threading
from tkinter import Toplevel, Label, Entry, Button, messagebox
from modules.device_manager import DeviceManager
from modules.gui_utils import GUIUtils  # Import the utility class

class DeviceManagerGUI:
    def __init__(self, app):
        self.app = app
        self.device_manager = DeviceManager(self.app.db_ops, self.app.logger)

    def add_device_dialog(self):
        self.device_dialog("Add Device", self.device_manager.add_device)

    def edit_device_dialog(self):
        device_id = self.ask_for_device_id()
        if device_id:
            device = self.device_manager.get_device(device_id)
            if device:
                self.device_dialog("Edit Device", self.device_manager.edit_device, include_id=True, device_info=device)
            else:
                messagebox.showerror("Edit Device", "Device not found.")

    def ask_for_device_id(self):
        dialog = Toplevel(self.app.gui.root)
        dialog.title("Enter Device ID")
        GUIUtils.set_icon(dialog)  # Use the utility method

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
        dialog = Toplevel(self.app.gui.root)
        GUIUtils.set_icon(dialog)  # Use the utility method
        dialog.title(title)

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
                    self.perform_action_in_background(action, device_id)
                else:
                    name = name_entry.get()
                    ip_address = ip_entry.get()
                    location = location_entry.get()
                    device_type = type_entry.get()
                    if name and ip_address and location and device_type:
                        self.perform_action_in_background(action, device_id, name, ip_address, location, device_type)
                    else:
                        messagebox.showerror(title, "All fields are required")
                        return
            else:
                name = name_entry.get()
                ip_address = ip_entry.get()
                location = location_entry.get()
                device_type = type_entry.get()
                if name and ip_address and location and device_type:
                    self.perform_action_in_background(action, name, ip_address, location, device_type)
                else:
                    messagebox.showerror(title, "All fields are required")
                    return
            dialog.destroy()

        Button(dialog, text="Submit", command=submit).grid(row=5 if include_id else 4, column=0, columnspan=2, pady=10)

    def perform_action_in_background(self, action, *args):
        """Run the device action in a background thread to keep the UI responsive."""
        def run_action():
            try:
                action(*args)
                messagebox.showinfo("Success", f"Action completed successfully.")
                self.app.gui.update_treeview_with_devices(self.device_manager.get_all_devices())
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        threading.Thread(target=run_action, daemon=True).start()
