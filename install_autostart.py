"""
Install ChronoVision to run automatically on Windows startup
"""
import os
import sys
from pathlib import Path

try:
    import win32com.client
except ImportError:
    print("Error: pywin32 is not installed. Please run: pip install pywin32")
    sys.exit(1)

def create_startup_shortcut():
    """Create a shortcut in Windows Startup folder using pywin32"""
    
    # Get the startup folder path
    shell = win32com.client.Dispatch("WScript.Shell")
    startup_folder = shell.SpecialFolders("Startup")
    
    # Get current script directory and paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pythonw_path = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    collector_path = os.path.join(current_dir, "collector.py")
    
    # Check if pythonw exists, if not fallback to python.exe
    if not os.path.exists(pythonw_path):
        pythonw_path = sys.executable
    
    # Shortcut path
    shortcut_path = os.path.join(startup_folder, "ChronoVision Collector.lnk")
    
    try:
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = pythonw_path
        shortcut.Arguments = f'"{collector_path}"'
        shortcut.WorkingDirectory = current_dir
        shortcut.Description = "ChronoVision AI - Automatic Screen Memory Collector"
        shortcut.IconLocation = pythonw_path
        shortcut.Save()
        
        print("✅ ChronoVision installed to startup!")
        print(f"📁 Shortcut created at: {shortcut_path}")
        print("\n🎯 The collector will now start automatically when you login to Windows.")
        return True
    except Exception as e:
        print(f"❌ Failed to create shortcut: {e}")
        return False

if __name__ == "__main__":
    create_startup_shortcut()
