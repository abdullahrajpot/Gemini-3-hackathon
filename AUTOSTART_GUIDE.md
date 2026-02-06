# 🚀 Auto-Start ChronoVision on Windows

## Option 1: Automatic Installation (Easiest)

### Step 1: Install Required Package
```bash
pip install pywin32
```

### Step 2: Run Installation Script
```bash
python install_autostart.py
```

Choose option 1 to install. The collector will now start automatically every time you login to Windows!

---

## Option 2: Manual Installation (No Extra Package Needed)

### Method A: Using Task Scheduler (Recommended)

1. **Open Task Scheduler**
   - Press `Win + R`
   - Type: `taskschd.msc`
   - Press Enter

2. **Create New Task**
   - Click "Create Task" (not "Create Basic Task")
   - Name: `ChronoVision Collector`
   - Description: `Automatic screen memory collector`
   - Check: "Run whether user is logged on or not"
   - Check: "Run with highest privileges"

3. **Triggers Tab**
   - Click "New"
   - Begin the task: "At log on"
   - Specific user: (your username)
   - Click OK

4. **Actions Tab**
   - Click "New"
   - Action: "Start a program"
   - Program/script: `C:\Path\To\pythonw.exe`
     (Find it by running: `where pythonw` in cmd)
   - Add arguments: `"C:\Path\To\Your\Project\collector.py"`
   - Start in: `C:\Path\To\Your\Project`
   - Click OK

5. **Conditions Tab**
   - Uncheck "Start the task only if the computer is on AC power"

6. **Settings Tab**
   - Check "Allow task to be run on demand"
   - Check "If the task fails, restart every: 1 minute"
   - Click OK

**Done!** The collector will start automatically on login.

---

### Method B: Using Startup Folder (Simpler but visible)

1. **Create Batch File**
   - Create a file named `start_collector.bat` in your project folder
   - Add this content:
   ```batch
   @echo off
   cd /d "%~dp0"
   start /min pythonw collector.py
   ```

2. **Add to Startup**
   - Press `Win + R`
   - Type: `shell:startup`
   - Press Enter
   - Copy `start_collector.bat` to this folder

**Done!** Collector starts on login.

---

## Option 3: Windows Service (Advanced - Most Professional)

For a true background service that runs even before login:

### Step 1: Install NSSM (Non-Sucking Service Manager)
```bash
# Download from: https://nssm.cc/download
# Or use chocolatey:
choco install nssm
```

### Step 2: Create Service
```bash
# Open cmd as Administrator
nssm install ChronoVision

# In the GUI that opens:
# Path: C:\Path\To\pythonw.exe
# Startup directory: C:\Path\To\Your\Project
# Arguments: collector.py
```

### Step 3: Configure Service
```bash
# Set to start automatically
nssm set ChronoVision Start SERVICE_AUTO_START

# Start the service
nssm start ChronoVision
```

### Manage Service
```bash
# Stop service
nssm stop ChronoVision

# Remove service
nssm remove ChronoVision confirm
```

---

## 🎯 For Your Hackathon Demo

### Best Approach:
Use **Task Scheduler** (Method A) because:
- ✅ Professional and reliable
- ✅ No extra packages needed
- ✅ Runs silently in background
- ✅ Starts automatically on login
- ✅ Easy to demonstrate

### Demo Script:
1. Show Task Scheduler with ChronoVision task
2. Explain it runs automatically on startup
3. Show the web interface for searching
4. Demonstrate the start/stop controls in the UI

---

## 📱 Accessing the Web Interface

The collector runs in background, but to search your memories:

### Option 1: Create Desktop Shortcut
Create `ChronoVision Search.bat`:
```batch
@echo off
start http://localhost:8501
python -m streamlit run search_app.py
```

### Option 2: Always-Running Web Interface
Use Task Scheduler to also auto-start the Streamlit app:
- Create another task for `streamlit run search_app.py`
- Access anytime at: `http://localhost:8501`

---

## 🛑 How to Stop Auto-Start

### Task Scheduler:
1. Open Task Scheduler
2. Find "ChronoVision Collector"
3. Right-click → Disable or Delete

### Startup Folder:
1. Press `Win + R`
2. Type: `shell:startup`
3. Delete the batch file

### Service:
```bash
nssm stop ChronoVision
nssm remove ChronoVision confirm
```

---

## 💡 Pro Tips

1. **Set Longer Intervals**: Edit `.env` to capture every 5-10 minutes instead of 1 minute to save API quota

2. **Monitor Status**: The web interface shows if collector is running

3. **Privacy Mode**: Add a pause button or schedule to stop during certain hours

4. **Resource Usage**: The collector uses minimal resources (~50MB RAM)

---

## 🏆 Hackathon Presentation Points

Highlight these features:
- ✅ "Runs completely in background - set it and forget it"
- ✅ "Starts automatically on system boot"
- ✅ "Web interface accessible anytime at localhost"
- ✅ "Professional Windows Task Scheduler integration"
- ✅ "Easy start/stop controls from the UI"
- ✅ "Minimal resource usage"

This shows enterprise-level thinking and production-ready design!
