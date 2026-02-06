"""
Script to stop the background collector process
"""
import subprocess
import sys

def stop_collector():
    """Stop the collector process"""
    
    if sys.platform == "win32":
        # Windows: Kill pythonw.exe processes running collector.py
        try:
            # Find and kill the process
            subprocess.run(
                ['taskkill', '/F', '/IM', 'pythonw.exe'],
                capture_output=True
            )
            print("✅ ChronoVision Collector stopped")
        except Exception as e:
            print(f"❌ Error stopping collector: {e}")
            print("Please manually stop it from Task Manager")
    else:
        # Linux/Mac: Kill python processes running collector.py
        try:
            subprocess.run(
                ['pkill', '-f', 'collector.py'],
                capture_output=True
            )
            print("✅ ChronoVision Collector stopped")
        except Exception as e:
            print(f"❌ Error stopping collector: {e}")

if __name__ == "__main__":
    print("🛑 Stopping ChronoVision Collector...")
    stop_collector()
