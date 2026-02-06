import os
import time
from datetime import datetime
from pathlib import Path
import pyautogui
from google import genai
from pymongo import MongoClient
from dotenv import load_dotenv
import psutil

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_CONNECTION_STRING")
DB_NAME = os.getenv("MONGODB_DATABASE", "ChronoVision")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION", "Memories")
CAPTURE_INTERVAL = int(os.getenv("CAPTURE_INTERVAL", 60))
STORAGE_PATH = os.getenv("SCREENSHOT_STORAGE_PATH", "./storage")

# Privacy-sensitive apps and windows to skip
SENSITIVE_KEYWORDS = [
    # Banking & Finance
    'bank', 'banking', 'paypal', 'venmo', 'stripe', 'payment',
    'credit card', 'debit card', 'wallet', 'crypto', 'coinbase',
    'binance', 'trading', 'investment',
    
    # Password Managers & Security
    'password', '1password', 'lastpass', 'bitwarden', 'keepass',
    'dashlane', 'nordpass', 'authenticator', '2fa', 'otp',
    
    # Private Browsing
    'incognito', 'private', 'inprivate',
    
    # Sensitive Apps
    'vpn', 'tor browser', 'signal', 'telegram secret',
    
    # Personal
    'medical', 'health', 'doctor', 'prescription',
    'tax', 'irs', 'social security'
]

# Setup storage directory
Path(STORAGE_PATH).mkdir(exist_ok=True)

# Initialize clients
client_ai = genai.Client(api_key=GEMINI_API_KEY)
db_client = MongoClient(MONGODB_URI)
db = db_client[DB_NAME]
collection = db[COLLECTION_NAME]

def get_active_window_title():
    """Get the title of the currently active window"""
    try:
        import win32gui
        window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(window)
        return title.lower()
    except:
        # Fallback method using psutil
        try:
            for proc in psutil.process_iter(['name', 'pid']):
                try:
                    # Get process name
                    proc_name = proc.info['name'].lower()
                    return proc_name
                except:
                    continue
        except:
            pass
    return ""

def is_sensitive_content(window_title):
    """Check if current window contains sensitive content"""
    window_title_lower = window_title.lower()
    
    for keyword in SENSITIVE_KEYWORDS:
        if keyword in window_title_lower:
            return True, keyword
    
    return False, None

def save_memory():
    """Capture screenshot, analyze with Gemini, and store in MongoDB"""
    try:
        # Check active window for sensitive content
        window_title = get_active_window_title()
        is_sensitive, matched_keyword = is_sensitive_content(window_title)
        
        if is_sensitive:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⏭️  Skipped - Sensitive content detected: '{matched_keyword}'")
            return
        
        # 1. Capture screenshot
        timestamp = int(time.time())
        img_path = os.path.join(STORAGE_PATH, f"mem_{timestamp}.jpg")
        img = pyautogui.screenshot()
        img.save(img_path)
        
        # 2. Analyze with Gemini Vision
        # Upload the file first
        uploaded_file = client_ai.files.upload(file=img_path)
        
        # Generate content with the uploaded file
        response = client_ai.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "Describe this screen activity in detail. Include: apps open, what the user is doing, and any important text visible.",
                uploaded_file
            ]
        )
        
        # 3. Store in MongoDB
        memory = {
            "timestamp": datetime.utcnow(),
            "summary": response.text,
            "image_path": img_path,
            "captured_at": timestamp,
            "window_title": window_title
        }
        collection.insert_one(memory)
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Memory captured and stored.")
        print(f"Summary: {response.text[:100]}...")
        
    except Exception as e:
        print(f"Error capturing memory: {e}")

def main():
    """Main loop to continuously capture memories"""
    print("=" * 60)
    print("  ChronoVision Collector - Privacy Protected")
    print("=" * 60)
    print(f"📸 Capturing every {CAPTURE_INTERVAL} seconds")
    print(f"🔒 Privacy mode: ON")
    print(f"🛡️  Skipping sensitive content automatically")
    print(f"\n⏭️  Will skip windows containing:")
    print(f"   - Banking & payment apps")
    print(f"   - Password managers")
    print(f"   - Private/Incognito browsing")
    print(f"   - Medical & tax information")
    print("=" * 60)
    print()
    
    while True:
        save_memory()
        time.sleep(CAPTURE_INTERVAL)

if __name__ == "__main__":
    main()
