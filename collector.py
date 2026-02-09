import os
import time
from datetime import datetime
from pathlib import Path
import pyautogui
from google import genai
from pymongo import MongoClient
from dotenv import load_dotenv
import psutil
import logging
import sys

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    filename='collector.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

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
    'binance', 'trading', 'investment', 'account balance',
    
    # Password Managers & Security
    'password', '1password', 'lastpass', 'bitwarden', 'keepass',
    'dashlane', 'nordpass', 'authenticator', '2fa', 'otp',
    'sign in', 'log in', 'login', 'signin', 'sign-in',
    'enter password', 'password required', 'credentials',
    
    # Private Browsing
    'incognito', 'private', 'inprivate', 'private browsing',
    
    # Sensitive Apps
    'vpn', 'tor browser', 'signal', 'telegram secret',
    
    # Personal & Authentication
    'medical', 'health', 'doctor', 'prescription',
    'tax', 'irs', 'social security', 'ssn',
    'authentication', 'verify', 'security code',
    'unlock', 'passcode', 'pin code'
]

# Setup storage directory
Path(STORAGE_PATH).mkdir(exist_ok=True)

# Initialize clients
try:
    client_ai = genai.Client(api_key=GEMINI_API_KEY)
    db_client = MongoClient(MONGODB_URI)
    db = db_client[DB_NAME]
    collection = db[COLLECTION_NAME]
    logging.info("Clients initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize clients: {e}")
    sys.exit(1)

def get_active_window_title():
    """Get the title of the currently active window"""
    try:
        import win32gui
        import win32process
        
        # Get foreground window
        hwnd = win32gui.GetForegroundWindow()
        
        # Get window title
        title = win32gui.GetWindowText(hwnd)
        
        # Get process ID
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        
        # Get process name
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            return f"{title} {process_name}".lower()
        except:
            return title.lower()
    except Exception as e:
        logging.warning(f"Error getting window title with win32gui: {e}")
        # Fallback: try to get any active process
        try:
            for proc in psutil.process_iter(['name', 'exe']):
                try:
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
    
    # Check each keyword
    for keyword in SENSITIVE_KEYWORDS:
        if keyword in window_title_lower:
            return True, keyword
    
    # Additional checks for common patterns
    sensitive_patterns = [
        'sign in', 'log in', 'login', 'signin',
        'enter password', 'password required',
        'authentication', 'verify', 'security',
        'account', 'credentials'
    ]
    
    for pattern in sensitive_patterns:
        if pattern in window_title_lower:
            return True, pattern
    
    return False, None

def save_memory():
    """Capture screenshot, analyze with Gemini, and store in MongoDB"""
    try:
        logging.info("Attempting used to capture memory...")
        # Check active window for sensitive content
        window_title = get_active_window_title()
        is_sensitive, matched_keyword = is_sensitive_content(window_title)
        
        if is_sensitive:
            logging.info(f"🔒 SKIPPED - Sensitive: '{matched_keyword}' in '{window_title[:50]}'")
            return
        
        # 1. Capture screenshot
        timestamp = int(time.time())
        img_path = os.path.join(STORAGE_PATH, f"mem_{timestamp}.jpg")
        
        try:
            img = pyautogui.screenshot()
            img.save(img_path)
            logging.info(f"Screenshot saved to {img_path}")
        except Exception as e:
             logging.error(f"Screenshot failed: {e}")
             return
        
        # Quick OCR check for sensitive text in screenshot (optional but recommended)
        # This adds an extra layer of protection
        try:
            import pytesseract
            from PIL import Image
            
            # Sample a small portion of the image for quick text detection
            sample = img.crop((img.width//4, img.height//4, 3*img.width//4, 3*img.height//4))
            text = pytesseract.image_to_string(sample).lower()
            
            # Check for sensitive keywords in the image text
            for keyword in ['password', 'login', 'sign in', 'credit card', 'ssn', 'social security']:
                if keyword in text:
                    logging.info(f"🔒 SKIPPED - Detected '{keyword}' in screenshot via OCR")
                    try:
                        os.remove(img_path)
                    except:
                        pass
                    return
        except ImportError:
            pass # OCR skipped
        except Exception as e:
            logging.warning(f"OCR check failed: {e}")
        
        # 2. Analyze with Gemini Vision
        analysis_text = "Analysis pending/skipped"
        try:
            logging.info("Attempting to upload file to Gemini...")
            uploaded_file = client_ai.files.upload(file=img_path)
            logging.info(f"Image uploaded to Gemini. URI: {uploaded_file.uri}")
            
            prompt = "Describe this screen activity in detail. Include: apps open, what the user is doing, and any important text visible."
            logging.info("Sending prompt to Gemini model...")
            response = client_ai.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, uploaded_file]
            )
            logging.info("Gemini analysis complete.")
            analysis_text = response.text
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                logging.warning(f"Gemini Query/Quota Limit Exceeded. Skipping analysis. Error: {e}")
                analysis_text = "Analysis skipped due to API quota limits."
            else:
                logging.error(f"Gemini API Error (Analysis Step): {e}")
                analysis_text = "Analysis failed."
        
        # 3. Store in MongoDB
        try:
            # Encode image to base64 for cloud retrieval
            import base64
            from io import BytesIO
            
            buffered = BytesIO()
            img.save(buffered, format="JPEG", quality=70) # Compress slightly
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            memory = {
                "timestamp": datetime.utcnow(),
                "summary": analysis_text,
                "image_path": img_path,
                "image_data": img_str, # Store base64 data
                "captured_at": timestamp,
                "window_title": window_title
            }
            collection.insert_one(memory)
            logging.info(f"✅ Memory captured and stored (with Base64). Window: {window_title[:60]}")
        except Exception as e:
            logging.error(f"MongoDB Error: {e}")

    except Exception as e:
        logging.error(f"Unexpected error in save_memory: {e}")

def main():
    """Main loop to continuously capture memories"""
    logging.info("=" * 60)
    logging.info("  ChronoVision Collector - Started")
    logging.info("=" * 60)
    logging.info(f"📸 Capturing every {CAPTURE_INTERVAL} seconds")
    
    while True:
        save_memory()
        time.sleep(CAPTURE_INTERVAL)

if __name__ == "__main__":
    main()
