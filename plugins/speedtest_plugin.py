#Speedtest Plugin
#speedtest_plugin.py
#version: 1.2
#description:

import threading
import tkinter as tk
import speedtest
from tkinter import Toplevel, Label, Button, messagebox

class SpeedTestPlugin:
    def __init__(self, app):
        self.app = app

    def run_speed_test(self):
        """Run the speed test and update the GUI with the results."""
        speed_test_window = Toplevel(self.app.root)
        speed_test_window.title("Speed Test")
        self.app.set_icon(speed_test_window)

        Label(speed_test_window, text="Running speed test...").pack(pady=10)

        results_frame = tk.Frame(speed_test_window)
        results_frame.pack(pady=10)

        close_button = Button(speed_test_window, text="Close", state=tk.DISABLED, command=speed_test_window.destroy)
        close_button.pack(pady=5)

        def perform_speed_test():
            try:
                st = speedtest.Speedtest()
                download_speed = st.download() / 10**6  # Convert to Mbps
                upload_speed = st.upload() / 10**6      # Convert to Mbps
                ping = st.results.ping

                Label(results_frame, text=f"Download: {download_speed:.2f} Mbps").pack()
                Label(results_frame, text=f"Upload: {upload_speed:.2f} Mbps").pack()
                Label(results_frame, text=f"Ping: {ping} ms").pack()

            except speedtest.ConfigRetrievalError:
                messagebox.showerror("Error", "Failed to retrieve speedtest configuration. Please check your network connection or try again later.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

            close_button.config(state=tk.NORMAL)

        threading.Thread(target=perform_speed_test, daemon=True).start()

# Plugin initialization
def init_plugin(app):
    speedtest_plugin = SpeedTestPlugin(app)
    app.add_tool_menu("Speed Test", speedtest_plugin.run_speed_test)
