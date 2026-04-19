<<<<<<< HEAD
import sys, os, json, datetime, uuid, hashlib, sqlite3
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
import streamlit as st
=======
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

import streamlit as st
import json
>>>>>>> dba419a332508878fc47ed5bddc846ff792eabe6
from groq import Groq
from prompts import explain_report_prompt
from utils.extractor import extract_text_from_pdf, extract_text_from_image
from utils.ai_extractor import ai_extract_parameters
<<<<<<< HEAD
from utils.parser import analyze_report, KEY_METRICS, PARAMETERS
from chatbot.memory import trim_history, summarize_memory

st.set_page_config(page_title="MediScan AI", page_icon="🩺",
                   layout="wide", initial_sidebar_state="expanded")

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE  (SQLite — users + reports)
# ─────────────────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "mediscan.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    NOT NULL UNIQUE,
            pw_hash  TEXT    NOT NULL,
            created  TEXT    NOT NULL
        );
        CREATE TABLE IF NOT EXISTS reports (
            id        TEXT    PRIMARY KEY,
            user_id   INTEGER NOT NULL,
            timestamp TEXT    NOT NULL,
            conditions TEXT   NOT NULL,
            params    INTEGER NOT NULL,
            abnormal  INTEGER NOT NULL,
            data      TEXT    NOT NULL,
            summary   TEXT    NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    conn.commit(); conn.close()

init_db()

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def create_user(name, email, password):
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (name,email,pw_hash,created) VALUES (?,?,?,?)",
            (name.strip(), email.strip().lower(), hash_pw(password),
             datetime.datetime.now().isoformat(timespec="seconds"))
        )
        conn.commit(); conn.close()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    except Exception as e:
        return False, str(e)

def login_user(email, password):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM users WHERE email=? AND pw_hash=?",
        (email.strip().lower(), hash_pw(password))
    ).fetchone()
    conn.close()
    if row:
        return True, dict(row)
    return False, None

def save_report(user_id, final_data, conditions, summary):
    rid = str(uuid.uuid4())[:8].upper()
    conn = get_db()
    conn.execute(
        "INSERT INTO reports (id,user_id,timestamp,conditions,params,abnormal,data,summary) VALUES (?,?,?,?,?,?,?,?)",
        (rid, user_id,
         datetime.datetime.now().isoformat(timespec="seconds"),
         json.dumps(conditions),
         len(final_data),
         sum(1 for d in final_data.values() if d.get("status","").lower() in ("high","low")),
         json.dumps(final_data, default=str),
         summary)
    )
    conn.commit(); conn.close()
    return rid

def get_user_reports(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM reports WHERE user_id=? ORDER BY timestamp DESC LIMIT 50",
        (user_id,)
    ).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["conditions"] = json.loads(d["conditions"])
        d["data"]       = json.loads(d["data"])
        result.append(d)
    return result

# ─────────────────────────────────────────────────────────────────────────────
# SESSION BOOTSTRAP
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    "user": None,               # dict with id, name, email
    "page": "landing",
    "auth_tab": "login",        # login | signup
    "report_text": "", "final_data": {}, "conditions": [],
    "summary": "", "chat_history": [], "memory_summary": "",
    "system_prompt": "", "analyzed": False,
    "prec_chat": [], "diet_chat": [],
    "prec_bullets": [], "diet_bullets": [],
    "show_prec_chat": False, "show_diet_chat": False,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

load_dotenv(dotenv_path=".env")
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not found in .env"); st.stop()
=======
from utils.parser import analyze_report
from chatbot.memory import trim_history, summarize_memory
from auth import init_db, register_user, login_user, save_report, get_user_reports, get_report_by_id, delete_report

# ── DB & page config ──────────────────────────────────────────────────────────
init_db()

st.set_page_config(page_title="MediScan AI", page_icon="🩺", layout="wide",
                   initial_sidebar_state="expanded")

