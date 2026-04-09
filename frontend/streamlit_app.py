import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
import streamlit as st
import json
from groq import Groq
from prompts import explain_report_prompt
from utils.extractor import extract_text_from_pdf, extract_text_from_image
from utils.ai_extractor import ai_extract_parameters
from utils.parser import analyze_report
from chatbot.memory import trim_history, summarize_memory

# Show login ONLY when button clicked
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_login" not in st.session_state:
    st.session_state.show_login = False
 


# ─────────────────────────────────────────────
# CONFIG & INIT
# ─────────────────────────────────────────────
load_dotenv(dotenv_path=".env")
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ GROQ_API_KEY not found in .env file.")
    st.stop()

client = Groq(api_key=api_key)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MediScan AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Clean clinical + modern dark UI
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Syne:wght@700;800&display=swap');

:root {
    --bg: #0a0d14;
    --surface: #111520;
    --surface2: #181e2e;
    --border: rgba(99,139,255,0.15);
    --accent: #638bff;
    --accent2: #3fffc2;
    --danger: #ff5c7a;
    --warn: #ffb347;
    --text: #e8eaf6;
    --muted: #7b83a0;
    --card-radius: 16px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1200px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Logo area ── */
.logo-wrap {
    display: flex; align-items: center; gap: 10px;
    padding: 0 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.logo-icon {
    width: 40px; height: 40px; border-radius: 10px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.logo-text { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }
.logo-text span { color: var(--accent2); }

/* ── Cards ── */
.card {
    background: rgba(17,21,32,0.65);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.03);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
}
.card:hover {
    transform: translateY(-4px);
    transition: 0.2s;
    border-color: rgba(99,139,255,0.4);
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 0.75rem;
}

/* ── Metric pills ── */
.metrics-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 1.25rem; }
.metric-pill {
    flex: 1; min-width: 120px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    text-align: center;
}
.metric-pill .val { font-family: 'Syne', sans-serif; font-size: 22px; font-weight: 800; }
.metric-pill .lbl { font-size: 11px; color: var(--muted); margin-top: 2px; text-transform: uppercase; letter-spacing: 0.06em; }
.status-high { color: var(--danger); }
.status-low  { color: var(--warn);   }
.status-norm { color: var(--accent2); }

/* ── Status badge ── */
.badge {
    display: inline-block; font-size: 11px; font-weight: 600;
    padding: 3px 10px; border-radius: 99px;
    text-transform: uppercase; letter-spacing: 0.05em;
}
.badge-high { background: rgba(255,92,122,0.15); color: var(--danger); border: 1px solid rgba(255,92,122,0.3); }
.badge-low  { background: rgba(255,179,71,0.12);  color: var(--warn);   border: 1px solid rgba(255,179,71,0.3); }
.badge-norm { background: rgba(63,255,194,0.1);  color: var(--accent2); border: 1px solid rgba(63,255,194,0.25); }

/* ── Parameter table ── */
.param-table { width: 100%; border-collapse: collapse; font-size: 13.5px; }
.param-table th { color: var(--muted); font-weight: 500; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; padding: 0 0 0.5rem; text-align: left; border-bottom: 1px solid var(--border); }
.param-table td { padding: 0.6rem 0; border-bottom: 1px solid rgba(99,139,255,0.07); vertical-align: middle; }
.param-table tr:last-child td { border-bottom: none; }

/* ── Chat bubbles ── */
.bubble-user {
    background: linear-gradient(135deg, rgba(99,139,255,0.2), rgba(99,139,255,0.1));
    border: 1px solid rgba(99,139,255,0.3);
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1rem; margin: 0.5rem 0; margin-left: 15%;
    font-size: 14px; line-height: 1.6;
}
.bubble-ai {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 18px 18px 18px 4px;
    padding: 0.75rem 1rem; margin: 0.5rem 0; margin-right: 10%;
    font-size: 14px; line-height: 1.6;
}
.bubble-label {
    font-size: 11px; font-weight: 600; letter-spacing: 0.06em;
    text-transform: uppercase; margin-bottom: 4px;
}
.label-user { color: var(--accent); text-align: right; }
.label-ai   { color: var(--accent2); }

/* ── Page header ── */
.page-header {
    margin-bottom: 2rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border);
}
.page-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 28px; font-weight: 800;
    letter-spacing: -0.5px; margin: 0; line-height: 1.2;
}
.page-header p { color: var(--muted); font-size: 14px; margin-top: 6px; }

