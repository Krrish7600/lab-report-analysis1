import streamlit as st
from db import get_user_reports

def render(user):
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
          <div style="font-size:13px;margin-top:6px;">Go to Dashboard and analyse your first report.</div>
        </div>""", unsafe_allow_html=True)
        return

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