# ── Session defaults ──────────────────────────────────────────────────────────
_defaults = {
    "logged_in":      False,
    "is_guest":       False,
    "auth_page":      "login",   # login | signup
    "page":           "analyse", # analyse | dashboard
    "user":           {},
    "report_text":    "",
    "final_data":     {},
    "conditions":     [],
    "summary":        "",
    "chat_history":   [],
    "memory_summary": "",
    "system_prompt":  "",
    "analyzed":       False,
    "view_report_id": None,      # dashboard: report being viewed
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Groq client ───────────────────────────────────────────────────────────────
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ GROQ_API_KEY not found in .env file.")
    st.stop()
>>>>>>> dba419a332508878fc47ed5bddc846ff792eabe6
client = Groq(api_key=api_key)
MAX_HISTORY = 8

# ─────────────────────────────────────────────────────────────────────────────
<<<<<<< HEAD
# VALIDATION
# ─────────────────────────────────────────────────────────────────────────────
MEDICAL_KW = [
    "hemoglobin","haemoglobin","glucose","wbc","rbc","platelet","cholesterol",
    "creatinine","sodium","potassium","calcium","bilirubin","hba1c","tsh",
    "vitamin","iron","triglyceride","urea","albumin","protein","lymphocyte",
    "neutrophil","eosinophil","basophil","monocyte","hematocrit","mcv","mch",
    "mchc","rdw","mpv","esr","crp","ferritin","transferrin","cortisol",
    "insulin","testosterone","estrogen","progesterone","prolactin","lh","fsh",
    "mg/dl","g/dl","mmol/l","iu/l","u/l","meq/l","ng/ml","pg/ml","miu/ml",
    "blood","urine","serum","plasma","test","report","lab","result","panel",
    "normal","range","reference","level","count","value","fasting","random",
    "complete blood","cbc","lipid","liver","kidney","thyroid","metabolic",
]

def validate_medical_input(text: str):
    t = text.strip()
    if len(t) < 30:
        return False, "Input is too short. Please paste a complete lab report."
    lower = t.lower()
    hits = sum(1 for kw in MEDICAL_KW if kw in lower)
    if hits < 2:
        return False, (
            "⚠️ Invalid input detected.\n\n"
            "This does not appear to be a medical or lab report.\n"
            "Please upload a valid lab report (blood test, CBC, lipid panel, etc.).\n\n"
            "Resumes, random text, and non-medical documents are not accepted."
        )
    return True, ""

# ─────────────────────────────────────────────────────────────────────────────
# AI HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _sc(status):
    s = status.lower()
    if s == "high":  return "s-high",  "b-high",  "i-high",  "High ↑"
    if s == "low":   return "s-low",   "b-low",   "i-low",   "Low ↓"
    return                  "s-normal","b-normal","i-normal","Normal ✓"

ICONS = {
    "hemoglobin":"🩸","glucose":"🍬","wbc":"🦠","platelets":"🔵",
    "cholesterol":"🫀","hba1c":"📊","creatinine":"🫘","tsh":"🦋",
    "rbc":"🔴","triglycerides":"🧈","urea":"💧","sodium":"🧂",
    "potassium":"🍌","calcium":"🦴","bilirubin":"🟡","alt":"🔬",
    "ast":"🔬","vitamin_d":"☀️","vitamin_b12":"💊","iron":"⚙️",
}
DEFAULT_ICON = "🧪"
SPARK = {"high":"📈","low":"📉","normal":"〰️"}

def get_summary(prompt):
    try:
        r = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role":"system","content":"""You are an AI medical assistant.
Return EXACTLY two sections with these headings and nothing else:

## PRECAUTIONS
- bullet 1
- bullet 2
- bullet 3
- bullet 4

## DIET RECOMMENDATIONS
- bullet 1
- bullet 2
- bullet 3
- bullet 4

Rules: no doctor mentions, be specific, 4 bullets each."""},
                {"role":"user","content":prompt}
            ], temperature=0.2)
        return r.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def parse_sections(text):
    prec, diet, cur = [], [], None
    for line in text.splitlines():
        l = line.strip()
        if "PRECAUTION" in l.upper():  cur = "prec"
        elif "DIET" in l.upper():      cur = "diet"
        elif l.startswith("-") and cur == "prec":
            prec.append(l.lstrip("- ").strip())
        elif l.startswith("-") and cur == "diet":
            diet.append(l.lstrip("- ").strip())
    return prec, diet

def chat_with_ai(user_q, history_key, system_extra=""):
    sys_p = st.session_state.system_prompt + "\n" + system_extra
    msgs  = [{"role":"system","content":sys_p}]
    if st.session_state.memory_summary:
        msgs.append({"role":"system","content":f"Previous context: {st.session_state.memory_summary}"})
    msgs += [m for m in st.session_state[history_key] if m["role"] != "system"]
    msgs.append({"role":"user","content":f"Patient: {st.session_state.conditions}\n\n{user_q}"})
    try:
        r = client.chat.completions.create(
            model="openai/gpt-oss-120b", messages=msgs, temperature=0.3)
        reply = r.choices[0].message.content
        st.session_state[history_key].append({"role":"user","content":user_q})
        st.session_state[history_key].append({"role":"assistant","content":reply})
        st.session_state[history_key] = trim_history(st.session_state[history_key], MAX_HISTORY)
        return reply
    except Exception as e:
        return f"Error: {e}"

def render_inline_chat(panel_key, input_key, placeholder, system_extra=""):
    for msg in st.session_state[panel_key]:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-label cl-user">You</div>'
                        f'<div class="cbubble-user">{msg["content"]}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-label cl-ai">MediScan AI</div>'
                        f'<div class="cbubble-ai">{msg["content"]}</div>',
                        unsafe_allow_html=True)
    with st.form(key=f"form_{panel_key}", clear_on_submit=True):
        ci, cb = st.columns([5,1])
        with ci:
            q = st.text_input("", placeholder=placeholder,
                              label_visibility="collapsed", key=input_key)
        with cb:
            sent = st.form_submit_button("Send")
        if sent and q.strip():
            with st.spinner("Thinking…"):
                chat_with_ai(q.strip(), panel_key, system_extra)
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
=======
>>>>>>> dba419a332508878fc47ed5bddc846ff792eabe6
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
<<<<<<< HEAD
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@700;800&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"],.stApp{
  font-family:'Inter',sans-serif !important;
  color:#1e2d4a !important;
}
.stApp{
  background:linear-gradient(145deg,#c8daf5 0%,#dce8f7 35%,#e8f0fb 65%,#d0e4f5 100%) !important;
  min-height:100vh;
}
.stApp::before{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    radial-gradient(ellipse 700px 500px at 15% 20%,rgba(147,197,253,.35) 0%,transparent 70%),
    radial-gradient(ellipse 600px 400px at 85% 75%,rgba(167,243,208,.25) 0%,transparent 70%);
}
#MainMenu,footer,header{visibility:hidden;}
/* Single block-container rule — sidebar is native Streamlit, no manual offset needed */
.block-container{
  padding:1.2rem 1.8rem 3rem !important;
  max-width:100% !important;
  position:relative;z-index:1;
}
/* keep Streamlit native sidebar visible — we use it for nav */
/* section[data-testid="stSidebar"] is NOT hidden */

/* ── Native Streamlit sidebar — themed to match app ── */
/* Explicitly show sidebar — overrides any scoped display:none from auth page */
section[data-testid="stSidebar"]{
  display:flex !important;
  background:linear-gradient(180deg,rgba(214,232,250,.92) 0%,rgba(200,224,248,.88) 100%) !important;
  backdrop-filter:blur(22px) saturate(200%) !important;
  border-right:1px solid rgba(255,255,255,.7) !important;
  min-width:250px !important; max-width:270px !important;
  box-shadow:3px 0 24px rgba(74,144,226,.12) !important;
}
section[data-testid="stSidebar"] > div:first-child{
  padding:1.4rem 1rem 1.4rem !important;
}
/* sidebar heading */
section[data-testid="stSidebar"] h3{
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-size:17px !important; font-weight:800 !important;
  color:#1e2d4a !important; letter-spacing:-.3px !important;
  margin-bottom:4px !important;
}
/* sidebar divider */
section[data-testid="stSidebar"] hr{
  border-color:rgba(74,144,226,.18) !important; margin:10px 0 !important;
}
/* sidebar text (user info) */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] .stMarkdown{
  color:#3d5278 !important; font-size:13px !important;
}
/* sidebar nav buttons — default state */
section[data-testid="stSidebar"] .stButton>button{
  background:rgba(255,255,255,.5) !important;
  color:#2d4070 !important;
  border:1px solid rgba(74,144,226,.2) !important;
  border-radius:11px !important;
  font-weight:500 !important; font-size:14px !important;
  text-align:left !important; justify-content:flex-start !important;
  padding:10px 14px !important;
  box-shadow:0 1px 4px rgba(74,144,226,.08) !important;
  margin-bottom:3px !important;
  transition:all .18s ease !important;
  width:100% !important;
}
section[data-testid="stSidebar"] .stButton>button:hover{
  background:rgba(74,144,226,.14) !important;
  color:#1a5fd4 !important;
  border-color:rgba(74,144,226,.4) !important;
  transform:translateX(2px) !important;
  box-shadow:0 2px 10px rgba(74,144,226,.18) !important;
}
/* active / primary sidebar button */
section[data-testid="stSidebar"] .stButton>button[kind="primary"]{
  background:linear-gradient(135deg,#3b82f6,#14b8a6) !important;
  color:#ffffff !important;
  border:none !important;
  font-weight:700 !important;
  box-shadow:0 4px 14px rgba(59,130,246,.35) !important;
}
section[data-testid="stSidebar"] .stButton>button[kind="primary"]:hover{
  opacity:.92 !important; transform:translateX(2px) !important;
}
/* logout button */
section[data-testid="stSidebar"] .stButton:last-of-type>button{
  background:rgba(220,53,69,.08) !important;
  color:#dc3545 !important;
  border:1px solid rgba(220,53,69,.2) !important;
}
section[data-testid="stSidebar"] .stButton:last-of-type>button:hover{
  background:rgba(220,53,69,.15) !important;
  border-color:rgba(220,53,69,.4) !important;
  transform:translateX(2px) !important;
}
/* remove block-container left margin — native sidebar handles layout */
/* (intentionally empty — single rule above is the source of truth) */
/* ── MAIN CONTENT (offset for sidebar — kept for any direct .main-wrap usage) ── */
.main-wrap{margin-left:256px;padding:0;}

/* ── GLASS CARD ── */
.glass-card{
  background:rgba(255,255,255,.65);
  backdrop-filter:blur(18px) saturate(160%);
  border:1px solid rgba(255,255,255,.78);
  border-radius:18px;
  box-shadow:0 4px 24px rgba(74,144,226,.09),0 1px 4px rgba(0,0,0,.04);
  position:relative;overflow:hidden;
}
.glass-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.85),transparent);
}

/* ── PAGE HEADER ── */
.page-header{
  margin-bottom:20px;padding-bottom:16px;
  border-bottom:1px solid rgba(74,144,226,.1);
}
.page-title{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:22px;font-weight:800;color:#1e2d4a;letter-spacing:-.5px;
}
.page-sub{font-size:13px;color:#6b82a8;margin-top:4px;line-height:1.5;}

/* ── SECTION TITLE ── */
.section-title{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:14px;font-weight:700;color:#1e2d4a;
  margin:18px 0 10px;letter-spacing:-.2px;
  display:flex;align-items:center;gap:7px;
}

/* ── METRIC CARDS ── */
.metric-card{
  background:rgba(255,255,255,.7);
  backdrop-filter:blur(18px) saturate(160%);
  border:1px solid rgba(255,255,255,.82);
  border-radius:16px;padding:16px 18px 14px;
  box-shadow:0 4px 20px rgba(74,144,226,.09);
  transition:transform .22s ease,box-shadow .22s ease;
  position:relative;overflow:hidden;min-height:126px;
}
.metric-card:hover{transform:translateY(-4px);box-shadow:0 12px 32px rgba(74,144,226,.16);}
.mc-header{display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:600;color:#3d5278;margin-bottom:10px;}
.mc-icon{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;}
.mc-value{font-family:'Plus Jakarta Sans',sans-serif;font-size:26px;font-weight:800;line-height:1;margin-bottom:3px;letter-spacing:-.5px;}
.mc-unit{font-size:12px;font-weight:500;color:#8a9bbf;margin-left:2px;}
.mc-badge{display:inline-flex;align-items:center;font-size:10.5px;font-weight:600;padding:3px 9px;border-radius:99px;margin-top:7px;}
.mc-ref{font-size:10.5px;color:#a0aec0;margin-top:3px;}
.mc-sparkline{position:absolute;bottom:10px;right:12px;opacity:.2;font-size:20px;}

/* status */
.s-high{color:#dc3545;}.s-low{color:#e67e22;}.s-normal{color:#27ae60;}
.b-high{background:rgba(220,53,69,.1);color:#dc3545;border:1px solid rgba(220,53,69,.22);}
.b-low{background:rgba(230,126,34,.1);color:#e67e22;border:1px solid rgba(230,126,34,.22);}
.b-normal{background:rgba(39,174,96,.1);color:#27ae60;border:1px solid rgba(39,174,96,.22);}
.i-high{background:rgba(220,53,69,.1);}.i-low{background:rgba(230,126,34,.1);}.i-normal{background:rgba(39,174,96,.1);}
.card-tint-high{border-left:3.5px solid rgba(220,53,69,.5) !important;}
.card-tint-low{border-left:3.5px solid rgba(230,126,34,.5) !important;}
.card-tint-normal{border-left:3.5px solid rgba(39,174,96,.4) !important;}

/* ── COUNTS BAR ── */
.counts-bar{display:flex;gap:10px;margin-bottom:18px;flex-wrap:wrap;}
.count-chip{
  display:flex;align-items:center;gap:10px;
  background:rgba(255,255,255,.68);backdrop-filter:blur(14px);
  border:1px solid rgba(255,255,255,.82);border-radius:14px;padding:10px 18px;
  box-shadow:0 2px 12px rgba(74,144,226,.07);
}
.count-chip .num{font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:800;line-height:1;}
.count-chip .lbl{font-size:11.5px;color:#6b82a8;font-weight:500;}

/* ── BAR CARDS ── */
.bar-card{
  background:rgba(255,255,255,.68);backdrop-filter:blur(16px);
  border:1px solid rgba(255,255,255,.82);border-radius:16px;padding:16px 18px;
  box-shadow:0 4px 16px rgba(74,144,226,.07);transition:transform .2s;
}
.bar-card:hover{transform:translateY(-3px);}
.bar-track{background:rgba(0,0,0,.06);border-radius:99px;height:8px;overflow:hidden;margin:10px 0 5px;}
.bar-fill{height:100%;border-radius:99px;}

/* ── PANEL BOXES ── */
.panel-box{
  background:rgba(255,255,255,.68);backdrop-filter:blur(18px) saturate(160%);
  border:1px solid rgba(255,255,255,.82);border-radius:18px;
  padding:18px 20px 14px;box-shadow:0 4px 22px rgba(74,144,226,.08);
}
.panel-header{display:flex;align-items:center;gap:9px;margin-bottom:12px;}
.panel-icon{width:32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:15px;}
.panel-title{font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;font-weight:700;color:#1e2d4a;}
.panel-item{display:flex;align-items:flex-start;gap:9px;padding:7px 0;border-bottom:1px solid rgba(74,144,226,.07);font-size:13px;color:#2c3e6a;line-height:1.55;}
.panel-item:last-of-type{border-bottom:none;}
.panel-check{color:#27ae60;font-size:13px;flex-shrink:0;margin-top:2px;}
.panel-warn{color:#e67e22;font-size:13px;flex-shrink:0;margin-top:2px;}

/* ── GUARDRAILS ── */
.guardrail-card{
  background:linear-gradient(135deg,rgba(235,244,255,.85),rgba(224,242,254,.75));
  backdrop-filter:blur(16px);border:1px solid rgba(74,144,226,.2);
  border-radius:16px;padding:18px 22px;box-shadow:0 4px 20px rgba(74,144,226,.1);
}
.gr-row{display:flex;align-items:center;gap:9px;padding:5px 0;font-size:13px;color:#2c3e6a;}
.gr-no{color:#dc3545;font-weight:700;font-size:14px;}
.gr-yes{color:#27ae60;font-weight:700;font-size:14px;}

/* ── INLINE CHAT ── */
.chat-panel{
  margin-top:10px;background:rgba(235,244,255,.82);backdrop-filter:blur(12px);
  border:1px solid rgba(59,130,246,.18);border-radius:14px;padding:14px 16px;
}
.cbubble-user{
  background:linear-gradient(135deg,#3b82f6,#14b8a6);color:#ffffff;
  border-radius:14px 14px 4px 14px;padding:9px 13px;margin:6px 0;margin-left:18%;
  font-size:13px;line-height:1.6;box-shadow:0 3px 12px rgba(59,130,246,.3);
}
.cbubble-ai{
  background:rgba(255,255,255,.95);border:1px solid rgba(59,130,246,.15);
  border-radius:14px 14px 14px 4px;padding:9px 13px;margin:6px 0;margin-right:8%;
  font-size:13px;line-height:1.6;color:#1e2d4a;
  box-shadow:0 2px 8px rgba(0,0,0,.06);
}
.chat-label{font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:2px;}
.cl-user{color:#3b82f6;text-align:right;}.cl-ai{color:#14b8a6;}

/* ── PARAM TABLE ── */
.ptable{width:100%;border-collapse:collapse;font-size:13px;}
.ptable th{color:#8a9bbf;font-size:10.5px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;padding:0 0 10px;text-align:left;border-bottom:1.5px solid rgba(74,144,226,.12);}
.ptable td{padding:9px 0;border-bottom:1px solid rgba(74,144,226,.06);vertical-align:middle;}
.ptable tr:last-child td{border-bottom:none;}
.ptable tr:hover td{background:rgba(74,144,226,.03);}

/* ── BIG CHAT BUBBLES ── */
.big-bubble-user{
  background:linear-gradient(135deg,rgba(59,130,246,.16),rgba(59,130,246,.07));
  border:1px solid rgba(59,130,246,.3);border-radius:18px 18px 4px 18px;
  padding:11px 15px;margin:7px 0;margin-left:10%;font-size:14px;line-height:1.65;
  color:#1e2d4a;
}
.big-bubble-ai{
  background:rgba(255,255,255,.9);border:1px solid rgba(59,130,246,.14);
  border-radius:18px 18px 18px 4px;padding:11px 15px;margin:7px 0;margin-right:6%;
  font-size:14px;line-height:1.65;color:#1e2d4a;
  box-shadow:0 2px 10px rgba(0,0,0,.06);
}

/* ── HISTORY ROWS ── */
.hist-row{
  display:flex;align-items:center;gap:12px;
  padding:12px 16px;border-radius:12px;
  background:rgba(255,255,255,.58);border:1px solid rgba(255,255,255,.78);
  margin-bottom:8px;transition:background .18s;
}
.hist-row:hover{background:rgba(255,255,255,.78);}
.hist-id{font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;font-weight:700;color:#4a90e2;min-width:76px;}
.hist-time{font-size:11.5px;color:#8a9bbf;min-width:140px;}

/* ── STAT CARDS ── */
.stat-card{
  background:rgba(255,255,255,.68);backdrop-filter:blur(16px);
  border:1px solid rgba(255,255,255,.82);border-radius:16px;
  padding:20px 22px;text-align:center;
  box-shadow:0 4px 16px rgba(74,144,226,.07);
}
.stat-num{font-family:'Plus Jakarta Sans',sans-serif;font-size:34px;font-weight:800;color:#4a90e2;}
.stat-lbl{font-size:12px;color:#6b82a8;font-weight:500;margin-top:4px;}

/* ── LANDING ── */
.hero{
  text-align:center;
  padding:3.5rem 2rem 2.5rem;
  max-width:860px;
  margin:0 auto;
}
.hero-badge{
  display:inline-flex;align-items:center;gap:7px;
  background:rgba(255,255,255,.75);backdrop-filter:blur(14px);
  border:1px solid rgba(59,130,246,.28);border-radius:99px;
  padding:7px 20px;font-size:12.5px;font-weight:600;color:#3b82f6;
  margin-bottom:1.4rem;
  box-shadow:0 2px 12px rgba(59,130,246,.1);
}
.hero-title{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:clamp(28px,4.5vw,54px);font-weight:800;
  color:#1e2d4a;letter-spacing:-1.5px;line-height:1.12;
  margin-bottom:1.1rem;
}
.hero-title span{
  background:linear-gradient(135deg,#3b82f6,#14b8a6);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero-sub{
  font-size:16px;color:#334e68;line-height:1.75;
  max-width:640px;
  margin:0 auto 2rem auto;
  text-align:center;
  font-weight:400;
}
.feature-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
  gap:20px;
  max-width:1100px;
  margin:0 auto;
}
.feature-card{
  background:rgba(255,255,255,.72);
  backdrop-filter:blur(18px) saturate(160%);
  border:1px solid rgba(255,255,255,.88);
  border-radius:18px;
  padding:26px 22px 22px;
  text-align:left;
  box-shadow:0 6px 24px rgba(59,130,246,.09),0 1px 4px rgba(0,0,0,.04);
  transition:transform .28s ease,box-shadow .28s ease;
  animation:fadeUp .55s ease both;
  position:relative;overflow:hidden;
}
.feature-card::before{
  content:'';
  position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,#3b82f6,#14b8a6);
  border-radius:18px 18px 0 0;
  opacity:0;
  transition:opacity .28s ease;
}
.feature-card:hover{transform:translateY(-6px);box-shadow:0 16px 40px rgba(59,130,246,.18),0 2px 8px rgba(0,0,0,.06);}
.feature-card:hover::before{opacity:1;}
@keyframes fadeUp{from{opacity:0;transform:translateY(22px);}to{opacity:1;transform:translateY(0);}}
.feature-card:nth-child(1){animation-delay:.06s;}
.feature-card:nth-child(2){animation-delay:.12s;}
.feature-card:nth-child(3){animation-delay:.18s;}
.feature-card:nth-child(4){animation-delay:.24s;}
.feature-card:nth-child(5){animation-delay:.30s;}
.fc-icon{
  font-size:26px;margin-bottom:14px;
  display:inline-flex;align-items:center;justify-content:center;
  width:50px;height:50px;border-radius:13px;
  background:linear-gradient(135deg,rgba(59,130,246,.12),rgba(20,184,166,.1));
  border:1px solid rgba(59,130,246,.15);
}
.fc-title{font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;font-weight:700;color:#1e2d4a;margin-bottom:8px;letter-spacing:-.1px;}
.fc-desc{font-size:12.5px;color:#4a6080;line-height:1.65;font-weight:400;}

/* ── AUTH CARD ── */
.auth-card{
  background:rgba(255,255,255,.85);backdrop-filter:blur(24px) saturate(180%);
  border:1px solid rgba(255,255,255,.92);border-radius:22px;padding:2.2rem 2.4rem;
  box-shadow:0 20px 60px rgba(74,144,226,.18);
}

/* ── AI SEARCH BAR ── */
.ai-search-wrap{
  background:rgba(255,255,255,.78);
  backdrop-filter:blur(18px) saturate(160%);
  border:1.5px solid rgba(59,130,246,.22);
  border-radius:16px;padding:18px 20px;
  box-shadow:0 4px 20px rgba(59,130,246,.1);
  margin-top:20px;
}
.ai-search-label{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:13.5px;font-weight:700;color:#1e2d4a;
  margin-bottom:10px;display:flex;align-items:center;gap:7px;
}
.ai-search-response{
  margin-top:12px;padding:14px 16px;
  background:rgba(235,244,255,.9);
  border:1px solid rgba(59,130,246,.18);
  border-radius:12px;font-size:13.5px;
  color:#1e2d4a;line-height:1.75;
  white-space:pre-wrap;
}

/* ── UPLOAD CARDS ── */
.upload-grid{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:16px;
  margin-bottom:16px;
}
.upload-card{
  background:rgba(255,255,255,.82);
  backdrop-filter:blur(18px) saturate(160%);
  border:2px solid rgba(59,130,246,.18);
  border-radius:16px;
  padding:24px 16px 20px;
  text-align:center;
  cursor:pointer;
  color:#1e293b !important;
  transition:transform .22s ease, box-shadow .22s ease, border-color .22s ease, background .22s ease;
  box-shadow:0 2px 12px rgba(59,130,246,.08);
  position:relative; z-index:1;
}
.upload-card:hover{
  border-color:rgba(59,130,246,.5);
  background:rgba(255,255,255,.96);
  transform:translateY(-4px);
  box-shadow:0 10px 28px rgba(59,130,246,.18);
}
.uc-icon{
  font-size:32px;
  margin-bottom:10px;
  display:block;
  line-height:1;
}
.uc-title{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:14px;font-weight:700;
  color:#1e293b !important;
  margin-bottom:5px;
  display:block;
}
.uc-sub{
  font-size:12px;
  color:#334e68 !important;
  font-weight:500;
  display:block;
}

/* ── FLOATING CHAT ── */
.float-chat{
  position:fixed;bottom:28px;right:28px;
  background:linear-gradient(135deg,#3b82f6 0%,#14b8a6 100%);
  border-radius:50px;padding:14px 24px;
  display:flex;align-items:center;gap:9px;
  font-size:14px;font-weight:700;color:#ffffff;
  box-shadow:0 8px 32px rgba(59,130,246,.55), 0 2px 8px rgba(0,0,0,.15);
  cursor:pointer;z-index:9999;
  transition:transform .2s ease,box-shadow .2s ease;
  border:1.5px solid rgba(255,255,255,.3);
  letter-spacing:.01em;
}
.float-chat:hover{
  transform:translateY(-4px) scale(1.03);
  box-shadow:0 14px 40px rgba(59,130,246,.65), 0 4px 12px rgba(0,0,0,.18);
}

/* ── WIDGET OVERRIDES ── */
.stTextArea textarea,.stTextInput input{
  background:rgba(255,255,255,.92) !important;
  border:1.5px solid rgba(74,144,226,.25) !important;
  border-radius:10px !important;
  color:#1e2d4a !important;
  font-family:'Inter',sans-serif !important;font-size:13.5px !important;
}
.stTextArea textarea::placeholder,.stTextInput input::placeholder{
  color:#94a3b8 !important;
}
.stTextArea textarea:focus,.stTextInput input:focus{
  border-color:#3b82f6 !important;
  box-shadow:0 0 0 3px rgba(59,130,246,.16) !important;
}
/* input labels */
.stTextInput label,.stTextArea label,.stSelectbox label,
.stFileUploader label,.stRadio label span{
  color:#1e2d4a !important; font-weight:600 !important; font-size:13px !important;
}
/* main buttons */
.stButton>button{
  background:linear-gradient(135deg,#3b82f6,#14b8a6) !important;
  color:#ffffff !important;border:none !important;border-radius:10px !important;
  font-weight:600 !important;font-size:13.5px !important;padding:.55rem 1.3rem !important;
  box-shadow:0 3px 14px rgba(59,130,246,.3) !important;
  transition:opacity .2s,transform .15s !important;width:100%;
}
.stButton>button:hover{opacity:.9 !important;transform:translateY(-1px) !important;}
.stFileUploader{
  background:rgba(255,255,255,.7) !important;
  border:1.5px dashed rgba(74,144,226,.3) !important;border-radius:12px !important;
}
.stSelectbox>div>div{
  background:rgba(255,255,255,.9) !important;
  border:1.5px solid rgba(74,144,226,.25) !important;
  border-radius:10px !important;color:#1e2d4a !important;
}
div[data-baseweb="tab-list"]{
  background:rgba(255,255,255,.6) !important;
  backdrop-filter:blur(12px) !important;border-radius:11px !important;
  border:1px solid rgba(255,255,255,.8) !important;padding:4px !important;gap:3px !important;
}
div[data-baseweb="tab"]{
  border-radius:8px !important;font-weight:500 !important;
  color:#3d5278 !important;font-size:13px !important;
}
div[aria-selected="true"][data-baseweb="tab"]{
  background:rgba(255,255,255,.95) !important;
  color:#1e2d4a !important;font-weight:700 !important;
  box-shadow:0 2px 8px rgba(74,144,226,.12) !important;
}
.stSpinner>div{border-top-color:#3b82f6 !important;}
.stAlert{border-radius:11px !important;}
/* chat input — dark text, visible */
div[data-testid="stChatInput"]>div{
  background:rgba(255,255,255,.92) !important;
  border:1.5px solid rgba(74,144,226,.28) !important;
  border-radius:14px !important;
  box-shadow:0 3px 14px rgba(74,144,226,.1) !important;
}
div[data-testid="stChatInput"] textarea{
  color:#1e2d4a !important;font-size:14px !important;
}
div[data-testid="stChatInput"] textarea::placeholder{
  color:#94a3b8 !important;
}
/* ── ANALYSE BUTTON — full width, prominent CTA ── */
div[data-testid="stExpander"] .stButton>button{
  background:linear-gradient(135deg,#3b82f6 0%,#14b8a6 100%) !important;
  color:#ffffff !important;
  border:none !important;
  border-radius:12px !important;
  font-size:15px !important;
  font-weight:700 !important;
  padding:14px 20px !important;
  width:100% !important;
  box-shadow:0 4px 18px rgba(59,130,246,.35) !important;
  letter-spacing:.01em !important;
  transition:opacity .2s ease, transform .15s ease, box-shadow .2s ease !important;
}
div[data-testid="stExpander"] .stButton>button:hover{
  opacity:.92 !important;
  transform:translateY(-2px) !important;
  box-shadow:0 8px 28px rgba(59,130,246,.45) !important;
}
/* Reset button — secondary style */
div[data-testid="stExpander"] .stButton:nth-of-type(2)>button{
  background:rgba(255,255,255,.75) !important;
  color:#3d5278 !important;
  border:1.5px solid rgba(59,130,246,.25) !important;
  box-shadow:0 2px 8px rgba(59,130,246,.08) !important;
  font-weight:500 !important;
  font-size:13.5px !important;
}
div[data-testid="stExpander"] .stButton:nth-of-type(2)>button:hover{
  background:rgba(59,130,246,.08) !important;
  border-color:rgba(59,130,246,.4) !important;
  transform:translateY(-1px) !important;
}

/* ── EXPANDER — fix dark overlay on header text ── */
div[data-testid="stExpander"]{
  background:rgba(255,255,255,.78) !important;
  backdrop-filter:blur(18px) !important;
  border:1.5px solid rgba(59,130,246,.18) !important;
  border-radius:16px !important;
  overflow:hidden;
  box-shadow:0 4px 20px rgba(59,130,246,.08) !important;
}
/* expander header — remove dark background, make text visible */
div[data-testid="stExpander"] details summary{
  background:rgba(255,255,255,.9) !important;
  padding:14px 18px !important;
  border-radius:14px !important;
}
div[data-testid="stExpander"] details[open] summary{
  border-radius:14px 14px 0 0 !important;
  border-bottom:1px solid rgba(59,130,246,.12) !important;
}
div[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] summary{
  color:#1e2d4a !important;
  font-weight:700 !important;
  font-size:14px !important;
  background:transparent !important;
}
/* expander body */
div[data-testid="stExpander"] details > div{
  background:rgba(255,255,255,.72) !important;
  padding:16px 18px !important;
}
div[data-testid="stRadio"] label{
  background:rgba(255,255,255,.65) !important;
  border:1px solid rgba(74,144,226,.2) !important;
  border-radius:8px !important;padding:6px 13px !important;
  font-size:13px !important;font-weight:500 !important;color:#2d4070 !important;
}
div[data-testid="stRadio"] label:hover{
  background:rgba(74,144,226,.12) !important;
}
/* form submit button */
button[kind="secondaryFormSubmit"],button[kind="formSubmit"]{
  background:linear-gradient(135deg,#3b82f6,#14b8a6) !important;
  color:white !important;border-radius:10px !important;
  border:none !important;font-weight:600 !important;
}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(74,144,226,.28);border-radius:99px;}
=======
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');
:root {
    --bg:#0a0d14; --surface:#111520; --surface2:#181e2e;
    --border:rgba(99,139,255,0.15); --accent:#638bff; --accent2:#3fffc2;
    --danger:#ff5c7a; --warn:#ffb347; --text:#e8eaf6; --muted:#7b83a0;
}
html,body,[class*="css"]{ font-family:'Inter',sans-serif; background-color:var(--bg)!important; color:var(--text)!important; }
#MainMenu,footer,header{ visibility:hidden; }
.block-container{ padding:2rem 2.5rem 4rem; max-width:1200px; }
section[data-testid="stSidebar"]{ background:var(--surface)!important; border-right:1px solid var(--border); }
section[data-testid="stSidebar"] *{ color:var(--text)!important; }
.logo-wrap{ display:flex; align-items:center; gap:10px; padding:0 0 1.5rem; border-bottom:1px solid var(--border); margin-bottom:1.5rem; }
.logo-icon{ width:40px; height:40px; border-radius:10px; background:linear-gradient(135deg,var(--accent),var(--accent2)); display:flex; align-items:center; justify-content:center; font-size:20px; }
.logo-text{ font-family:'Syne',sans-serif; font-size:20px; font-weight:800; letter-spacing:-0.5px; }
.logo-text span{ color:var(--accent2); }
.card{ background:rgba(17,21,32,0.65); backdrop-filter:blur(12px); border:1px solid rgba(255,255,255,0.03); border-radius:16px; padding:1.25rem 1.5rem; margin-bottom:1rem; transition:all .25s ease; }
.card:hover{ transform:translateY(-4px); border-color:rgba(99,139,255,0.4); }
.card-title{ font-family:'Syne',sans-serif; font-size:13px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin-bottom:.75rem; }
.metrics-row{ display:flex; gap:12px; flex-wrap:wrap; margin-bottom:1.25rem; }
.metric-pill{ flex:1; min-width:120px; background:var(--surface2); border:1px solid var(--border); border-radius:12px; padding:.75rem 1rem; text-align:center; }
.metric-pill .val{ font-family:'Syne',sans-serif; font-size:22px; font-weight:800; }
.metric-pill .lbl{ font-size:11px; color:var(--muted); margin-top:2px; text-transform:uppercase; letter-spacing:.06em; }
.status-high{ color:var(--danger); } .status-low{ color:var(--warn); } .status-norm{ color:var(--accent2); }
.badge{ display:inline-block; font-size:11px; font-weight:600; padding:3px 10px; border-radius:99px; text-transform:uppercase; letter-spacing:.05em; }
.badge-high{ background:rgba(255,92,122,0.15); color:var(--danger); border:1px solid rgba(255,92,122,0.3); }
.badge-low{ background:rgba(255,179,71,0.12); color:var(--warn); border:1px solid rgba(255,179,71,0.3); }
.badge-norm{ background:rgba(63,255,194,0.1); color:var(--accent2); border:1px solid rgba(63,255,194,0.25); }
.param-table{ width:100%; border-collapse:collapse; font-size:13.5px; }
.param-table th{ color:var(--muted); font-weight:500; font-size:11px; text-transform:uppercase; letter-spacing:.06em; padding:0 0 .5rem; text-align:left; border-bottom:1px solid var(--border); }
.param-table td{ padding:.6rem 0; border-bottom:1px solid rgba(99,139,255,0.07); vertical-align:middle; }
.param-table tr:last-child td{ border-bottom:none; }
.bubble-user{ background:linear-gradient(135deg,rgba(99,139,255,0.2),rgba(99,139,255,0.1)); border:1px solid rgba(99,139,255,0.3); border-radius:18px 18px 4px 18px; padding:.75rem 1rem; margin:.5rem 0; margin-left:15%; font-size:14px; line-height:1.6; }
.bubble-ai{ background:var(--surface2); border:1px solid var(--border); border-radius:18px 18px 18px 4px; padding:.75rem 1rem; margin:.5rem 0; margin-right:10%; font-size:14px; line-height:1.6; }
.bubble-label{ font-size:11px; font-weight:600; letter-spacing:.06em; text-transform:uppercase; margin-bottom:4px; }
.label-user{ color:var(--accent); text-align:right; } .label-ai{ color:var(--accent2); }
.page-header{ margin-bottom:2rem; padding-bottom:1.25rem; border-bottom:1px solid var(--border); }
.page-header h1{ font-family:'Syne',sans-serif; font-size:28px; font-weight:800; letter-spacing:-.5px; margin:0; line-height:1.2; }
.page-header p{ color:var(--muted); font-size:14px; margin-top:6px; }
.disclaimer{ background:rgba(255,179,71,0.07); border:1px solid rgba(255,179,71,0.25); border-radius:10px; padding:.6rem 1rem; font-size:12px; color:var(--warn); margin-top:.5rem; }
.stTextArea textarea,.stTextInput input{ background:var(--surface2)!important; border:1px solid var(--border)!important; border-radius:10px!important; color:var(--text)!important; font-family:'Inter',sans-serif!important; }
.stTextArea textarea:focus,.stTextInput input:focus{ border-color:var(--accent)!important; box-shadow:0 0 0 2px rgba(99,139,255,0.2)!important; }
.stButton>button{ background:linear-gradient(135deg,var(--accent),#4f7aff)!important; color:white!important; border:none!important; border-radius:10px!important; font-family:'Inter',sans-serif!important; font-weight:600!important; font-size:14px!important; padding:.55rem 1.5rem!important; transition:opacity .2s,transform .1s!important; width:100%; }
.stButton>button:hover{ opacity:.85!important; transform:translateY(-1px)!important; }
.stFileUploader{ background:var(--surface2)!important; border:1px dashed var(--border)!important; border-radius:12px!important; }
.stSelectbox>div>div{ background:var(--surface2)!important; border:1px solid var(--border)!important; border-radius:10px!important; color:var(--text)!important; }
div[data-baseweb="tab-list"]{ background:var(--surface)!important; border-radius:10px!important; border:1px solid var(--border)!important; padding:4px!important; gap:4px!important; }
div[data-baseweb="tab"]{ border-radius:8px!important; font-family:'Inter',sans-serif!important; font-weight:500!important; color:var(--muted)!important; }
div[aria-selected="true"][data-baseweb="tab"]{ background:var(--surface2)!important; color:var(--text)!important; }
.stSpinner>div{ border-top-color:var(--accent)!important; }
.stAlert{ border-radius:10px!important; }
/* topbar */
.topbar{ position:sticky; top:0; z-index:999; background:rgba(10,13,20,0.92); backdrop-filter:blur(12px); border:1px solid rgba(99,139,255,0.15); border-radius:14px; padding:.7rem 1.2rem; margin-bottom:1.5rem; }
.topbar-inner{ display:flex; justify-content:space-between; align-items:center; }
.brand{ font-family:'Syne',sans-serif; font-size:18px; font-weight:800; }
.brand span{ color:#3fffc2; }
.user-chip{ display:inline-flex; align-items:center; gap:8px; background:rgba(99,139,255,0.1); border:1px solid rgba(99,139,255,0.2); border-radius:99px; padding:4px 14px 4px 6px; font-size:13px; cursor:pointer; transition:background .2s; }
.user-chip:hover{ background:rgba(99,139,255,0.2); }
.user-avatar{ width:26px; height:26px; border-radius:50%; background:linear-gradient(135deg,#638bff,#3fffc2); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#0a0d14; }
.guest-chip{ display:inline-flex; align-items:center; gap:8px; background:rgba(255,179,71,0.1); border:1px solid rgba(255,179,71,0.25); border-radius:99px; padding:4px 14px 4px 10px; font-size:13px; color:var(--warn); }
/* dashboard report cards */
.report-card{ background:var(--surface2); border:1px solid var(--border); border-radius:14px; padding:1.1rem 1.3rem; margin-bottom:.75rem; transition:border-color .2s; }
.report-card:hover{ border-color:rgba(99,139,255,0.4); }
.report-card-title{ font-weight:600; font-size:14px; margin-bottom:.3rem; }
.report-card-meta{ font-size:12px; color:var(--muted); }
/* nav pill */
.nav-pill{ display:inline-block; padding:5px 14px; border-radius:8px; font-size:13px; font-weight:500; cursor:pointer; }
.nav-active{ background:rgba(99,139,255,0.15); color:var(--accent); border:1px solid rgba(99,139,255,0.3); }
.nav-inactive{ color:var(--muted); border:1px solid transparent; }
>>>>>>> dba419a332508878fc47ed5bddc846ff792eabe6
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
<<<<<<< HEAD
# AUTH PAGES  (shown when not logged in)
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.user:
    # Full-page auth background
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg,#c8daf5 0%,#d6eaf8 40%,#c8f0e8 100%) !important; }
    /* auth page — sidebar hidden only while on auth screen */
    section[data-testid="stSidebar"]{ display:none !important; }
    /* narrow centred layout for auth form only */
    .block-container{ max-width:480px !important; margin:0 auto !important; padding:3rem 1rem !important; }
    /* override tab colours for auth page */
    div[data-baseweb="tab-list"]{ background:rgba(255,255,255,.5) !important; }
    div[data-baseweb="tab"]{ color:#3d5278 !important; font-weight:600 !important; }
    div[aria-selected="true"][data-baseweb="tab"]{ background:white !important; color:#1e2d4a !important; }
    /* input labels dark */
    .stTextInput label{ color:#1e2d4a !important; font-weight:600 !important; font-size:13px !important; }
    .stTextInput input{ color:#1e2d4a !important; background:rgba(255,255,255,.92) !important;
      border:1.5px solid rgba(74,144,226,.3) !important; border-radius:10px !important;
      font-size:14px !important; padding:10px 14px !important; }
    .stTextInput input::placeholder{ color:#94a3b8 !important; }
    .stTextInput input:focus{ border-color:#3b82f6 !important;
      box-shadow:0 0 0 3px rgba(59,130,246,.18) !important; }
=======
# AUTH PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_auth():
    st.markdown("""
    <style>
    section[data-testid="stSidebar"]{ display:none!important; }
    .block-container{ max-width:460px!important; padding-top:3rem!important; }
    .stTextInput label{ font-size:13px!important; font-weight:500!important; color:var(--muted)!important; }
    .auth-divider{ display:flex; align-items:center; gap:.75rem; color:var(--muted); font-size:12px; margin:1rem 0; }
    .auth-divider::before,.auth-divider::after{ content:''; flex:1; height:1px; background:var(--border); }
>>>>>>> dba419a332508878fc47ed5bddc846ff792eabe6
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
<<<<<<< HEAD
    <div style="text-align:center;margin-bottom:28px;margin-top:20px;">
      <div style="font-size:48px;margin-bottom:10px;">🩺</div>
      <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:26px;
                  font-weight:800;color:#1e2d4a;letter-spacing:-.6px;">MediScan AI</div>
      <div style="font-size:13.5px;color:#4a6080;margin-top:6px;font-weight:500;">
        AI-powered lab report analysis
      </div>
    </div>""", unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["🔐  Login", "📝  Sign Up"])

    with tab_login:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        email_l = st.text_input("Email address", key="l_email",
                                placeholder="you@example.com")
        pass_l  = st.text_input("Password", type="password", key="l_pass",
                                placeholder="Your password")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Login →", key="btn_login", use_container_width=True):
            if not email_l or not pass_l:
                st.error("Please fill in all fields.")
            else:
                ok, user = login_user(email_l, pass_l)
                if ok:
                    st.session_state.user = user
                    st.session_state.page = "landing"
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
        st.markdown("""
        <div style="text-align:center;font-size:12px;color:#64748b;margin-top:14px;
                    background:rgba(255,255,255,.5);border-radius:8px;padding:8px 12px;">
          🔑 Demo: <b>admin@mediscan.ai</b> / <b>admin123</b>
        </div>""", unsafe_allow_html=True)

    with tab_signup:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        name_s  = st.text_input("Full name", key="s_name", placeholder="Your name")
        email_s = st.text_input("Email address", key="s_email",
                                placeholder="you@example.com")
        pass_s  = st.text_input("Password", type="password", key="s_pass",
                                placeholder="Min 6 characters")
        pass_s2 = st.text_input("Confirm password", type="password", key="s_pass2",
                                placeholder="Repeat password")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Create Account →", key="btn_signup", use_container_width=True):
            if not all([name_s, email_s, pass_s, pass_s2]):
                st.error("Please fill in all fields.")
            elif len(pass_s) < 6:
                st.error("Password must be at least 6 characters.")
            elif pass_s != pass_s2:
                st.error("Passwords do not match.")
            else:
                ok, msg = create_user(name_s, email_s, pass_s)
                if ok:
                    st.success(msg + " Please log in.")
                else:
                    st.error(msg)

    # seed demo account silently
    try:
        create_user("Admin", "admin@mediscan.ai", "admin123")
    except Exception:
        pass
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR  (only shown when logged in)
# ─────────────────────────────────────────────────────────────────────────────
user  = st.session_state.user
page  = st.session_state.page

NAV = [
    ("landing",   "🏠", "Home"),
    ("dashboard", "📊", "Dashboard"),
    ("reports",   "📋", "Reports"),
    ("history",   "🕐", "History"),
    ("analytics", "📈", "Analytics"),
    ("settings",  "⚙️", "Settings"),
]


# ── Native Streamlit sidebar — ONLY navigation source ─────────────────────────
with st.sidebar:
    st.markdown("### 🩺 MediScan AI")
    st.markdown("---")
    for pg, icon, label in NAV:
        btn_style = "primary" if page == pg else "secondary"
        if st.button(f"{icon}  {label}", key=f"sb_{pg}", use_container_width=True,
                     type=btn_style if pg == page else "secondary"):
            st.session_state.page = pg
            st.rerun()
    st.markdown("---")
    st.markdown(f"**{user['name']}**  \n{user['email']}")
    if st.button("🚪 Logout", key="sb_logout", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: LANDING
# ─────────────────────────────────────────────────────────────────────────────
if page == "landing":
    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
      <div class="hero-badge">✨ AI-Powered Healthcare Analysis</div>
      <div class="hero-title">
        Understand Your Lab Report<br>
        <span>Instantly &amp; Accurately</span>
      </div>
      <p class="hero-sub">
        Upload your lab report and get a structured, AI-powered breakdown of every
        parameter — with smart health insights, precautions, and personalised
        diet recommendations.
      </p>
    </div>""", unsafe_allow_html=True)

    _, cc, _ = st.columns([1.5, 2, 1.5])
    with cc:
        if st.button("🚀  Get Started", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    # ── Features ──────────────────────────────────────────────────────────────
    st.markdown("<div style='height:52px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;margin-bottom:28px;max-width:600px;margin-left:auto;margin-right:auto;">
      <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;
                  font-weight:800;color:#1e2d4a;letter-spacing:-.4px;margin-bottom:8px;">
        Everything you need to understand your health
      </div>
      <div style="font-size:13.5px;color:#5a6a8a;line-height:1.6;">
        Five powerful features, one seamless experience
      </div>
    </div>
    <div class="feature-grid">
      <div class="feature-card">
        <div class="fc-icon">🔬</div>
        <div class="fc-title">AI Report Analysis</div>
        <div class="fc-desc">Instantly extract and interpret every parameter from your lab report using advanced AI.</div>
      </div>
      <div class="feature-card">
        <div class="fc-icon">📊</div>
        <div class="fc-title">Parameter Detection</div>
        <div class="fc-desc">Automatically detects 20+ blood parameters and compares them against clinical reference ranges.</div>
      </div>
      <div class="feature-card">
        <div class="fc-icon">💡</div>
        <div class="fc-title">Smart Health Insights</div>
        <div class="fc-desc">Visual metric cards with status badges, progress bars, and colour-coded severity indicators.</div>
      </div>
      <div class="feature-card">
        <div class="fc-icon">🥗</div>
        <div class="fc-title">Recommendations</div>
        <div class="fc-desc">Personalised diet and lifestyle recommendations tailored to your specific report findings.</div>
      </div>
      <div class="feature-card">
        <div class="fc-icon">🤖</div>
        <div class="fc-title">Chatbot Assistance</div>
        <div class="fc-desc">Ask follow-up questions about your report and get context-aware AI responses instantly.</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Guardrails ────────────────────────────────────────────────────────────
    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="max-width:700px;margin:0 auto;">
      <div class="guardrail-card">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;
                    font-weight:700;color:#1e2d4a;margin-bottom:12px;">
          🛡 Guardrails — What MediScan AI will &amp; won't do
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;">
          <div class="gr-row"><span class="gr-no">✗</span> Provide a medical diagnosis</div>
          <div class="gr-row"><span class="gr-yes">✓</span> Only uses your report data</div>
          <div class="gr-row"><span class="gr-no">✗</span> Prescribe medicines</div>
          <div class="gr-row"><span class="gr-yes">✓</span> Rejects non-medical inputs</div>
          <div class="gr-row"><span class="gr-no">✗</span> Hallucinate or invent data</div>
          <div class="gr-row"><span class="gr-yes">✓</span> Structured, evidence-based output</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: HISTORY
# ─────────────────────────────────────────────────────────────────────────────
if page == "history":
    st.markdown("""
    <div class="page-header">
      <div class="page-title">🕐 Report History</div>
      <div class="page-sub">All lab reports you have analysed, most recent first.</div>
    </div>""", unsafe_allow_html=True)
    reports = get_user_reports(user["id"])
    if not reports:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:#8a9bbf;">
          <div style="font-size:40px;margin-bottom:10px;">📭</div>
          <div style="font-size:15px;font-weight:600;color:#1e2d4a;">No reports yet</div>
          <div style="font-size:13px;margin-top:6px;">
            Go to Dashboard and analyse your first report.
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        for r in reports:
            abn = r["abnormal"]
            bc  = "b-high" if abn > 0 else "b-normal"
            bt  = f"{abn} Abnormal" if abn > 0 else "All Normal"
            conds = ", ".join(r["conditions"][:3]) or "—"
            st.markdown(f"""
            <div class="hist-row">
              <div class="hist-id">#{r['id']}</div>
              <div class="hist-time">🕐 {r['timestamp']}</div>
              <div style="flex:1;font-size:12.5px;color:#5a6a8a;">{conds}</div>
              <div style="font-size:12px;color:#8a9bbf;margin-right:8px;">{r['params']} params</div>
              <span class="mc-badge {bc}">{bt}</span>
            </div>""", unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────
if page == "analytics":
    st.markdown("""
    <div class="page-header">
      <div class="page-title">📈 Analytics</div>
      <div class="page-sub">Statistics based on your analysed reports.</div>
    </div>""", unsafe_allow_html=True)
    reports  = get_user_reports(user["id"])
    total    = len(reports)
    total_p  = sum(r["params"]   for r in reports)
    total_a  = sum(r["abnormal"] for r in reports)
    total_n  = total_p - total_a
    rate     = round(total_a / total_p * 100, 1) if total_p else 0

    c1,c2,c3,c4 = st.columns(4)
    for col, num, lbl in [
        (c1, total,   "Reports Analysed"),
        (c2, total_p, "Total Parameters"),
        (c3, total_a, "Abnormal Findings"),
        (c4, f"{rate}%", "Abnormal Rate"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-card">
              <div class="stat-num">{num}</div>
              <div class="stat-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    if reports:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Recent Reports</div>', unsafe_allow_html=True)
        for r in reports[:10]:
            abn = r["abnormal"]
            bc  = "b-high" if abn > 0 else "b-normal"
            st.markdown(f"""
            <div class="hist-row">
              <div class="hist-id">#{r['id']}</div>
              <div class="hist-time">{r['timestamp']}</div>
              <div style="flex:1;font-size:12.5px;color:#5a6a8a;">{r['params']} params detected</div>
              <span class="mc-badge {bc}">{abn} abnormal</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("No data yet. Analyse a report to see analytics.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: REPORTS
# ─────────────────────────────────────────────────────────────────────────────
if page == "reports":
    st.markdown("""
    <div class="page-header">
      <div class="page-title">📋 Saved Reports</div>
      <div class="page-sub">View the full parameter breakdown of any past report.</div>
    </div>""", unsafe_allow_html=True)
    reports = get_user_reports(user["id"])
    if not reports:
        st.info("No saved reports yet. Analyse a report from the Dashboard.")
        st.stop()
    ids    = [f"#{r['id']}  —  {r['timestamp']}" for r in reports]
    choice = st.selectbox("Select a report", ids, label_visibility="collapsed")
    idx    = ids.index(choice)
    entry  = reports[idx]
    fd     = entry["data"]

    st.markdown(f"""
    <div class="glass-card" style="padding:18px 22px;margin-bottom:14px;">
      <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:15px;
                  font-weight:700;color:#1e2d4a;margin-bottom:4px;">
        Report #{entry['id']}
      </div>
      <div style="font-size:12px;color:#8a9bbf;">
        {entry['timestamp']} &nbsp;·&nbsp; {entry['params']} parameters
        &nbsp;·&nbsp; {entry['abnormal']} abnormal
      </div>
    </div>""", unsafe_allow_html=True)

    if fd:
        rows_html = ""
        for param, details in fd.items():
            val    = details.get("value","—")
            unit   = details.get("unit","")
            ref    = details.get("reference_range","—")
            status = details.get("status","normal")
            sc,bc,_,label = _sc(status)
            name   = param.replace("_"," ").title()
            icon   = ICONS.get(param, DEFAULT_ICON)
            rows_html += f"""<tr>
              <td style="font-weight:500;padding-right:1rem;">{icon} {name}</td>
              <td class="{sc}" style="font-weight:700;">{val}
                <span style="font-size:11px;color:#a0aec0;margin-left:2px;">{unit}</span></td>
              <td style="color:#8a9bbf;font-size:12px;">{ref}</td>
              <td><span class="mc-badge {bc}">{label}</span></td>
            </tr>"""
        st.markdown(f"""
        <div class="glass-card" style="padding:18px 22px;">
          <table class="ptable">
            <thead><tr>
              <th>Parameter</th><th>Value</th><th>Reference</th><th>Status</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>""", unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: SETTINGS
# ─────────────────────────────────────────────────────────────────────────────
if page == "settings":
    st.markdown("""
    <div class="page-header">
      <div class="page-title">⚙️ Settings</div>
      <div class="page-sub">Manage your account and preferences.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="glass-card" style="padding:22px 26px;max-width:560px;margin-bottom:16px;">
      <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;
                  font-weight:700;color:#1e2d4a;margin-bottom:14px;">Account Information</div>
      <div style="font-size:13.5px;color:#5a6a8a;line-height:2.2;">
        <b style="color:#1e2d4a;">Name:</b> {user['name']}<br>
        <b style="color:#1e2d4a;">Email:</b> {user['email']}<br>
        <b style="color:#1e2d4a;">Member since:</b> {user.get('created','—')}<br>
        <b style="color:#1e2d4a;">AI Model:</b> openai/gpt-oss-120b<br>
        <b style="color:#1e2d4a;">Max chat history:</b> 8 messages
      </div>
    </div>""", unsafe_allow_html=True)

    col_lo, _ = st.columns([1,3])
    with col_lo:
        if st.button("🚪  Logout", key="settings_logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div class="page-title">📊 Dashboard</div>
  <div class="page-sub">Upload a lab report to get an instant AI-powered analysis.</div>
</div>""", unsafe_allow_html=True)

# ── upload type cards — single HTML grid, full-width, no columns ─────────────
st.markdown("""
<div class="upload-grid">
  <div class="upload-card">
    <span class="uc-icon">📝</span>
    <span class="uc-title">Paste Text</span>
    <span class="uc-sub">Type or paste report values</span>
  </div>
  <div class="upload-card">
    <span class="uc-icon">🖼️</span>
    <span class="uc-title">Image Upload</span>
    <span class="uc-sub">JPG / PNG lab report scan</span>
  </div>
  <div class="upload-card">
    <span class="uc-icon">📄</span>
    <span class="uc-title">PDF Upload</span>
    <span class="uc-sub">Digital lab report PDF</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── upload expander ───────────────────────────────────────────────────────────
with st.expander("📂  Open Upload Panel", expanded=not st.session_state.analyzed):
    method = st.radio("Input method",
                      ["📝 Paste Text", "🖼️ Image", "📄 PDF"],
                      horizontal=True, label_visibility="collapsed")
    report_text_input = img_file = pdf_file = None

    if method == "📝 Paste Text":
        report_text_input = st.text_area(
            "Paste your lab report here", height=160,
            placeholder="e.g.  Hemoglobin: 10.5 g/dL\nBlood Sugar (Fasting): 130 mg/dL\n...",
        )
    elif method == "🖼️ Image":
        img_file = st.file_uploader("Upload image", type=["png","jpg","jpeg"])
    else:
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

    # full-width Analyse button + optional Reset below
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    analyze_btn = st.button("🔬  Analyse Report", use_container_width=True)
    if st.session_state.analyzed:
        if st.button("🔄  Reset & Upload New Report", use_container_width=True, key="reset_btn"):
            for k in ["report_text","final_data","conditions","summary",
                      "chat_history","memory_summary","system_prompt","analyzed",
                      "prec_chat","diet_chat","prec_bullets","diet_bullets",
                      "show_prec_chat","show_diet_chat"]:
                st.session_state[k] = _DEFAULTS.get(k, [] if "chat" in k or "bullets" in k else ("" if k not in ("analyzed",) else False))
            st.rerun()
    st.markdown('<div style="font-size:12px;color:#e67e22;margin-top:6px;">'
                '⚠️ Not a substitute for professional medical advice.</div>',
                unsafe_allow_html=True)

# ── analyse logic ─────────────────────────────────────────────────────────────
if analyze_btn:
    raw = ""
    try:
        if method == "📝 Paste Text":
            raw = report_text_input or ""
        elif method == "🖼️ Image" and img_file:
            with open("frontend/_tmp_img","wb") as f: f.write(img_file.read())
            raw = extract_text_from_image("frontend/_tmp_img")
        elif method == "📄 PDF" and pdf_file:
            with open("frontend/_tmp.pdf","wb") as f: f.write(pdf_file.read())
            raw = extract_text_from_pdf("frontend/_tmp.pdf")

        # ── STRICT GUARDRAIL — validate before any AI call ────────────────────
        valid, msg = validate_medical_input(raw)
        if not valid:
            st.error(msg)
            st.stop()

        with st.spinner("Analysing your report…"):
            ai_raw = ai_extract_parameters(raw, client)
            ai_raw = ai_raw.strip().replace("```json","").replace("```","")
            try:
                parsed = json.loads(ai_raw)
            except Exception:
                parsed = {}

            if not parsed:
                st.error("Could not extract any medical parameters. Please upload a clearer lab report.")
                st.stop()

            final_data = analyze_report(parsed)
            conditions = [
                f"{p} is {d['status']}"
                for p,d in final_data.items()
                if d.get("status","").lower() in ("high","low")
            ] or ["All parameters are normal"]

            summary = get_summary(explain_report_prompt(str(final_data)))
            prec, diet = parse_sections(summary)

            sys_prompt = (
                f"You are a smart AI medical assistant.\n"
                f"Patient Report: {final_data}\n"
                f"Detected Conditions: {conditions}\n"
                f"Give personalized, specific answers. No generic advice.\n"
                f"Always end with: This is not a medical diagnosis."
            )

            rid = save_report(user["id"], final_data, conditions, summary)

            st.session_state.update({
                "report_text":   raw,
                "final_data":    final_data,
                "conditions":    conditions,
                "summary":       summary,
                "prec_bullets":  prec,
                "diet_bullets":  diet,
                "system_prompt": sys_prompt,
                "chat_history":  [],
                "prec_chat":     [],
                "diet_chat":     [],
                "memory_summary":"",
                "analyzed":      True,
            })
            st.success(f"✅ Report analysed and saved as #{rid}")
            st.rerun()
    except Exception as e:
        st.error(f"❌ {e}")

# ── empty state ───────────────────────────────────────────────────────────────
if not st.session_state.analyzed:
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem;">
      <div style="font-size:52px;margin-bottom:12px;">🩺</div>
      <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;
                  font-weight:800;color:#1e2d4a;letter-spacing:-.5px;margin-bottom:8px;">
        No report analysed yet
      </div>
      <p style="color:#6b82a8;font-size:13.5px;line-height:1.8;max-width:420px;margin:0 auto;">
        Use the upload panel above to paste text, upload an image,
        or drop a PDF lab report to get started.
      </p>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD RESULTS
# ─────────────────────────────────────────────────────────────────────────────
final_data = st.session_state.final_data
tab_dash, tab_chat, tab_raw = st.tabs(["📊  Results", "💬  AI Chat", "📄  Raw Report"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_dash:
    # header
    hL, hR = st.columns([3,1])
    with hL:
        st.markdown("""
        <div style="margin-bottom:4px;">
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:20px;
                      font-weight:800;color:#1e2d4a;letter-spacing:-.4px;">
            Health Dashboard
          </div>
          <div style="font-size:13px;color:#6b82a8;margin-top:3px;">
            Your lab results have been analysed. Review the breakdown below.
          </div>
        </div>""", unsafe_allow_html=True)
    with hR:
        today = datetime.date.today().strftime("%d %B %Y")
        st.markdown(f"""
        <div style="text-align:right;font-size:12px;color:#8a9bbf;line-height:1.9;padding-top:4px;">
          Date: <b style="color:#1e2d4a;">{today}</b>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # counts
    high_c = sum(1 for d in final_data.values() if d.get("status","").lower()=="high")
    low_c  = sum(1 for d in final_data.values() if d.get("status","").lower()=="low")
    norm_c = len(final_data) - high_c - low_c

    st.markdown(f"""
    <div class="counts-bar">
      <div class="count-chip"><div class="num s-high">{high_c}</div><div class="lbl">High</div></div>
      <div class="count-chip"><div class="num s-low">{low_c}</div><div class="lbl">Low</div></div>
      <div class="count-chip"><div class="num s-normal">{norm_c}</div><div class="lbl">Normal</div></div>
      <div class="count-chip"><div class="num" style="color:#4a90e2;">{len(final_data)}</div><div class="lbl">Total</div></div>
    </div>""", unsafe_allow_html=True)

    # key metric cards
    st.markdown('<div class="section-title">📊 Key Health Parameters</div>', unsafe_allow_html=True)
    display_keys = [k for k in KEY_METRICS if k in final_data] or list(final_data.keys())

    for row_keys in [display_keys[i:i+4] for i in range(0, len(display_keys), 4)]:
        cols = st.columns(len(row_keys))
        for col, key in zip(cols, row_keys):
            d      = final_data[key]
            val    = d.get("value","—")
            unit   = d.get("unit","")
            ref    = d.get("reference_range","—")
            status = d.get("status","normal").lower()
            sc,bc,ic,label = _sc(status)
            icon   = ICONS.get(key, DEFAULT_ICON)
            spark  = SPARK.get(status,"〰️")
            name   = key.replace("_"," ").title()
            with col:
                st.markdown(f"""
                <div class="metric-card card-tint-{status}">
                  <div class="mc-header">
                    <div class="mc-icon {ic}">{icon}</div>{name}
                  </div>
                  <div class="mc-value {sc}">{val}<span class="mc-unit">{unit}</span></div>
                  <span class="mc-badge {bc}">{label}</span>
                  <div class="mc-ref">Ref: {ref}</div>
                  <div class="mc-sparkline">{spark}</div>
                </div>""", unsafe_allow_html=True)

    # abnormal bar charts
    abnormal = {k:v for k,v in final_data.items() if v.get("status","").lower() in ("high","low")}
    if abnormal:
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚠️ Abnormal Parameters</div>', unsafe_allow_html=True)
        bar_cols = st.columns(min(len(abnormal),4))
        for col,(key,d) in zip(bar_cols, list(abnormal.items())[:4]):
            val    = float(d.get("value",0))
            status = d.get("status","normal").lower()
            meta   = PARAMETERS.get(key,{})
            mn     = float(meta.get("min",0))
            mx     = float(meta.get("max", val*1.5 or 1))
            unit   = d.get("unit","")
            name   = key.replace("_"," ").title()
            pct    = min(max((val/(mx*1.3))*100, 5), 100)
            clr    = "#dc3545" if status=="high" else "#e67e22"
            with col:
                st.markdown(f"""
                <div class="bar-card">
                  <div style="font-size:12px;font-weight:600;color:#6b82a8;margin-bottom:8px;">
                    {ICONS.get(key,DEFAULT_ICON)} {name}
                  </div>
                  <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;
                              font-weight:800;color:{clr};">{val}
                    <span style="font-size:12px;color:#a0aec0;font-weight:500;margin-left:2px;">{unit}</span>
                  </div>
                  <div class="bar-track">
                    <div class="bar-fill" style="width:{pct}%;background:{clr};
                         box-shadow:0 0 8px {clr}55;"></div>
                  </div>
                  <div style="display:flex;justify-content:space-between;
                              font-size:10.5px;color:#a0aec0;margin-top:2px;">
                    <span>Min {mn}</span><span>Max {mx}</span>
                  </div>
                </div>""", unsafe_allow_html=True)

    # precautions + diet
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    prec_bullets = st.session_state.get("prec_bullets",[])
    diet_bullets = st.session_state.get("diet_bullets",[])
    pL, pR = st.columns(2)

    with pL:
        items = "".join(
            f'<div class="panel-item"><span class="panel-warn">⚠</span>{b}</div>'
            for b in prec_bullets
        ) if prec_bullets else '<div style="color:#a0aec0;font-size:13px;">No precautions generated.</div>'
        st.markdown(f"""
        <div class="panel-box">
          <div class="panel-header">
            <div class="panel-icon" style="background:rgba(220,53,69,.1);">⚠️</div>
            <span class="panel-title">Precautions</span>
          </div>{items}
        </div>""", unsafe_allow_html=True)
        if st.button("💬  Ask more about Precautions", key="prec_toggle", use_container_width=True):
            st.session_state.show_prec_chat = not st.session_state.show_prec_chat
        if st.session_state.show_prec_chat:
            st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
            render_inline_chat("prec_chat","prec_q","Ask about precautions…",
                               "Focus only on precautions and safety advice.")
            st.markdown("</div>", unsafe_allow_html=True)

    with pR:
        items = "".join(
            f'<div class="panel-item"><span class="panel-check">✓</span>{b}</div>'
            for b in diet_bullets
        ) if diet_bullets else '<div style="color:#a0aec0;font-size:13px;">No diet recommendations generated.</div>'
        st.markdown(f"""
        <div class="panel-box">
          <div class="panel-header">
            <div class="panel-icon" style="background:rgba(39,174,96,.1);">🥗</div>
            <span class="panel-title">Diet Recommendations</span>
          </div>{items}
        </div>""", unsafe_allow_html=True)
        if st.button("💬  Ask more about Diet", key="diet_toggle", use_container_width=True):
            st.session_state.show_diet_chat = not st.session_state.show_diet_chat
        if st.session_state.show_diet_chat:
            st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
            render_inline_chat("diet_chat","diet_q","Ask about diet & nutrition…",
                               "Focus only on diet and nutrition recommendations.")
            st.markdown("</div>", unsafe_allow_html=True)

    # ── unified AI search bar ─────────────────────────────────────────────────
    st.markdown('<div class="ai-search-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="ai-search-label">🔍 Ask anything about your report</div>',
                unsafe_allow_html=True)
    with st.form(key="search_form", clear_on_submit=True):
        sc1, sc2 = st.columns([6, 1])
        with sc1:
            search_q = st.text_input(
                "", placeholder="e.g. What does high cholesterol mean for me?",
                label_visibility="collapsed", key="search_input"
            )
        with sc2:
            search_sent = st.form_submit_button("Ask →", use_container_width=True)
        if search_sent and search_q.strip():
            with st.spinner("Thinking…"):
                ans = chat_with_ai(search_q.strip(), "chat_history")
            st.markdown(f'<div class="ai-search-response">{ans}</div>',
                        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # guardrails
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="guardrail-card">
      <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:13.5px;
                  font-weight:700;color:#1e2d4a;margin-bottom:10px;">🛡 Guardrails</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:3px;">
        <div class="gr-row"><span class="gr-no">✗</span> No medical diagnosis</div>
        <div class="gr-row"><span class="gr-yes">✓</span> Only uses your report data</div>
        <div class="gr-row"><span class="gr-no">✗</span> No medicine prescriptions</div>
        <div class="gr-row"><span class="gr-yes">✓</span> Rejects non-medical inputs</div>
        <div class="gr-row"><span class="gr-no">✗</span> No hallucinated data</div>
        <div class="gr-row"><span class="gr-yes">✓</span> Structured, evidence-based output</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # full param table
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔬 Full Parameter Breakdown</div>', unsafe_allow_html=True)
    rows_html = ""
    for param, details in final_data.items():
        val    = details.get("value","—")
        unit   = details.get("unit","")
        ref    = details.get("reference_range","—")
        status = details.get("status","normal")
        sc,bc,_,label = _sc(status)
        name   = param.replace("_"," ").title()
        icon   = ICONS.get(param, DEFAULT_ICON)
        rows_html += f"""<tr>
          <td style="font-weight:500;padding-right:1rem;">{icon} {name}</td>
          <td class="{sc}" style="font-weight:700;">{val}
            <span style="font-size:11px;color:#a0aec0;margin-left:2px;">{unit}</span></td>
          <td style="color:#8a9bbf;font-size:12px;">{ref}</td>
          <td><span class="mc-badge {bc}">{label}</span></td>
        </tr>"""
    st.markdown(f"""
    <div class="glass-card" style="padding:18px 22px;">
      <table class="ptable">
        <thead><tr>
          <th>Parameter</th><th>Value</th><th>Reference Range</th><th>Status</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — AI CHAT
# ═══════════════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("""
    <div style="margin-bottom:12px;">
      <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:16px;
                  font-weight:700;color:#1e2d4a;">💬 Chat with MediScan AI</div>
      <div style="font-size:13px;color:#6b82a8;margin-top:3px;">
        Ask anything about your report — diet, lifestyle, what a parameter means.
      </div>
    </div>""", unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align:center;padding:2.5rem 1rem;color:#a0aec0;">
          <div style="font-size:36px;margin-bottom:.5rem;">💬</div>
          <div style="font-size:14px;">Ask me anything about your report</div>
        </div>""", unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f'<div style="font-size:10px;font-weight:700;color:#3b82f6;'
                    f'text-align:right;text-transform:uppercase;letter-spacing:.06em;'
                    f'margin-bottom:2px;">You</div>'
                    f'<div class="big-bubble-user">{msg["content"]}</div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div style="font-size:10px;font-weight:700;color:#14b8a6;'
                    f'text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;">'
                    f'MediScan AI</div>'
                    f'<div class="big-bubble-ai">{msg["content"]}</div>',
                    unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:10.5px;color:#a0aec0;text-transform:uppercase;'
                'letter-spacing:.06em;margin-bottom:6px;">Suggested questions</div>',
                unsafe_allow_html=True)
    sq1,sq2,sq3 = st.columns(3)
    for col,q,i in zip([sq1,sq2,sq3],[
        "What foods should I eat?",
        "What lifestyle changes help?",
        "Explain my key abnormalities",
    ], range(3)):
        with col:
            if st.button(q, key=f"sug_{i}", use_container_width=True):
                with st.spinner("Thinking…"):
                    chat_with_ai(q, "chat_history")
                st.rerun()

    user_input = st.chat_input("Ask about your report…")
    if user_input:
        with st.spinner("Thinking…"):
            chat_with_ai(user_input, "chat_history")
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RAW REPORT
# ═══════════════════════════════════════════════════════════════════════════════
with tab_raw:
    st.markdown(f"""
    <div class="glass-card" style="padding:20px 24px;">
      <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;
                  font-weight:700;color:#1e2d4a;margin-bottom:10px;">📄 Extracted Report Text</div>
      <div style="font-size:13px;color:#6b82a8;white-space:pre-wrap;line-height:1.85;">
        {st.session_state.report_text}
      </div>
    </div>""", unsafe_allow_html=True)

# floating chat button — clicking it scrolls to / activates the AI Chat tab
st.markdown("""
<div class="float-chat" onclick="
  var tabs = window.parent.document.querySelectorAll('[data-baseweb=tab]');
  if(tabs.length >= 2){ tabs[1].click(); }
  window.parent.scrollTo({top:0, behavior:'smooth'});
">
  🤖 &nbsp;Chat with AI
</div>
""", unsafe_allow_html=True)
=======
    <div style="display:flex;align-items:center;gap:10px;justify-content:center;margin-bottom:2rem;">
      <div style="width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,#638bff,#3fffc2);display:flex;align-items:center;justify-content:center;font-size:22px;">🩺</div>
      <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;">Medi<span style='color:#3fffc2;'>Scan</span> AI</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.auth_page == "login":
        _render_login()
    else:
        _render_signup()


def _render_login():
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:22px;font-weight:800;text-align:center;margin-bottom:.3rem;">Welcome back</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;color:var(--muted);font-size:14px;margin-bottom:1.5rem;">Sign in to your MediScan account</div>', unsafe_allow_html=True)

    identifier = st.text_input("Username or Email", placeholder="you@example.com", key="li_id")
    password   = st.text_input("Password", type="password", placeholder="••••••••", key="li_pw")
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    if st.button("Sign in", use_container_width=True, key="li_btn"):
        if not identifier or not password:
            st.error("Please fill in all fields.")
        else:
            ok, msg, user = login_user(identifier, password)
            if ok:
                st.session_state.logged_in = True
                st.session_state.is_guest  = False
                st.session_state.user      = user
                st.rerun()
            else:
                st.error(msg)

    st.markdown('<div class="auth-divider">or</div>', unsafe_allow_html=True)

    if st.button("Continue as Guest", use_container_width=True, key="guest_btn"):
        st.session_state.logged_in = True
        st.session_state.is_guest  = True
        st.session_state.user      = {"username": "Guest", "id": None}
        st.rerun()

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:13px;color:var(--muted);">Don\'t have an account?</div>', unsafe_allow_html=True)
    if st.button("Create an account", use_container_width=True, key="go_signup"):
        st.session_state.auth_page = "signup"
        st.rerun()


def _render_signup():
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:22px;font-weight:800;text-align:center;margin-bottom:.3rem;">Create your account</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;color:var(--muted);font-size:14px;margin-bottom:1.5rem;">Start analysing your lab reports with AI</div>', unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="johndoe", key="su_user")
    email    = st.text_input("Email", placeholder="you@example.com", key="su_email")
    password = st.text_input("Password", type="password", placeholder="Min. 6 characters", key="su_pw")
    confirm  = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="su_cpw")
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    if st.button("Create account", use_container_width=True, key="su_btn"):
        if not all([username, email, password, confirm]):
            st.error("Please fill in all fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            ok, msg = register_user(username, email, password)
            if ok:
                st.success(msg + " Please sign in.")
                st.session_state.auth_page = "login"
                st.rerun()
            else:
                st.error(msg)

    st.markdown('<div class="auth-divider">or</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:13px;color:var(--muted);">Already have an account?</div>', unsafe_allow_html=True)
    if st.button("Sign in instead", use_container_width=True, key="go_login"):
        st.session_state.auth_page = "login"
        st.rerun()


# ── Auth gate ─────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    render_auth()
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def status_badge(status):
    s = status.lower()
    if s == "high":         return '<span class="badge badge-high">High ↑</span>'
    if s == "low":          return '<span class="badge badge-low">Low ↓</span>'
    if s == "unrecognized": return '<span class="badge" style="background:rgba(123,131,160,0.15);color:#7b83a0;border:1px solid rgba(123,131,160,0.3);">Unknown</span>'
    return '<span class="badge badge-norm">Normal ✓</span>'

def status_class(status):
    s = status.lower()
    if s == "high": return "status-high"
    if s == "low":  return "status-low"
    return "status-norm"

def get_summary(prompt):
    try:
        r = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are an AI medical assistant.\nFormat strictly:\n🧠 Explanation: (4-5 sentences)\n💡 Key Advice:\nDiet: - 3-4 specific food suggestions\nLifestyle: - 2-3 daily routine tips\nPrecautions: - 2-3 warnings\nRULES: NEVER mention doctors. ALWAYS use headings. Be specific."},
                {"role": "user", "content": prompt}
            ], temperature=0.2)
        return r.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

def chat_with_ai(user_q):
    msgs = [{"role": "system", "content": st.session_state.system_prompt}]
    if st.session_state.memory_summary:
        msgs.append({"role": "system", "content": f"Previous context: {st.session_state.memory_summary}"})
    msgs.extend([m for m in st.session_state.chat_history if m["role"] != "system"])
    msgs.append({"role": "user", "content": f"Patient condition: {st.session_state.conditions}\n\nUser question: {user_q}"})
    try:
        r = client.chat.completions.create(model="openai/gpt-oss-120b", messages=msgs, temperature=0.3)
        reply = r.choices[0].message.content
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.session_state.chat_history = trim_history(st.session_state.chat_history, MAX_HISTORY)
        if len(st.session_state.chat_history) >= MAX_HISTORY:
            st.session_state.memory_summary = summarize_memory(st.session_state.chat_history, client)
            st.session_state.chat_history = []
        return reply
    except Exception as e:
        return f"❌ Error: {str(e)}"

def render_param_table(final_data):
    rows_html = ""
    for param, details in final_data.items():
        val    = details.get("value", "N/A")
        unit   = details.get("unit", "")
        ref    = details.get("reference_range", "—")
        status = details.get("status", "normal")
        rows_html += f"""<tr>
          <td style="font-weight:500;padding-right:1rem;">{param}</td>
          <td class="{status_class(status)}" style="font-weight:600;">{val} {unit}</td>
          <td style="color:#7b83a0;font-size:12px;">{ref}</td>
          <td>{status_badge(status)}</td>
        </tr>"""
    st.markdown(f"""
    <table class="param-table">
      <thead><tr><th>Parameter</th><th>Value</th><th>Reference</th><th>Status</th></tr></thead>
      <tbody>{rows_html}</tbody>
    </table>""", unsafe_allow_html=True)

def reset_analysis():
    for k in ["report_text","final_data","conditions","summary","chat_history",
              "memory_summary","system_prompt","analyzed","view_report_id"]:
        st.session_state[k] = _defaults[k]


# ─────────────────────────────────────────────────────────────────────────────
# TOPBAR
# ─────────────────────────────────────────────────────────────────────────────
is_guest           = st.session_state.is_guest
username_display   = st.session_state.user.get("username", "User")
avatar_letter      = username_display[0].upper()

if is_guest:
    user_html = '<div class="guest-chip">👤 Guest Session</div>'
else:
    user_html = f'<div class="user-chip"><div class="user-avatar">{avatar_letter}</div>{username_display}</div>'

st.markdown(f"""
<div class="topbar">
  <div class="topbar-inner">
    <div class="brand">🩺 Medi<span>Scan</span> AI</div>
    {user_html}
  </div>
</div>
""", unsafe_allow_html=True)

# Top-right controls
if is_guest:
    c1, c2, c3 = st.columns([9, 1.4, 1])
    with c2:
        if st.button("🔐 Sign in", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
    with c3:
        if st.button("🚪", help="Exit guest", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
else:
    c1, c2, c3 = st.columns([9, 1.5, 1])
    with c2:
        # Clicking the username goes to dashboard
        if st.button(f"👤 {username_display}", use_container_width=True, key="dash_btn"):
            st.session_state.page = "dashboard"
            st.session_state.view_report_id = None
            st.rerun()
    with c3:
        if st.button("🚪", help="Logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
      <div class="logo-icon">🩺</div>
      <div class="logo-text">Medi<span>Scan</span> AI</div>
    </div>
    """, unsafe_allow_html=True)

    # Nav
    if not is_guest:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔬 Analyse", use_container_width=True, key="nav_analyse"):
                st.session_state.page = "analyse"
                st.rerun()
        with col_b:
            if st.button("📋 Dashboard", use_container_width=True, key="nav_dash"):
                st.session_state.page = "dashboard"
                st.session_state.view_report_id = None
                st.rerun()
        st.markdown("<hr style='border-color:var(--border);margin:.75rem 0'>", unsafe_allow_html=True)

    if st.session_state.page == "analyse" or is_guest:
        st.markdown('<div style="font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem;">Input Method</div>', unsafe_allow_html=True)
        input_method = st.selectbox("", ["Upload Image", "Upload PDF"], label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)

        img_file = None
        pdf_file = None
        if input_method == "Upload Image":
            img_file = st.file_uploader("Upload image", type=["png","jpg","jpeg"], label_visibility="collapsed")
        else:
            pdf_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

        analyze_btn = st.button("🔬 Analyse Report")

        if is_guest:
            st.markdown("""
            <div style="background:rgba(255,179,71,0.08);border:1px solid rgba(255,179,71,0.25);border-radius:10px;padding:.6rem .9rem;font-size:12px;color:#ffb347;margin-top:.75rem;">
              👤 Guest mode — results won't be saved
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="disclaimer">⚠️ Not a substitute for professional medical advice.</div>', unsafe_allow_html=True)

        if st.session_state.analyzed:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Reset"):
                reset_analysis()
                st.rerun()
    else:
        analyze_btn = False
        input_method = None
        img_file = None
        pdf_file = None


# ─────────────────────────────────────────────────────────────────────────────
# ANALYSE LOGIC
# ─────────────────────────────────────────────────────────────────────────────
if analyze_btn:
    raw_text  = ""
    file_data = b""
    filename  = ""
    file_type = ""
    try:
        if input_method == "Upload Image" and img_file:
            file_data = img_file.read()
            filename  = img_file.name
            file_type = "image"
            tmp = os.path.join(os.path.dirname(__file__), "_tmp_img")
            with open(tmp, "wb") as f:
                f.write(file_data)
            raw_text = extract_text_from_image(tmp)
        elif input_method == "Upload PDF" and pdf_file:
            file_data = pdf_file.read()
            filename  = pdf_file.name
            file_type = "pdf"
            tmp = os.path.join(os.path.dirname(__file__), "_tmp.pdf")
            with open(tmp, "wb") as f:
                f.write(file_data)
            raw_text = extract_text_from_pdf(tmp)

        if len(raw_text.strip()) < 30:
            st.sidebar.error("⚠️ Could not extract enough text. Try a clearer file.")
            st.stop()

        with st.spinner("Analysing report…"):
            ai_data = ai_extract_parameters(raw_text, client)
            ai_data = ai_data.strip().replace("```json","").replace("```","")
            try:
                parsed_data = json.loads(ai_data)
            except json.JSONDecodeError:
                st.sidebar.error("❌ Could not parse AI response.")
                parsed_data = {}

            final_data = analyze_report(parsed_data)
            conditions = []
            for param, details in final_data.items():
                s = details.get("status","").lower()
                if s == "low":    conditions.append(f"{param} is low")
                elif s == "high": conditions.append(f"{param} is high")
            if not conditions:
                conditions.append("All parameters are normal")

            summary = get_summary(explain_report_prompt(str(final_data)))
            system_prompt = f"""You are a smart AI medical assistant.
Patient Report: {final_data}
Detected Conditions: {conditions}
Answer ONLY based on patient data. Give personalized diet, lifestyle, precautions.
RULES: No generic answers. Be specific. Always end with: "This is not a medical diagnosis.\""""

            st.session_state.report_text    = raw_text
            st.session_state.final_data     = final_data
            st.session_state.conditions     = conditions
            st.session_state.summary        = summary
            st.session_state.system_prompt  = system_prompt
            st.session_state.chat_history   = []
            st.session_state.memory_summary = ""
            st.session_state.analyzed       = True

            # Save to DB only for logged-in users
            if not is_guest and st.session_state.user.get("id") and file_data:
                save_report(
                    user_id    = st.session_state.user["id"],
                    filename   = filename,
                    file_type  = file_type,
                    file_data  = file_data,
                    raw_text   = raw_text,
                    final_data = final_data,
                    conditions = conditions,
                    summary    = summary,
                )

    except Exception as e:
        st.sidebar.error(f"❌ {str(e)}")


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_dashboard():
    user_id = st.session_state.user["id"]

    # ── Viewing a single report ───────────────────────────────────────────────
    if st.session_state.view_report_id:
        report = get_report_by_id(st.session_state.view_report_id, user_id)
        if not report:
            st.error("Report not found.")
            st.session_state.view_report_id = None
            st.rerun()

        if st.button("← Back to Dashboard", key="back_dash"):
            st.session_state.view_report_id = None
            st.rerun()

        st.markdown(f"""
        <div class="page-header">
          <h1>{report['filename']}</h1>
          <p>Uploaded {report['uploaded_at']}</p>
        </div>
        """, unsafe_allow_html=True)

        final_data = report["final_data"]
        if final_data:
            high_c = sum(1 for d in final_data.values() if d.get("status","").lower()=="high")
            low_c  = sum(1 for d in final_data.values() if d.get("status","").lower()=="low")
            norm_c = sum(1 for d in final_data.values() if d.get("status","").lower()=="normal")
            st.markdown(f"""
            <div class="metrics-row">
              <div class="metric-pill"><div class="val status-high">{high_c}</div><div class="lbl">High</div></div>
              <div class="metric-pill"><div class="val status-low">{low_c}</div><div class="lbl">Low</div></div>
              <div class="metric-pill"><div class="val status-norm">{norm_c}</div><div class="lbl">Normal</div></div>
              <div class="metric-pill"><div class="val" style="color:#638bff;">{len(final_data)}</div><div class="lbl">Total</div></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="card"><div class="card-title">Parameter Breakdown</div>', unsafe_allow_html=True)
            render_param_table(final_data)
            st.markdown('</div>', unsafe_allow_html=True)

        if report["conditions"]:
            cond_items = "".join(f'<li style="margin-bottom:4px;font-size:14px;">{c}</li>' for c in report["conditions"])
            st.markdown(f'<div class="card"><div class="card-title">Detected Conditions</div><ul style="margin:0;padding-left:1.2rem;">{cond_items}</ul></div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">🧠 AI Summary & Advice</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:14px;line-height:1.8;white-space:pre-wrap;">{report["summary"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Delete this report", key="del_report"):
            delete_report(st.session_state.view_report_id, user_id)
            st.session_state.view_report_id = None
            st.success("Report deleted.")
            st.rerun()
        return

    # ── Report list ───────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="page-header">
      <h1>My Dashboard</h1>
      <p>Welcome back, {username_display}. Here are all your uploaded reports.</p>
    </div>
    """, unsafe_allow_html=True)

    reports = get_user_reports(user_id)

    if not reports:
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;color:#7b83a0;">
          <div style="font-size:48px;margin-bottom:1rem;">📂</div>
          <div style="font-size:16px;font-weight:500;margin-bottom:.5rem;">No reports yet</div>
          <div style="font-size:13px;">Upload a lab report from the Analyse page to get started.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Analyse →", key="goto_analyse"):
            st.session_state.page = "analyse"
            st.rerun()
        return

    # Summary stats across all reports
    total_reports = len(reports)
    total_abnormal = sum(
        1 for r in reports
        for c in r["conditions"]
        if "is high" in c or "is low" in c
    )
    st.markdown(f"""
    <div class="metrics-row">
      <div class="metric-pill"><div class="val" style="color:#638bff;">{total_reports}</div><div class="lbl">Total Reports</div></div>
      <div class="metric-pill"><div class="val status-high">{total_abnormal}</div><div class="lbl">Abnormal Findings</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card-title" style="margin-bottom:.75rem;">Recent Reports</div>', unsafe_allow_html=True)

    for rep in reports:
        abnormal = [c for c in rep["conditions"] if "is high" in c or "is low" in c]
        badge_html = ""
        if abnormal:
            badge_html = f'<span class="badge badge-high">{len(abnormal)} abnormal</span>'
        else:
            badge_html = '<span class="badge badge-norm">All normal</span>'

        icon = "🖼️" if rep["file_type"] == "image" else "📄"
        date_str = rep["uploaded_at"][:16] if rep["uploaded_at"] else "—"

        col_info, col_btn = st.columns([5, 1])
        with col_info:
            st.markdown(f"""
            <div class="report-card">
              <div class="report-card-title">{icon} {rep['filename']}</div>
              <div class="report-card-meta">{date_str} &nbsp;·&nbsp; {badge_html}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
            if st.button("View →", key=f"view_{rep['id']}"):
                st.session_state.view_report_id = rep["id"]
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ANALYSE RESULTS PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_analyse():
    if not st.session_state.analyzed:
        st.markdown("""
        <div style="max-width:640px;margin:4rem auto;text-align:center;padding:2rem;">
          <div style="font-size:56px;margin-bottom:1rem;">🩺</div>
          <h1 style="font-family:'Syne',sans-serif;font-size:36px;font-weight:800;letter-spacing:-1px;margin-bottom:.75rem;">
            Lab Report <span style="color:#638bff;">Analyser</span>
          </h1>
          <p style="color:#7b83a0;font-size:16px;line-height:1.7;margin-bottom:2rem;">
            Upload an image or PDF of your lab report —<br>
            get a clear AI-powered breakdown of your results instantly.
          </p>
          <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
            <div style="background:rgba(63,255,194,0.08);border:1px solid rgba(63,255,194,0.2);border-radius:12px;padding:1rem 1.25rem;text-align:left;min-width:160px;">
              <div style="font-size:22px;">🖼️</div>
              <div style="font-size:13px;font-weight:500;margin-top:6px;">Image Upload</div>
              <div style="font-size:12px;color:#7b83a0;">JPG, PNG supported</div>
            </div>
            <div style="background:rgba(255,92,122,0.08);border:1px solid rgba(255,92,122,0.2);border-radius:12px;padding:1rem 1.25rem;text-align:left;min-width:160px;">
              <div style="font-size:22px;">📄</div>
              <div style="font-size:13px;font-weight:500;margin-top:6px;">PDF Upload</div>
              <div style="font-size:12px;color:#7b83a0;">Lab report PDFs</div>
            </div>
          </div>
          <p style="margin-top:2rem;font-size:13px;color:#7b83a0;">← Use the sidebar to get started</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("""
    <div class="page-header">
      <h1>Report Analysis</h1>
      <p>Your lab results have been analysed. See the breakdown below.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊  Results & Summary", "💬  AI Chatbot", "📄  Raw Report"])

    with tab1:
        final_data = st.session_state.final_data
        if final_data:
            high_c = sum(1 for d in final_data.values() if d.get("status","").lower()=="high")
            low_c  = sum(1 for d in final_data.values() if d.get("status","").lower()=="low")
            norm_c = sum(1 for d in final_data.values() if d.get("status","").lower()=="normal")
            st.markdown(f"""
            <div class="metrics-row">
              <div class="metric-pill"><div class="val status-high">{high_c}</div><div class="lbl">High</div></div>
              <div class="metric-pill"><div class="val status-low">{low_c}</div><div class="lbl">Low</div></div>
              <div class="metric-pill"><div class="val status-norm">{norm_c}</div><div class="lbl">Normal</div></div>
              <div class="metric-pill"><div class="val" style="color:#638bff;">{len(final_data)}</div><div class="lbl">Total</div></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="card"><div class="card-title">Parameter Breakdown</div>', unsafe_allow_html=True)
            render_param_table(final_data)
            st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.conditions:
            cond_items = "".join(f'<li style="margin-bottom:4px;font-size:14px;">{c}</li>' for c in st.session_state.conditions)
            st.markdown(f'<div class="card"><div class="card-title">Detected Conditions</div><ul style="margin:0;padding-left:1.2rem;color:#e8eaf6;">{cond_items}</ul></div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">🧠 AI Summary & Advice</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:14px;line-height:1.8;white-space:pre-wrap;">{st.session_state.summary}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div style="font-size:13px;color:#7b83a0;line-height:1.6;margin-bottom:1rem;">Ask anything about your report — diet, lifestyle, what a parameter means, or follow-up questions.</div>', unsafe_allow_html=True)
        if not st.session_state.chat_history:
            st.markdown('<div style="text-align:center;padding:2rem;color:#7b83a0;"><div style="font-size:32px;margin-bottom:.5rem;">💬</div><div style="font-size:14px;">Ask me anything about your report</div></div>', unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="label-user bubble-label">You</div><div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="label-ai bubble-label">MediScan AI</div><div class="bubble-ai">{msg["content"]}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px;color:#7b83a0;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.4rem;">Suggested questions</div>', unsafe_allow_html=True)
        q_cols = st.columns(3)
        for i, (col, q) in enumerate(zip(q_cols, ["What foods should I eat?", "What lifestyle changes help?", "Explain my key abnormalities"])):
            with col:
                if st.button(q, key=f"sug_{i}"):
                    with st.spinner("Thinking…"):
                        chat_with_ai(q)
                    st.rerun()

        user_input = st.chat_input("Ask about your report…")
        if user_input:
            with st.spinner("Thinking…"):
                chat_with_ai(user_input)
            st.rerun()

    with tab3:
        st.markdown('<div class="card"><div class="card-title">Extracted Text</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:13px;color:#7b83a0;white-space:pre-wrap;line-height:1.7;">{st.session_state.report_text}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.page == "dashboard" and not is_guest:
    render_dashboard()
else:
    render_analyse()
>>>>>>> dba419a332508878fc47ed5bddc846ff792eabe6
