import streamlit as st
from db import get_user_reports
from components.helpers import _sc, ICONS, DEFAULT_ICON

def render(user):
    st.markdown("""
    <div class="page-header">
      <div class="page-title">📋 Saved Reports</div>
      <div class="page-sub">View the full parameter breakdown of any past report.</div>
    </div>""", unsafe_allow_html=True)

    reports = get_user_reports(user["id"])
    if not reports:
        st.info("No saved reports yet. Analyse a report from the Dashboard.")
        return

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
            sc, bc, _, label = _sc(status)
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
