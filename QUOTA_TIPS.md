# 💡 Managing API Quota

## The Issue
Gemini free tier has limits:
- **20 requests per day** for gemini-2.5-flash
- Each screenshot capture = 1 request
- Each AI search = 1 request

## Solutions

### 1. Increase Capture Interval (Recommended)
Edit `.env` file:
```env
# Capture every 5 minutes instead of 1 minute
CAPTURE_INTERVAL=300

# Or every 10 minutes
CAPTURE_INTERVAL=600
```

This reduces API usage dramatically:
- 60 seconds = 1,440 captures/day ❌
- 300 seconds (5 min) = 288 captures/day ❌
- 600 seconds (10 min) = 144 captures/day ❌

### 2. Use Keyword Search
- Keyword search is **instant** and uses **zero API quota**
- Works great for specific terms: "email", "Python", "YouTube"
- AI search is only needed for complex questions

### 3. Upgrade API Plan
Get more quota at: https://ai.google.dev/pricing
- Pay-as-you-go: $0.075 per 1K requests
- Much higher limits

### 4. Run Collector Only When Needed
```bash
# Start when you want to track
python run_background.py

# Stop when done
python stop_collector.py
```

### 5. Use Local AI (Advanced)
Replace Gemini with local models:
- Ollama with LLaVA (vision model)
- No API costs
- Runs on your computer
- Requires good GPU

## Best Practice for Hackathon

**For Demo:**
- Set `CAPTURE_INTERVAL=300` (5 minutes)
- Use keyword search primarily
- Show AI search as a "premium feature"
- Highlight that it works with any interval

**For Presentation:**
- Explain the quota management strategy
- Show both search modes
- Mention scalability with paid API or local models

## Current Quota Status

Check your usage: https://ai.dev/rate-limit

Your quota resets every 24 hours!
