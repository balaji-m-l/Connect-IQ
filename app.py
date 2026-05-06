import streamlit as st
from components.styles import inject_styles

st.set_page_config(
    page_title="ConnectionsFun – Visualize Your LinkedIn Network",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles(hide_sidebar=True)

# Redirect if already logged in
if st.session_state.get("user"):
    st.switch_page("pages/2_Home.py")

# ── Navbar ──────────────────────────────────────────────────────────────────
nav_l, nav_mid, nav_r1, nav_r2 = st.columns([3, 5, 1, 1])
with nav_l:
    st.markdown(
        '<p style="font-size:22px;font-weight:800;color:#FF385C;margin:0;padding:8px 0;">🔗 ConnectionsFun</p>',
        unsafe_allow_html=True,
    )
with nav_r1:
    if st.button("Log In", key="nav_login"):
        st.switch_page("pages/1_Login.py")
with nav_r2:
    if st.button("Sign Up", key="nav_signup"):
        st.switch_page("pages/1_Login.py")

st.markdown('<hr style="margin:4px 0 40px 0;">', unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
hero_l, hero_r = st.columns([1.15, 1], gap="large")

with hero_l:
    st.markdown(
        """
        <div style="padding:10px 0 32px 0;">
            <h1 style="font-size:3.2rem;font-weight:800;line-height:1.15;color:#222222;margin-bottom:20px;">
                Understand your<br>
                <span style="color:#FF385C;">LinkedIn network</span><br>
                like never before
            </h1>
            <p style="font-size:1.1rem;color:#717171;line-height:1.7;max-width:480px;margin-bottom:36px;">
                Upload your LinkedIn connections export and instantly discover who's in your
                network, where they work, and what roles they hold — powered by AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cta_col, _ = st.columns([1, 2])
    with cta_col:
        if st.button("Get started free →", key="hero_cta"):
            st.switch_page("pages/1_Login.py")

with hero_r:
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,rgba(255,56,92,.08) 0%,rgba(255,56,92,.02) 100%);
                    border-radius:20px;padding:32px;margin-top:10px;">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div style="background:#fff;border-radius:14px;padding:22px;
                            box-shadow:0 2px 12px rgba(0,0,0,.07);">
                    <div style="font-size:2rem;font-weight:800;color:#FF385C;">500+</div>
                    <div style="color:#717171;font-size:.88rem;margin-top:4px;">Connections analyzed</div>
                </div>
                <div style="background:#fff;border-radius:14px;padding:22px;
                            box-shadow:0 2px 12px rgba(0,0,0,.07);">
                    <div style="font-size:2rem;font-weight:800;color:#FF385C;">20+</div>
                    <div style="color:#717171;font-size:.88rem;margin-top:4px;">Industries mapped</div>
                </div>
                <div style="background:#fff;border-radius:14px;padding:22px;
                            box-shadow:0 2px 12px rgba(0,0,0,.07);">
                    <div style="font-size:2rem;font-weight:800;color:#FF385C;">RAG</div>
                    <div style="color:#717171;font-size:.88rem;margin-top:4px;">AI-powered search</div>
                </div>
                <div style="background:#fff;border-radius:14px;padding:22px;
                            box-shadow:0 2px 12px rgba(0,0,0,.07);">
                    <div style="font-size:2rem;font-weight:800;color:#FF385C;">🔒</div>
                    <div style="color:#717171;font-size:.88rem;margin-top:4px;">Private & secure</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ── Features ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center;margin:48px 0 36px;">
        <h2 style="font-size:2rem;font-weight:800;color:#222222;">Everything you need to know your network</h2>
        <p style="color:#717171;font-size:1rem;margin-top:6px;">Powerful visualizations and AI insights — in one place.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

fc1, fc2, fc3 = st.columns(3, gap="medium")
_CARD = (
    '<div style="background:#F7F7F7;border-radius:16px;padding:28px 24px;height:100%;">'
    '<div style="font-size:2.4rem;margin-bottom:14px;">{icon}</div>'
    '<h3 style="font-size:1.05rem;font-weight:700;color:#222222;margin-bottom:8px;">{title}</h3>'
    '<p style="color:#717171;font-size:.9rem;line-height:1.65;">{desc}</p>'
    "</div>"
)
with fc1:
    st.markdown(
        _CARD.format(
            icon="📊",
            title="Visual Network Map",
            desc="Interactive charts show your connections by company, job title, and time — giving you an instant picture of your network.",
        ),
        unsafe_allow_html=True,
    )
with fc2:
    st.markdown(
        _CARD.format(
            icon="🤖",
            title="RAG-Powered AI Chat",
            desc='Ask questions like "List all recruiters in Finance" or "Who do I know at FAANG companies?" — grounded answers, zero hallucinations.',
        ),
        unsafe_allow_html=True,
    )
with fc3:
    st.markdown(
        _CARD.format(
            icon="🔒",
            title="Private & Secure",
            desc="Your data is stored securely in your own Supabase project with row-level security. Only you can access your connections.",
        ),
        unsafe_allow_html=True,
    )

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ── How it works ─────────────────────────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;margin:48px 0 36px;">'
    '<h2 style="font-size:2rem;font-weight:800;color:#222222;">How it works</h2>'
    "</div>",
    unsafe_allow_html=True,
)

sc1, sc2, sc3 = st.columns(3, gap="medium")
_STEP = (
    '<div style="text-align:center;padding:10px 16px;">'
    '<div style="width:46px;height:46px;background:#FF385C;border-radius:50%;'
    'display:flex;align-items:center;justify-content:center;margin:0 auto 16px;'
    'font-size:1.15rem;font-weight:800;color:#fff;">{num}</div>'
    '<h3 style="font-size:1rem;font-weight:700;color:#222222;margin-bottom:8px;">{title}</h3>'
    '<p style="color:#717171;font-size:.9rem;line-height:1.6;">{desc}</p>'
    "</div>"
)
with sc1:
    st.markdown(
        _STEP.format(
            num="1",
            title="Export from LinkedIn",
            desc="Go to LinkedIn → Settings & Privacy → Data Privacy → Get a copy of your data → Connections.",
        ),
        unsafe_allow_html=True,
    )
with sc2:
    st.markdown(
        _STEP.format(
            num="2",
            title="Upload your file",
            desc="Click the Upload CSV button on the dashboard and select your connections CSV or Excel file.",
        ),
        unsafe_allow_html=True,
    )
with sc3:
    st.markdown(
        _STEP.format(
            num="3",
            title="Explore & chat",
            desc="View interactive charts and ask the AI anything about your professional network.",
        ),
        unsafe_allow_html=True,
    )

st.markdown("<br><br>", unsafe_allow_html=True)

# ── CTA banner ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="background:linear-gradient(135deg,#FF385C,#E31C5F);border-radius:20px;
                padding:52px 40px;text-align:center;margin:8px 0 32px;">
        <h2 style="color:#fff;font-size:2rem;font-weight:800;margin-bottom:10px;">
            Ready to explore your network?
        </h2>
        <p style="color:rgba(255,255,255,.85);font-size:1rem;margin:0;">
            Free to get started. No credit card required.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
_, cta_mid, _ = st.columns([2, 1, 2])
with cta_mid:
    if st.button("Create free account →", key="bottom_cta"):
        st.switch_page("pages/1_Login.py")

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#AAAAAA;font-size:.82rem;padding:8px 0 4px;">'
    "© 2024 ConnectionsFun · Built for network explorers"
    "</p>",
    unsafe_allow_html=True,
)
