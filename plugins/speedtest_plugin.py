# Speedtest Plugin
# speedtest_plugin.py
# version: 1.2
# description:

import threading
import tkinter as tk
import speedtest
from tkinter import Toplevel, Label, Button, messagebox

class SpeedTestPlugin:
    def __init__(self, app):
        self.app = app
        self.speed_test_thread = None
        self.speed_test_window = None

    def run_speed_test(self):
        """Run the speed test and update the GUI with the results."""
        self.speed_test_window = Toplevel(self.app.root)
        self.speed_test_window.title("Speed Test")
        self.app.set_icon(self.speed_test_window)

        Label(self.speed_test_window, text="Running speed test...").pack(pady=10)

        self.results_frame = tk.Frame(self.speed_test_window)
        self.results_frame.pack(pady=10)

        self.close_button = Button(self.speed_test_window, text="Close", state=tk.DISABLED, command=self.on_close)
        self.close_button.pack(pady=5)

        # Start the speed test in a background thread
        self.speed_test_thread = threading.Thread(target=self.perform_speed_test, daemon=True)
        self.speed_test_thread.start()

        # Bind the close event to ensure the thread stops if the window is closed
        self.speed_test_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def perform_speed_test(self):
        """Perform the speed test and update the GUI with the results."""
        try:
            st = speedtest.Speedtest()
            download_speed = st.download() / 10**6  # Convert to Mbps
            upload_speed = st.upload() / 10**6      # Convert to Mbps
            ping = st.results.ping

            # Queue the updates to the main thread
            if self.speed_test_window is not None:
                self.app.update_queue.put(lambda: self.display_results(download_speed, upload_speed, ping))

        except speedtest.ConfigRetrievalError:
            if self.speed_test_window is not None:
                self.app.update_queue.put(lambda: messagebox.showerror("Error", "Failed to retrieve speedtest configuration. Please check your network connection or try again later."))
        except Exception as e:
            if self.speed_test_window is not None:
                self.app.update_queue.put(lambda: messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}"))
        finally:
            # Enable the close button
            if self.speed_test_window is not None:
                self.app.update_queue.put(lambda: self.close_button.config(state=tk.NORMAL))

    def display_results(self, download_speed, upload_speed, ping):
        """Display the results in the GUI."""
        if self.speed_test_window is not None:
            Label(self.results_frame, text=f"Download: {download_speed:.2f} Mbps").pack()
            Label(self.results_frame, text=f"Upload: {upload_speed:.2f} Mbps").pack()
            Label(self.results_frame, text=f"Ping: {ping} ms").pack()

    def on_close(self):
        """Handle the closing of the speed test window."""
        if self.speed_test_window is not None:
            self.speed_test_window.destroy()
            self.speed_test_window = None
            if self.speed_test_thread and self.speed_test_thread.is_alive():
                self.speed_test_thread = None  # This allows the thread to exit gracefully

# Plugin initialization
def init_plugin(app):
    speedtest_plugin = SpeedTestPlugin(app)
    app.add_tool_menu("Speed Test", speedtest_plugin.run_speed_test)