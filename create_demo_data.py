"""
Create demo data for ChronoVision hackathon presentation
This populates MongoDB with sample memories for demonstration
"""
import os
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import random

load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
db = client[os.getenv("MONGODB_DATABASE", "ChronoVision")]
collection = db[os.getenv("MONGODB_COLLECTION", "Memories")]

# Sample activities for demo
demo_activities = [
    "Working on Python machine learning project using Jupyter Notebook. Training a neural network model with TensorFlow.",
    "Reading React documentation on hooks. Learning about useState and useEffect on React.dev.",
    "Watching YouTube tutorial on Docker containerization. Taking notes in Notion about container orchestration.",
    "Writing email in Gmail about project deadline. Discussing sprint planning with team.",
    "Designing UI mockup in Figma for mobile app. Working on dark mode theme for user profile screen.",
    "Debugging JavaScript code in VS Code. Stack Overflow tab open searching for async/await solutions.",
    "Reading research paper on arXiv about transformer models and attention mechanisms.",
    "Attending Zoom meeting with 8 participants. Presentation about Q4 roadmap visible.",
    "Writing blog post in Medium about API design best practices with code examples.",
    "Browsing GitHub trending repositories. Looking at popular Python ML libraries.",
    "Editing video in Adobe Premiere Pro. Working on web development tutorial.",
    "Analyzing sales data in Excel. Creating pivot tables and charts for quarterly report.",
    "Learning SQL on DataCamp. Writing SELECT queries and JOIN statements.",
    "Configuring AWS EC2 instances. Setting up security groups and load balancers.",
    "Chatting on Slack with development team about code review and merge conflicts.",
    "Listening to Spotify lo-fi playlist while coding Python in VS Code.",
    "Reading Hacker News articles about AI and startups. Multiple tabs open.",
    "Creating hackathon pitch presentation in Google Slides with problem and solution slides.",
    "Testing mobile app in Android Studio emulator. Checking logcat for errors.",
    "Browsing LinkedIn feed reading posts about tech industry trends.",
    "Researching competitors on Product Hunt. Taking notes about feature comparisons.",
    "Writing documentation in Markdown for open source project README.",
    "Reviewing pull requests on GitHub. Leaving comments on code changes.",
    "Planning sprint in Jira. Creating user stories and assigning story points.",
    "Designing database schema in dbdiagram.io. Creating ERD for new feature.",
]

def create_demo_memories(days_back=7, memories_per_day=12):
    """Create demo memories for the past N days"""
    
    print(f"🎬 Creating demo data for ChronoVision...")
    print(f"📅 Days: {days_back}")
    print(f"💾 Memories per day: {memories_per_day}")
    print()
    
    created_count = 0
    
    for day in range(days_back):
        date = datetime.now() - timedelta(days=day)
        
        # Create memories throughout the day
        for i in range(memories_per_day):
            # Random time during work hours (9 AM - 6 PM)
            hour = random.randint(9, 18)
            minute = random.randint(0, 59)
            
            timestamp = date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Pick random activity
            summary = random.choice(demo_activities)
            
            memory = {
                "timestamp": timestamp,
                "summary": summary,
                "image_path": f"./demo_screenshots/demo_{day}_{i}.jpg",
                "captured_at": int(timestamp.timestamp()),
                "window_title": "demo_data",
                "is_demo": True
            }
            
            collection.insert_one(memory)
            created_count += 1
            
            if created_count % 20 == 0:
                print(f"  ✓ Created {created_count} memories...")
    
    print()
    print(f"✅ Successfully created {created_count} demo memories!")
    print(f"📊 Total memories in database: {collection.count_documents({})}")
    print()
    print("🔍 Try these searches in your app:")
    print("  • 'Python machine learning'")
    print("  • 'What was I learning about React?'")
    print("  • 'Show me design work in Figma'")
    print("  • 'When was I in Zoom meetings?'")
    print("  • 'GitHub repositories'")
    print()
    print("🚀 Your demo is ready! Open the search interface.")

def clear_demo_data():
    """Remove all demo data"""
    result = collection.delete_many({"is_demo": True})
    print(f"🗑️  Deleted {result.deleted_count} demo memories")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_demo_data()
    else:
        create_demo_memories(days_back=7, memories_per_day=15)
