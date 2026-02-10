"""
Test screenshot capture functionality
"""
import pyautogui
from pathlib import Path
import os

def test_screenshot_capture():
    print("🧪 Testing Screenshot Capture...")
    print()
    
    # Create storage directory
    storage_path = Path("./storage")
    storage_path.mkdir(exist_ok=True)
    print(f"✅ Storage directory ready: {storage_path.absolute()}")
    
    # Capture screenshot
    try:
        print("📸 Capturing screenshot...")
        img = pyautogui.screenshot()
        
        # Save to file
        test_path = storage_path / "test_capture.jpg"
        img.save(test_path)
        
        # Verify file exists
        if test_path.exists():
            file_size = os.path.getsize(test_path)
            print(f"✅ Screenshot saved successfully!")
            print(f"   Path: {test_path.absolute()}")
            print(f"   Size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")
            print(f"   Dimensions: {img.size}")
            print()
            print("✅ Screenshot test PASSED")
            return True
        else:
            print("❌ Screenshot file not found")
            return False
            
    except Exception as e:
        print(f"❌ Screenshot test FAILED: {e}")
        return False

if __name__ == "__main__":
    test_screenshot_capture()
