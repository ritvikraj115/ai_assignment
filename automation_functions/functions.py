import os
import webbrowser
import psutil  # For system monitoring

def open_chrome():
    """Opens Google Chrome browser."""
    webbrowser.open("https://www.google.com")

def open_calculator():
    """Launches the system calculator."""
    os.system("calc")

def get_cpu_usage():
    """Returns the current CPU usage as a string."""
    return f"CPU Usage: {psutil.cpu_percent()}%"

def get_ram_usage():
    """Returns the current RAM usage as a string."""
    return f"RAM Usage: {psutil.virtual_memory().percent}%"
