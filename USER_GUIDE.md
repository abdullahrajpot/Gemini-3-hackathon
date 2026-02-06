# 🧠 ChronoVision AI - User Guide

## What is ChronoVision?

ChronoVision is your personal "eyetic memory" - it runs silently in the background, taking screenshots of your computer activity every 60 seconds. Using AI, it understands what you're doing and stores it in a searchable database. Days or weeks later, you can ask "What was I doing on Monday?" or "When was I looking at flight tickets?" and instantly find the answer with screenshots!

---

## 🚀 Quick Start

### Option 1: One-Click Start (Easiest)
Double-click `START_CHRONOVISION.bat` - this will:
1. Start the background collector
2. Open the search interface in your browser

### Option 2: Manual Start

**Step 1: Start Background Collector**
```bash
python run_background.py
```
This runs silently in the background, capturing screenshots every 60 seconds.

**Step 2: Open Search Interface**
```bash
streamlit run search_app.py
```
This opens the web interface where you can search your memories.

---

## 🔍 How to Search Your Memories

### Keyword Search
Simple text matching - fast and direct:
- "flight tickets"
- "Python tutorial"
- "email from John"

### AI-Powered Search (Recommended)
Let Gemini understand your question:
- "When was I stressed about money?"
- "What was I working on last Monday afternoon?"
- "Show me when I was watching YouTube videos"

### Date Filters
Use the sidebar to filter by:
- Today
- Yesterday
- Last 7 Days
- Last 30 Days
- Custom Date Range

---

## 📊 Features

### 1. Memory Cards
Each result shows:
- 📅 Date and time
- ⏰ How long ago (e.g., "2 days ago")
- 📝 AI description of what you were doing
- 🖼️ Screenshot (click to expand)

### 2. Timeline View
Enable in sidebar to see a chronological list of all activities

### 3. Stats Dashboard
- Total memories captured
- Days tracked
- Latest capture time

---

## 🛑 How to Stop the Collector

### Option 1: Using Script
```bash
python stop_collector.py
```

### Option 2: Task Manager
1. Press `Ctrl + Shift + Esc`
2. Find `pythonw.exe` process
3. End task

---

## ⚙️ Configuration

Edit `.env` file to customize:

```env
# How often to capture (in seconds)
CAPTURE_INTERVAL=60

# Where to store screenshots
SCREENSHOT_STORAGE_PATH=./storage
```

**Recommended intervals:**
- 30 seconds: Very detailed tracking (uses more storage)
- 60 seconds: Balanced (default)
- 120 seconds: Light tracking (saves storage)

---

## 💡 Use Cases

### For Students
- "What lecture was I watching on Tuesday?"
- "When did I work on my math assignment?"

### For Professionals
- "What was I working on during the client call?"
- "When did I review that contract?"

### For Everyone
- "What YouTube video made me laugh yesterday?"
- "When was I shopping for that product?"
- "What was I doing when I got that idea?"

---

## 🔒 Privacy Tips

1. **Pause During Sensitive Work**
   - Stop the collector: `python stop_collector.py`
   - Restart when done: `python run_background.py`

2. **Auto-Pause Feature** (Coming Soon)
   - Automatically pause when incognito browser detected
   - Pause when password managers are open

3. **Local Storage**
   - All screenshots stored locally in `./storage` folder
   - You control your data

---

## 📈 Storage Management

Screenshots accumulate over time:
- 1 screenshot/minute = ~1,440 images/day
- Average size: 200-500 KB per image
- Daily storage: ~300-700 MB

**To clean old memories:**
```python
# Delete memories older than 30 days
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
db = client.ChronoVision

thirty_days_ago = datetime.utcnow() - timedelta(days=30)
old_memories = db.Memories.find({"timestamp": {"$lt": thirty_days_ago}})

# Delete images and database entries
for memory in old_memories:
    if os.path.exists(memory['image_path']):
        os.remove(memory['image_path'])
    db.Memories.delete_one({"_id": memory["_id"]})

print("Old memories cleaned!")
```

---

## 🏆 Hackathon Tips

### Impressive Features to Add:

1. **Smart Summaries**
   - "Summarize my day"
   - "What did I accomplish this week?"

2. **Activity Analytics**
   - Most used apps
   - Productivity heatmap
   - Time spent on different tasks

3. **Voice Search**
   - Speak your query instead of typing

4. **Export Reports**
   - Generate PDF reports of your activities
   - Share specific memories

5. **Privacy Guard**
   - Auto-detect sensitive apps
   - Blur sensitive information in screenshots

---

## 🐛 Troubleshooting

### Collector Not Capturing
- Check if process is running: Task Manager → pythonw.exe
- Verify MongoDB connection in `.env`
- Check Gemini API key is valid

### Search Not Finding Results
- Try different keywords
- Use AI-powered search mode
- Check date filter settings

### Screenshots Not Displaying
- Verify `./storage` folder exists
- Check file paths in MongoDB

---

## 📞 Need Help?

Check the logs:
- Collector logs: Check console output when running manually
- Search app logs: Check Streamlit console

---

**Enjoy your eyetic memory! 🧠✨**
