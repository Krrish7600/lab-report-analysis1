import streamlit as st

def get_theme(dark_mode: bool) -> dict:
    if dark_mode:
        return {
            "app_bg":    "#0f172a",
            "card":      "#1e293b",
            "card2":     "#263348",
            "border":    "#334155",
            "text":      "#e2e8f0",
            "text2":     "#94a3b8",
            "text3":     "#64748b",
            "sidebar":   "#0f172a",
            "sb_border": "#1e3a5f",
            "input_bg":  "#1e293b",
            "shadow":    "rgba(0,0,0,.45)",
            "tab_bg":    "rgba(15,23,42,.9)",
            "tab_sel":   "#263348",
            "exp_bg":    "#1e293b",
            "exp_sum":   "#263348",
            "panel":     "#1e293b",
            "chat_bg":   "#1a2744",
            "bubble_ai": "#263348",
            "hist_row":  "#1e293b",
            "search_bg": "#1e293b",
            "upload_bg": "#1e293b",
            "count_bg":  "#1e293b",
            "bar_bg":    "#1e293b",
            "stat_bg":   "#1e293b",
            "summary_bg":"linear-gradient(135deg,#1e293b 0%,#1a2744 100%)",
            "summary_border":"rgba(59,130,246,.4)",
            "hero_sub":  "#94a3b8",
            "feat_bg":   "#1e293b",
            "feat_border":"#334155",
        }
    return {
        "app_bg":    "linear-gradient(145deg,#c8daf5 0%,#dce8f7 35%,#e8f0fb 65%,#d0e4f5 100%)",
        "card":      "rgba(255,255,255,.70)",
        "card2":     "rgba(255,255,255,.68)",
        "border":    "rgba(255,255,255,.78)",
        "text":      "#1e2d4a",
        "text2":     "#6b82a8",
        "text3":     "#8a9bbf",
        "sidebar":   "linear-gradient(180deg,rgba(214,232,250,.92) 0%,rgba(200,224,248,.88) 100%)",
        "sb_border": "rgba(255,255,255,.7)",
        "input_bg":  "rgba(255,255,255,.92)",
        "shadow":    "rgba(74,144,226,.09)",
        "tab_bg":    "rgba(255,255,255,.6)",
        "tab_sel":   "rgba(255,255,255,.95)",
        "exp_bg":    "rgba(255,255,255,.78)",
        "exp_sum":   "rgba(255,255,255,.9)",
        "panel":     "rgba(255,255,255,.68)",
        "chat_bg":   "rgba(235,244,255,.82)",
        "bubble_ai": "rgba(255,255,255,.95)",
        "hist_row":  "rgba(255,255,255,.58)",
        "search_bg": "rgba(255,255,255,.78)",
        "upload_bg": "rgba(255,255,255,.82)",
        "count_bg":  "rgba(255,255,255,.68)",
        "bar_bg":    "rgba(255,255,255,.68)",
        "stat_bg":   "rgba(255,255,255,.68)",
        "summary_bg":"linear-gradient(135deg,rgba(255,255,255,.92) 0%,rgba(235,244,255,.88) 100%)",
        "summary_border":"rgba(59,130,246,.2)",
        "hero_sub":  "#334e68",
        "feat_bg":   "rgba(255,255,255,.72)",
        "feat_border":"rgba(255,255,255,.88)",
    }


