import os, json
import streamlit as st
from prompts import explain_report_prompt
from utils.extractor import extract_text_from_pdf, extract_text_from_image
from utils.ai_extractor import ai_extract_parameters
from utils.parser import analyze_report, KEY_METRICS, PARAMETERS
from db import save_report
from components.helpers import (
    _sc, ICONS, DEFAULT_ICON, SPARK,
    validate_medical_input, get_summary, generate_patient_summary,
    parse_sections, chat_with_ai, render_inline_chat, _md_to_html,
)

_DEFAULTS = {
    "report_text": "", "final_data": {}, "conditions": [],
    "summary": "", "patient_summary": "", "chat_history": [], "memory_summary": "",
    "system_prompt": "", "analyzed": False,
    "prec_chat": [], "diet_chat": [],
    "prec_bullets": [], "diet_bullets": [],
    "show_prec_chat": False, "show_diet_chat": False,
}

def render(user, client):
    import datetime

    st.markdown("""
    <div class="page-header">
      <div class="page-title">📊 Dashboard</div>
      <div class="page-sub">Upload a lab report to get an instant AI-powered analysis.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-grid">
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
    </div>""", unsafe_allow_html=True)

    # ── Upload panel ──────────────────────────────────────────────────────────
    with st.expander("📂  Open Upload Panel", expanded=not st.session_state.analyzed):
        method = st.radio("Input method", ["🖼️ Image", "📄 PDF"],
                          horizontal=True, label_visibility="collapsed")
        img_file = pdf_file = None

        if method == "🖼️ Image":
            img_file = st.file_uploader("Upload images", type=["png","jpg","jpeg"],
                                        accept_multiple_files=True)
        else:
            pdf_file = st.file_uploader("Upload PDFs", type=["pdf"],
                                        accept_multiple_files=True)

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        analyze_btn = st.button("🔬  Analyse Report", use_container_width=True)

        if st.session_state.analyzed:
            if st.button("🔄  Reset & Upload New Report", use_container_width=True, key="reset_btn"):
                for k, v in _DEFAULTS.items():
                    st.session_state[k] = v
                st.rerun()

        st.markdown('<div style="font-size:12px;color:#e67e22;margin-top:6px;">'
                    '⚠️ Not a substitute for professional medical advice.</div>',
                    unsafe_allow_html=True)

    # ── Analyse logic ─────────────────────────────────────────────────────────
    if analyze_btn:
        raw = ""
        try:
            if method == "🖼️ Image" and img_file:
                for i, f in enumerate(img_file):
                    tmp = os.path.join(os.path.dirname(__file__), f"_tmp_img_{i}")
                    with open(tmp, "wb") as fp: fp.write(f.read())
                    raw += f"\n--- File: {f.name} ---\n" + extract_text_from_image(tmp)
            elif method == "📄 PDF" and pdf_file:
                for i, f in enumerate(pdf_file):
                    tmp = os.path.join(os.path.dirname(__file__), f"_tmp_{i}.pdf")
                    with open(tmp, "wb") as fp: fp.write(f.read())
                    raw += f"\n--- File: {f.name} ---\n" + extract_text_from_pdf(tmp)

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
                    for p, d in final_data.items()
                    if d.get("status","").lower() in ("high","low")
                ] or ["All parameters are normal"]

                summary         = get_summary(client, explain_report_prompt(str(final_data)))
                prec, diet      = parse_sections(summary)
                patient_summary = generate_patient_summary(client, final_data, conditions)
                sys_prompt      = (
                    f"You are a smart AI medical assistant.\n"
                    f"Patient Report: {final_data}\n"
                    f"Detected Conditions: {conditions}\n"
                    f"Give personalized, specific answers. No generic advice.\n"
                    f"Always end with: This is not a medical diagnosis."
                )
                rid = save_report(user["id"], final_data, conditions, summary)

                st.session_state.update({
                    "report_text":     raw,
                    "final_data":      final_data,
                    "conditions":      conditions,
                    "summary":         summary,
                    "patient_summary": patient_summary,
                    "prec_bullets":    prec,
                    "diet_bullets":    diet,
                    "system_prompt":   sys_prompt,
                    "chat_history":    [],
                    "prec_chat":       [],
                    "diet_chat":       [],
                    "memory_summary":  "",
                    "analyzed":        True,
                })
                st.success(f"✅ Report analysed and saved as #{rid}")
                st.rerun()
        except Exception as e:
            st.error(f"❌ {e}")

    # ── Empty state ───────────────────────────────────────────────────────────
    if not st.session_state.analyzed:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem;">
          <div style="font-size:52px;margin-bottom:12px;">🩺</div>
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;
                      font-weight:800;color:#1e2d4a;letter-spacing:-.5px;margin-bottom:8px;">
            No report analysed yet
          </div>
          <p style="color:#6b82a8;font-size:13.5px;line-height:1.8;max-width:420px;margin:0 auto;">
            Use the upload panel above to upload an image or PDF lab report to get started.
          </p>
        </div>""", unsafe_allow_html=True)
        return

    # ── Results tabs ──────────────────────────────────────────────────────────
    final_data = st.session_state.final_data
    tab_dash, tab_chat, tab_raw = st.tabs(["📊  Results", "💬  AI Chat", "📄  Raw Report"])

    # ── TAB 1: Results ────────────────────────────────────────────────────────
    with tab_dash:
        hL, hR = st.columns([3,1])
        with hL:
            st.markdown("""
            <div style="margin-bottom:4px;">
              <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:20px;
                          font-weight:800;color:#1e2d4a;letter-spacing:-.4px;">Health Dashboard</div>
              <div style="font-size:13px;color:#6b82a8;margin-top:3px;">
                Your lab results have been analysed. Review the breakdown below.
              </div>
            </div>""", unsafe_allow_html=True)
        with hR:
            today = datetime.date.today().strftime("%d %B %Y")
            st.markdown(f'<div style="text-align:right;font-size:12px;color:#8a9bbf;line-height:1.9;padding-top:4px;">Date: <b style="color:#1e2d4a;">{today}</b></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        patient_summary = st.session_state.get("patient_summary","")
        if patient_summary:
            st.markdown(f'<div class="summary-card"><div class="summary-title">🩺 Report Summary</div><div class="summary-text">{patient_summary}</div></div>', unsafe_allow_html=True)

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

        # Key metric cards
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
                sc, bc, ic, label = _sc(status)
                icon   = ICONS.get(key, DEFAULT_ICON)
                spark  = SPARK.get(status,"〰️")
                name   = key.replace("_"," ").title()
                with col:
                    st.markdown(f"""
                    <div class="metric-card card-tint-{status}">
                      <div class="mc-header"><div class="mc-icon {ic}">{icon}</div>{name}</div>
                      <div class="mc-value {sc}">{val}<span class="mc-unit">{unit}</span></div>
                      <span class="mc-badge {bc}">{label}</span>
                      <div class="mc-ref">Ref: {ref}</div>
                      <div class="mc-sparkline">{spark}</div>
                    </div>""", unsafe_allow_html=True)

        # Abnormal bar charts
        abnormal = {k:v for k,v in final_data.items() if v.get("status","").lower() in ("high","low")}
        if abnormal:
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">⚠️ Abnormal Parameters</div>', unsafe_allow_html=True)
            bar_cols = st.columns(min(len(abnormal), 4))
            for col, (key, d) in zip(bar_cols, list(abnormal.items())[:4]):
                val    = float(d.get("value", 0))
                status = d.get("status","normal").lower()
                meta   = PARAMETERS.get(key, {})
                mn     = float(meta.get("min", 0))
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
                      <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:800;color:{clr};">{val}
                        <span style="font-size:12px;color:#a0aec0;font-weight:500;margin-left:2px;">{unit}</span>
                      </div>
                      <div class="bar-track">
                        <div class="bar-fill" style="width:{pct}%;background:{clr};box-shadow:0 0 8px {clr}55;"></div>
                      </div>
                      <div style="display:flex;justify-content:space-between;font-size:10.5px;color:#a0aec0;margin-top:2px;">
                        <span>Min {mn}</span><span>Max {mx}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

        # Precautions + Diet panels
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        prec_bullets = st.session_state.get("prec_bullets", [])
        diet_bullets = st.session_state.get("diet_bullets", [])
        pL, pR = st.columns(2)

        with pL:
            items = "".join(f'<div class="panel-item"><span class="panel-warn">⚠</span>{b}</div>' for b in prec_bullets) \
                    if prec_bullets else '<div style="color:#a0aec0;font-size:13px;">No precautions generated.</div>'
            st.markdown(f'<div class="panel-box"><div class="panel-header"><div class="panel-icon" style="background:rgba(220,53,69,.1);">⚠️</div><span class="panel-title">Precautions</span></div>{items}</div>', unsafe_allow_html=True)
            if st.button("💬  Ask more about Precautions", key="prec_toggle", use_container_width=True):
                st.session_state.show_prec_chat = not st.session_state.show_prec_chat
            if st.session_state.show_prec_chat:
                st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
                render_inline_chat(client, "prec_chat","prec_q","Ask about precautions…","Focus only on precautions and safety advice.")
                st.markdown("</div>", unsafe_allow_html=True)

        with pR:
            items = "".join(f'<div class="panel-item"><span class="panel-check">✓</span>{b}</div>' for b in diet_bullets) \
                    if diet_bullets else '<div style="color:#a0aec0;font-size:13px;">No diet recommendations generated.</div>'
            st.markdown(f'<div class="panel-box"><div class="panel-header"><div class="panel-icon" style="background:rgba(39,174,96,.1);">🥗</div><span class="panel-title">Diet Recommendations</span></div>{items}</div>', unsafe_allow_html=True)
            if st.button("💬  Ask more about Diet", key="diet_toggle", use_container_width=True):
                st.session_state.show_diet_chat = not st.session_state.show_diet_chat
            if st.session_state.show_diet_chat:
                st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
                render_inline_chat(client, "diet_chat","diet_q","Ask about diet & nutrition…","Focus only on diet and nutrition recommendations.")
                st.markdown("</div>", unsafe_allow_html=True)

        # AI search bar
        st.markdown('<div class="ai-search-wrap"><div class="ai-search-label">🔍 Ask anything about your report</div>', unsafe_allow_html=True)
        with st.form(key="search_form", clear_on_submit=True):
            sc1, sc2 = st.columns([6,1])
            with sc1:
                search_q = st.text_input("", placeholder="e.g. What does high cholesterol mean for me?",
                                         label_visibility="collapsed", key="search_input")
            with sc2:
                search_sent = st.form_submit_button("Ask →", use_container_width=True)
            if search_sent and search_q.strip():
                with st.spinner("Thinking…"):
                    ans = chat_with_ai(client, search_q.strip(), "chat_history")
                st.markdown(f'<div class="ai-search-response">{_md_to_html(ans)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Full param table
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔬 Full Parameter Breakdown</div>', unsafe_allow_html=True)
        rows_html = ""
        for param, details in final_data.items():
            val    = details.get("value","—")
            unit   = details.get("unit","")
            ref    = details.get("reference_range","—")
            status = details.get("status","normal")
            sc, bc, _, label = _sc(status)
            name   = param.replace("_"," ").title()
            icon   = ICONS.get(param, DEFAULT_ICON)
            rows_html += f"""<tr>
              <td style="font-weight:500;padding-right:1rem;">{icon} {name}</td>
              <td class="{sc}" style="font-weight:700;">{val}<span style="font-size:11px;color:#a0aec0;margin-left:2px;">{unit}</span></td>
              <td style="color:#8a9bbf;font-size:12px;">{ref}</td>
              <td><span class="mc-badge {bc}">{label}</span></td>
            </tr>"""
        st.markdown(f'<div class="glass-card" style="padding:18px 22px;"><table class="ptable"><thead><tr><th>Parameter</th><th>Value</th><th>Reference Range</th><th>Status</th></tr></thead><tbody>{rows_html}</tbody></table></div>', unsafe_allow_html=True)

    # ── TAB 2: Chat ───────────────────────────────────────────────────────────
    with tab_chat:
        st.markdown("""
        <div style="margin-bottom:12px;">
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:16px;font-weight:700;color:#1e2d4a;">💬 Chat with MediScan AI</div>
          <div style="font-size:13px;color:#6b82a8;margin-top:3px;">Ask anything about your report — diet, lifestyle, what a parameter means.</div>
        </div>""", unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown('<div style="text-align:center;padding:2.5rem 1rem;color:#a0aec0;"><div style="font-size:36px;margin-bottom:.5rem;">💬</div><div style="font-size:14px;">Ask me anything about your report</div></div>', unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div style="font-size:10px;font-weight:700;color:#3b82f6;text-align:right;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;">You</div><div class="big-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="font-size:10px;font-weight:700;color:#14b8a6;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;">MediScan AI</div><div class="big-bubble-ai">{_md_to_html(msg["content"])}</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:10.5px;color:#a0aec0;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;">Suggested questions</div>', unsafe_allow_html=True)
        sq1, sq2, sq3 = st.columns(3)
        for col, q, i in zip([sq1,sq2,sq3], ["What foods should I eat?","What lifestyle changes help?","Explain my key abnormalities"], range(3)):
            with col:
                if st.button(q, key=f"sug_{i}", use_container_width=True):
                    with st.spinner("Thinking…"):
                        chat_with_ai(client, q, "chat_history")
                    st.rerun()

        user_input = st.chat_input("Ask about your report…")
        if user_input:
            with st.spinner("Thinking…"):
                chat_with_ai(client, user_input, "chat_history")
            st.rerun()

    # ── TAB 3: Raw ────────────────────────────────────────────────────────────
    with tab_raw:
        st.markdown(f'<div class="glass-card" style="padding:20px 24px;"><div style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:14px;font-weight:700;color:#1e2d4a;margin-bottom:10px;">📄 Extracted Report Text</div><div style="font-size:13px;color:#6b82a8;white-space:pre-wrap;line-height:1.85;">{st.session_state.report_text}</div></div>', unsafe_allow_html=True)
