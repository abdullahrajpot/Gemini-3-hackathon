import os
import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Configuration
MONGODB_URI = os.getenv("MONGODB_CONNECTION_STRING")
DB_NAME = os.getenv("MONGODB_DATABASE", "ChronoVision")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION", "Memories")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize clients
db_client = MongoClient(MONGODB_URI)
db = db_client[DB_NAME]
collection = db[COLLECTION_NAME]
client_ai = genai.Client(api_key=GEMINI_API_KEY)

# Streamlit UI
st.set_page_config(page_title="ChronoVision AI", page_icon="🧠", layout="wide")

st.title("🧠 ChronoVision AI")
st.subheader("Your Eyetic Memory - Search Your Screen History")

# Search bar
query = st.text_input("🔍 What were you doing?", placeholder="e.g., When was I looking at flight tickets to Tokyo?")

if query:
    st.write("Searching memories...")
    
    # Simple keyword search in MongoDB
    results = collection.find(
        {"summary": {"$regex": query, "$options": "i"}},
        limit=10
    ).sort("timestamp", -1)
    
    results_list = list(results)
    
    if results_list:
        st.success(f"Found {len(results_list)} matching memories")
        
        for memory in results_list:
            with st.expander(f"📅 {memory['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                st.write(f"**Activity:** {memory['summary']}")
                
                # Display screenshot if exists
                if os.path.exists(memory['image_path']):
                    st.image(memory['image_path'], width=600)
    else:
        st.warning("No memories found matching your query.")

# Sidebar stats
st.sidebar.title("📊 Memory Stats")
total_memories = collection.count_documents({})
st.sidebar.metric("Total Memories", total_memories)

if total_memories > 0:
    latest = collection.find_one(sort=[("timestamp", -1)])
    if latest:
        st.sidebar.write(f"**Latest Capture:** {latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
