"""
Script to run the collector in the background on Windows
This will start the collector as a background process
"""
import subprocess
import sys
import os

def run_in_background():
    """Start collector.py as a background process"""
    
    # Get the path to collector.py
    collector_path = os.path.join(os.path.dirname(__file__), "collector.py")
    
    # Start the process in the background (detached)
    if sys.platform == "win32":
        # Windows: Use pythonw.exe to run without console window
        pythonw = sys.executable.replace("python.exe", "pythonw.exe")
        
        # Create a startup info to hide the window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen(
            [pythonw, collector_path],
            startupinfo=startupinfo,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        print(f"✅ ChronoVision Collector started in background (PID: {process.pid})")
        print(f"📸 Taking screenshots every 60 seconds")
        print(f"\nTo stop the collector:")
        print(f"  1. Open Task Manager (Ctrl+Shift+Esc)")
        print(f"  2. Find 'pythonw.exe' process")
        print(f"  3. End the task")
        print(f"\nOr run: python stop_collector.py")
        
    else:
        # Linux/Mac: Use nohup
        process = subprocess.Popen(
            ["nohup", sys.executable, collector_path, "&"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"✅ ChronoVision Collector started in background (PID: {process.pid})")

if __name__ == "__main__":
    print("🚀 Starting ChronoVision Collector in background...")
    run_in_background()
