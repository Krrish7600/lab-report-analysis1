import re
import streamlit as st
from chatbot.memory import trim_history

# ── Status helpers ────────────────────────────────────────────────────────────
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

# ── Markdown → clean HTML converter ──────────────────────────────────────────
def _md_to_html(text: str) -> str:
    """Convert LLM markdown output to compact HTML for bubble rendering."""
    text = text.strip()

    # collapse 3+ blank lines to 1
    text = re.sub(r'\n{3,}', '\n\n', text)

    lines = text.splitlines()
    html_parts = []
    in_ul = False

    for line in lines:
        stripped = line.strip()

        # blank line — close any open list, add small spacer
        if not stripped:
            if in_ul:
                html_parts.append('</ul>')
                in_ul = False
            html_parts.append('<div style="height:6px"></div>')
            continue

        # headings: ## or ###
        if stripped.startswith('### '):
            if in_ul: html_parts.append('</ul>'); in_ul = False
            content = _inline_md(stripped[4:])
            html_parts.append(f'<div style="font-weight:700;font-size:13.5px;margin:10px 0 4px;">{content}</div>')
            continue
        if stripped.startswith('## '):
            if in_ul: html_parts.append('</ul>'); in_ul = False
            content = _inline_md(stripped[3:])
            html_parts.append(f'<div style="font-weight:800;font-size:14px;margin:12px 0 5px;">{content}</div>')
            continue
        if stripped.startswith('# '):
            if in_ul: html_parts.append('</ul>'); in_ul = False
            content = _inline_md(stripped[2:])
            html_parts.append(f'<div style="font-weight:800;font-size:15px;margin:12px 0 6px;">{content}</div>')
            continue

        # bullet: - or * or numbered 1.
        if re.match(r'^[-*]\s+', stripped) or re.match(r'^\d+\.\s+', stripped):
            if not in_ul:
                html_parts.append('<ul style="margin:4px 0 4px 16px;padding:0;">')
                in_ul = True
            content = re.sub(r'^[-*]\s+', '', stripped)
            content = re.sub(r'^\d+\.\s+', '', content)
            html_parts.append(f'<li style="margin-bottom:3px;line-height:1.55;">{_inline_md(content)}</li>')
            continue

        # normal paragraph
        if in_ul:
            html_parts.append('</ul>')
            in_ul = False
        html_parts.append(f'<p style="margin:0 0 5px;line-height:1.65;">{_inline_md(stripped)}</p>')

    if in_ul:
        html_parts.append('</ul>')

    return ''.join(html_parts)


def _inline_md(text: str) -> str:
    """Handle bold, italic, inline code."""
    # bold+italic ***text***
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # bold **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # italic *text*
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # inline code `text`
    text = re.sub(r'`(.*?)`', r'<code style="background:rgba(99,139,255,0.15);padding:1px 5px;border-radius:4px;font-size:12px;">\1</code>', text)
    return text

# ── Validation ────────────────────────────────────────────────────────────────
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
            "Please upload a valid lab report (blood test, CBC, lipid panel, etc.)."
        )
    return True, ""

# ── AI helpers ────────────────────────────────────────────────────────────────
def get_summary(client, prompt):
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

def generate_patient_summary(client, final_data: dict, conditions: list) -> str:
    from prompts import patient_summary_prompt
    try:
        prompt = patient_summary_prompt(final_data, conditions)
        r = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return r.choices[0].message.content.strip()
    except Exception as e:
        return f"Unable to generate summary: {e}"

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

def chat_with_ai(client, user_q, history_key, system_extra=""):
    sys_p = st.session_state.system_prompt + "\n" + system_extra
    msgs  = [{"role":"system","content":sys_p}]
    if st.session_state.memory_summary:
        msgs.append({"role":"system","content":f"Previous context: {st.session_state.memory_summary}"})
    msgs += [m for m in st.session_state[history_key] if m["role"] != "system"]
    msgs.append({"role":"user","content":f"Patient: {st.session_state.conditions}\n\n{user_q}"})
    try:
        r = client.chat.completions.create(
            model="openai/gpt-oss-120b", messages=msgs, temperature=0.3)
        # store raw text, render as HTML when displaying
        reply = r.choices[0].message.content.strip()
        st.session_state[history_key].append({"role":"user","content":user_q})
        st.session_state[history_key].append({"role":"assistant","content":reply})
        st.session_state[history_key] = trim_history(st.session_state[history_key], 8)
        return reply
    except Exception as e:
        return f"Error: {e}"

def render_inline_chat(client, panel_key, input_key, placeholder, system_extra=""):
    for msg in st.session_state[panel_key]:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-label cl-user">You</div>'
                        f'<div class="cbubble-user">{msg["content"]}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-label cl-ai">MediScan AI</div>'
                        f'<div class="cbubble-ai">{_md_to_html(msg["content"])}</div>',
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
                chat_with_ai(client, q.strip(), panel_key, system_extra)
            st.rerun()
