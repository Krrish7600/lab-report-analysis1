import streamlit as st
from db import login_user, create_user

def render():
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg,#c8daf5 0%,#d6eaf8 40%,#c8f0e8 100%) !important; }
    section[data-testid="stSidebar"]{ display:none !important; }
    .block-container{ max-width:480px !important; margin:0 auto !important; padding:3rem 1rem !important; }
    div[data-baseweb="tab-list"]{ background:rgba(255,255,255,.6) !important; }
    div[data-baseweb="tab"],div[data-baseweb="tab"] *,button[role="tab"],button[role="tab"] *
      { color:#1e2d4a !important; font-weight:600 !important; }
    div[aria-selected="true"][data-baseweb="tab"],div[aria-selected="true"][data-baseweb="tab"] *,
    button[aria-selected="true"],button[aria-selected="true"] *
      { background:white !important; color:#1e2d4a !important; font-weight:700 !important; }
    .stTextInput label{ color:#1e2d4a !important; font-weight:600 !important; font-size:13px !important; }
    .stTextInput input{ color:#1e2d4a !important; background:rgba(255,255,255,.92) !important;
      border:1.5px solid rgba(74,144,226,.3) !important; border-radius:10px !important;
      font-size:14px !important; padding:10px 14px !important; }
    .stTextInput input::placeholder{ color:#94a3b8 !important; }
    .stTextInput input:focus{ border-color:#3b82f6 !important; box-shadow:0 0 0 3px rgba(59,130,246,.18) !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
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
        email_l = st.text_input("Email address", key="l_email", placeholder="you@example.com")
        pass_l  = st.text_input("Password", type="password", key="l_pass", placeholder="Your password")
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
        name_s  = st.text_input("Full name",       key="s_name",  placeholder="Your name")
        email_s = st.text_input("Email address",   key="s_email", placeholder="you@example.com")
        pass_s  = st.text_input("Password",        type="password", key="s_pass",  placeholder="Min 6 characters")
        pass_s2 = st.text_input("Confirm password",type="password", key="s_pass2", placeholder="Repeat password")
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