/* ── Disclaimer ── */
.disclaimer {
    background: rgba(255,179,71,0.07);
    border: 1px solid rgba(255,179,71,0.25);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 12px; color: var(--warn);
    margin-top: 0.5rem;
}

/* ── Streamlit widget overrides ── */
.stTextArea textarea, .stTextInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(99,139,255,0.2) !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #4f7aff) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 0.55rem 1.5rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }
.stFileUploader {
    background: var(--surface2) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 12px !important;
}
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
div[data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    padding: 4px !important;
    gap: 4px !important;
}
div[data-baseweb="tab"] {
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
}
div[aria-selected="true"][data-baseweb="tab"] {
    background: var(--surface2) !important;
    color: var(--text) !important;
}
.stSpinner > div { border-top-color: var(--accent) !important; }
.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# TOP NAVBAR (FINAL CLEAN VERSION)
# ─────────────────────────────────────────────
st.markdown("""
<style>
.topbar {
    position: sticky;
    top: 0;
    z-index: 999;
    background: rgba(10,13,20,0.9);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(99,139,255,0.15);
    border-radius: 14px;
    padding: 0.7rem 1.2rem;
    margin-bottom: 1.5rem;
}
.topbar-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.brand {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 800;
}
.brand span {
    color: #3fffc2;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
  <div class="topbar-inner">
    <div class="brand">🩺 Medi<span>Scan</span> AI</div>
    <div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# Right-side buttons
col1, col2 = st.columns([9,1])

with col2:
    if not st.session_state.logged_in:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.show_login = True
    else:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

# ─────────────────────────────────────────────
# INLINE LOGIN PANEL (NO MODAL)
# ─────────────────────────────────────────────
# ✅ SHOW LOGIN CARD
if st.session_state.show_login and not st.session_state.logged_in:

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 4, 3])

    with col2:
        st.markdown("""
        <div style="
            background: rgba(17,21,32,0.95);
            border: 1px solid rgba(99,139,255,0.25);
            border-radius: 18px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.6);
            text-align: center;
        ">
        """, unsafe_allow_html=True)

        st.markdown("## 🔐 Login to MediScan AI")

        username = st.text_input("Username", key="login_user_final")
        password = st.text_input("Password", type="password", key="login_pass_final")

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("Login", use_container_width=True):
                if username == "admin" and password == "1234":
                    st.session_state.logged_in = True
                    st.session_state.show_login = False
                    st.success("Logged in successfully")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with col_btn2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_login = False
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # 🔥 STOP rest of page (IMPORTANT)
    st.stop()
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "report_text": "",
        "final_data": {},
        "conditions": [],
        "summary": "",
        "chat_history": [],
        "memory_summary": "",
        "system_prompt": "",
        "analyzed": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
MAX_HISTORY = 8

def login_ui():
    st.markdown("## 🔐 Login to MediScan AI")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email == "demo@mediscan.ai" and password == "1234":
            st.session_state.user = email
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Invalid credentials")

def signup_ui():
    st.markdown("## 📝 Create Account")

    new_email = st.text_input("New Email")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Sign Up"):
        st.success("Account created (demo only)")


# ─────────────────────────────────────────────
# AI HELPERS
# ─────────────────────────────────────────────
def get_summary(prompt):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": """You are an AI medical assistant.

You MUST follow this format strictly:

🧠 Explanation:
(4-5 sentences)

💡 Key Advice:

Diet:
- Give 3-4 specific food suggestions

Lifestyle:
- Give 2-3 daily routine tips

Precautions:
- Give 2-3 warnings

