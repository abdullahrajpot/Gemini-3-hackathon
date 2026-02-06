"""
Install ChronoVision to run automatically on Windows startup
"""
import os
import sys
import winshell
from pathlib import Path

def create_startup_shortcut():
    """Create a shortcut in Windows Startup folder"""
    
    # Get the startup folder path
    startup_folder = winshell.startup()
    
    # Get current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to pythonw.exe (runs without console window)
    pythonw = sys.executable.replace("python.exe", "pythonw.exe")
    
    # Path to collector.py
    collector_path = os.path.join(current_dir, "collector.py")
    
    # Create shortcut
    shortcut_path = os.path.join(startup_folder, "ChronoVision Collector.lnk")
    
    with winshell.shortcut(shortcut_path) as shortcut:
        shortcut.path = pythonw
        shortcut.arguments = f'"{collector_path}"'
        shortcut.working_directory = current_dir
        shortcut.description = "ChronoVision AI - Automatic Screen Memory Collector"
        shortcut.icon_location = (pythonw, 0)
    
    print("✅ ChronoVision installed to startup!")
    print(f"📁 Shortcut created at: {shortcut_path}")
    print("\n🎯 The collector will now start automatically when you login to Windows")
    print("\nTo remove from startup:")
    print(f"  1. Press Win+R")
    print(f"  2. Type: shell:startup")
    print(f"  3. Delete 'ChronoVision Collector.lnk'")

def remove_startup_shortcut():
    """Remove the startup shortcut"""
    startup_folder = winshell.startup()
    shortcut_path = os.path.join(startup_folder, "ChronoVision Collector.lnk")
    
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        print("✅ ChronoVision removed from startup")
    else:
        print("⚠️ Startup shortcut not found")

if __name__ == "__main__":
    print("=" * 60)
    print("  ChronoVision AI - Startup Installation")
    print("=" * 60)
    print("\nOptions:")
    print("  1. Install to startup (run automatically on login)")
    print("  2. Remove from startup")
    print("  3. Cancel")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        try:
            create_startup_shortcut()
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nTry installing 'pywin32' package:")
            print("  pip install pywin32")
    elif choice == "2":
        remove_startup_shortcut()
    else:
        print("Cancelled")
