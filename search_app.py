import os
import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai
import subprocess
import sys
import psutil

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
st.set_page_config(page_title="ChronoVision AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# Professional Custom CSS with unified elegant theme
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove default padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        margin: 0;
        opacity: 0.95;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* Sidebar headers */
    section[data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 600;
        margin-top: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: white;
        color: #667eea;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        background: #f8f9fa;
    }
    
    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.2);
        color: white;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-2px);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 1rem 1.5rem;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        background: white;
        color: #2d3748 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #a0aec0 !important;
        opacity: 1;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Input labels */
    .stTextInput label {
        color: #2d3748 !important;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Search section */
    .search-section {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    /* Memory cards */
    .memory-card {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }
    
    .memory-card:hover {
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.15);
        transform: translateY(-4px);
        border-color: #667eea;
    }
    
    /* Metrics */
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: white !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.9) !important;
        font-size: 0.9rem;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        gap: 1rem;
    }
    
    .stRadio label {
        background: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        color: #2d3748 !important;
    }
    
    .stRadio label span {
        color: #2d3748 !important;
    }
    
    .stRadio label:has(input:checked) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: #667eea;
    }
    
    .stRadio label:has(input:checked) span {
        color: white !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border-radius: 10px;
        font-weight: 600;
        padding: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .streamlit-expanderHeader:hover {
        background: #e9ecef;
        border-color: #667eea;
    }
    
    /* Status indicators */
    .status-running {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        background: rgba(16, 185, 129, 0.2);
        color: white;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.95rem;
        border: 2px solid rgba(255,255,255,0.3);
        margin-bottom: 1rem;
    }
    
    .status-stopped {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        background: rgba(239, 68, 68, 0.2);
        color: white;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.95rem;
        border: 2px solid rgba(255,255,255,0.3);
        margin-bottom: 1rem;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
    }
    
    /* Select box */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid rgba(255,255,255,0.3);
        background: rgba(255,255,255,0.1);
    }
    
    .stSelectbox label {
        color: white !important;
    }
    
    /* Main content text colors */
    .main p, .main span, .main div {
        color: #2d3748;
    }
    
    /* Success/Warning/Error messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 12px;
        padding: 1rem 1.5rem;
    }
    
    /* Section titles */
    h2 {
        color: #2d3748;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
    }
    
    h4 {
        color: #667eea;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><h1>🧠 ChronoVision AI</h1><p>Your Eyetic Memory - Search Your Screen History</p></div>', unsafe_allow_html=True)

# Helper functions for collector control
def is_collector_running():
    """Check if collector is running"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and 'collector.py' in ' '.join(cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def start_collector():
    """Start the collector in background"""
    try:
        if sys.platform == "win32":
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
            collector_path = os.path.join(os.path.dirname(__file__), "collector.py")
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            subprocess.Popen(
                [pythonw, collector_path],
                startupinfo=startupinfo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            subprocess.Popen(
                ["nohup", sys.executable, "collector.py", "&"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        return True
    except Exception as e:
        st.error(f"Error starting collector: {e}")
        return False

def stop_collector():
    """Stop the collector"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and 'collector.py' in ' '.join(cmdline):
                    proc.terminate()
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
    except Exception as e:
        st.error(f"Error stopping collector: {e}")
        return False

# Sidebar - Collector Control
st.sidebar.markdown("### 🎛️ Collector Control")

collector_status = is_collector_running()

if collector_status:
    st.sidebar.markdown('<span class="status-running">● RUNNING</span>', unsafe_allow_html=True)
    st.sidebar.write("")
    if st.sidebar.button("⏸️ Stop Collector", use_container_width=True):
        if stop_collector():
            st.sidebar.success("✅ Collector stopped")
            st.rerun()
        else:
            st.sidebar.warning("⚠️ Collector not found")
else:
    st.sidebar.markdown('<span class="status-stopped">● STOPPED</span>', unsafe_allow_html=True)
    st.sidebar.write("")
    if st.sidebar.button("▶️ Start Collector", use_container_width=True):
        if start_collector():
            st.sidebar.success("✅ Collector started")
            st.rerun()
        else:
            st.sidebar.error("❌ Failed to start")

st.sidebar.markdown("---")

# Sidebar stats
st.sidebar.markdown("### 📊 Memory Stats")
total_memories = collection.count_documents({})
st.sidebar.metric("Total Memories", total_memories)

if total_memories > 0:
    latest = collection.find_one(sort=[("timestamp", -1)])
    oldest = collection.find_one(sort=[("timestamp", 1)])
    
    if latest:
        st.sidebar.write(f"**Latest Capture:**")
        st.sidebar.write(f"{latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    if oldest:
        days_tracked = (latest['timestamp'] - oldest['timestamp']).days
        st.sidebar.metric("Days Tracked", days_tracked)

st.sidebar.markdown("---")

# Date filter in sidebar
st.sidebar.markdown("### 🗓️ Filter by Date")
date_filter = st.sidebar.selectbox(
    "Time Range",
    ["All Time", "Today", "Yesterday", "Last 7 Days", "Last 30 Days", "Custom Range"]
)

date_query = {}
if date_filter == "Today":
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    date_query = {"timestamp": {"$gte": start_of_day}}
elif date_filter == "Yesterday":
    yesterday = datetime.now() - timedelta(days=1)
    start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    date_query = {"timestamp": {"$gte": start_of_yesterday, "$lte": end_of_yesterday}}
elif date_filter == "Last 7 Days":
    seven_days_ago = datetime.now() - timedelta(days=7)
    date_query = {"timestamp": {"$gte": seven_days_ago}}
elif date_filter == "Last 30 Days":
    thirty_days_ago = datetime.now() - timedelta(days=30)
    date_query = {"timestamp": {"$gte": thirty_days_ago}}
elif date_filter == "Custom Range":
    col1, col2 = st.sidebar.columns(2)
    start_date = col1.date_input("From")
    end_date = col2.date_input("To")
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    date_query = {"timestamp": {"$gte": start_datetime, "$lte": end_datetime}}

# Main search interface
st.markdown("## 🔍 Search Your Memories")
st.write("")
query = st.text_input(
    "What are you looking for?",
    placeholder="e.g., When was I looking at flight tickets to Tokyo? or What was I doing on Monday afternoon?",
    key="search_query",
    label_visibility="collapsed"
)

# Search mode
search_mode = st.radio(
    "Search Mode:",
    ["🔤 Keyword Search", "🤖 AI-Powered Search (Uses API quota)"],
    horizontal=True,
    help="Keyword search is fast and doesn't use API quota. AI search understands natural questions but uses your Gemini API quota."
)

if query:
    with st.spinner("🔍 Searching through your memories..."):
        
        if search_mode == "🔤 Keyword Search":
            # Simple keyword search
            search_query = {"summary": {"$regex": query, "$options": "i"}}
            search_query.update(date_query)
            
            results = collection.find(search_query, limit=20).sort("timestamp", -1)
            results_list = list(results)
            
        else:
            # AI-Powered search
            # Get recent memories and let Gemini find the best matches
            all_memories = list(collection.find(date_query, limit=100).sort("timestamp", -1))
            
            if all_memories:
                # Create a summary of memories for Gemini
                memory_context = "\n\n".join([
                    f"[{i+1}] Time: {mem['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\nActivity: {mem['summary'][:200]}"
                    for i, mem in enumerate(all_memories)
                ])
                
                # Ask Gemini to find relevant memories
                ai_prompt = f"""User is searching for: "{query}"

Here are their recent screen activities:

{memory_context}

Based on the user's question, identify which memory entries (by number) are most relevant. 
Return ONLY the numbers of relevant entries, separated by commas. For example: 1,5,12

If no memories match, return: NONE"""

                try:
                    ai_response = client_ai.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=ai_prompt
                    )
                    
                    response_text = ai_response.text.strip()
                    
                    if response_text != "NONE":
                        # Parse the numbers
                        indices = [int(x.strip()) - 1 for x in response_text.split(",") if x.strip().isdigit()]
                        results_list = [all_memories[i] for i in indices if i < len(all_memories)]
                    else:
                        results_list = []
                        
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                        st.error("⚠️ API quota exceeded! The free tier allows 20 requests per day.")
                        st.info("💡 Use **Keyword Search** instead - it works without using API quota and is faster!")
                        st.info("📊 Your quota resets in about 1 hour. Or upgrade your API plan at https://ai.google.dev/pricing")
                    else:
                        st.error(f"AI search error: {e}")
                    results_list = []
            else:
                results_list = []
        
        # Display results
        if results_list:
            st.success(f"✅ Found {len(results_list)} matching memories")
            st.write("")
            
            for idx, memory in enumerate(results_list):
                # Create elegant memory card
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.markdown(f"#### 📅 Memory #{idx + 1}")
                    st.write(f"**{memory['timestamp'].strftime('%A')}**")
                    st.write(f"{memory['timestamp'].strftime('%B %d, %Y')}")
                    st.write(f"🕐 {memory['timestamp'].strftime('%I:%M %p')}")
                    
                    # Time ago
                    time_diff = datetime.utcnow() - memory['timestamp']
                    if time_diff.days > 0:
                        st.caption(f"({time_diff.days} days ago)")
                    else:
                        hours = time_diff.seconds // 3600
                        if hours > 0:
                            st.caption(f"({hours} hours ago)")
                        else:
                            minutes = time_diff.seconds // 60
                            st.caption(f"({minutes} minutes ago)")
                
                with col2:
                    st.markdown("**📝 Activity Description**")
                    st.write(memory['summary'])
                    
                    # Display screenshot
                    if os.path.exists(memory['image_path']):
                        with st.expander("🖼️ View Screenshot", expanded=False):
                            st.image(memory['image_path'], use_container_width=True)
                
                st.divider()
        else:
            st.warning("😕 No memories found matching your query. Try different keywords or adjust the date range.")

# Timeline view
st.sidebar.markdown("---")
if st.sidebar.checkbox("📈 Show Timeline View"):
    st.markdown("## 📈 Activity Timeline")
    st.write("")
    
    timeline_memories = list(collection.find(date_query).sort("timestamp", -1).limit(50))
    
    if timeline_memories:
        for memory in timeline_memories:
            col1, col2 = st.columns([1, 5])
            with col1:
                st.markdown(f"**{memory['timestamp'].strftime('%H:%M')}**")
            with col2:
                st.write(f"{memory['summary'][:120]}...")
            st.markdown("---")
    else:
        st.info("No memories in selected time range.")
