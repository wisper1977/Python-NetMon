import tkinter as tk
from tkinter import messagebox, filedialog
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class FTPServerPlugin:
    def __init__(self, root):
        self.root = root
        self.server = None
        self.server_thread = None

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame, text="Port:").grid(row=0, column=0, padx=10, pady=10)
        self.port_entry = tk.Entry(self.frame)
        self.port_entry.grid(row=0, column=1, padx=10, pady=10)
        self.port_entry.insert(0, "21")

        tk.Label(self.frame, text="Root Directory:").grid(row=1, column=0, padx=10, pady=10)
        self.root_dir_entry = tk.Entry(self.frame)
        self.root_dir_entry.grid(row=1, column=1, padx=10, pady=10)
        self.browse_button = tk.Button(self.frame, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=1, column=2, padx=10, pady=10)

        self.start_button = tk.Button(self.frame, text="Start FTP Server", command=self.start_server)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.stop_button = tk.Button(self.frame, text="Stop FTP Server", command=self.stop_server)
        self.stop_button.grid(row=2, column=2, padx=10, pady=10)
        self.stop_button.config(state=tk.DISABLED)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.root_dir_entry.delete(0, tk.END)
            self.root_dir_entry.insert(0, directory)

    def start_server(self):
        port = int(self.port_entry.get())
        root_dir = self.root_dir_entry.get()

        if not root_dir:
            messagebox.showerror("Error", "Please select a root directory")
            return

        # Set up the FTP server
        authorizer = DummyAuthorizer()
        authorizer.add_anonymous(root_dir, perm="elradfmw")

        handler = FTPHandler
        handler.authorizer = authorizer

        self.server = FTPServer(("0.0.0.0", port), handler)

        # Start the server
        self.server_thread = self.server.serve_forever
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.root.after(100, self.server_thread)

        messagebox.showinfo("FTP Server", f"FTP server started on port {port}")

    def stop_server(self):
        if self.server:
            self.server.close_all()
            self.server = None
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            messagebox.showinfo("FTP Server", "FTP server stopped")

def init_plugin(application):
    """Initialize the plugin and add it to the Tools menu."""
    application.add_tool_menu(
        label="FTP Server",
        command=lambda: open_ftp_server_window(application.root)
    )

def open_ftp_server_window(root):
    """Open the FTP Server Plugin GUI in a new Toplevel window."""
    ftp_window = tk.Toplevel(root)
    ftp_window.title("FTP Server")
    ftp_window.geometry("400x200")  # Set a reasonable default size for the window
    
    # Set the custom icon
    ftp_window.iconbitmap('media/NetMon.ico') 
    
    FTPServerPlugin(ftp_window)
