import streamlit as st
from components.styles import inject_styles
from utils.auth import login, signup, is_authenticated

st.set_page_config(
    page_title="Connect-IQ – Sign In",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles(hide_sidebar=True)

if is_authenticated():
    st.switch_page("pages/2_Home.py")

# ── Page-level CSS ────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp { background: #FFFFFF !important; }
    .main, .block-container { background: transparent !important; padding-top: 1rem !important; }
    [data-testid="column"], [data-testid="stHorizontalBlock"] > div {
        background: transparent !important;
    }
    /* Primary button (Sign In / Create Account) */
    [data-testid="baseButton-primary"] {
        background: #FF385C !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: none !important;
    }
    [data-testid="baseButton-primary"]:hover {
        background: #E31C5F !important;
    }
    /* Form card column (1st horizontal block, middle column) */
    div[data-testid="stHorizontalBlock"]:nth-of-type(1) [data-testid="column"]:nth-child(2) {
        background: #FFFFFF !important;
        border: 1px solid #EBEBEB !important;
        border-radius: 16px !important;
        padding: 32px 36px 28px !important;
        box-shadow: 0 2px 16px rgba(0,0,0,.06) !important;
    }
    hr { border-color: #EBEBEB !important; margin: 6px 0 72px !important; }
    /* Nav link hover */
    .cf-nav-link:hover { color: #222222 !important; background: #F7F7F7 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Nav ───────────────────────────────────────────────────────────────────────
_L = ("color:#717171;font-size:14px;font-weight:500;padding:8px 14px;"
      "border-radius:8px;text-decoration:none;white-space:nowrap;")
st.markdown(
    f"""
    <nav style="display:flex;align-items:center;padding:8px 0 10px;">
        <a href="/" target="_self"
           style="font-size:18px;font-weight:800;color:#FF385C;text-decoration:none;
                  white-space:nowrap;margin-right:24px;">🔗 Connect-IQ</a>
        <div style="display:flex;align-items:center;gap:2px;flex:1;">
            <a href="/" target="_self" class="cf-nav-link" style="{_L}">Features</a>
            <a href="/" target="_self" class="cf-nav-link" style="{_L}">How it works</a>
            <a href="/4_About" target="_self" class="cf-nav-link" style="{_L}">About</a>
            <a href="/4_About" target="_self" class="cf-nav-link" style="{_L}">FAQ</a>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
            <a href="/1_Login" target="_self"
               style="border:1.5px solid #DDDDDD;border-radius:8px;color:#222222;
                      font-size:14px;font-weight:500;padding:7px 16px;
                      text-decoration:none;white-space:nowrap;">Log in</a>
            <a href="/1_Login" target="_self"
               style="background:#FF385C;color:#FFFFFF;border-radius:8px;font-weight:600;
                      font-size:14px;padding:8px 18px;text-decoration:none;
                      white-space:nowrap;">Sign up free</a>
        </div>
    </nav>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr style="margin:6px 0 72px;">', unsafe_allow_html=True)

# ── Centered logo + subtitle ──────────────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;margin-bottom:28px;">'
    '<p style="font-size:22px;font-weight:800;color:#FF385C;margin:0 0 8px;'
    'font-family:Inter,sans-serif;">🔗 Connect-IQ</p>'
    '<p style="color:#717171;font-size:.92rem;margin:0;font-family:Inter,sans-serif;">'
    "Sign in to explore your network</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ── Centered form card ────────────────────────────────────────────────────────
_, form_col, _ = st.columns([1.3, 2, 1.3])

with form_col:
    tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

    # ── Sign In ───────────────────────────────────────────────────────────────
    with tab_login:
        st.markdown("<br>", unsafe_allow_html=True)
        email = st.text_input("Email address", key="li_email", placeholder="you@example.com")
        password = st.text_input(
            "Password", type="password", key="li_password", placeholder="Your password"
        )

        # "Forgot password?" right-aligned
        st.markdown(
            '<div style="text-align:right;margin-top:-8px;margin-bottom:18px;">'
            '<span style="color:#FF385C;font-size:.83rem;font-weight:500;'
            'cursor:pointer;text-decoration:underline;">Forgot password?</span>'
            "</div>",
            unsafe_allow_html=True,
        )

        if st.button("Sign In", key="login_btn", use_container_width=True, type="primary"):
            if not email or not password:
                st.error("Please fill in both fields.")
            else:
                with st.spinner("Signing in…"):
                    ok, err = login(email, password)
                if ok:
                    st.switch_page("pages/2_Home.py")
                else:
                    st.error(f"Sign-in failed: {err}")


    # ── Create Account ────────────────────────────────────────────────────────
    with tab_signup:
        st.markdown("<br>", unsafe_allow_html=True)
        new_email = st.text_input(
            "Email address", key="su_email", placeholder="you@example.com"
        )
        new_pw = st.text_input(
            "Password",
            type="password",
            key="su_password",
            placeholder="Choose a password (8+ characters)",
        )
        confirm_pw = st.text_input(
            "Confirm password",
            type="password",
            key="su_confirm",
            placeholder="Repeat your password",
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Create Account", key="signup_btn", use_container_width=True, type="primary"):
            if not new_email or not new_pw or not confirm_pw:
                st.error("Please fill in all fields.")
            elif new_pw != confirm_pw:
                st.error("Passwords do not match.")
            elif len(new_pw) < 8:
                st.error("Password must be at least 8 characters.")
            else:
                with st.spinner("Creating your account…"):
                    ok, msg = signup(new_email, new_pw)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)


st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#AAAAAA;font-size:.8rem;">'
    "🔒 Your data is encrypted and only accessible to you."
    "</p>",
    unsafe_allow_html=True,
)
