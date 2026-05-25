import streamlit as st

from components.styles import inject_styles
from components.nav import render_nav
from utils.auth import is_authenticated

st.set_page_config(
    page_title="Connect-IQ – About",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles(hide_sidebar=True)

# ── Page-level overrides ───────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp { background: #F7F8FA !important; }
    .main, .block-container { background: transparent !important; padding-top: 0 !important; }
    [data-testid="column"], [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > div { background: transparent !important; }
    /* FAQ expander styling */
    [data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
    }
    [data-testid="stExpander"] summary {
        font-weight: 600 !important;
        color: #111113 !important;
        font-size: .95rem !important;
    }
    /* Marketing nav row */
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
            '<p style="font-size:18px;font-weight:800;color:#FF385C;margin:0;'
            'padding:0;font-family:Inter,sans-serif;white-space:nowrap;line-height:1;">🔗 Connect-IQ</p>',
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

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<div id="cf-about-top"></div>', unsafe_allow_html=True)
_, hero_col, _ = st.columns([1, 3, 1])
with hero_col:
    st.markdown(
        '<div style="text-align:center;padding:48px 0 36px;">'
        '<h1 style="font-size:2.6rem;font-weight:800;color:#111113;line-height:1.2;'
        'margin:0 0 18px;font-family:Inter,sans-serif;">'
        'We make your <span style="color:#FF385C;">network</span> conversational'
        '</h1>'
        '<p style="color:#6B7280;font-size:1rem;line-height:1.75;margin:0 auto;'
        'max-width:520px;font-family:Inter,sans-serif;">'
        'Connect-IQ is built for everyone who\'s ever scrolled through their LinkedIn '
        'connections wishing they could see all. We combine RAG AI with beautiful '
        'visualizations so anyone can find the right person, fast.'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Stats strip ───────────────────────────────────────────────────────────────
s1, s2, s3, s4 = st.columns(4, gap="medium")

_STAT = (
    '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:14px;'
    'padding:24px 20px;text-align:center;">'
    '<p style="font-size:1.8rem;font-weight:800;color:#111113;margin:0 0 4px;'
    'font-family:Inter,sans-serif;">{value}</p>'
    '<p style="font-size:.83rem;color:#9CA3AF;margin:0;font-family:Inter,sans-serif;">{label}</p>'
    '</div>'
)

with s1:
    st.markdown(_STAT.format(value="2,000+", label="Active users"), unsafe_allow_html=True)
with s2:
    st.markdown(_STAT.format(value="1.2M", label="Connections analyzed"), unsafe_allow_html=True)
with s3:
    st.markdown(_STAT.format(value="99.9%", label="Uptime"), unsafe_allow_html=True)
with s4:
    st.markdown(_STAT.format(value="&lt;2s", label="Average response"), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── Built on best-in-class technology ────────────────────────────────────────
st.markdown(
    '<h2 style="text-align:center;font-size:1.6rem;font-weight:800;color:#111113;'
    'margin:0 0 28px;font-family:Inter,sans-serif;">Built on best-in-class technology</h2>',
    unsafe_allow_html=True,
)

_TECH = (
    '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:14px;'
    'padding:26px 20px;text-align:center;height:100%;">'
    '<div style="font-size:2rem;margin-bottom:10px;">{icon}</div>'
    '<p style="font-size:1rem;font-weight:700;color:#111113;margin:0 0 4px;'
    'font-family:Inter,sans-serif;">{name}</p>'
    '<p style="font-size:.82rem;color:#9CA3AF;margin:0;font-family:Inter,sans-serif;">{sub}</p>'
    '</div>'
)

tc1, tc2, tc3, tc4 = st.columns(4, gap="medium")
with tc1:
    st.markdown(_TECH.format(icon="🎈", name="Streamlit", sub="Frontend"), unsafe_allow_html=True)
with tc2:
    st.markdown(_TECH.format(icon="⚡", name="Supabase", sub="Database + Auth"), unsafe_allow_html=True)
with tc3:
    st.markdown(_TECH.format(icon="🧠", name="Gemini 2.5 Flash", sub="LLM"), unsafe_allow_html=True)
with tc4:
    st.markdown(_TECH.format(icon="🔍", name="pgvector", sub="Vector search"), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── FAQ ───────────────────────────────────────────────────────────────────────
st.markdown('<div id="cf-faq"></div>', unsafe_allow_html=True)
_, faq_col, _ = st.columns([0.5, 4, 0.5])
with faq_col:
    st.markdown(
        '<div style="text-align:center;margin-bottom:32px;">'
        '<span style="display:inline-block;background:#FFE8EE;color:#FF385C;'
        'font-size:.78rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;'
        'border-radius:20px;padding:5px 14px;margin-bottom:14px;">FAQ</span>'
        '<h2 style="font-size:2rem;font-weight:800;color:#111113;margin:0;'
        'font-family:Inter,sans-serif;">Frequently asked questions</h2>'
        '</div>',
        unsafe_allow_html=True,
    )

    FAQ = [
        (
            "What file types does Connect-IQ support?",
            "We support **.csv**, **.xlsx**, and **.xls** files up to 10 MB. "
            "The LinkedIn connections export is a CSV file by default — just download it from your Privacy settings.",
        ),
        (
            "Is my data private?",
            "Yes. Your connections are stored in **your own** Supabase project with Row Level Security (RLS) enabled. "
            "Only your authenticated account can read your data — not other users, not us.",
        ),
        (
            "How does the AI understand my network?",
            "Each connection is converted into a 768-dimensional vector embedding using **gemini-embedding-001**. "
            "When you ask a question, the query is embedded and matched against your connections using cosine "
            "similarity, then Gemini 2.5 Flash generates a grounded answer from the retrieved results.",
        ),
        (
            "How do I export my LinkedIn connections?",
            "Go to **LinkedIn → Me → Settings & Privacy → Data Privacy → Get a copy of your data**, "
            "select **Connections**, then request the archive. You'll receive an email with a ZIP containing `Connections.csv`.",
        ),
        (
            "Can I upload multiple files over time?",
            "Yes — uploads are **additive**. Each new file is checked against existing records and only "
            "truly new connections (matched on first name + last name + company) are inserted. "
            "Duplicates are skipped automatically.",
        ),
        (
            "Is there a free plan?",
            "The app itself is open source and free. You'll need a **Supabase** account (free tier works) "
            "and a **Google AI Studio** API key (free tier: 15 req/min).",
        ),
    ]

    for question, answer in FAQ:
        with st.expander(question):
            st.markdown(answer)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<hr style="margin:0 0 12px;">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#AAAAAA;font-size:.82rem;padding:0 0 10px;">'
    "© 2025 Connect-IQ · MIT License"
    "</p>",
    unsafe_allow_html=True,
)

# ── Anchor scroll ─────────────────────────────────────────────────────────────
if st.session_state.get("_about_scroll"):
    import streamlit.components.v1 as components
    target = st.session_state.pop("_about_scroll")
    components.html(
        f'<script>window.parent.document.getElementById("{target}")'
        f'.scrollIntoView({{behavior:"smooth",block:"start"}});</script>',
        height=0,
    )