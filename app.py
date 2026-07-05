import streamlit as st
from components.styles import inject_styles

st.set_page_config(
    page_title="Connect-IQ – Visualize Your LinkedIn Network",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles(hide_sidebar=True)

# ── Landing-specific overrides ────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp { background: #FFFFFF !important; }
    .main, .block-container {
        background: transparent !important;
        padding-top: 1rem !important;
    }
    [data-testid="column"], [data-testid="stHorizontalBlock"] > div {
        background: transparent !important;
    }
    [data-testid="baseButton-primary"] {
        background: #FF385C !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: none !important;
    }
    hr { border-color: #EBEBEB !important; }
    /* Nav row: compact gaps, vertically centered */
    div[data-testid="stHorizontalBlock"]:first-of-type {
        gap: 4px !important;
        align-items: center !important;
        padding: 4px 0 10px !important;
    }
    /* Nav link buttons (columns 3-6) — ghost style */
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(3) .stButton > button,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(4) .stButton > button,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(5) .stButton > button,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(6) .stButton > button {
        background: transparent !important;
        color: #484848 !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 8px 14px !important;
        box-shadow: none !important;
        white-space: nowrap !important;
        width: auto !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(3) .stButton > button:hover,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(4) .stButton > button:hover,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(5) .stButton > button:hover,
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(6) .stButton > button:hover {
        background: #F7F7F7 !important;
        color: #222222 !important;
        transform: none !important;
        box-shadow: none !important;
    }
    /* Log in button — 8th column */
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(8) .stButton > button {
        border: 1.5px solid #DDDDDD !important;
        color: #222222 !important;
        background: transparent !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 10px 20px !important;
        white-space: nowrap !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(8) .stButton > button:hover {
        background: #F7F7F7 !important;
        transform: none !important;
    }
    /* Sign up free button — 9th column */
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(9) .stButton > button {
        background: #FF385C !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        font-size: 15px !important;
        padding: 10px 22px !important;
        white-space: nowrap !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child(9) .stButton > button:hover {
        background: #E31C5F !important;
        transform: translateY(-1px) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Redirect email verification callbacks to the login page
st.markdown("""
<script>
(function() {
  var h = window.location.hash;
  if (h && h.indexOf('type=signup') !== -1) {
    window.location.replace('/Login?verified=1');
  }
})();
</script>
""", unsafe_allow_html=True)

if st.session_state.get("user"):
    st.switch_page("pages/2_Home.py")

# ── Top nav ───────────────────────────────────────────────────────────────────
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

with hiw_c:
    if st.button("How it works", key="nav_hiw"):
        st.session_state["_scroll_to"] = "cf-how-it-works"

with about_c:
    if st.button("About", key="nav_about"):
        st.session_state["_about_scroll"] = "cf-about-top"
        st.switch_page("pages/4_About.py")

with faq_c:
    if st.button("FAQ", key="nav_faq"):
        st.session_state["_about_scroll"] = "cf-faq"
        st.switch_page("pages/4_About.py")

with login_c:
    if st.button("Log in", key="nav_login", type="secondary"):
        st.session_state["_show_signup"] = False
        st.switch_page("pages/1_Login.py")

with signup_c:
    if st.button("Sign up free", key="nav_signup", type="primary"):
        st.session_state["_show_signup"] = True
        st.switch_page("pages/1_Login.py")

# ── Dark hero card (self-contained HTML) ──────────────────────────────────────
st.markdown(
    """
    <div style="
        background: radial-gradient(ellipse 90% 55% at 50% -10%,
            rgba(200, 22, 58, 0.60) 0%, transparent 65%),
        #111113;
        border-radius: 24px;
        padding: 80px 60px 64px;
        text-align: center;
        margin: 14px 0 0;
    ">
        <!-- Badge -->
        <div style="display:inline-flex;align-items:center;gap:8px;
                    background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.16);
                    border-radius:20px;padding:6px 16px;margin-bottom:30px;">
            <span style="width:7px;height:7px;background:#FF385C;border-radius:50%;
                         display:inline-block;flex-shrink:0;"></span>
            <span style="color:rgba(255,255,255,.82);font-size:.77rem;font-weight:600;
                         letter-spacing:.09em;text-transform:uppercase;">
                RAG-Powered · No Hallucinations
            </span>
        </div>
        <!-- Headline -->
        <h1 style="color:#FFFFFF;font-size:4rem;font-weight:800;line-height:1.1;
                   margin:0 auto 22px;max-width:760px;font-family:Inter,sans-serif;">
            Understand your<br>
            <span style="color:#FF385C;">LinkedIn network</span> like<br>
            never before
        </h1>
        <!-- Subtitle -->
        <p style="color:rgba(255,255,255,.58);font-size:1.05rem;line-height:1.78;
                  max-width:530px;margin:0 auto 36px;font-family:Inter,sans-serif;">
            Upload your LinkedIn connections export and instantly discover
            who's in your network, where they work, and what roles they hold —
            powered by AI.
        </p>
        <!-- CTA buttons -->
        <div style="display:flex;justify-content:center;gap:12px;margin-bottom:18px;">
            <a href="/Login?signup=1" target="_self"
               style="display:inline-flex;align-items:center;justify-content:center;
                      background:#FF385C;color:#FFFFFF;font-weight:700;font-size:15px;
                      border-radius:8px;padding:12px 28px;text-decoration:none;
                      font-family:Inter,sans-serif;white-space:nowrap;
                      transition:background .18s ease;">
                Get started free &rarr;
            </a>
        </div>
        <!-- Caption -->
        <p style="color:rgba(255,255,255,.30);font-size:.82rem;margin:0;
                  font-family:Inter,sans-serif;">
            Free to get started &middot; No credit card required
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr style="margin:40px 0 60px;">', unsafe_allow_html=True)

# ── Built on best-in-class technology ────────────────────────────────────────
st.markdown(
    '<h2 style="text-align:center;font-size:2rem;font-weight:800;color:#222222;'
    'margin:0 0 32px;font-family:Inter,sans-serif;">Built on best-in-class technology</h2>',
    unsafe_allow_html=True,
)

_TECH = (
    '<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:14px;'
    'padding:28px 22px;text-align:center;height:100%;">'
    '<div style="font-size:2rem;margin-bottom:12px;">{icon}</div>'
    '<p style="font-size:1.05rem;font-weight:700;color:#111113;margin:0 0 4px;'
    'font-family:Inter,sans-serif;">{name}</p>'
    '<p style="font-size:.83rem;color:#9CA3AF;margin:0;font-family:Inter,sans-serif;">{sub}</p>'
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

# ── Features section (white bg, light cards) ──────────────────────────────────
st.markdown('<div id="cf-features"></div>', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;margin-bottom:44px;">'
    '<span style="display:inline-block;background:#FFE8EE;color:#FF385C;'
    'font-size:.8rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;'
    'border-radius:20px;padding:5px 14px;margin-bottom:20px;">Features</span>'
    '<h2 style="font-size:2rem;font-weight:800;color:#222222;margin:0 0 8px;">'
    "Everything you need to know your network</h2>"
    '<p style="color:#717171;font-size:1rem;margin:0;">'
    "Powerful visualizations and AI insights — in one place.</p>"
    "</div>",
    unsafe_allow_html=True,
)

fc1, fc2, fc3 = st.columns(3, gap="medium")

def _feature_card(icon, title, desc, tags):
    tag_html = "".join(
        f'<span style="background:#EFEFEF;border-radius:20px;padding:4px 12px;'
        f'font-size:.78rem;font-weight:500;color:#484848;">{t}</span>'
        for t in tags
    )
    return (
        f'<div style="background:#F3F4F6;border-radius:16px;padding:28px 24px;height:100%;'
        f'border:1px solid #E5E7EB;">'
        f'<div style="font-size:2.2rem;margin-bottom:16px;">{icon}</div>'
        f'<p style="font-size:1rem;font-weight:700;color:#111113;margin:0 0 10px;font-family:Inter,sans-serif;">{title}</p>'
        f'<p style="color:#6B7280;font-size:.88rem;line-height:1.65;margin:0 0 18px;">{desc}</p>'
        f'<div style="display:flex;flex-wrap:wrap;gap:6px;">{tag_html}</div>'
        f"</div>"
    )

with fc1:
    st.markdown(
        _feature_card(
            "📊", "Visual Network Map",
            "Interactive charts show your connections by company, job title, and time — giving you an instant picture of your network.",
            ["Bar charts", "Timeline", "Donut"],
        ),
        unsafe_allow_html=True,
    )
with fc2:
    st.markdown(
        _feature_card(
            "🤖", "RAG-Powered AI Chat",
            'Ask questions like "List all recruiters in Finance" or "Who do I know at FAANG companies?" — grounded answers, zero hallucinations.',
            ["Natural language", "Grounded", "Fast"],
        ),
        unsafe_allow_html=True,
    )
with fc3:
    st.markdown(
        _feature_card(
            "🔒", "Private & Secure",
            "Your data is stored securely in your own Supabase project with row-level security. Only you can access your connections.",
            ["RLS", "Encrypted", "Yours"],
        ),
        unsafe_allow_html=True,
    )

st.markdown("<br><br>", unsafe_allow_html=True)

# ── How it works — light gray section, white cards, left-aligned ──────────────
st.markdown('<div id="cf-how-it-works"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="background:#F7F8FA;border-radius:20px;padding:64px 48px;margin:0 0 0;">
        <!-- Header -->
        <div style="text-align:center;margin-bottom:44px;">
            <span style="display:inline-block;background:#FFE8EE;color:#FF385C;
                         font-size:.8rem;font-weight:700;letter-spacing:.06em;
                         text-transform:uppercase;border-radius:20px;padding:5px 14px;
                         margin-bottom:18px;">How it works</span>
            <h2 style="font-size:2rem;font-weight:800;color:#222222;margin:0;
                       font-family:Inter,sans-serif;">
                From export to insights in 3 steps
            </h2>
        </div>
        <!-- Cards grid -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;">
            <div style="background:#FFFFFF;border-radius:14px;padding:28px 24px;
                        border:1px solid #E5E7EB;box-shadow:0 2px 8px rgba(0,0,0,.04);">
                <div style="width:42px;height:42px;background:#FF385C;border-radius:50%;
                             display:flex;align-items:center;justify-content:center;
                             margin-bottom:18px;">
                    <span style="color:#FFFFFF;font-weight:800;font-size:1.05rem;
                                 font-family:Inter,sans-serif;">1</span>
                </div>
                <h3 style="font-size:1rem;font-weight:700;color:#111113;margin:0 0 10px;
                           font-family:Inter,sans-serif;">Export from LinkedIn</h3>
                <p style="color:#6B7280;font-size:.88rem;line-height:1.65;margin:0;
                          font-family:Inter,sans-serif;">
                    Go to LinkedIn &rarr; Settings &amp; Privacy &rarr; Data Privacy
                    &rarr; Download my data &rarr; Download larger data archive &rarr; Request Archive
                    &rarr; upload the <b>Connections.csv</b> file here.
                </p>
            </div>
            <div style="background:#FFFFFF;border-radius:14px;padding:28px 24px;
                        border:1px solid #E5E7EB;box-shadow:0 2px 8px rgba(0,0,0,.04);">
                <div style="width:42px;height:42px;background:#FF385C;border-radius:50%;
                             display:flex;align-items:center;justify-content:center;
                             margin-bottom:18px;">
                    <span style="color:#FFFFFF;font-weight:800;font-size:1.05rem;
                                 font-family:Inter,sans-serif;">2</span>
                </div>
                <h3 style="font-size:1rem;font-weight:700;color:#111113;margin:0 0 10px;
                           font-family:Inter,sans-serif;">Upload your file</h3>
                <p style="color:#6B7280;font-size:.88rem;line-height:1.65;margin:0;
                          font-family:Inter,sans-serif;">
                    Click the Upload CSV button on the dashboard and select your
                    connections CSV or Excel file.
                </p>
            </div>
            <div style="background:#FFFFFF;border-radius:14px;padding:28px 24px;
                        border:1px solid #E5E7EB;box-shadow:0 2px 8px rgba(0,0,0,.04);">
                <div style="width:42px;height:42px;background:#FF385C;border-radius:50%;
                             display:flex;align-items:center;justify-content:center;
                             margin-bottom:18px;">
                    <span style="color:#FFFFFF;font-weight:800;font-size:1.05rem;
                                 font-family:Inter,sans-serif;">3</span>
                </div>
                <h3 style="font-size:1rem;font-weight:700;color:#111113;margin:0 0 10px;
                           font-family:Inter,sans-serif;">Explore &amp; chat</h3>
                <p style="color:#6B7280;font-size:.88rem;line-height:1.65;margin:0;
                          font-family:Inter,sans-serif;">
                    View interactive charts and ask the AI anything about your
                    professional network.
                </p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── CTA banner — white button on red gradient ─────────────────────────────────
st.markdown(
    """
    <div style="background:linear-gradient(135deg,#FF385C,#E31C5F);border-radius:20px;
                padding:64px 40px;text-align:center;margin:8px 0 32px;">
        <h2 style="color:#FFFFFF;font-size:2rem;font-weight:800;margin:0 0 10px;
                   font-family:Inter,sans-serif;">Ready to explore your network?</h2>
        <p style="color:rgba(255,255,255,.82);font-size:1rem;margin:0 0 28px;
                  font-family:Inter,sans-serif;">Free to get started. No credit card required.</p>
        <a href="/Login?signup=1" target="_self"
           style="display:inline-flex;align-items:center;justify-content:center;
                  background:#FFFFFF;color:#222222;font-weight:700;font-size:15px;
                  border-radius:8px;padding:13px 32px;text-decoration:none;
                  font-family:Inter,sans-serif;white-space:nowrap;">
            Create free account &rarr;
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<hr style="margin:0 0 12px;">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#AAAAAA;font-size:.82rem;padding:0 0 10px;">'
    "© 2025 Connect-IQ · Built for network explorers"
    "</p>",
    unsafe_allow_html=True,
)

# ── Anchor scroll ─────────────────────────────────────────────────────────────
if st.session_state.get("_scroll_to"):
    target = st.session_state.pop("_scroll_to")
    st.iframe(
        f'<script>window.parent.document.getElementById("{target}")'
        f'.scrollIntoView({{behavior:"smooth",block:"start"}});</script>',
        height=1,
    )