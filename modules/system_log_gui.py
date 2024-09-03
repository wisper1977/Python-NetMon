import tkinter as tk
from tkinter import Toplevel, Label, Text, Scrollbar, RIGHT, Y, END, filedialog
from modules.system_log import SystemLog

class SystemLogGUI:
    def __init__(self, root, config, logger):
        self.root = root
        self.config = config
        self.logger = logger

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
        scrollbar = Scrollbar(log_window, orient=tk.VERTICAL)
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

    def set_icon(self, window):
        """Sets the application icon for the provided window."""
        window.iconbitmap('media/NetMon.ico')
