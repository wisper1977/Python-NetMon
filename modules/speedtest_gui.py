#Description:
#Version:1.1.4

import tkinter as tk
from tkinter import ttk
from modules.speedtest import SpeedTest
import threading

class SpeedTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("250x300")

        # Create the SpeedTest instance
        self.speed_test = SpeedTest()

        # Add GUI elements
        self.label = ttk.Label(root, text="Press 'Start Test' to begin", font=("Arial", 12))
        self.label.pack(pady=20)

        self.start_button = ttk.Button(root, text="Start Test", command=self.run_speed_test)
        self.start_button.pack(pady=10)

        self.result_label = ttk.Label(root, text="", font=("Arial", 10))
        self.result_label.pack(pady=10)

        self.close_button = ttk.Button(root, text="Close", command=self.close_window)
        self.close_button.pack(pady=10)
        self.close_button.config(state=tk.DISABLED)  # Disable initially

    def run_speed_test(self):
        # Disable start button and show waiting indicator
        self.start_button.config(state=tk.DISABLED)
        self.result_label.config(text="Running speed test...")
        self.close_button.config(state=tk.DISABLED)  # Disable close button until test is complete

        # Run speed test in a separate thread
        threading.Thread(target=self.perform_speed_test).start()

    def perform_speed_test(self):
        try:
            # Run the speed test and update the result labels
            download_speed, upload_speed, ping = self.speed_test.get_speeds()
            result_text = (f"Download Speed: {download_speed:.2f} Mbps\n"
                           f"Upload Speed: {upload_speed:.2f} Mbps\n"
                           f"Ping: {ping:.2f} ms")
            # Update GUI from the main thread
            self.root.after(0, self.update_results, result_text)
        except Exception as e:
            # Update GUI from the main thread with error message
            self.root.after(0, self.update_results, f"Error: {e}")

    def update_results(self, result_text):
        self.result_label.config(text=result_text)
        self.start_button.config(state=tk.NORMAL)
        self.close_button.config(state=tk.NORMAL)  # Enable close button after test

    def close_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTestGUI(root)
    root.mainloop()
