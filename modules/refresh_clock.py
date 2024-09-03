# Network Monitor App
# refresh_clock.py
# version: 1.2
# description: Handles the refresh clock.

import tkinter as tk
from tkinter import ttk

class RefreshClock:
    def __init__(self, root, network_monitor, interval_callback):
        self.root = root
        self.network_monitor = network_monitor
        self.interval_callback = interval_callback

        self.refresh_interval = network_monitor.refresh_interval
        self.remaining_time = self.refresh_interval // 1000

        self.refresh_label = tk.Label(self.root, text="Next refresh in:")
        self.refresh_label.pack()

        self.progress_bar = ttk.Progressbar(self.root, maximum=self.refresh_interval // 1000, length=300)
        self.progress_bar.pack()
        self.progress_bar['value'] = self.remaining_time

        self._run_refresh_clock()

    def _run_refresh_clock(self):
        if self.remaining_time <= 0:
            self.remaining_time = self.refresh_interval // 1000
            self.interval_callback()  # Trigger the actual refresh

        self.remaining_time -= 1
        self.refresh_label.config(text=f"Next refresh in: {self.remaining_time} seconds")
        self.progress_bar['value'] = self.remaining_time

        self.root.after(1000, self._run_refresh_clock)

    def update_display(self, remaining_time):
        self.refresh_label.config(text=f"Next refresh in: {remaining_time} seconds")
        self.progress_bar['value'] = remaining_time