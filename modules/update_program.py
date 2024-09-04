# Network Monitor App
# update_program.py
# version: 1.2
# description: Handles checking for updates from the GitHub repository, installing Git automatically if needed, and pulling the latest changes.

import os
import subprocess
import sys
import platform
import tkinter as tk
from tkinter import messagebox
import webbrowser
import threading
import shutil
import requests

class ProgramUpdater:
    REPO_URL = "https://github.com/wisper1977/Python-NetMon.git"
    
    GIT_INSTALLER_URL_WINDOWS = "https://github.com/git-for-windows/git/releases/download/v2.41.0.windows.1/Git-2.41.0-64-bit.exe"
    GIT_INSTALLER_PATH_WINDOWS = os.path.join(os.getenv('TEMP'), 'git_installer.exe')

    @staticmethod
    def is_git_installed():
        """Check if Git is installed and accessible."""
        try:
            result = subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        git_path = shutil.which('git')
        return git_path is not None

    @staticmethod
    def is_git_repository():
        """Check if the current directory is a Git repository."""
        try:
            result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.strip() == 'true'
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    @staticmethod
    def install_git():
        """Install Git based on the operating system."""
        os_name = platform.system()

        if os_name == 'Windows':
            ProgramUpdater.install_git_windows()
        elif os_name == 'Linux':
            ProgramUpdater.install_git_linux()
        elif os_name == 'Darwin':  # macOS
            ProgramUpdater.install_git_mac()
        else:
            messagebox.showerror("Unsupported OS", f"Your operating system ({os_name}) is not supported for automatic Git installation.")

    @staticmethod
    def install_git_windows():
        """Download and install Git for Windows."""
        try:
            response = requests.get(ProgramUpdater.GIT_INSTALLER_URL_WINDOWS, stream=True)
            response.raise_for_status()

            with open(ProgramUpdater.GIT_INSTALLER_PATH_WINDOWS, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            subprocess.run([ProgramUpdater.GIT_INSTALLER_PATH_WINDOWS, '/VERYSILENT', '/NORESTART'], check=True)
            messagebox.showinfo("Git Installation", "Git was installed successfully. Please restart the program.")
            sys.exit(0)

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to download Git installer: {str(e)}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to install Git: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def install_git_linux():
        """Install Git on Linux using the package manager."""
        try:
            distro = platform.linux_distribution()[0].lower()
            if 'ubuntu' in distro or 'debian' in distro:
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'git'], check=True)
            elif 'centos' in distro or 'redhat' in distro or 'fedora' in distro:
                subprocess.run(['sudo', 'yum', 'install', '-y', 'git'], check=True)
            else:
                messagebox.showerror("Unsupported Linux Distro", f"Automatic Git installation is not supported on your distribution: {distro}.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to install Git on Linux: {str(e)}")

    @staticmethod
    def install_git_mac():
        """Install Git on macOS using Homebrew."""
        try:
            brew_check = subprocess.run(['brew', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if brew_check.returncode != 0:
                messagebox.showerror("Homebrew Not Found", "Homebrew is not installed. Please install Homebrew to continue.")
                return

            subprocess.run(['brew', 'install', 'git'], check=True)
            messagebox.showinfo("Git Installation", "Git was installed successfully via Homebrew. Please restart the program.")
            sys.exit(0)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to install Git on macOS: {str(e)}")

    @staticmethod
    def check_for_update():
        """Check for updates from the GitHub repository and pull the latest files."""
        def update_process():
            if not ProgramUpdater.is_git_installed():
                install_git = messagebox.askyesno("Git Not Found", "Git is not installed. Would you like to install it now?")
                if install_git:
                    ProgramUpdater.install_git()
                else:
                    messagebox.showinfo("Update Canceled", "Git is required to update the program. Please install Git and try again.")
                return

            if not ProgramUpdater.is_git_repository():
                messagebox.showerror("Not a Git Repository", "This directory is not a Git repository. Please ensure you are running this from the correct location.")
                return

            root = tk.Tk()
            root.withdraw()  # Hide the main Tkinter window
            result = messagebox.askyesno("Update Program", "This will update the program by pulling the latest files from the repository. Do you want to continue?")

            if result:
                try:
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root = os.path.join(script_dir, "..")
                    os.chdir(project_root)

                    result = subprocess.run(["git", "pull"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    messagebox.showinfo("Update Complete", f"The program has been updated successfully:\n{result.stdout}")
                    os._exit(0)

                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Update Failed", f"Git command failed: {e.stderr}")
                except Exception as e:
                    messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            else:
                messagebox.showinfo("Update Canceled", "The update has been canceled.")

        threading.Thread(target=update_process, daemon=True).start()

    @staticmethod
    def open_github_page():
        """Open the GitHub repository in the default browser."""
        webbrowser.open(ProgramUpdater.REPO_URL)
