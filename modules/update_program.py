# Network Monitor App
# update_program.py
# version: 1.2
# description: Handles checking for updates from the GitHub repository and pulling the latest changes.

import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import webbrowser

class ProgramUpdater:
    REPO_URL = "https://github.com/wisper1977/Python-NetMon.git"

    @staticmethod
    def check_for_update():
        """Check for updates from the GitHub repository and pull the latest files."""
        # Get confirmation from the user
        root = tk.Tk()
        root.withdraw()  # Hide the main Tkinter window
        result = messagebox.askyesno("Update Program", "This will update the program by pulling the latest files from the repository. Do you want to continue?")

        if result:
            try:
                # Change directory to the location of the main script (assumes it's the root of the Git repo)
                script_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.join(script_dir, "..")

                # Navigate to the project root
                os.chdir(project_root)

                # Run the git pull command to fetch updates
                subprocess.run(["git", "pull", ProgramUpdater.REPO_URL], check=True)

                messagebox.showinfo("Update Complete", "The program has been updated successfully. Please restart the application.")
                
                # Exit the program after the update
                os._exit(0)

            except subprocess.CalledProcessError as e:
                messagebox.showerror("Update Failed", f"An error occurred while updating: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        else:
            messagebox.showinfo("Update Canceled", "The update has been canceled.")

    @staticmethod
    def open_github_page():
        """Open the GitHub repository in the default browser."""
        webbrowser.open(ProgramUpdater.REPO_URL)