STRICT RULES:
- NEVER mention doctors
- NEVER write everything in one paragraph
- ALWAYS follow headings exactly
- ALWAYS give specific advice"""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"


def chat_with_ai(user_q):
    messages_to_send = [{"role": "system", "content": st.session_state.system_prompt}]
    if st.session_state.memory_summary:
        messages_to_send.append({
            "role": "system",
            "content": f"Previous context: {st.session_state.memory_summary}"
        })
    messages_to_send.extend([
        m for m in st.session_state.chat_history if m["role"] != "system"
    ])

    contextual_q = f"Patient condition: {st.session_state.conditions}\n\nUser question: {user_q}"
    messages_to_send.append({"role": "user", "content": contextual_q})

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages_to_send,
            temperature=0.3
        )
        reply = response.choices[0].message.content

        st.session_state.chat_history.append({"role": "user", "content": user_q})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        st.session_state.chat_history = trim_history(st.session_state.chat_history, MAX_HISTORY)

        if len(st.session_state.chat_history) >= MAX_HISTORY:
            st.session_state.memory_summary = summarize_memory(st.session_state.chat_history, client)
            st.session_state.chat_history = []

        return reply
    except Exception as e:
        return f"❌ Error: {str(e)}"


def status_badge(status):
    s = status.lower()
    if s == "high":
        return '<span class="badge badge-high">High ↑</span>'
    elif s == "low":
        return '<span class="badge badge-low">Low ↓</span>'
    else:
        return '<span class="badge badge-norm">Normal ✓</span>'

def status_class(status):
    s = status.lower()
    if s == "high": return "status-high"
    if s == "low": return "status-low"
    return "status-norm"


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
      <div class="logo-icon">🩺</div>
      <div class="logo-text">Medi<span>Scan</span> AI</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem;">Input Method</div>', unsafe_allow_html=True)
    input_method = st.selectbox("", ["Text", "Upload Image", "Upload PDF"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    if input_method == "Text":
        report_text_input = st.text_area(
            "Paste lab report",
            height=220,
            placeholder="e.g. Hemoglobin: 10.5 g/dL\nBlood Sugar (Fasting): 130 mg/dL\n...",
            label_visibility="collapsed"
        )
    elif input_method == "Upload Image":
        img_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        report_text_input = None
    else:
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
        report_text_input = None

    analyze_btn = st.button("🔬 Analyse Report")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="disclaimer">⚠️ Not a substitute for professional medical advice.</div>', unsafe_allow_html=True)

    if st.session_state.analyzed:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
# ─────────────────────────────────────────────
# ANALYSE LOGIC
# ─────────────────────────────────────────────
if analyze_btn:
    raw_text = ""
    try:
        if input_method == "Text":
            raw_text = report_text_input or ""
        elif input_method == "Upload Image":
            if img_file:
                with open("_tmp_img", "wb") as f:
                    f.write(img_file.read())
                raw_text = extract_text_from_image("_tmp_img")
        else:
            if pdf_file:
                with open("_tmp.pdf", "wb") as f:
                    f.write(pdf_file.read())
                raw_text = extract_text_from_pdf("_tmp.pdf")

        if len(raw_text.strip()) < 30:
            st.sidebar.error("⚠️ Could not extract enough text. Try a clearer file or paste text directly.")
            st.stop()

        with st.spinner("Analysing report…"):
            ai_data = ai_extract_parameters(raw_text, client)
            ai_data = ai_data.strip().replace("```json", "").replace("```", "")
            try:
                parsed_data = json.loads(ai_data)
            except json.JSONDecodeError as e:
                st.sidebar.error(f"❌ JSON parse error: {e}")
                parsed_data = {}

            final_data = analyze_report(parsed_data)
            conditions = []
            for param, details in final_data.items():
                s = details.get("status", "").lower()
                if s == "low":
                    conditions.append(f"{param} is low")
                elif s == "high":
                    conditions.append(f"{param} is high")
            if not conditions:
                conditions.append("All parameters are normal")

            prompt = explain_report_prompt(str(final_data))
            summary = get_summary(prompt)

            system_prompt = f"""You are a smart AI medical assistant.

Patient Report:
{final_data}

