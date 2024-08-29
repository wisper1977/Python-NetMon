import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from modules.log_manager import LogManager

class SyslogGUI:
    def __init__(self, master, app):
        """Initialize the Syslog GUI window."""
        self.master = master  # Reference to the main application window
        self.app = app  # Reference to the main application class
        self.logger = LogManager.get_instance()  # Get the singleton instance of LogManager
        
        self.window = tk.Toplevel(self.master)
        self.window.title("Syslog Viewer")
        self.window.geometry("1500x600")
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.create_widgets()
        self.load_syslog_entries()  # Load log entries when the window opens

    def create_widgets(self):
        """Create the widgets for the Syslog Viewer GUI."""
        try:
            # Create the frame for the filter options
            filter_frame = tk.Frame(self.window)
            filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

            tk.Label(filter_frame, text="Filter by Severity:").pack(side=tk.LEFT)
            self.severity_filter = ttk.Combobox(filter_frame, values=["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
            self.severity_filter.current(0)
            self.severity_filter.pack(side=tk.LEFT, padx=5)

            tk.Label(filter_frame, text="Search Description:").pack(side=tk.LEFT)
            self.description_search_entry = tk.Entry(filter_frame)
            self.description_search_entry.pack(side=tk.LEFT, padx=5)
            
            tk.Label(filter_frame, text="Search Host:").pack(side=tk.LEFT)
            self.host_search_entry = tk.Entry(filter_frame)
            self.host_search_entry.pack(side=tk.LEFT, padx=5)
            
            tk.Button(filter_frame, text="Apply", command=self.apply_filter).pack(side=tk.LEFT, padx=5)
            tk.Button(filter_frame, text="Clear", command=self.clear_filter).pack(side=tk.LEFT, padx=5)
            tk.Button(filter_frame, text="Save Log", command=self.save_log).pack(side=tk.LEFT, padx=5)

            # Create the Treeview for displaying syslog entries
            columns = ("Timestamp", "Host", "Severity", "Message")
            self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor="w")
            self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            # Add a scrollbar
            scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        except Exception as e:
            self.logger.log_error("Failed to create Syslog GUI widgets: " + str(e))
            messagebox.showerror("Error", "Failed to create Syslog GUI widgets.")

    def load_syslog_entries(self):
        """Load the syslog entries from the log file into the Treeview."""
        try:
            with open('log/syslog.log', 'r') as file:
                lines = file.readlines()
            
            for line in lines:
                parts = line.strip().split(' - ', 3)  # Split by ' - ' for the 4 parts
                if len(parts) == 4:
                    timestamp, severity, host, message = parts
                    self.tree.insert('', 'end', values=(timestamp, host, severity, message))
            
            self.adjust_column_widths()

        except Exception as e:
            self.logger.log_error("Failed to load syslog entries: " + str(e))
            messagebox.showerror("Error", "Failed to load syslog entries.")

    def apply_filter(self):
        """Apply the filter based on severity, description, and host search query."""
        try:
            severity = self.severity_filter.get()
            description_query = self.description_search_entry.get().lower()
            host_query = self.host_search_entry.get().lower()

            # Clear the existing entries in the Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Open and read the syslog file
            with open('log/syslog.log', 'r') as file:
                lines = file.readlines()
            
            # Debug: Print out queries for verification
            print(f"Filtering with Severity: {severity}, Description Query: {description_query}, Host Query: {host_query}")
            
            # Process and filter log lines
            filtered_logs = []
            for line in lines:
                parts = line.strip().split(' - ', 3)  # Split by ' - ' for the 4 parts
                if len(parts) == 4:
                    timestamp, severity_log, host, message = parts
                    
                    # Debug: Print each part to verify correct splitting
                    print(f"Log Parts: Timestamp: {timestamp}, Host: {host}, Severity: {severity_log}, Message: {message}")

                    # Apply filtering conditions
                    if (severity == "ALL" or severity_log == severity) and \
                    (description_query in message.lower()) and \
                    (host_query in host.lower()):
                        filtered_logs.append((timestamp, host, severity_log, message))

            # Check if any logs were filtered
            if not filtered_logs:
                print("No logs matched the filter criteria.")

            # Insert filtered logs into the Treeview
            for log in filtered_logs:
                self.tree.insert('', 'end', values=log)
            
            self.adjust_column_widths()

        except Exception as e:
            self.logger.log_error("Failed to apply filter: " + str(e))
            messagebox.showerror("Error", "Failed to apply filter.")

    def clear_filter(self):
        """Clear the filters and reload all syslog entries."""
        try:
            self.severity_filter.current(0)
            self.description_search_entry.delete(0, tk.END)
            self.host_search_entry.delete(0, tk.END)
            self.load_syslog_entries()
        except Exception as e:
            self.logger.log_error("Failed to clear filter: " + str(e))
            messagebox.showerror("Error", "Failed to clear filter.")

    def save_log(self):
        """Save the currently displayed log to a file."""
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log files", "*.log"), ("All files", "*.*")])
            if file_path:
                with open(file_path, 'w') as log_file:
                    for item in self.tree.get_children():
                        log_entry = self.tree.item(item)['values']
                        log_file.write(f"{log_entry[0]} - {log_entry[1]} - {log_entry[2]} - {log_entry[3]}\n")
                messagebox.showinfo("Success", "Log saved successfully.")
        except Exception as e:
            self.logger.log_error("Failed to save log: " + str(e))
            messagebox.showerror("Error", "Failed to save log.")

    def adjust_column_widths(self):
        """Adjust column widths based on the content."""
        for col in self.tree["columns"]:
            max_width = max(
                [len(str(self.tree.item(child)["values"][self.tree["columns"].index(col)])) for child in self.tree.get_children()]
                + [len(col)]  # Include the column heading width
            )
            self.tree.column(col, width=max_width * 10)  # Multiply to add some padding

    def show(self):
        """Display the Syslog Viewer window."""
        self.window.deiconify()

    def close(self):
        """Handle closing of the Syslog Viewer window."""
        try:
            self.window.destroy()
        except Exception as e:
            self.logger.log_error("Failed to close Syslog Viewer: " + str(e))
            messagebox.showerror("Error", "Failed to close Syslog Viewer.")