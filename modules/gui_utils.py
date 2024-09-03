# Network Monitor App
# gui_utils.py
# version: 1.2
# description: Contains utility functions to support GUI operations, such as setting icons, handling common dialog actions, and playing alert sounds.

import webbrowser, pygame
import tkinter as tk
from tkinter import filedialog, messagebox

class GUIUtils:
    @staticmethod
    def set_icon(window, icon_path='media/NetMon.ico'):
        """Sets the application icon for the provided window."""
        try:
            window.iconbitmap(icon_path)
        except tk.TclError as e:
            print(f"Failed to set icon: {e}")

    @staticmethod
    def import_devices(app, update_treeview_callback, device_manager):
        """Handle the import devices action from the File menu."""
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            app.db_ops.import_devices(file_path)
            update_treeview_callback(device_manager.get_all_devices())

    @staticmethod
    def show_about(version, developer):
        try:
            messagebox.showinfo("About Python NetMon", f"Version: {version}\nDeveloped by: {developer}\nA simple network monitoring tool built with Python and Tkinter.")
        except Exception as e:
            print(f"Failed to show about dialog: {str(e)}")

    @staticmethod
    def open_online_help(help_url):
        try:
            webbrowser.open(help_url)
        except Exception as e:
            print(f"Failed to open online help: {str(e)}")
            messagebox.showerror("Error", "Unable to open the online help link.")

    @staticmethod
    def on_exit(root):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            root.destroy()

    @staticmethod
    def play_alert_sound(alert_sound='media/alert.wav'):
        """Plays the alert sound if not already playing."""
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(alert_sound)
            pygame.mixer.music.play()