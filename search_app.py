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
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg-color: #0E1117;
        --card-bg: rgba(30, 41, 59, 0.7);
        --primary: #00F0FF;
        --secondary: #7C3AED;
        --text-primary: #FFFFFF;
        --text-secondary: #E2E8F0;
        --accent-glow: 0 0 20px rgba(0, 240, 255, 0.15);
    }
    
    /* Global Reset & Typography */
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-primary);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.02em;
        color: #FFFFFF !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    p, span, div, label, li {
        color: var(--text-primary);
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Main App Background */
    .stApp {
        background-color: var(--bg-color);
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(124, 58, 237, 0.1) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(0, 240, 255, 0.1) 0%, transparent 40%);
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Container Adjustments */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        max-width: 1200px;
    }
    
    /* Glass Morphism Base */
    .glass-panel {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 4rem 1rem;
        margin-bottom: 3rem;
        position: relative;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #CBD5E1;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Stats Cards - Compact */
    .stat-card-compact {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card-compact:hover {
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }
    
    .stat-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary);
        line-height: 1.2;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #E2E8F0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Memory Cards */
    .memory-card {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.6) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .memory-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: var(--primary);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .memory-card:hover {
        transform: translateY(-4px) scale(1.01);
        border-color: rgba(0, 240, 255, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }
    
    .memory-card:hover::before {
        opacity: 1;
    }
    
    .memory-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .memory-time {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: var(--primary);
        background: rgba(0, 240, 255, 0.1);
        padding: 4px 8px;
        border-radius: 4px;
    }
    
    .memory-ago {
        font-size: 0.8rem;
        color: #CBD5E1;
        font-weight: 500;
    }
    
    .memory-content {
        color: #FFFFFF;
        font-size: 1.05rem;
        line-height: 1.6;
        font-weight: 400;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f15;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    section[data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    
    /* Status Indicator */
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        box-shadow: 0 0 10px currentColor;
    }
    
    /* Input Fields */
    .stTextInput input {
        background: rgba(15, 23, 42, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        padding: 1.2rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        caret-color: var(--primary) !important;
    }
    
    .stTextInput input::placeholder {
        color: #94A3B8 !important;
        opacity: 0.8 !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(0, 240, 255, 0.1) !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #2563EB 0%, #7C3AED 100%);
        border: none;
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
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
<div class="hero-container">
    <h1 class="hero-title">ChronoVision</h1>
    <p class="hero-subtitle">Intelligent Memory Augmentation • <span style="color:var(--primary)">System Active</span></p>
</div>
""", unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.markdown("## 🎛️ System Control")
collector_status = is_collector_running()

if collector_status:
    st.sidebar.markdown("""
    <div class="status-indicator">
        <div class="status-dot" style="color:#00F0FF; box-shadow: 0 0 10px #00F0FF;"></div>
        <div>
            <div style="font-weight:600; color:white;">System Online</div>
            <div style="font-size:0.8rem; color:rgba(255,255,255,0.5);">Monitoring active</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("")
    if st.sidebar.button("⏸️ Pause Collection", use_container_width=True):
        if stop_collector():
            st.sidebar.success("✅ Stopped")
            st.rerun()
else:
    st.sidebar.markdown("""
    <div class="status-indicator">
        <div class="status-dot" style="color:#EF4444; box-shadow: 0 0 10px #EF4444;"></div>
        <div>
            <div style="font-weight:600; color:white;">System Offline</div>
            <div style="font-size:0.8rem; color:rgba(255,255,255,0.5);"> monitoring paused</div>
        </div>
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
    <div class="stat-card-compact">
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
            <div class="stat-card-compact">
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
st.markdown('<div class="glass-panel" style="padding: 2rem; margin-bottom: 2rem;">', unsafe_allow_html=True)
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
            <div class="memory-card">
                <div class="memory-header">
                    <span class="memory-time">{mem['timestamp'].strftime('%H:%M')}</span>
                    <span class="memory-ago">{time_ago}</span>
                </div>
                <div class="memory-content">{mem['summary']}</div>
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