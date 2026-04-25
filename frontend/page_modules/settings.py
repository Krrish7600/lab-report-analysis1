import streamlit as st

def render(user):
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

    col_lo, _ = st.columns([1, 3])
    with col_lo:
        if st.button("🚪  Logout", key="settings_logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