Detected Conditions:
{conditions}

Your job:
- Answer ONLY based on this patient's data
- Give personalized diet, lifestyle, precautions
- Explain reasons clearly

STRICT RULES:
- DO NOT give generic answers
- ALWAYS refer to patient condition
- Be specific (mention exact foods, habits)
- Keep answers structured

Always end with: "This is not a medical diagnosis.\""""

            st.session_state.report_text = raw_text
            st.session_state.final_data = final_data
            st.session_state.conditions = conditions
            st.session_state.summary = summary
            st.session_state.system_prompt = system_prompt
            st.session_state.chat_history = []
            st.session_state.memory_summary = ""
            st.session_state.analyzed = True

    except Exception as e:
        st.sidebar.error(f"❌ {str(e)}")

# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────


if not st.session_state.analyzed:
    # Landing state
    st.markdown("""
    <div style="max-width:640px; margin: 4rem auto; text-align:center; padding: 2rem;">
      <div style="font-size:56px; margin-bottom:1rem;">🩺</div>
      <h1 style="font-family:'Syne',sans-serif; font-size:36px; font-weight:800; letter-spacing:-1px; margin-bottom:0.75rem;">
        Lab Report <span style="color:#638bff;">Analyser</span>
      </h1>
      <p style="color:#7b83a0; font-size:16px; line-height:1.7; margin-bottom:2rem;">
        Paste your lab report, upload an image, or drop a PDF —<br>
        get a clear AI-powered breakdown of your results instantly.
      </p>
      <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
        <div style="background:rgba(99,139,255,0.1); border:1px solid rgba(99,139,255,0.25); border-radius:12px; padding:1rem 1.25rem; text-align:left; min-width:160px;">
          <div style="font-size:22px;">📋</div>
          <div style="font-size:13px; font-weight:500; margin-top:6px;">Text Input</div>
          <div style="font-size:12px; color:#7b83a0;">Paste report details</div>
        </div>
        <div style="background:rgba(63,255,194,0.08); border:1px solid rgba(63,255,194,0.2); border-radius:12px; padding:1rem 1.25rem; text-align:left; min-width:160px;">
          <div style="font-size:22px;">🖼️</div>
          <div style="font-size:13px; font-weight:500; margin-top:6px;">Image Upload</div>
          <div style="font-size:12px; color:#7b83a0;">JPG, PNG supported</div>
        </div>
        <div style="background:rgba(255,92,122,0.08); border:1px solid rgba(255,92,122,0.2); border-radius:12px; padding:1rem 1.25rem; text-align:left; min-width:160px;">
          <div style="font-size:22px;">📄</div>
          <div style="font-size:13px; font-weight:500; margin-top:6px;">PDF Upload</div>
          <div style="font-size:12px; color:#7b83a0;">Lab report PDFs</div>
        </div>
      </div>
      <p style="margin-top:2rem; font-size:13px; color:#7b83a0;">← Use the sidebar to get started</p>
    </div>
    """, unsafe_allow_html=True)

