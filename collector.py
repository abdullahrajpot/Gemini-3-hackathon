import os
import time
from datetime import datetime
from pathlib import Path
import pyautogui
from google import genai
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_CONNECTION_STRING")
DB_NAME = os.getenv("MONGODB_DATABASE", "ChronoVision")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION", "Memories")
CAPTURE_INTERVAL = int(os.getenv("CAPTURE_INTERVAL", 60))
STORAGE_PATH = os.getenv("SCREENSHOT_STORAGE_PATH", "./storage")

# Setup storage directory
Path(STORAGE_PATH).mkdir(exist_ok=True)

# Initialize clients
client_ai = genai.Client(api_key=GEMINI_API_KEY)
db_client = MongoClient(MONGODB_URI)
db = db_client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_memory():
    """Capture screenshot, analyze with Gemini, and store in MongoDB"""
    try:
        # 1. Capture screenshot
        timestamp = int(time.time())
        img_path = os.path.join(STORAGE_PATH, f"mem_{timestamp}.jpg")
        img = pyautogui.screenshot()
        img.save(img_path)
        
        # 2. Analyze with Gemini Vision
        with open(img_path, "rb") as f:
            response = client_ai.models.generate_content(
                model="gemini-3-pro-preview",
                contents=[
                    "Describe this screen activity in detail. Include: apps open, what the user is doing, and any important text visible.",
                    f.read()
                ]
            )
        
        # 3. Store in MongoDB
        memory = {
            "timestamp": datetime.utcnow(),
            "summary": response.text,
            "image_path": img_path,
            "captured_at": timestamp
        }
        collection.insert_one(memory)
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Memory captured and stored.")
        
    except Exception as e:
        print(f"Error capturing memory: {e}")

def main():
    """Main loop to continuously capture memories"""
    print("ChronoVision Collector started...")
    print(f"Capturing every {CAPTURE_INTERVAL} seconds")
    
    while True:
        save_memory()
        time.sleep(CAPTURE_INTERVAL)

if __name__ == "__main__":
    main()
