import streamlit as st

from components.styles import inject_styles, logo
from components.nav import render_nav
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

    /* Stats card — overlaps hero */
    .stats-wrap { margin-top: -36px; margin-bottom: 48px; }
    .stats-card {
      background: #fff; border: 1px solid var(--cf-border);
      border-radius: 16px; padding: 28px 36px;
      display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;
      box-shadow: var(--shadow-md);
    }
    .stat-cell { text-align: center; }
    .stat-value {
      font-size: 32px; font-weight: 800;
      color: var(--cf-red); letter-spacing: -0.5px;
    }
    .stat-label { font-size: 13px; color: var(--cf-text-muted); margin-top: 4px; }

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
    .tech-icon { font-size: 26px; margin-bottom: 8px; }
    .tech-name { font-size: 15px; font-weight: 700; color: var(--cf-text); }
    .tech-role { font-size: 13px; color: var(--cf-text-muted); margin-top: 2px; }

    /* FAQ section */
    .faq-head { text-align: center; padding: 48px 0 32px; background: var(--cf-bg-soft);
                border-radius: 20px 20px 0 0; }
    [data-testid="stExpander"] {
      background: #fff !important;
      border: 1px solid var(--cf-border) !important;
      border-radius: 16px !important;
      margin-bottom: 10px !important;
      box-shadow: none !important;
    }
    [data-testid="stExpander"] summary {
      padding: 20px 24px !important;
      font-size: 16px !important; font-weight: 600 !important;
      color: var(--cf-text) !important;
    }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
      padding: 4px 24px 20px !important;
      font-size: 14.5px !important; color: var(--cf-text-muted) !important;
      line-height: 1.65 !important;
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
    render_nav(active="about")
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
            st.switch_page("pages/1_Login.py")
    with signup_c:
        if st.button("Sign up free", key="nav_signup", type="primary"):
            st.switch_page("pages/1_Login.py")

# ── Content data ───────────────────────────────────────────────────────────────
STATS = [
    ("2,000+", "Active users"),
    ("1.2M",   "Connections analyzed"),
    ("99.9%",  "Uptime"),
    ("<2s",    "Average query time"),
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
        "Go to **LinkedIn → Settings & Privacy → Data Privacy → Get a copy of your data → "
        "select Connections → Request archive**. You'll get an email with a download link, "
        "and the ZIP contains `Connections.csv` ready to upload.",
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
    f'<div class="stat-value">{v}</div>'
    f'<div class="stat-label">{l}</div>'
    f'</div>'
    for v, l in STATS
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

_, faq_col, _ = st.columns([1, 3, 1])
with faq_col:
    for i, (question, answer) in enumerate(FAQS):
        with st.expander(question, expanded=(i == 0)):
            st.markdown(answer)

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
    import streamlit.components.v1 as components
    target = st.session_state.pop("_about_scroll")
    components.html(
        f'<script>window.parent.document.getElementById("{target}")'
        f'.scrollIntoView({{behavior:"smooth",block:"start"}});</script>',
        height=0,
    )