# ChronoVision AI - Setup Guide

## 📋 Prerequisites Checklist

### 1. Python Installation
- [ ] Python 3.8+ installed
- [ ] pip package manager available

### 2. MongoDB Atlas Setup
- [ ] Create free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [ ] Create a new cluster (free tier M0 is fine)
- [ ] Create database: `ChronoVision`
- [ ] Create collection: `Memories`
- [ ] Get connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
- [ ] Whitelist your IP address in Network Access

### 3. Gemini API Key
- [ ] Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
- [ ] Create/Get your Gemini API key
- [ ] Note: Check if "gemini-3-pro-preview" is available, or use "gemini-1.5-pro" as alternative

## 🚀 Installation Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment
1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your credentials:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `MONGODB_CONNECTION_STRING`: Your MongoDB connection string

### Step 3: Test MongoDB Connection
```python
# Quick test script
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
print("Connected:", client.server_info())
```

### Step 4: Run the Collector
```bash
python collector.py
```
This will start capturing screenshots every 60 seconds.

### Step 5: Run the Search Interface
In a separate terminal:
```bash
streamlit run search_app.py
```
This will open the search interface in your browser.

## ⚠️ Important Notes

1. **Gemini Model Name**: The readme mentions "gemini-3-pro-preview" but verify the actual model name in Google AI Studio. You might need to use:
   - `gemini-1.5-pro`
   - `gemini-1.5-flash`
   - Or check latest available models

2. **Storage Space**: Screenshots will accumulate quickly. Monitor your `./storage` folder.

3. **Privacy**: The collector captures everything on screen. Be mindful of sensitive information.

4. **Performance**: Adjust `CAPTURE_INTERVAL` in `.env` based on your needs (default: 60 seconds).

## 🎯 Hackathon Bonus Features to Add

1. **Privacy Guard**: Auto-pause on incognito/password managers
2. **Semantic Search**: Use Gemini to understand query intent
3. **Visual Timeline**: Show screenshot timeline in Streamlit
4. **Activity Analytics**: Track most-used apps, productivity patterns
5. **Export Feature**: Export memories as PDF report

## 🐛 Troubleshooting

- **MongoDB Connection Error**: Check connection string and IP whitelist
- **Gemini API Error**: Verify API key and model name
- **Screenshot Permission**: Some systems require screen recording permissions
- **Import Errors**: Ensure all packages installed: `pip install -r requirements.txt`
