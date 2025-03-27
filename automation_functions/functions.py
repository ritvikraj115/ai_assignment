import os
import webbrowser
import psutil
import shutil
import subprocess
import platform
import datetime
import socket

#  Application Control
def open_chrome():
    """Opens Google Chrome browser."""
    webbrowser.open("https://www.google.com")

def open_calculator():
    """Launches the system calculator."""
    os.system("calc" if platform.system() == "Windows" else "gnome-calculator")

def open_notepad():
    """Opens Notepad (Windows only)."""
    os.system("notepad" if platform.system() == "Windows" else "gedit")

def open_file_explorer():
    """Opens the system file explorer."""
    os.system("explorer" if platform.system() == "Windows" else "xdg-open .")


#  System Monitoring
def get_cpu_usage():
    """Returns the current CPU usage percentage."""
    return f"CPU Usage: {psutil.cpu_percent()}%"

def get_ram_usage():
    """Returns the current RAM usage percentage."""
    return f"RAM Usage: {psutil.virtual_memory().percent}%"

def get_disk_usage():
    """Returns disk usage statistics."""
    disk = psutil.disk_usage("/")
    return f"Disk Usage: {disk.percent}% (Used: {disk.used / (1024 ** 3):.2f}GB / Total: {disk.total / (1024 ** 3):.2f}GB)"

def get_battery_status():
    """Returns battery percentage and status."""
    battery = psutil.sensors_battery()
    if battery:
        return f"Battery: {battery.percent}% {'(Charging)' if battery.power_plugged else '(Not Charging)'}"
    return "Battery info not available."


#  Command Execution
def run_shell_command(command):
    """Executes a shell command and returns output."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Execution error: {str(e)}"

def get_system_info():
    """Returns basic system information."""
    return f"System: {platform.system()} {platform.release()} ({platform.architecture()[0]})"

def get_ip_address():
    """Returns the system's local IP address."""
    return f"IP Address: {socket.gethostbyname(socket.gethostname())}"
