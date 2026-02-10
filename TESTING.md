# ChronoVision Testing Instructions

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Environment Setup Verification](#environment-setup-verification)
- [Component Testing](#component-testing)
- [Demo Data Generation](#demo-data-generation)
- [End-to-End Testing](#end-to-end-testing)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before testing, ensure you have:

1. **Python 3.8+** installed
2. **MongoDB Atlas** account with a cluster created
3. **Gemini API Key** from Google AI Studio
4. All dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Setup Verification

### 1. Check Environment Variables

Ensure your `.env` file contains:

```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_CONNECTION_STRING=your_mongodb_connection_string
MONGODB_DATABASE=ChronoVision
MONGODB_COLLECTION=Memories
CAPTURE_INTERVAL=60
SCREENSHOT_STORAGE_PATH=./storage
```

### 2. Verify Dependencies

Run the import test script:

```bash
python test_imports.py
```

**Expected Output:**
```
✅ All imports successful
✅ google-genai: OK
✅ pymongo: OK
✅ pyautogui: OK
✅ streamlit: OK
✅ psutil: OK
```

### 3. Check Gemini API Access

```bash
python check_models.py
```

**Expected Output:**
```
Available Gemini Models:
- gemini-2.5-flash
- gemini-2.5-pro
...
```

---

## Component Testing

### Test 1: MongoDB Connection

**Purpose:** Verify database connectivity

**Steps:**
1. Open Python interactive shell:
   ```bash
   python
   ```

2. Run the following:
   ```python
   from pymongo import MongoClient
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
   db = client.ChronoVision
   print(f"✅ Connected to MongoDB: {db.name}")
   print(f"Collections: {db.list_collection_names()}")
   ```

**Expected Result:**
```
✅ Connected to MongoDB: ChronoVision
Collections: ['Memories']
```

---

### Test 2: Screenshot Capture

**Purpose:** Verify PyAutoGUI can capture screenshots

**Steps:**
1. Create a test script `test_screenshot.py`:
   ```python
   import pyautogui
   from pathlib import Path
   
   # Create storage directory
   Path("./storage").mkdir(exist_ok=True)
   
   # Capture screenshot
   img = pyautogui.screenshot()
   img.save("./storage/test_capture.jpg")
   print("✅ Screenshot saved to ./storage/test_capture.jpg")
   ```

2. Run:
   ```bash
   python test_screenshot.py
   ```

3. Verify the image exists in `./storage/test_capture.jpg`

---

### Test 3: Gemini Vision Analysis

**Purpose:** Test Gemini API with image analysis

**Steps:**
1. Create `test_gemini_vision.py`:
   ```python
   from google import genai
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
   
   # Upload test image
   uploaded = client.files.upload(file="./storage/test_capture.jpg")
   print(f"✅ Image uploaded: {uploaded.uri}")
   
   # Analyze
   response = client.models.generate_content(
       model="gemini-2.5-flash",
       contents=["Describe this screen in detail.", uploaded]
   )
   
   print(f"✅ Analysis: {response.text[:200]}...")
   ```

2. Run:
   ```bash
   python test_gemini_vision.py
   ```

**Expected Output:**
```
✅ Image uploaded: https://generativelanguage.googleapis.com/...
✅ Analysis: The screen shows...
```

---

### Test 4: Privacy Filter

**Purpose:** Verify sensitive content detection

**Steps:**
1. Create `test_privacy.py`:
   ```python
   from collector import is_sensitive_content
   
   test_cases = [
       ("Chrome - Sign in to Google", True),
       ("1Password - Vault", True),
       ("Incognito - New Tab", True),
       ("VS Code - main.py", False),
       ("Spotify - Playlist", False),
   ]
   
   for window_title, should_block in test_cases:
       is_blocked, keyword = is_sensitive_content(window_title)
       status = "✅" if is_blocked == should_block else "❌"
       print(f"{status} '{window_title}' -> Blocked: {is_blocked} (Keyword: {keyword})")
   ```

2. Run:
   ```bash
   python test_privacy.py
   ```

**Expected Output:**
```
✅ 'Chrome - Sign in to Google' -> Blocked: True (Keyword: sign in)
✅ '1Password - Vault' -> Blocked: True (Keyword: 1password)
✅ 'Incognito - New Tab' -> Blocked: True (Keyword: incognito)
✅ 'VS Code - main.py' -> Blocked: False (Keyword: None)
✅ 'Spotify - Playlist' -> Blocked: False (Keyword: None)
```

---

## Demo Data Generation

### Generate Sample Memories

**Purpose:** Populate database with test data for UI testing

**Steps:**
1. Run the demo data script:
   ```bash
   python create_demo_data.py
   ```

2. Verify in MongoDB Atlas:
   - Go to **Collections** → **Memories**
   - You should see 10-20 sample entries

**What it creates:**
- Fake timestamps spanning the last 7 days
- Sample activities (coding, browsing, meetings)
- Placeholder summaries
- Base64-encoded placeholder images

---

## End-to-End Testing

### Full System Test

**Purpose:** Test the complete ChronoVision workflow

#### Step 1: Start the Collector

```bash
python run_background.py
```

**Expected Output:**
```
✅ Collector started in background (PID: 12345)
```

**Verification:**
- Check `collector.log` for entries:
  ```
  2026-02-09 15:30:00 - INFO - Attempting to capture memory...
  2026-02-09 15:30:05 - INFO - ✅ Memory captured and stored
  ```

#### Step 2: Launch the Web Interface

```bash
python -m streamlit run search_app.py
```

**Or use the quick start:**
```bash
START_CHRONOVISION.bat
```

#### Step 3: Test the UI

**Command Center Page:**
- [ ] Verify "Memory Density" shows total count
- [ ] Check "Session Health" shows "Active" (green)
- [ ] Confirm "Recent Activity" shows time since last capture
- [ ] View the latest screenshot in "Recent Capture Stream"

**Memory Grid Page:**
- [ ] Filter by "Today" and verify results
- [ ] Click "View Capture" on any entry
- [ ] Verify timestamps are correct

**Intelligence Page:**
- [ ] Enter query: "What was I working on?"
- [ ] Verify AI response appears
- [ ] Check that relevant screenshots are displayed

#### Step 4: Test Collector Controls

1. **Stop Collector:**
   - Click "⏹ STOP SCAN" in sidebar
   - Verify status changes to "SYSTEM DORMANT"
   - Check `collector.log` stops updating

2. **Restart Collector:**
   - Click "INITIATE SCAN"
   - Verify status changes to "SYSTEM ACTIVE"
   - Confirm new captures appear

---

## Troubleshooting

### Issue: "Screenshot failed: Permission denied"

**Solution:**
- On Windows: Run as Administrator
- On macOS: Grant Screen Recording permissions in System Preferences

---

### Issue: "Gemini API Error: 429 RESOURCE_EXHAUSTED"

**Solution:**
- You've hit the free tier quota limit
- Wait 60 seconds or upgrade to paid tier
- Check `QUOTA_TIPS.md` for optimization strategies

---

### Issue: "MongoDB Connection Failed"

**Solutions:**
1. **Check Network Access:**
   - Go to MongoDB Atlas → Network Access
   - Add IP: `0.0.0.0/0` (Allow from anywhere)

2. **Verify Connection String:**
   - Ensure it includes username, password, and cluster name
   - Format: `mongodb+srv://username:password@cluster.mongodb.net/`

3. **Test Connection:**
   ```bash
   python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); print(MongoClient(os.getenv('MONGODB_CONNECTION_STRING')).server_info())"
   ```

---

### Issue: "Collector not starting in background"

**Solution:**
1. Check if already running:
   ```bash
   python -c "from collector import is_collector_running; print(is_collector_running())"
   ```

2. Manually start:
   ```bash
   pythonw collector.py  # Windows
   python collector.py &  # Linux/Mac
   ```

3. Check logs:
   ```bash
   type collector.log  # Windows
   tail -f collector.log  # Linux/Mac
   ```

---

### Issue: "No images showing in UI"

**Possible Causes:**
1. **Local Mode:** Images stored in `./storage/` but not in MongoDB
   - Solution: Collector now saves base64 data to MongoDB

2. **Cloud Mode (Vercel):** Local file paths don't exist
   - Solution: Images are embedded as base64 in `image_data` field

**Verification:**
```python
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
db = client.ChronoVision
mem = db.Memories.find_one()

print("Has image_path:", "image_path" in mem)
print("Has image_data:", "image_data" in mem)
print("Image data length:", len(mem.get("image_data", "")) if mem else 0)
```

---

## Test Checklist Summary

Before deploying or demoing ChronoVision, ensure:

- [ ] All dependencies installed (`test_imports.py` passes)
- [ ] Gemini API accessible (`check_models.py` works)
- [ ] MongoDB connection successful
- [ ] Screenshot capture working
- [ ] Privacy filters blocking sensitive content
- [ ] Collector running in background
- [ ] Web UI accessible at `http://localhost:8501`
- [ ] All three pages (Command Center, Memory Grid, Intelligence) functional
- [ ] AI search returning relevant results
- [ ] Images displaying correctly

---

## Performance Testing

### Recommended Tests:

1. **Memory Usage:**
   ```bash
   # Monitor collector process
   python -c "import psutil; [print(f'{p.name()}: {p.memory_info().rss / 1024 / 1024:.2f} MB') for p in psutil.process_iter() if 'collector' in p.name().lower()]"
   ```

2. **Database Size:**
   - After 24 hours of 60-second intervals = ~1,440 entries
   - Estimated size: ~500MB (with base64 images)
   - Consider cleanup strategy for production

3. **API Quota:**
   - Free tier: 15 requests/minute
   - At 60-second intervals: Safe ✅
   - At 10-second intervals: May hit limits ⚠️

---

## Demo Scenario

**For hackathon judges or presentations:**

1. **Setup (5 minutes before demo):**
   ```bash
   python create_demo_data.py
   START_CHRONOVISION.bat
   ```

2. **Demo Script:**
   - Show Command Center with live stats
   - Navigate to Memory Grid, filter "Today"
   - Go to Intelligence, ask: "Summarize my work today"
   - Show live capture updating in real-time

3. **Highlight Features:**
   - Privacy protection (show sensitive keywords list)
   - AI-powered search
   - Beautiful UI with dark/neon theme
   - Background operation (show system tray/process)

---

## Additional Resources

- **Logs:** `collector.log` - All capture activity
- **Storage:** `./storage/` - Screenshot files
- **Database:** MongoDB Atlas - Structured memory data
- **API Docs:** [Gemini API Reference](https://ai.google.dev/docs)

---

**Last Updated:** 2026-02-09  
**Version:** Chronicle V3.0 Pro
