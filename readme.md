README: ChronoVision AI
The "Eyetic Memory" for your Laptop

ChronoVision is an automated background assistant that records your screen activity, understands it using Gemini 3, and stores it in MongoDB for instant natural language recall.

🏗️ The Stack (Why these?)
Python: The best ecosystem for AI and system automation.

Gemini 3 API: Specifically for its 1M+ Token Context (to remember weeks of data) and Multimodal Vision (to "see" your screen).

MongoDB (Atlas): To store JSON-like memory objects and perform fast searches across timestamps.

PyAutoGUI: To capture screenshots silently.

Streamlit: To build a beautiful "Google-style" search interface in minutes.

🚀 How to Build It (Phase by Phase)
Phase 1: The Collector (Background Script)
You need a Python script that runs in an infinite loop. Every 60 seconds, it:

Captures: Takes a screenshot of your current window.

Analyzes: Sends that image to Gemini 3 with a prompt: "Describe exactly what the user is doing, the apps open, and any important text visible."

Stores: Saves the JSON response into MongoDB.

Phase 2: The Database (MongoDB)
Each "Memory" in your MongoDB collection will look like this:

JSON

{
  "timestamp": "2026-02-05T10:30:00Z",
  "app_name": "Chrome",
  "activity_summary": "Watching a tutorial on Quantum Computing",
  "extracted_text": "Qubits and Entanglement explained...",
  "screenshot_path": "./storage/mem_001.jpg"
}
Phase 3: The Search (Recall Interface)
Build a search bar where you ask: "When was I looking at flight tickets to Tokyo?"

Behind the scenes: The app queries MongoDB for keywords or uses Gemini 3 to scan the last 100 summaries to find the matching timestamp.

🛠️ Step-by-Step Installation
1. Prerequisites
Install the required Python libraries:

Bash

pip install -U google-genai pymongo pyautogui pillow streamlit python-dotenv
2. MongoDB Setup
Create a free cluster at MongoDB Atlas.

Get your Connection String.

Create a Database named ChronoVision and a Collection named Memories.

3. Basic "Memory Capture" Script (collector.py)
Python

import pyautogui
from google import genai
from pymongo import MongoClient
import time
from datetime import datetime

# Setup
client_ai = genai.Client(api_key="YOUR_GEMINI_KEY")
db_client = MongoClient("YOUR_MONGODB_CONNECTION_STRING")
db = db_client.ChronoVision

def save_memory():
    # 1. Capture
    img = pyautogui.screenshot()
    img_path = f"mem_{int(time.time())}.jpg"
    img.save(img_path)

    # 2. Gemini 3 Vision
    with open(img_path, "rb") as f:
        response = client_ai.models.generate_content(
            model="gemini-3-pro-preview",
            contents=["Describe this screen activity in detail.", f.read()]
        )

    # 3. MongoDB Store
    memory = {
        "timestamp": datetime.utcnow(),
        "summary": response.text,
        "image_path": img_path
    }
    db.Memories.insert_one(memory)
    print("Memory captured and stored.")

while True:
    save_memory()
    time.sleep(60) # Capture every minute
🏆 How to Win the Hackathon
Semantic Search: Don't just search for exact words. Use Gemini 3 to translate the user's "vibe" into a query (e.g., User asks "I was stressed about money" -> AI searches for "Bank statements" or "Bills").

Privacy Guard: Add a feature where if the app name is "Incognito" or "1Password," the collector automatically pauses.

Visual Timeline: In your Streamlit app, show a "Timeline" of screenshots so the user can scroll through their day visually.