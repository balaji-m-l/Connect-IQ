import streamlit as st

from components.styles import inject_styles, logo
from components.nav import render_app_nav
from utils.auth import is_authenticated

st.set_page_config(
    page_title="Connect-IQ – About",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles(hide_sidebar=True)

# ── Page-level CSS ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp { background: #FFFFFF !important; }
    .main, .block-container { background: transparent !important; padding-top: 0 !important; }
    [data-testid="column"], [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > div { background: transparent !important; }

    /* About hero band */
    .about-hero {
      padding: 64px 60px 80px;
      background: var(--cf-bg-soft);
      text-align: center;
    }
    .about-hero .inner { max-width: 720px; margin: 0 auto; }
    .about-hero h1 {
      font-size: 44px; font-weight: 800; line-height: 1.05;
      letter-spacing: -1.5px; color: var(--cf-text);
      margin: 16px 0 16px;
    }
    .about-hero h1 .accent { color: var(--cf-red); }
    .about-hero p {
      font-size: 17px; color: var(--cf-text-muted);
      line-height: 1.65; max-width: 580px; margin: 0 auto;
    }

    /* Capabilities card — overlaps hero */
    .stats-wrap { margin-top: -36px; margin-bottom: 48px; }
    .stats-card {
      background: #fff; border: 1px solid var(--cf-border);
      border-radius: 16px; padding: 28px 36px;
      display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;
      box-shadow: var(--shadow-md);
    }
    .stat-cell { text-align: center; }
    .stat-value {
      font-size: 2rem; margin-bottom: 12px;
    }
    .stat-label {
      font-size: 1.05rem; font-weight: 700; color: var(--cf-red);
      letter-spacing: -.2px; margin-bottom: 6px;
    }
    .stat-desc { font-size: .83rem; color: var(--cf-text-muted); line-height: 1.5; margin-top: 4px; }

    /* Tech stack */
    .tech-wrap { padding: 12px 0 56px; }
    .tech-title { text-align: center; margin-bottom: 32px; }
    .tech-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
    .tech-card {
      background: #fff; border: 1px solid var(--cf-border);
      border-radius: 16px; text-align: center; padding: 28px 16px;
      transition: box-shadow .18s, transform .18s;
    }
    .tech-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
    .tech-icon { font-size: 2rem; margin-bottom: 12px; }
    .tech-name { font-size: 1.05rem; font-weight: 700; color: var(--cf-text); }
    .tech-role { font-size: .83rem; color: var(--cf-text-muted); margin-top: 4px; }

    /* FAQ section */
    .faq-head { text-align: center; padding: 48px 0 32px; background: var(--cf-bg-soft);
                border-radius: 20px 20px 0 0; }

    /* Custom accordion */
    .cf-faq-wrap { max-width: 760px; margin: 0 auto; }
    .cf-faq-item {
      background: #fff; border: 1px solid var(--cf-border);
      border-radius: 14px; margin-bottom: 8px; overflow: hidden;
    }
    .cf-faq-q {
      display: flex; align-items: center; justify-content: space-between;
      padding: 20px 24px; cursor: pointer;
      font-size: 15.5px; font-weight: 600; color: var(--cf-text);
    }
    .cf-faq-icon {
      flex-shrink: 0; width: 22px; height: 22px; font-size: 20px;
      line-height: 1; color: #717171; transition: transform .2s;
    }
    .cf-faq-icon.open { transform: rotate(45deg); color: #FF385C; }
    .cf-faq-a {
      padding: 0 24px 18px; font-size: 14.5px;
      color: var(--cf-text-muted); line-height: 1.65;
    }
    /* Streamlit button reset inside FAQ rows */
    .cf-faq-btn button {
      background: transparent !important; border: none !important;
      box-shadow: none !important; padding: 0 !important;
      width: 100% !important; text-align: left !important;
      min-height: 0 !important;
    }
    /* Prevent white text on click for all FAQ toggle buttons */
    div[class*="st-key-faq_toggle_"] button,
    div[class*="st-key-faq_toggle_"] button:active,
    div[class*="st-key-faq_toggle_"] button:focus,
    div[class*="st-key-faq_toggle_"] button:focus-visible,
    div[class*="st-key-faq_toggle_"] button p,
    div[class*="st-key-faq_toggle_"] button:active p,
    div[class*="st-key-faq_toggle_"] button:focus p,
    div[class*="st-key-faq_toggle_"] button:focus-visible p {
      color: #222222 !important;
      background: transparent !important;
      box-shadow: none !important;
      outline: none !important;
      transition: color 0s !important;
    }

    /* Footer */
    .cf-footer {
      padding: 32px 0; margin-top: 48px;
      border-top: 1px solid var(--cf-border);
      display: flex; align-items: center; justify-content: space-between;
    }
    .cf-footer-links { display: flex; gap: 24px; }
    .cf-footer-links span { font-size: 13px; color: var(--cf-text-muted); cursor: pointer; }
    .cf-footer-copy { font-size: 13px; color: var(--cf-text-faint); }

    /* Marketing nav row (unauthenticated) */
    div[data-testid="stHorizontalBlock"]:first-of-type {
        gap: 4px !important; align-items: center !important;
        padding: 14px 0 !important; background: #FFFFFF !important;
        border-bottom: 1px solid #EBEBEB !important; margin-bottom: 0 !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(3) .stButton > button,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(4) .stButton > button,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(5) .stButton > button,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(6) .stButton > button {
        background: transparent !important; color: #484848 !important;
        border: none !important; font-weight: 500 !important;
        font-size: 14px !important; padding: 8px 14px !important;
        box-shadow: none !important; white-space: nowrap !important; width: auto !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(3) .stButton > button:hover,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(4) .stButton > button:hover,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(5) .stButton > button:hover,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(6) .stButton > button:hover {
        background: #F7F7F7 !important; color: #222222 !important;
        transform: none !important; box-shadow: none !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(8) .stButton > button {
        border: 1.5px solid #DDDDDD !important; color: #222222 !important;
        background: transparent !important; font-weight: 600 !important;
        font-size: 15px !important; padding: 10px 20px !important; white-space: nowrap !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(8) .stButton > button:hover {
        background: #F7F7F7 !important; transform: none !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(9) .stButton > button {
        background: #FF385C !important; color: #FFFFFF !important;
        font-weight: 600 !important; border: none !important;
        font-size: 15px !important; padding: 10px 22px !important; white-space: nowrap !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(9) .stButton > button:hover {
        background: #E31C5F !important; transform: translateY(-1px) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Nav ────────────────────────────────────────────────────────────────────────
if is_authenticated():
    render_app_nav(active="about")
else:
    logo_c, lf_c, feat_c, hiw_c, about_c, faq_c, rf_c, login_c, signup_c = st.columns(
        [2.2, 1.6, 1.2, 1.6, 1.0, 0.8, 1.6, 1.1, 1.4]
    )
    with logo_c:
        st.markdown(
            '<a href="/" target="_self" style="text-decoration:none;color:inherit;">'
            '<p style="font-size:18px;font-weight:800;color:#FF385C;margin:0;'
            'padding:0;font-family:Inter,sans-serif;white-space:nowrap;line-height:1;">🔗 Connect-IQ</p>'
            '</a>',
            unsafe_allow_html=True,
        )
    with feat_c:
        if st.button("Features", key="nav_feat"):
            st.session_state["_scroll_to"] = "cf-features"
            st.switch_page("app.py")
    with hiw_c:
        if st.button("How it works", key="nav_hiw"):
            st.session_state["_scroll_to"] = "cf-how-it-works"
            st.switch_page("app.py")
    with about_c:
        st.button("About", key="nav_about")
    with faq_c:
        if st.button("FAQ", key="nav_faq"):
            st.session_state["_about_scroll"] = "cf-faq"
            st.rerun()
    with login_c:
        if st.button("Log in", key="nav_login", type="secondary"):
            st.session_state["_show_signup"] = False
            st.switch_page("pages/1_Login.py")
    with signup_c:
        if st.button("Sign up free", key="nav_signup", type="primary"):
            st.session_state["_show_signup"] = True
            st.switch_page("pages/1_Login.py")

# ── Content data ───────────────────────────────────────────────────────────────
STATS = [
    ("🔎", "Plain-English search",    "Ask questions the way you'd talk — no filters or queries to learn"),
    ("🎯", "Grounded answers",         "Every reply is drawn from your real connections, no made-up results"),
    ("📊", "Instant visualizations",   "See your network by company, role, and growth over time at a glance"),
    ("🔒", "Private by design",        "Your data stays in your own database and never trains any model"),
]

TECH = [
    ("🎈", "Streamlit",        "Frontend"),
    ("⚡", "Supabase",         "Database + Auth"),
    ("🧠", "Gemini 2.5 Flash", "LLM"),
    ("🔍", "pgvector",         "Vector search"),
]

FAQS = [
    (
        "What file types does Connect-IQ support?",
        "We support **.csv**, **.xlsx**, and **.xls** files up to 50 MB. "
        "The LinkedIn connections export is a CSV file by default — just upload it directly.",
    ),
    (
        "Is my data private?",
        "Yes. Your data is stored in your own Supabase project with Row Level Security (RLS) enabled. "
        "Only you can access your connections, and we never use your data to train models.",
    ),
    (
        "How does the AI understand my network?",
        "Connect-IQ uses a RAG (Retrieval-Augmented Generation) system. We generate embeddings for each "
        "connection using **gemini-embedding-001**, store them in pgvector, then retrieve the most relevant "
        "connections for each question. Gemini 2.5 Flash then crafts a grounded answer — no hallucinations.",
    ),
    (
        "How do I export my LinkedIn connections?",
        "Go to **LinkedIn → Settings & Privacy → Data Privacy → Download my data → "
        "Download larger data archive → Request archive** → upload the **Connections.csv** file here.",
    ),
    (
        "Can I upload multiple files over time?",
        "Yes! Uploads are **additive**. When you upload a new file, Connect-IQ appends only the new "
        "connections and automatically skips duplicates.",
    ),
    (
        "Is there a free plan?",
        "Yes — Connect-IQ is free to get started. No credit card required.",
    ),
]

# ── Hero + Stats (combined so the overlap CSS works) ───────────────────────────
st.markdown('<div id="cf-about-top"></div>', unsafe_allow_html=True)

stat_cells = "".join(
    f'<div class="stat-cell">'
    f'<div class="stat-value">{icon}</div>'
    f'<div class="stat-label">{title}</div>'
    f'<div class="stat-desc">{desc}</div>'
    f'</div>'
    for icon, title, desc in STATS
)
st.markdown(
    f"""
    <div class="about-hero">
      <div class="inner">
        <span style="display:inline-block;background:#FFE8EE;color:#FF385C;
          font-size:.78rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
          border-radius:20px;padding:5px 14px;margin-bottom:18px;">About Connect-IQ</span>
        <h1>We make your <span class="accent">network</span> conversational</h1>
        <p>
          Connect-IQ was built for everyone who's ever scrolled through their LinkedIn
          connections wishing they could just <em>ask</em>. We combine RAG AI with
          beautiful visualizations so anyone can find the right person, fast.
        </p>
      </div>
    </div>
    <div class="stats-wrap">
      <div class="stats-card">{stat_cells}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Tech stack ─────────────────────────────────────────────────────────────────
tech_cells = "".join(
    f'<div class="tech-card">'
    f'<div class="tech-icon">{icon}</div>'
    f'<div class="tech-name">{name}</div>'
    f'<div class="tech-role">{role}</div>'
    f'</div>'
    for icon, name, role in TECH
)
st.markdown(
    f"""
    <div class="tech-wrap">
      <div class="tech-title">
        <h2 style="font-size:2rem;font-weight:800;color:var(--cf-text);margin:0;">
          Built on best-in-class technology
        </h2>
      </div>
      <div class="tech-grid">{tech_cells}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── FAQ ────────────────────────────────────────────────────────────────────────
st.markdown('<div id="cf-faq"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="faq-head">
      <span style="display:inline-block;background:#FFE8EE;color:#FF385C;
        font-size:.78rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
        border-radius:20px;padding:5px 14px;margin-bottom:14px;">FAQ</span>
      <h2 style="font-size:2rem;font-weight:800;color:var(--cf-text);margin:12px 0 0;">
        Frequently asked questions
      </h2>
    </div>
    """,
    unsafe_allow_html=True,
)

if "faq_open_idx" not in st.session_state:
    st.session_state["faq_open_idx"] = 0

# Inject per-item active styles
faq_btn_css = "<style>"
for _i in range(len(FAQS)):
    _color = "#222222"
    faq_btn_css += f"""
    div[class*="st-key-faq_toggle_{_i}"] button,
    div[class*="st-key-faq_toggle_{_i}"] button:active,
    div[class*="st-key-faq_toggle_{_i}"] button:focus,
    div[class*="st-key-faq_toggle_{_i}"] button:focus-visible {{
        background: transparent !important; border: none !important;
        box-shadow: none !important; width: 100% !important;
        padding: 20px 24px !important; text-align: left !important;
        min-height: 0 !important; border-radius: 0 !important;
        font-size: 15.5px !important; font-weight: 600 !important;
        color: {_color} !important;
        justify-content: space-between !important; display: flex !important;
        outline: none !important; transition: color 0s !important;
    }}
    div[class*="st-key-faq_toggle_{_i}"] button p,
    div[class*="st-key-faq_toggle_{_i}"] button:active p,
    div[class*="st-key-faq_toggle_{_i}"] button:focus p,
    div[class*="st-key-faq_toggle_{_i}"] button:focus-visible p {{
        color: {_color} !important;
        transition: color 0s !important;
    }}
    div[class*="st-key-faq_toggle_{_i}"] button:hover,
    div[class*="st-key-faq_toggle_{_i}"] button:hover p {{
        color: #FF385C !important; background: #FFF8F9 !important;
        transform: none !important;
    }}
    """
faq_btn_css += "</style>"
st.markdown(faq_btn_css, unsafe_allow_html=True)

_, faq_col, _ = st.columns([1, 3, 1])
with faq_col:
    for i, (question, answer) in enumerate(FAQS):
        is_open = st.session_state["faq_open_idx"] == i
        icon = "×" if is_open else "+"

        # Card wrapper open
        st.markdown(
            f'<div class="cf-faq-item" style="border-color:{"#FF385C" if is_open else "var(--cf-border)"};">',
            unsafe_allow_html=True,
        )
        # Clickable row button
        if st.button(f"{question}  {icon}", key=f"faq_toggle_{i}"):
            st.session_state["faq_open_idx"] = i if not is_open else -1
            st.rerun()
        # Answer (visible when open)
        if is_open:
            st.markdown(
                f'<div class="cf-faq-a">{answer}</div>',
                unsafe_allow_html=True,
            )
        # Card wrapper close
        st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="cf-footer">
      {logo()}
      <div class="cf-footer-links">
        <span>Privacy</span>
        <span>Terms</span>
        <span>Contact</span>
        <span>GitHub</span>
      </div>
      <span class="cf-footer-copy">© 2026 Connect-IQ</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Anchor scroll ──────────────────────────────────────────────────────────────
if st.session_state.get("_about_scroll"):
    target = st.session_state.pop("_about_scroll")
    st.iframe(
        f'<script>window.parent.document.getElementById("{target}")'
        f'.scrollIntoView({{behavior:"smooth",block:"start"}});</script>',
        height=1,
    )