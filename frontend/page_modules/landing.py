import streamlit as st

def render():
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
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