def inject_css(T: dict):
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
html,body,[class*="css"],.stApp{{font-family:'Inter',sans-serif !important;color:{T['text']} !important;transition:background .3s,color .3s;}}
.stApp{{background:{T['app_bg']} !important;min-height:100vh;}}
#MainMenu,footer,header{{visibility:hidden;}}
.block-container{{padding:1.2rem 1.8rem 3rem !important;max-width:100% !important;position:relative;z-index:1;}}
section[data-testid="stSidebar"]{{display:flex !important;background:{T['sidebar']} !important;backdrop-filter:blur(22px) saturate(200%) !important;border-right:1px solid {T['sb_border']} !important;min-width:250px !important;max-width:270px !important;box-shadow:3px 0 24px {T['shadow']} !important;transition:background .3s;}}
section[data-testid="stSidebar"] > div:first-child{{padding:1.4rem 1rem !important;}}
section[data-testid="stSidebar"] h3{{font-family:'Plus Jakarta Sans',sans-serif !important;font-size:17px !important;font-weight:800 !important;color:{T['text']} !important;letter-spacing:-.3px !important;margin-bottom:4px !important;}}
section[data-testid="stSidebar"] hr{{border-color:rgba(74,144,226,.18) !important;margin:10px 0 !important;}}
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] .stMarkdown{{color:{T['text2']} !important;font-size:13px !important;}}
section[data-testid="stSidebar"] .stButton>button{{background:{T['card']} !important;color:{T['text']} !important;border:1px solid {T['border']} !important;border-radius:11px !important;font-weight:500 !important;font-size:14px !important;text-align:left !important;justify-content:flex-start !important;padding:10px 14px !important;margin-bottom:3px !important;transition:all .18s ease !important;width:100% !important;}}
section[data-testid="stSidebar"] .stButton>button:hover{{background:rgba(59,130,246,.18) !important;color:#3b82f6 !important;border-color:rgba(59,130,246,.4) !important;transform:translateX(2px) !important;}}
section[data-testid="stSidebar"] .stButton>button[kind="primary"]{{background:linear-gradient(135deg,#3b82f6,#14b8a6) !important;color:#ffffff !important;border:none !important;font-weight:700 !important;box-shadow:0 4px 14px rgba(59,130,246,.35) !important;}}
section[data-testid="stSidebar"] .stButton:last-of-type>button{{background:rgba(220,53,69,.1) !important;color:#ef4444 !important;border:1px solid rgba(220,53,69,.25) !important;}}
section[data-testid="stSidebar"] .stButton:last-of-type>button:hover{{background:rgba(220,53,69,.2) !important;}}
.glass-card{{background:{T['card']};backdrop-filter:blur(18px) saturate(160%);border:1px solid {T['border']};border-radius:18px;box-shadow:0 4px 24px {T['shadow']},0 1px 4px rgba(0,0,0,.04);position:relative;overflow:hidden;}}
.glass-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.25),transparent);}}
.page-header{{margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid rgba(74,144,226,.15);}}
.page-title{{font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:800;color:{T['text']};letter-spacing:-.5px;}}
.page-sub{{font-size:13px;color:{T['text2']};margin-top:4px;line-height:1.5;}}
.section-title{{font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;font-weight:700;color:{T['text']};margin:18px 0 10px;letter-spacing:-.2px;display:flex;align-items:center;gap:7px;}}
.metric-card{{background:{T['card']};backdrop-filter:blur(18px) saturate(160%);border:1px solid {T['border']};border-radius:16px;padding:16px 18px 14px;box-shadow:0 4px 20px {T['shadow']};transition:transform .22s ease,box-shadow .22s ease;position:relative;overflow:hidden;min-height:126px;}}
.metric-card:hover{{transform:translateY(-4px);box-shadow:0 12px 32px rgba(59,130,246,.2);}}
.mc-header{{display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:600;color:{T['text2']};margin-bottom:10px;}}
.mc-icon{{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;}}
.mc-value{{font-family:'Plus Jakarta Sans',sans-serif;font-size:26px;font-weight:800;line-height:1;margin-bottom:3px;letter-spacing:-.5px;}}
.mc-unit{{font-size:12px;font-weight:500;color:{T['text3']};margin-left:2px;}}
.mc-badge{{display:inline-flex;align-items:center;font-size:10.5px;font-weight:600;padding:3px 9px;border-radius:99px;margin-top:7px;}}
.mc-ref{{font-size:10.5px;color:{T['text3']};margin-top:3px;}}
.mc-sparkline{{position:absolute;bottom:10px;right:12px;opacity:.2;font-size:20px;}}
.s-high{{color:#ef4444;}}.s-low{{color:#f97316;}}.s-normal{{color:#22c55e;}}
.b-high{{background:rgba(239,68,68,.12);color:#ef4444;border:1px solid rgba(239,68,68,.25);}}
.b-low{{background:rgba(249,115,22,.12);color:#f97316;border:1px solid rgba(249,115,22,.25);}}
.b-normal{{background:rgba(34,197,94,.12);color:#22c55e;border:1px solid rgba(34,197,94,.25);}}
.i-high{{background:rgba(239,68,68,.12);}}.i-low{{background:rgba(249,115,22,.12);}}.i-normal{{background:rgba(34,197,94,.12);}}
.card-tint-high{{border-left:3.5px solid rgba(239,68,68,.6) !important;}}
.card-tint-low{{border-left:3.5px solid rgba(249,115,22,.6) !important;}}
.card-tint-normal{{border-left:3.5px solid rgba(34,197,94,.5) !important;}}
.counts-bar{{display:flex;gap:10px;margin-bottom:18px;flex-wrap:wrap;}}
.count-chip{{display:flex;align-items:center;gap:10px;background:{T['count_bg']};backdrop-filter:blur(14px);border:1px solid {T['border']};border-radius:14px;padding:10px 18px;box-shadow:0 2px 12px {T['shadow']};}}
.count-chip .num{{font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:800;line-height:1;}}
.count-chip .lbl{{font-size:11.5px;color:{T['text2']};font-weight:500;}}
.bar-card{{background:{T['bar_bg']};backdrop-filter:blur(16px);border:1px solid {T['border']};border-radius:16px;padding:16px 18px;box-shadow:0 4px 16px {T['shadow']};transition:transform .2s;}}
.bar-card:hover{{transform:translateY(-3px);}}
.bar-track{{background:rgba(128,128,128,.15);border-radius:99px;height:8px;overflow:hidden;margin:10px 0 5px;}}
.bar-fill{{height:100%;border-radius:99px;}}
.panel-box{{background:{T['panel']};backdrop-filter:blur(18px) saturate(160%);border:1px solid {T['border']};border-radius:18px;padding:18px 20px 14px;box-shadow:0 4px 22px {T['shadow']};}}
.panel-header{{display:flex;align-items:center;gap:9px;margin-bottom:12px;}}
.panel-icon{{width:32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:15px;}}
.panel-title{{font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;font-weight:700;color:{T['text']};}}
.panel-item{{display:flex;align-items:flex-start;gap:9px;padding:7px 0;border-bottom:1px solid rgba(74,144,226,.1);font-size:13px;color:{T['text']};line-height:1.55;}}
.panel-item:last-of-type{{border-bottom:none;}}
.panel-check{{color:#22c55e;font-size:13px;flex-shrink:0;margin-top:2px;}}
.panel-warn{{color:#f97316;font-size:13px;flex-shrink:0;margin-top:2px;}}
.summary-card{{background:{T['summary_bg']};backdrop-filter:blur(20px) saturate(180%);border:1.5px solid {T['summary_border']};border-left:4px solid #3b82f6;border-radius:18px;padding:22px 26px 20px;box-shadow:0 6px 28px rgba(59,130,246,.15),0 1px 4px rgba(0,0,0,.06);margin-bottom:20px;position:relative;overflow:hidden;}}
.summary-card::before{{content:'';position:absolute;top:0;right:0;width:180px;height:180px;background:radial-gradient(circle,rgba(59,130,246,.1) 0%,transparent 70%);pointer-events:none;}}
.summary-title{{font-family:'Plus Jakarta Sans',sans-serif;font-size:15px;font-weight:800;color:{T['text']};letter-spacing:-.3px;margin-bottom:10px;display:flex;align-items:center;gap:8px;}}
.summary-text{{font-size:14px;color:{T['text']};line-height:1.85;font-weight:400;}}
.chat-panel{{margin-top:10px;background:{T['chat_bg']};backdrop-filter:blur(12px);border:1px solid rgba(59,130,246,.2);border-radius:14px;padding:14px 16px;}}
.cbubble-user{{background:linear-gradient(135deg,#3b82f6,#14b8a6);color:#ffffff;border-radius:14px 14px 4px 14px;padding:9px 13px;margin:6px 0;margin-left:18%;font-size:13px;line-height:1.6;box-shadow:0 3px 12px rgba(59,130,246,.3);}}
.cbubble-ai{{background:{T['bubble_ai']};border:1px solid {T['border']};border-radius:14px 14px 14px 4px;padding:9px 13px;margin:6px 0;margin-right:8%;font-size:13px;line-height:1.6;color:{T['text']};box-shadow:0 2px 8px rgba(0,0,0,.1);white-space:pre-wrap;}}
.chat-label{{font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:2px;}}
.cl-user{{color:#3b82f6;text-align:right;}}.cl-ai{{color:#14b8a6;}}
.ptable{{width:100%;border-collapse:collapse;font-size:13px;}}
.ptable th{{color:{T['text3']};font-size:10.5px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;padding:0 0 10px;text-align:left;border-bottom:1.5px solid {T['border']};}}
.ptable td{{padding:9px 0;border-bottom:1px solid {T['border']};vertical-align:middle;color:{T['text']};}}
.ptable tr:last-child td{{border-bottom:none;}}
.ptable tr:hover td{{background:rgba(59,130,246,.05);}}
.big-bubble-user{{background:linear-gradient(135deg,rgba(59,130,246,.2),rgba(59,130,246,.08));border:1px solid rgba(59,130,246,.35);border-radius:18px 18px 4px 18px;padding:11px 15px;margin:7px 0;margin-left:10%;font-size:14px;line-height:1.65;color:{T['text']};}}
.big-bubble-ai{{background:{T['bubble_ai']};border:1px solid {T['border']};border-radius:18px 18px 18px 4px;padding:11px 15px;margin:7px 0;margin-right:6%;font-size:14px;line-height:1.65;color:{T['text']};box-shadow:0 2px 10px rgba(0,0,0,.1);}}
.hist-row{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:12px 16px;border-radius:12px;background:{T['hist_row']};border:1px solid {T['border']};margin-bottom:8px;transition:background .18s;}}
.hist-row:hover{{background:{T['card2']};}}
.hist-id{{font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;font-weight:700;color:#4a90e2;min-width:76px;}}
.hist-time{{font-size:11.5px;color:{T['text3']};min-width:140px;}}
.stat-card{{background:{T['stat_bg']};backdrop-filter:blur(16px);border:1px solid {T['border']};border-radius:16px;padding:20px 22px;text-align:center;box-shadow:0 4px 16px {T['shadow']};}}
.stat-num{{font-family:'Plus Jakarta Sans',sans-serif;font-size:34px;font-weight:800;color:#4a90e2;}}
.stat-lbl{{font-size:12px;color:{T['text2']};font-weight:500;margin-top:4px;}}
.hero{{text-align:center;padding:3.5rem 2rem 2.5rem;max-width:860px;margin:0 auto;}}
.hero-badge{{display:inline-flex;align-items:center;gap:7px;background:{T['card']};backdrop-filter:blur(14px);border:1px solid rgba(59,130,246,.3);border-radius:99px;padding:7px 20px;font-size:12.5px;font-weight:600;color:#3b82f6;margin-bottom:1.4rem;box-shadow:0 2px 12px rgba(59,130,246,.12);}}
.hero-title{{font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(28px,4.5vw,54px);font-weight:800;color:{T['text']};letter-spacing:-1.5px;line-height:1.12;margin-bottom:1.1rem;}}
.hero-title span{{background:linear-gradient(135deg,#3b82f6,#14b8a6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}}
.hero-sub{{font-size:16px;color:{T['hero_sub']};line-height:1.75;max-width:640px;margin:0 auto 2rem;text-align:center;font-weight:400;}}
.feature-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;max-width:1100px;margin:0 auto;}}
.feature-card{{background:{T['feat_bg']};backdrop-filter:blur(18px) saturate(160%);border:1px solid {T['feat_border']};border-radius:18px;padding:26px 22px 22px;text-align:left;box-shadow:0 6px 24px {T['shadow']};transition:transform .28s ease,box-shadow .28s ease;animation:fadeUp .55s ease both;position:relative;overflow:hidden;}}
.feature-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#3b82f6,#14b8a6);border-radius:18px 18px 0 0;opacity:0;transition:opacity .28s ease;}}
.feature-card:hover{{transform:translateY(-6px);box-shadow:0 16px 40px rgba(59,130,246,.2);}}
.feature-card:hover::before{{opacity:1;}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(22px);}}to{{opacity:1;transform:translateY(0);}}}}
.feature-card:nth-child(1){{animation-delay:.06s;}}.feature-card:nth-child(2){{animation-delay:.12s;}}.feature-card:nth-child(3){{animation-delay:.18s;}}.feature-card:nth-child(4){{animation-delay:.24s;}}.feature-card:nth-child(5){{animation-delay:.30s;}}
.fc-icon{{font-size:26px;margin-bottom:14px;display:inline-flex;align-items:center;justify-content:center;width:50px;height:50px;border-radius:13px;background:linear-gradient(135deg,rgba(59,130,246,.15),rgba(20,184,166,.12));border:1px solid rgba(59,130,246,.18);}}
.fc-title{{font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;font-weight:700;color:{T['text']};margin-bottom:8px;letter-spacing:-.1px;}}
.fc-desc{{font-size:12.5px;color:{T['text2']};line-height:1.65;font-weight:400;}}
.auth-card{{background:{T['card']};backdrop-filter:blur(24px) saturate(180%);border:1px solid {T['border']};border-radius:22px;padding:2.2rem 2.4rem;box-shadow:0 20px 60px {T['shadow']};}}
.ai-search-wrap{{background:{T['search_bg']};backdrop-filter:blur(18px) saturate(160%);border:1.5px solid rgba(59,130,246,.28);border-radius:16px;padding:18px 20px;box-shadow:0 4px 20px rgba(59,130,246,.12);margin-top:20px;}}
.ai-search-label{{font-family:'Plus Jakarta Sans',sans-serif;font-size:13.5px;font-weight:700;color:{T['text']};margin-bottom:10px;display:flex;align-items:center;gap:7px;}}
.ai-search-response{{margin-top:12px;padding:14px 16px;background:{T['card2']};border:1px solid {T['border']};border-radius:12px;font-size:13.5px;color:{T['text']};line-height:1.75;}}
.upload-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:16px;}}
@media(max-width:640px){{.upload-grid{{grid-template-columns:1fr;}}}}
.upload-card{{background:{T['upload_bg']};backdrop-filter:blur(18px) saturate(160%);border:2px solid rgba(59,130,246,.2);border-radius:16px;padding:24px 16px 20px;text-align:center;cursor:pointer;color:{T['text']} !important;transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease;box-shadow:0 2px 12px {T['shadow']};position:relative;z-index:1;}}
.upload-card:hover{{border-color:rgba(59,130,246,.55);transform:translateY(-4px);box-shadow:0 10px 28px rgba(59,130,246,.2);}}
.uc-icon{{font-size:32px;margin-bottom:10px;display:block;line-height:1;}}
.uc-title{{font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;font-weight:700;color:{T['text']} !important;margin-bottom:5px;display:block;}}
.uc-sub{{font-size:12px;color:{T['text2']} !important;font-weight:500;display:block;}}
.stTextArea textarea,.stTextInput input{{background:{T['input_bg']} !important;border:1.5px solid rgba(59,130,246,.3) !important;border-radius:10px !important;color:{T['text']} !important;font-family:'Inter',sans-serif !important;font-size:13.5px !important;}}
.stTextArea textarea::placeholder,.stTextInput input::placeholder{{color:{T['text3']} !important;}}
.stTextArea textarea:focus,.stTextInput input:focus{{border-color:#3b82f6 !important;box-shadow:0 0 0 3px rgba(59,130,246,.18) !important;}}
.stTextInput label,.stTextArea label,.stSelectbox label,.stFileUploader label,.stRadio label span{{color:{T['text']} !important;font-weight:600 !important;font-size:13px !important;}}
.stButton>button{{background:linear-gradient(135deg,#3b82f6,#14b8a6) !important;color:#ffffff !important;border:none !important;border-radius:10px !important;font-weight:600 !important;font-size:13.5px !important;padding:.55rem 1.3rem !important;box-shadow:0 3px 14px rgba(59,130,246,.3) !important;transition:opacity .2s,transform .15s !important;width:100%;}}
.stButton>button:hover{{opacity:.9 !important;transform:translateY(-1px) !important;}}
.stFileUploader{{background:{T['input_bg']} !important;border:1.5px dashed rgba(59,130,246,.35) !important;border-radius:12px !important;}}
.stSelectbox>div>div{{background:{T['input_bg']} !important;border:1.5px solid rgba(59,130,246,.28) !important;border-radius:10px !important;color:{T['text']} !important;}}
div[data-baseweb="tab-list"]{{background:{T['tab_bg']} !important;backdrop-filter:blur(12px) !important;border-radius:11px !important;border:1px solid {T['border']} !important;padding:4px !important;gap:3px !important;}}
div[data-baseweb="tab"],div[data-baseweb="tab"] *,button[role="tab"],button[role="tab"] p,button[role="tab"] span{{border-radius:8px !important;font-weight:500 !important;color:{T['text']} !important;font-size:13px !important;}}
div[aria-selected="true"][data-baseweb="tab"],div[aria-selected="true"][data-baseweb="tab"] *,button[aria-selected="true"],button[aria-selected="true"] p,button[aria-selected="true"] span{{background:{T['tab_sel']} !important;color:{T['text']} !important;font-weight:700 !important;box-shadow:0 2px 8px rgba(74,144,226,.15) !important;}}
div[data-testid="stChatInput"]>div{{background:{T['input_bg']} !important;border:1.5px solid rgba(59,130,246,.35) !important;border-radius:14px !important;box-shadow:0 3px 14px rgba(59,130,246,.12) !important;}}
div[data-testid="stChatInput"] textarea{{color:{T['text']} !important;font-size:14px !important;}}
div[data-testid="stChatInput"] textarea::placeholder{{color:{T['text3']} !important;}}
div[data-testid="stExpander"]{{background:{T['exp_bg']} !important;backdrop-filter:blur(18px) !important;border:1.5px solid rgba(59,130,246,.2) !important;border-radius:16px !important;overflow:hidden;box-shadow:0 4px 20px {T['shadow']} !important;}}
div[data-testid="stExpander"] details summary{{background:{T['exp_sum']} !important;padding:14px 18px !important;border-radius:14px !important;}}
div[data-testid="stExpander"] details[open] summary{{border-radius:14px 14px 0 0 !important;border-bottom:1px solid {T['border']} !important;}}
div[data-testid="stExpander"] summary p,div[data-testid="stExpander"] summary span,div[data-testid="stExpander"] summary{{color:{T['text']} !important;font-weight:700 !important;font-size:14px !important;background:transparent !important;}}
div[data-testid="stExpander"] details > div{{background:{T['exp_bg']} !important;padding:16px 18px !important;}}
div[data-testid="stExpander"] .stButton>button{{background:linear-gradient(135deg,#3b82f6 0%,#14b8a6 100%) !important;color:#ffffff !important;border:none !important;border-radius:12px !important;font-size:15px !important;font-weight:700 !important;padding:14px 20px !important;width:100% !important;box-shadow:0 4px 18px rgba(59,130,246,.35) !important;transition:opacity .2s ease,transform .15s ease !important;}}
div[data-testid="stExpander"] .stButton>button:hover{{opacity:.92 !important;transform:translateY(-2px) !important;}}
div[data-testid="stExpander"] .stButton:nth-of-type(2)>button{{background:{T['card']} !important;color:{T['text']} !important;border:1.5px solid rgba(59,130,246,.28) !important;box-shadow:0 2px 8px {T['shadow']} !important;font-weight:500 !important;font-size:13.5px !important;}}
div[data-testid="stRadio"] label,div[data-testid="stRadio"] label *,div[data-testid="stRadio"] label p,div[data-testid="stRadio"] label span{{background:{T['card']} !important;border:1px solid {T['border']} !important;border-radius:8px !important;padding:6px 13px !important;font-size:13px !important;font-weight:500 !important;color:{T['text']} !important;}}
div[data-testid="stRadio"] label:hover,div[data-testid="stRadio"] label:hover *{{background:rgba(59,130,246,.15) !important;color:{T['text']} !important;}}
.stSpinner>div{{border-top-color:#3b82f6 !important;}}
.stAlert{{border-radius:11px !important;}}
::-webkit-scrollbar{{width:5px;height:5px;}}
::-webkit-scrollbar-track{{background:transparent;}}
::-webkit-scrollbar-thumb{{background:rgba(59,130,246,.3);border-radius:99px;}}
button[kind="secondaryFormSubmit"],button[kind="formSubmit"]{{background:linear-gradient(135deg,#3b82f6,#14b8a6) !important;color:white !important;border-radius:10px !important;border:none !important;font-weight:600 !important;}}
@media(max-width:768px){{.block-container{{padding:.8rem 1rem 2rem !important;}}.upload-grid{{grid-template-columns:1fr !important;}}.feature-grid{{grid-template-columns:1fr !important;}}.counts-bar{{gap:8px;}}.count-chip{{padding:8px 12px;}}.metric-card{{min-height:auto;}}.hist-row{{flex-direction:column;align-items:flex-start;gap:6px;}}.hist-time{{min-width:unset;}}.cbubble-user{{margin-left:5%;}}.cbubble-ai{{margin-right:2%;}}.big-bubble-user{{margin-left:2%;}}.big-bubble-ai{{margin-right:2%;}}.ptable{{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;}}section[data-testid="stSidebar"]{{min-width:200px !important;max-width:220px !important;}}}}
</style>
""", unsafe_allow_html=True)
