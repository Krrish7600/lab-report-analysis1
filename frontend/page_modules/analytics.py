import streamlit as st
from db import get_user_reports

def render(user):
    st.markdown("""
    <div class="page-header">
      <div class="page-title">📈 Analytics</div>
      <div class="page-sub">Statistics based on your analysed reports.</div>
    </div>""", unsafe_allow_html=True)

    reports  = get_user_reports(user["id"])
    total    = len(reports)
    total_p  = sum(r["params"]   for r in reports)
    total_a  = sum(r["abnormal"] for r in reports)
    rate     = round(total_a / total_p * 100, 1) if total_p else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, num, lbl in [
        (c1, total,      "Reports Analysed"),
        (c2, total_p,    "Total Parameters"),
        (c3, total_a,    "Abnormal Findings"),
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