else:
    # Results
    st.markdown("""
    <div class="page-header">
      <h1>Report Analysis</h1>
      <p>Your lab results have been analysed. See the breakdown below.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊  Results & Summary", "💬  AI Chatbot", "📄  Raw Report"])

    # ── TAB 1: Results ──────────────────────────
    with tab1:
        final_data = st.session_state.final_data

        if final_data:
            # Status summary pills
            high_c = sum(1 for d in final_data.values() if d.get("status","").lower()=="high")
            low_c  = sum(1 for d in final_data.values() if d.get("status","").lower()=="low")
            norm_c = len(final_data) - high_c - low_c

            st.markdown(f"""
            <div class="metrics-row">
              <div class="metric-pill">
                <div class="val status-high">{high_c}</div>
                <div class="lbl">High</div>
              </div>
              <div class="metric-pill">
                <div class="val status-low">{low_c}</div>
                <div class="lbl">Low</div>
              </div>
              <div class="metric-pill">
                <div class="val status-norm">{norm_c}</div>
                <div class="lbl">Normal</div>
              </div>
              <div class="metric-pill">
                <div class="val" style="color:#638bff;">{len(final_data)}</div>
                <div class="lbl">Total</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Parameter table
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Parameter Breakdown</div>', unsafe_allow_html=True)

            rows_html = ""
            for param, details in final_data.items():
                val    = details.get("value", "N/A")
                unit   = details.get("unit", "")
                ref    = details.get("reference_range", "—")
                status = details.get("status", "normal")
                rows_html += f"""
                <tr>
                  <td style="font-weight:500; padding-right:1rem;">{param}</td>
                  <td class="{status_class(status)}" style="font-weight:600;">{val} {unit}</td>
                  <td style="color:#7b83a0; font-size:12px;">{ref}</td>
                  <td>{status_badge(status)}</td>
                </tr>"""

            st.markdown(f"""
            <table class="param-table">
              <thead><tr>
                <th>Parameter</th>
                <th>Value</th>
                <th>Reference</th>
                <th>Status</th>
              </tr></thead>
              <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Conditions
        if st.session_state.conditions:
            cond_items = "".join(
                f'<li style="margin-bottom:4px; font-size:14px;">{c}</li>'
                for c in st.session_state.conditions
            )
            st.markdown(f"""
            <div class="card">
              <div class="card-title">Detected Conditions</div>
              <ul style="margin:0; padding-left:1.2rem; color:#e8eaf6;">{cond_items}</ul>
            </div>
            """, unsafe_allow_html=True)

        # AI Summary
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🧠 AI Summary & Advice</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:14px; line-height:1.8; white-space:pre-wrap;">{st.session_state.summary}</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 2: Chatbot ───────────────────────────
    with tab2:
        st.markdown("""
        <div style="margin-bottom:1rem;">
          <div style="font-size:13px; color:#7b83a0; line-height:1.6;">
            Ask anything about your report — diet, lifestyle, what a parameter means, or follow-up questions.
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Chat display
        chat_container = st.container()
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div style="text-align:center; padding:2rem; color:#7b83a0;">
                  <div style="font-size:32px; margin-bottom:0.5rem;">💬</div>
                  <div style="font-size:14px;">Ask me anything about your report</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f"""
                        <div class="label-user bubble-label">You</div>
                        <div class="bubble-user">{msg['content']}</div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="label-ai bubble-label">MediScan AI</div>
                        <div class="bubble-ai">{msg['content']}</div>
                        """, unsafe_allow_html=True)

        # Suggested questions
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px; color:#7b83a0; text-transform:uppercase; letter-spacing:.06em; margin-bottom:.4rem;">Suggested questions</div>', unsafe_allow_html=True)
        q_cols = st.columns(3)
        suggestions = [
            "What foods should I eat?",
            "What lifestyle changes help?",
            "Explain my key abnormalities",
        ]
        for i, (col, q) in enumerate(zip(q_cols, suggestions)):
            with col:
                if st.button(q, key=f"sug_{i}"):
                    with st.spinner("Thinking…"):
                        chat_with_ai(q)
                    st.rerun()

        # Chat input
        user_input = st.chat_input("Ask about your report…")
        if user_input:
            with st.spinner("Thinking…"):
                chat_with_ai(user_input)
            st.rerun()

    # ── TAB 3: Raw Report ───────────────────────
    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Extracted Text</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:13px; color:#7b83a0; white-space:pre-wrap; line-height:1.7;">{st.session_state.report_text}</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
# ─────────────────────────────────────────────
# ADD THIS CSS AT END OF YOUR EXISTING CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* Floating Chatbot Button */
.floating-chat-btn {
    position: fixed;
    bottom: 25px;
    right: 25px;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #638bff, #3fffc2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    cursor: pointer;
    z-index: 9999;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.floating-chat-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────────
# ADD FLOATING CHAT BUTTON (BOTTOM RIGHT)
# ─────────────────────────────────────────────
st.markdown("""
<div class="floating-chat-btn" onclick="window.location.href='#chatbot'">
    💬
</div>
""", unsafe_allow_html=True)
