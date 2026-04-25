import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# also make frontend/ itself importable (for db, auth_ui, etc.)
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

import streamlit as st
from openai import OpenAI

from db import init_db, create_user
from auth_ui import render as render_auth
from components.styles import get_theme, inject_css
import page_modules.landing   as pg_landing
import page_modules.dashboard as pg_dashboard
import page_modules.history   as pg_history
import page_modules.analytics as pg_analytics
import page_modules.reports   as pg_reports
import page_modules.settings  as pg_settings

# ── Bootstrap ─────────────────────────────────────────────────────────────────
init_db()
try:
    create_user("Admin", "admin@mediscan.ai", "admin123")
except Exception:
    pass

st.set_page_config(page_title="MediScan AI", page_icon="🩺",
                   layout="wide", initial_sidebar_state="expanded")

# ── Session defaults ──────────────────────────────────────────────────────────
_DEFAULTS = {
    "user": None, "page": "landing", "dark_mode": False,
    "report_text": "", "final_data": {}, "conditions": [],
    "summary": "", "patient_summary": "", "chat_history": [], "memory_summary": "",
    "system_prompt": "", "analyzed": False,
    "prec_chat": [], "diet_chat": [],
    "prec_bullets": [], "diet_bullets": [],
    "show_prec_chat": False, "show_diet_chat": False,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── CSS ───────────────────────────────────────────────────────────────────────
_T = get_theme(st.session_state.dark_mode)
inject_css(_T)

# ── Auth gate ─────────────────────────────────────────────────────────────────
if not st.session_state.user:
    render_auth()
    st.stop()

# ── API client ────────────────────────────────────────────────────────────────
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    st.error("OPENROUTER_API_KEY not found in .env"); st.stop()
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

user = st.session_state.user
page = st.session_state.page

NAV = [
    ("landing",   "🏠", "Home"),
    ("dashboard", "📊", "Dashboard"),
    ("reports",   "📋", "Reports"),
    ("history",   "🕐", "History"),
    ("analytics", "📈", "Analytics"),
    ("settings",  "⚙️", "Settings"),
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🩺 MediScan AI")
    st.markdown("---")
    _dm = st.session_state.dark_mode
    if st.button("🌙 Dark Mode" if not _dm else "☀️ Light Mode", key="dm_toggle", use_container_width=True):
        st.session_state.dark_mode = not _dm
        st.rerun()
    st.markdown("---")
    for pg, icon, label in NAV:
        if st.button(f"{icon}  {label}", key=f"sb_{pg}", use_container_width=True,
                     type="primary" if page == pg else "secondary"):
            st.session_state.page = pg
            st.rerun()
    st.markdown("---")
    st.markdown(f"**{user['name']}**  \n{user['email']}")
    if st.button("🚪 Logout", key="sb_logout", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── Router ────────────────────────────────────────────────────────────────────
if page == "landing":
    pg_landing.render()
elif page == "dashboard":
    pg_dashboard.render(user, client)
elif page == "history":
    pg_history.render(user)
elif page == "analytics":
    pg_analytics.render(user)
elif page == "reports":
    pg_reports.render(user)
elif page == "settings":
    pg_settings.render(user)
