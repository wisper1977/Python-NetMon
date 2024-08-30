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
        """Run the speed test and return the results."""
        try:
            st = speedtest.Speedtest()
            st.download()
            st.upload()
            return st.results.dict()
        except Exception as e:
            self.app.logger.log("ERROR", f"Speedtest failed: {str(e)}")
            messagebox.showerror("Error", f"Speedtest failed: {str(e)}")
            return None

    def show_speedtest_gui(self):
        """Show the SpeedTest GUI window."""
        speedtest_window = Toplevel(self.app.root)
        speedtest_window.title("SpeedTest")
        self.app.set_icon(speedtest_window)

        Label(speedtest_window, text="Running speed test...").pack(pady=10)

        def run_test():
            Button(speedtest_window, text="Close", state=tk.DISABLED).pack(pady=10)
            results = self.run_speed_test()
            if results:
                Label(speedtest_window, text=f"Download: {results['download'] / 1_000_000:.2f} Mbps").pack(pady=5)
                Label(speedtest_window, text=f"Upload: {results['upload'] / 1_000_000:.2f} Mbps").pack(pady=5)
                Label(speedtest_window, text=f"Ping: {results['ping']} ms").pack(pady=5)
            Button(speedtest_window, text="Close", command=speedtest_window.destroy).pack(pady=10)

        threading.Thread(target=run_test, daemon=True).start()

# Plugin initialization
def init_plugin(app):
    speedtest_plugin = SpeedTestPlugin(app)
    app.plugins.append(speedtest_plugin)
    app.add_tool_menu("SpeedTest", speedtest_plugin.show_speedtest_gui)