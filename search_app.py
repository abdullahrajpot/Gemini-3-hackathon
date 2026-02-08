import os
import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai
import subprocess
import sys
try:
    import psutil
except ImportError:
    psutil = None

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
    page_title="CHRONICLE V3.0 PRO",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CSS STYLING (Chronicle V3.0 Pro Theme)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg-dark: #05050A;
        --card-bg: #0F0F16;
        --accent-blue: #2E5CFF;
        --accent-purple: #7C3AED;
        --text-primary: #FFFFFF;
        --text-secondary: #94A3B8;
        --border-color: rgba(255, 255, 255, 0.08);
        --neon-glow: 0 0 10px rgba(46, 92, 255, 0.3);
    }

    /* Global Reset */
    .stApp {
        background-color: var(--bg-dark);
        color: var(--text-primary);
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, .stMetricLabel {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: white !important;
    }
    
    .data-font {
        font-family: 'JetBrains Mono', monospace;
    }

    /* Hide Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #08080E;
        border-right: 1px solid var(--border-color);
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: var(--border-color);
    }

    /* Navigation Radio (Sidebar) */
    .stRadio [role="radiogroup"] {
        background: transparent;
        padding: 0;
    }
    
    .stRadio label {
        background: transparent !important;
        border: 1px solid transparent;
        padding: 12px 16px;
        border-radius: 8px;
        color: #64748B !important;
        transition: all 0.2s;
        font-weight: 600;
        display: flex;
        align-items: center;
        margin-bottom: 4px;
    }
    
    .stRadio label:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
    }
    
    div[data-testid="stMarkdownContainer"] p {
        font-size: 0.95rem;
    }

    /* Cards */
    .dashboard-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .dashboard-card:hover {
        border-color: rgba(46, 92, 255, 0.3);
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    
    .card-label {
        color: var(--text-secondary);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .card-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        line-height: 1.1;
    }
    
    .card-sub {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 8px;
    }

    /* Buttons */
    .stButton button {
        background: var(--accent-blue);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        box-shadow: 0 0 15px rgba(46, 92, 255, 0.2);
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        box-shadow: 0 0 25px rgba(46, 92, 255, 0.4);
        transform: translateY(-1px);
    }
    
    .stButton button:active {
        background: #1a45d0;
    }

    /* Inputs */
    .stTextInput input {
        background-color: #0F0F16 !important;
        border: 1px solid var(--border-color) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 1px var(--accent-blue) !important;
    }

    /* Timeline Items */
    .timeline-row {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: flex-start;
        gap: 16px;
        transition: border-color 0.2s;
    }
    
    .timeline-row:hover {
        border-color: rgba(255,255,255,0.2);
    }
    
    .time-badge {
        font-family: 'JetBrains Mono', monospace;
        background: rgba(46, 92, 255, 0.1);
        color: #5C85FF;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
        white-space: nowrap;
    }

    /* Status Indicators */
    .status-dot {
        height: 8px; 
        width: 8px; 
        border-radius: 50%; 
        display: inline-block;
        margin-right: 6px;
    }
    .dot-green { background: #10B981; box-shadow: 0 0 8px #10B981; }
    .dot-red { background: #EF4444; box-shadow: 0 0 8px #EF4444; }
    .dot-grey { background: #64748B; }

    /* Header Bar */
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .app-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .brand-logo {
        width: 40px;
        height: 40px;
        background: var(--accent-blue);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }
    
    .brand-text h3 {
        margin: 0;
        line-height: 1.2;
        font-size: 1.2rem;
    }
    
    .brand-text span {
        font-size: 0.75rem;
        color: var(--text-secondary);
        font-weight: 600;
        letter-spacing: 1px;
    }

    /* Tabs Override */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        white-space: nowrap;
        background-color: transparent;
        border-radius: 4px;
        color: var(--text-secondary);
        font-weight: 600;
        padding: 4px 0;
    }
    
    .stTabs [aria-selected="true"] {
        color: white !important;
        border-bottom: 2px solid var(--accent-blue) !important;
    }
    
    /* Selectbox Styling */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #0F0F16 !important;
        border: 1px solid var(--border-color) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    div[data-baseweb="select"] span {
        color: white !important;
    }
    
    div[data-baseweb="menu"] {
        background-color: #1E293B !important;
    }
    
    div[data-baseweb="menu"] li {
        color: white !important;
    }
    
    div[data-baseweb="menu"] li:hover {
        background-color: var(--accent-blue) !important;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LOGIC
# -----------------------------------------------------------------------------

def is_collector_running():
    if psutil is None:
        return False
        
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and 'collector.py' in ' '.join(cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def start_collector():
    if psutil is None:
        st.error("Collector cannot be started in this environment (missing psutil).")
        return False
        
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
            # On Vercel/Linux, we likely can't start persistent background processes easily like this
            st.error("Collector starting not supported on this platform/environment.")
            return False
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def stop_collector():
    if psutil is None:
        return False
        
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

# -----------------------------------------------------------------------------
# LAYOUT
# -----------------------------------------------------------------------------

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0; margin-bottom: 1rem;">
        <h2 style="font-size: 1.2rem; color: #fff;">CHRONICLE <span style="font-size:0.7rem; color:#2E5CFF; border:1px solid #2E5CFF; padding: 2px 6px; border-radius:4px; vertical-align: middle;">V3.0</span></h2>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["Command Center", "Memory Grid", "Intelligence"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # System Controls in Sidebar
    collector_active = is_collector_running()
    
    if collector_active:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 12px; border-radius: 8px; display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <div class="status-dot dot-green"></div>
            <div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #10B981;">SYSTEM ACTIVE</div>
                <div style="font-size: 0.7rem; color: #94A3B8;">Collector running</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("TERMINATE PROCESS", use_container_width=True):
            stop_collector()
            st.rerun()
    else:
        st.markdown("""
        <div style="background: rgba(100, 116, 139, 0.1); border: 1px solid rgba(100, 116, 139, 0.3); padding: 12px; border-radius: 8px; display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <div class="status-dot dot-grey"></div>
            <div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #94A3B8;">SYSTEM DORMANT</div>
                <div style="font-size: 0.7rem; color: #64748B;">Collector inactive</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("INITIATE SCAN", use_container_width=True):
            start_collector()
            st.rerun()

# Top Header (Appears on all pages)
col_head_1, col_head_2, col_head_3 = st.columns([2, 1, 1])
with col_head_1:
    # Page Title injection
    page_title_map = {
        "Command Center": "COMMAND CENTER",
        "Memory Grid": "MEMORY ARCHIVE",
        "Intelligence": "TEMPORAL INTELLIGENCE"
    }
    st.markdown(f"<h1 style='margin:0; font-size:1.8rem;'>{page_title_map[page]}</h1>", unsafe_allow_html=True)

with col_head_3:
    # Status Pill in Header
    status_text = "ONLINE" if collector_active else "OFFLINE"
    status_color = "#10B981" if collector_active else "#64748B"
    st.markdown(f"""
    <div style="text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 10px; height: 100%;">
        <span style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: {status_color};">● API {status_text}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin-top: 10px; margin-bottom: 30px;'>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# PAGE: COMMAND CENTER
# -----------------------------------------------------------------------------
if page == "Command Center":
    # Stats Row
    total_memories = collection.count_documents({})
    last_memory = collection.find_one(sort=[("timestamp", -1)])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-label">
                <span style="font-size:1.2rem;">📚</span> MEMORY DENSITY
            </div>
            <div class="card-value data-font">{total_memories:,}<span style="font-size:1rem; color:#94A3B8;"> pts</span></div>
            <div class="card-sub">Total Indexed Moments</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        status_disp = "Active" if collector_active else "Offline"
        status_col = "#10B981" if collector_active else "#EF4444"
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-label">
                <span style="font-size:1.2rem;">⚡</span> SESSION HEALTH
            </div>
            <div class="card-value" style="color: {status_col}">{status_disp}</div>
            <div class="card-sub">Collector Process Status</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        if last_memory:
            time_diff = datetime.utcnow() - last_memory['timestamp']
            if time_diff.seconds < 60:
                time_str = "Just now"
            elif time_diff.seconds < 3600:
                time_str = f"{time_diff.seconds // 60}m ago"
            else:
                time_str =f"{time_diff.seconds // 3600}h ago"
        else:
            time_str = "N/A"
            
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-label">
                <span style="font-size:1.2rem;">🕒</span> RECENT ACTIVITY
            </div>
            <div class="card-value data-font">{time_str}</div>
            <div class="card-sub">Last Data Ingestion</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ RECENT CAPTURE STREAM")
    
    if last_memory and os.path.exists(last_memory.get('image_path', '')):
        # Display the image in a styled container
        st.markdown(f"""
        <div style="background: #0F0F16; border: 1px solid var(--border-color); border-radius: 16px; padding: 10px; margin-top: 10px;">
            <div style="margin-bottom: 10px; font-family:'JetBrains Mono'; font-size: 0.8rem; color: #94A3B8;">
                CAPTURE_ID: {str(last_memory['_id'])[-6:]} | TIMESTAMP: {last_memory['timestamp'].strftime('%Y-%m-%d %H:%M:%S UTC')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.image(last_memory['image_path'], use_container_width=True)
        st.caption(last_memory['summary'])
    else:
        st.markdown("""
        <div class="dashboard-card" style="height: 300px; display: flex; align-items: center; justify-content: center; flex-direction: column; border-style: dashed;">
            <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.2;">🖥️</div>
            <div style="color: #64748B; font-weight: 600;">AWAITING FIRST SIGNAL</div>
            <div style="color: #475569; font-size: 0.9rem;">No capture data available in stream</div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE: MEMORY GRID
# -----------------------------------------------------------------------------
elif page == "Memory Grid":
    # Filter Controls
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("##### Filter Archive")
    
    # Simple Date Filter
    filter_opt = st.selectbox(
        "Time Range",
        ["All Time", "Today", "Yesterday", "Last 7 Days"],
        label_visibility="collapsed"
    )
    
    q = {}
    if filter_opt == "Today":
        start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        q = {"timestamp": {"$gte": start}}
    elif filter_opt == "Yesterday":
        start = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        q = {"timestamp": {"$gte": start, "$lt": end}}
    elif filter_opt == "Last 7 Days":
        q = {"timestamp": {"$gte": datetime.now() - timedelta(days=7)}}
        
    memories = list(collection.find(q).sort("timestamp", -1).limit(50))
    
    if not memories:
        st.info("No memories found for this period.")
    
    for mem in memories:
        img_path = mem.get('image_path', '')
        has_img = os.path.exists(img_path)
        
        st.markdown(f"""
        <div class="timeline-row">
            <div style="min-width: 80px;">
                <div class="time-badge">{mem['timestamp'].strftime('%H:%M')}</div>
            </div>
            <div style="flex-grow: 1;">
                <div style="color: #E2E8F0; font-size: 1rem; line-height: 1.5; margin-bottom: 8px;">
                    {mem['summary']}
                </div>
                <div style="font-size: 0.8rem; color: #64748B; font-family: 'JetBrains Mono';">
                    ID: {str(mem['_id'])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Streamlit Image Expander
        if has_img:
            with st.expander("📸 View Capture", expanded=False):
                st.image(img_path, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE: INTELLIGENCE
# -----------------------------------------------------------------------------
elif page == "Intelligence":
    # Center Layout
    st.markdown("""
    <div style="text-align: center; padding: 4rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1rem; animation: float 6s ease-in-out infinite;">🧠</div>
        <h2 style="font-size: 2.5rem; margin-bottom: 0.5rem; background: linear-gradient(to right, #fff, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Temporal Intelligence</h2>
        <p style="color: #94A3B8; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            Ask me anything about your recorded history. I can recall screen context, activities, and specific details.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search Bar
    query = st.text_input("Ask Chronicle...", placeholder="What was I working on yesterday afternoon?", label_visibility="collapsed")
    
    # Suggestions
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; font-size: 0.9rem; color: #cbd5e1; text-align: center; cursor: pointer; border: 1px solid rgba(255,255,255,0.1);">
            "Summarize my work today"
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; font-size: 0.9rem; color: #cbd5e1; text-align: center; cursor: pointer; border: 1px solid rgba(255,255,255,0.1);">
            "Did I visit any news sites?"
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    if query:
        with st.spinner("Accessing Neural Archives..."):
             # Simple context retrieval logic
             relevant_docs = list(collection.find({"summary": {"$regex": query, "$options": "i"}}).sort("timestamp", -1).limit(10))
             
             if not relevant_docs:
                 # Fallback to general AI chat if no kw match, or just use recent
                 relevant_docs = list(collection.find().sort("timestamp", -1).limit(20))
             
             context = "\n".join([f"[{d['timestamp']}] {d['summary']}" for d in relevant_docs])
             
             prompt = f"""User Query: {query}
             
             Context from my screen history:
             {context}
             
             Answer functionality based on the context provided."""
             
             try:
                response = client_ai.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                st.markdown(f"""
                <div style="background: #0F0F16; border: 1px solid #2E5CFF; border-radius: 12px; padding: 20px; margin-top: 20px;">
                    <div style="display: flex; align-items: start; gap: 12px;">
                        <div style="font-size: 1.5rem;">🤖</div>
                        <div style="line-height: 1.6; color: #E2E8F0;">
                            {response.text}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
             except Exception as e:
                 st.error(f"Intelligence Module Error: {e}")