import os
import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai
import subprocess
import sys
import psutil
from collections import Counter

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

# Page Configuration
st.set_page_config(
    page_title="ChronoVision AI - Your Digital Memory",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Glassmorphism CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Animated Gradient Background */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .block-container {
        padding: 2rem 1rem;
        max-width: 1400px;
    }
    
    /* Glass Morphism Container */
    .glass-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        padding: 2.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Header */
    .hero-header {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        border-radius: 28px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 40px rgba(31, 38, 135, 0.3);
        margin-bottom: 2rem;
    }
    
    .hero-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-shadow: 0 2px 20px rgba(0,0,0,0.2);
        letter-spacing: -1px;
    }
    
    .hero-header .subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.3rem;
        margin-top: 1rem;
        font-weight: 400;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .hero-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Modern Memory Cards */
    .memory-card-modern {
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.35);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .memory-card-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .memory-card-modern:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    .memory-card-modern:hover::before {
        transform: scaleX(1);
    }
    
    .memory-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-right: 0.5rem;
    }
    
    .memory-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: white;
        margin: 1rem 0 0.5rem 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .memory-text {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.05rem;
        line-height: 1.7;
        margin: 1rem 0;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(16px);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    }
    
    .stat-value {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        text-shadow: 0 2px 15px rgba(0,0,0,0.3);
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.95rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Status Pills */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.8rem 1.5rem;
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.95rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .status-active {
        background: rgba(16, 185, 129, 0.25);
        color: #d1fae5;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    }
    
    .status-inactive {
        background: rgba(239, 68, 68, 0.25);
        color: #fecaca;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
    }
    
    .pulse {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .pulse-green {
        background: #10b981;
        box-shadow: 0 0 20px #10b981;
    }
    
    .pulse-red {
        background: #ef4444;
        box-shadow: 0 0 20px #ef4444;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    
    /* Search Box */
    .search-box-container {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.25);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 16px !important;
        padding: 1.2rem 1.5rem !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 0.9rem 2rem;
        font-weight: 600;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    /* Radio & Select */
    .stRadio > div,
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 14px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stRadio label,
    .stSelectbox label {
        color: white !important;
        font-weight: 500;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(30px);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        font-weight: 500;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        color: white !important;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Timeline */
    .timeline-item-glass {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 14px;
        border-left: 4px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 1rem;
        color: white;
        transition: all 0.3s ease;
    }
    
    .timeline-item-glass:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(8px);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.5);
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Labels */
    label {
        color: white !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def is_collector_running():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and 'collector.py' in ' '.join(cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def start_collector():
    try:
        if sys.platform == "win32":
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
            collector_path = os.path.join(os.path.dirname(__file__), "collector.py")
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            subprocess.Popen([pythonw, collector_path], startupinfo=startupinfo,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen(["nohup", sys.executable, "collector.py", "&"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def stop_collector():
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
        st.error(f"Error: {e}")
        return False

# Hero Header
st.markdown("""
<div class="hero-header">
    <div class="hero-icon">🧠</div>
    <h1>ChronoVision AI</h1>
    <p class="subtitle">Your Intelligent Digital Memory Assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.markdown("## 🎛️ System Control")
collector_status = is_collector_running()

if collector_status:
    st.sidebar.markdown("""
    <div class="status-pill status-active">
        <div class="pulse pulse-green"></div>
        ACTIVE
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("")
    if st.sidebar.button("⏸️ Stop Collection", use_container_width=True):
        if stop_collector():
            st.sidebar.success("✅ Stopped")
            st.rerun()
else:
    st.sidebar.markdown("""
    <div class="status-pill status-inactive">
        <div class="pulse pulse-red"></div>
        INACTIVE
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("")
    if st.sidebar.button("▶️ Start Collection", use_container_width=True):
        if start_collector():
            st.sidebar.success("✅ Started")
            st.rerun()

st.sidebar.markdown("---")

# Statistics
st.sidebar.markdown("## 📊 Analytics")
total_memories = collection.count_documents({})

col1, col2 = st.sidebar.columns(2)
with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{total_memories:,}</div>
        <div class="stat-label">Memories</div>
    </div>
    """, unsafe_allow_html=True)

if total_memories > 0:
    latest = collection.find_one(sort=[("timestamp", -1)])
    oldest = collection.find_one(sort=[("timestamp", 1)])
    
    if oldest and latest:
        days_tracked = (latest['timestamp'] - oldest['timestamp']).days
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{days_tracked}</div>
                <div class="stat-label">Days</div>
            </div>
            """, unsafe_allow_html=True)

st.sidebar.markdown("---")

# Date Filter
st.sidebar.markdown("## 🗓️ Time Filter")
date_filter = st.sidebar.selectbox(
    "Period",
    ["All Time", "Today", "Yesterday", "Last 7 Days", "Last 30 Days", "Custom"],
    label_visibility="collapsed"
)

date_query = {}
if date_filter == "Today":
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    date_query = {"timestamp": {"$gte": start_of_day}}
elif date_filter == "Yesterday":
    start = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    date_query = {"timestamp": {"$gte": start, "$lt": end}}
elif date_filter == "Last 7 Days":
    date_query = {"timestamp": {"$gte": datetime.now() - timedelta(days=7)}}
elif date_filter == "Last 30 Days":
    date_query = {"timestamp": {"$gte": datetime.now() - timedelta(days=30)}}
elif date_filter == "Custom":
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("From", datetime.now() - timedelta(days=7))
    with col2:
        end_date = st.date_input("To", datetime.now())
    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.max.time())
    date_query = {"timestamp": {"$gte": start_dt, "$lte": end_dt}}

# Main Search
st.markdown('<div class="glass-container search-box-container">', unsafe_allow_html=True)
st.markdown("### 🔍 Search Your Digital Past")

query = st.text_input(
    "search",
    placeholder="Ask me anything... e.g., 'What was I researching about AI last Tuesday?'",
    label_visibility="collapsed"
)

search_mode = st.radio(
    "Mode",
    ["⚡ Quick Search", "🤖 AI Search"],
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# Execute Search
if query:
    with st.spinner("🔍 Analyzing memories..."):
        if search_mode == "⚡ Quick Search":
            search_query = {"summary": {"$regex": query, "$options": "i"}}
            search_query.update(date_query)
            results_list = list(collection.find(search_query, limit=20).sort("timestamp", -1))
        else:
            all_memories = list(collection.find(date_query, limit=100).sort("timestamp", -1))
            if all_memories:
                memory_context = "\n\n".join([
                    f"[{i+1}] {mem['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}: {mem['summary'][:200]}"
                    for i, mem in enumerate(all_memories)
                ])
                
                prompt = f"""Search query: "{query}"

Activities:
{memory_context}

Return relevant entry numbers (comma-separated) or NONE."""
                
                try:
                    response = client_ai.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )
                    text = response.text.strip()
                    if text != "NONE":
                        indices = [int(x.strip())-1 for x in text.split(",") if x.strip().isdigit()]
                        results_list = [all_memories[i] for i in indices if i < len(all_memories)]
                    else:
                        results_list = []
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        st.error("⚠️ API limit reached. Use Quick Search!")
                    else:
                        st.error(f"Error: {e}")
                    results_list = []
            else:
                results_list = []
    
    if results_list:
        st.success(f"✨ Found {len(results_list)} memories")
        st.markdown("")
        
        for idx, mem in enumerate(results_list):
            time_diff = datetime.utcnow() - mem['timestamp']
            if time_diff.days > 0:
                time_ago = f"{time_diff.days}d ago"
            else:
                hours = time_diff.seconds // 3600
                time_ago = f"{hours}h ago" if hours > 0 else f"{time_diff.seconds // 60}m ago"
            
            st.markdown(f"""
            <div class="memory-card-modern">
                <div>
                    <span class="memory-badge">#{idx+1}</span>
                    <span class="memory-badge">🕐 {mem['timestamp'].strftime('%I:%M %p')}</span>
                    <span class="memory-badge">⏱️ {time_ago}</span>
                </div>
                <div class="memory-title">{mem['timestamp'].strftime('%A, %B %d, %Y')}</div>
                <div class="memory-text">{mem['summary']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if os.path.exists(mem['image_path']):
                with st.expander("🖼️ Screenshot"):
                    st.image(mem['image_path'], use_container_width=True)
    else:
        st.warning("😕 No matches found")

# Timeline
st.sidebar.markdown("---")
if st.sidebar.checkbox("📈 Timeline"):
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("## 📈 Activity Timeline")
    
    memories = list(collection.find(date_query).sort("timestamp", -1).limit(50))
    if memories:
        current_date = None
        for mem in memories:
            mem_date = mem['timestamp'].strftime('%Y-%m-%d')
            if mem_date != current_date:
                current_date = mem_date
                st.markdown(f"### 📅 {mem['timestamp'].strftime('%A, %b %d')}")
            
            st.markdown(f"""
            <div class="timeline-item-glass">
                <strong>{mem['timestamp'].strftime('%I:%M %p')}</strong><br>
                {mem['summary'][:150]}{'...' if len(mem['summary']) > 150 else ''}
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)