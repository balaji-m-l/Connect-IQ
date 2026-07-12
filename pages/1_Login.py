import streamlit as st
from components.styles import inject_styles
import streamlit.components.v1 as _components
from utils.auth import login, logout, signup, reset_password, is_authenticated

st.set_page_config(
    page_title="Connect-IQ – Sign In",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if st.query_params.get("verified") == "1":
    inject_styles(
        hide_sidebar=True,
        mobile_wall_icon="✅",
        mobile_wall_title="Email verified!",
        mobile_wall_body="Your account is ready.<br>Open <strong>connect-iq.site</strong> on your desktop to sign in.",
    )
else:
    inject_styles(hide_sidebar=True)

# Handle logout redirect: /Login?logout=1
if st.query_params.get("logout"):
    logout()
    st.query_params.clear()

if st.query_params.get("verified") == "1":
    import streamlit.components.v1 as components
    components.html("""
    <script>
    (function() {
      if (window.parent.document.getElementById('cf-verified-banner')) return;

      var s = window.parent.document.createElement('style');
      s.textContent = '@keyframes cf-shrink{from{width:100%}to{width:0%}}';
      window.parent.document.head.appendChild(s);

      var el = window.parent.document.createElement('div');
      el.id = 'cf-verified-banner';
      el.style.cssText = [
        'position:fixed','top:28px','left:50%','transform:translateX(-50%)',
        'z-index:99999','background:#fff','border:1px solid #EBEBEB',
        'border-radius:16px','padding:28px 44px 22px','text-align:center',
        'box-shadow:0 8px 32px rgba(0,0,0,.13)','min-width:300px',
        'font-family:Inter,system-ui,sans-serif','transition:opacity .4s'
      ].join(';');
      el.innerHTML = [
        '<button id="cf-vfy-close" style="position:absolute;top:10px;right:14px;',
        'background:none;border:none;font-size:22px;line-height:1;cursor:pointer;',
        'color:#717171;">&times;</button>',
        '<div style="font-size:2.6rem;margin-bottom:10px;">&#x2705;</div>',
        '<h3 style="font-size:1.15rem;font-weight:800;color:#222;margin:0 0 6px;">',
        'Email verified!</h3>',
        '<p style="color:#717171;font-size:.9rem;margin:0;">',
        'Your account is ready. Sign in below.</p>',
        '<div style="height:3px;background:#FF385C;border-radius:2px;margin-top:16px;',
        'animation:cf-shrink 5s linear forwards;"></div>'
      ].join('');
      window.parent.document.body.appendChild(el);

      function dismiss() {
        el.style.opacity = '0';
        setTimeout(function(){ if (el.parentNode) el.parentNode.removeChild(el); }, 420);
      }
      window.parent.document.getElementById('cf-vfy-close').addEventListener('click', dismiss);
      setTimeout(dismiss, 5000);
    })();
    </script>
    """, height=0)

if is_authenticated():
    st.switch_page("pages/2_Home.py")

# Derive state from query params (survive reruns cleanly)
show_forgot  = st.query_params.get("forgot")  == "1"
if "_show_signup" in st.session_state:
    show_signup = st.session_state.pop("_show_signup")
else:
    show_signup = st.query_params.get("signup") == "1"

# ── Page-level CSS ────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp { background: #FFFFFF !important; }
    .main, .block-container { background: transparent !important; padding-top: 0 !important; }
    [data-testid="column"], [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > div { background: transparent !important; }

    /* Nav row — white bar */
    div[data-testid="stHorizontalBlock"]:first-of-type {
        gap: 4px !important;
        align-items: center !important;
        padding: 14px 0 !important;
        background: #FFFFFF !important;
        border-bottom: 1px solid #EBEBEB !important;
        margin-bottom: 0 !important;
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
    /* Log in — 8th nav column */
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
    /* Sign up free — 9th nav column */
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

    /* Form card — 2nd horizontal block, middle column */
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) [data-testid="column"]:nth-child(2),
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) [data-testid="stColumn"]:nth-child(2) {
        background: #FFFFFF !important;
        border: 1px solid #EBEBEB !important;
        border-radius: 16px !important;
        padding: 32px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,.07) !important;
    }

    hr { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Nav ───────────────────────────────────────────────────────────────────────
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
    if st.button("About", key="nav_about"):
        st.session_state["_about_scroll"] = "cf-about-top"
        st.switch_page("pages/4_About.py")
with faq_c:
    if st.button("FAQ", key="nav_faq"):
        st.session_state["_about_scroll"] = "cf-faq"
        st.switch_page("pages/4_About.py")
with login_c:
    if st.button("Log in", key="nav_login", type="secondary"):
        st.query_params.clear()
        st.rerun()
with signup_c:
    if st.button("Sign up free", key="nav_signup", type="primary"):
        st.query_params["signup"] = "1"
        st.rerun()

# ── Logo + subtitle ───────────────────────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;padding:60px 0 32px;">'
    '<p style="font-size:28px;font-weight:800;color:#FF385C;margin:0 0 10px;'
    'font-family:Inter,sans-serif;">🔗 Connect-IQ</p>'
    '<p style="color:#717171;font-size:15px;margin:0;font-family:Inter,sans-serif;">'
    "Sign in to explore your network</p>"
    "</div>",
    unsafe_allow_html=True,
)


# ── Form card ─────────────────────────────────────────────────────────────────
_, form_col, _ = st.columns([1.3, 2, 1.3])

with form_col:
    if show_signup:
        tab_signup, tab_login = st.tabs(["Create Account", "Sign In"])
    else:
        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

    # ── Sign In ───────────────────────────────────────────────────────────────
    with tab_login:
        st.markdown("<br>", unsafe_allow_html=True)

        if not show_forgot:
            # ── Normal sign-in form ──────────────────────────────────────────
            email = st.text_input("Email address", key="li_email", placeholder="you@example.com")
            password = st.text_input(
                "Password", type="password", key="li_password", placeholder="Your password"
            )
            st.markdown(
                '<div style="text-align:right;margin-top:-8px;margin-bottom:18px;">'
                '<a href="?forgot=1" target="_self" style="'
                'color:#222222;font-size:14px;font-weight:500;'
                'text-decoration:underline;cursor:pointer;'
                'font-family:Inter,system-ui,sans-serif;">'
                'Forgot password?</a></div>',
                unsafe_allow_html=True,
            )
            if st.button("Sign In", key="login_btn", width='stretch', type="primary"):
                if not email or not password:
                    st.error("Please fill in both fields.")
                else:
                    with st.spinner("Signing in…"):
                        ok, err = login(email, password)
                    if ok:
                        marker = st.session_state.get("_cf_marker", "")
                        # Write marker to sessionStorage and navigate — done in
                        # one JS call so sessionStorage is guaranteed to be set
                        # before the browser loads the next page.
                        _components.html(
                            f"<script>"
                            f"try{{window.parent.sessionStorage.setItem('cf_marker','{marker}');}}catch(e){{}}"
                            f"window.parent.location.replace('/Home');"
                            f"</script>",
                            height=0,
                        )
                        st.stop()
                    else:
                        st.error(f"Sign-in failed: {err}")

        else:
            # ── Forgot password form ─────────────────────────────────────────
            st.markdown(
                '<p style="font-size:14px;color:#484848;margin:0 0 10px;font-weight:500;">'
                'Enter your email to receive a password reset link:</p>',
                unsafe_allow_html=True,
            )
            reset_email = st.text_input(
                "", key="reset_email_input",
                placeholder="you@example.com", label_visibility="collapsed",
            )
            st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)
            if st.button("Send reset link →", key="send_reset_btn", type="primary", width='stretch'):
                if not reset_email:
                    st.warning("Please enter your email address.")
                else:
                    with st.spinner("Sending reset link…"):
                        ok, msg = reset_password(reset_email)
                    if ok:
                        st.success(msg)
                        st.query_params.clear()
                        st.rerun()
                    else:
                        st.error(msg)
            st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
            if st.button("← Back to sign in", key="back_signin", width='stretch'):
                st.query_params.clear()
                st.rerun()

    # ── Create Account ────────────────────────────────────────────────────────
    with tab_signup:
        st.markdown("<br>", unsafe_allow_html=True)
        full_name = st.text_input(
            "Full name", key="su_name", placeholder="Your full name"
        )
        new_email = st.text_input(
            "Email address", key="su_email", placeholder="you@example.com"
        )
        new_pw = st.text_input(
            "Password", type="password", key="su_password",
            placeholder="Choose a password (8+ characters)",
        )
        confirm_pw = st.text_input(
            "Confirm password", type="password", key="su_confirm",
            placeholder="Repeat your password",
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Create Account", key="signup_btn", width='stretch', type="primary"):
            if not full_name or not new_email or not new_pw or not confirm_pw:
                st.error("Please fill in all fields.")
            elif new_pw != confirm_pw:
                st.error("Passwords do not match.")
            elif len(new_pw) < 8:
                st.error("Password must be at least 8 characters.")
            else:
                with st.spinner("Creating your account…"):
                    ok, msg = signup(new_email, new_pw, full_name)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)


# ── Trust strip + Back to home ────────────────────────────────────────────────
st.markdown(
    '<div style="display:flex;flex-direction:column;align-items:center;gap:0;margin-top:18px;">'
    '<div style="background:#F7F7F7;border-radius:12px;padding:12px 18px;'
    'width:38%;text-align:center;">'
    '<span style="font-size:13px;color:#717171;font-family:Inter,sans-serif;">'
    '🔒 Your data is encrypted and only accessible to you.'
    '</span></div>'
    '<div style="text-align:center;margin-top:18px;padding-bottom:40px;">'
    '<a href="/" target="_self" style="font-size:13px;color:#717171;'
    'text-decoration:none;font-family:Inter,sans-serif;">'
    '← <span style="color:#222222;font-weight:500;">Back to home</span>'
    '</a></div>'
    '</div>',
    unsafe_allow_html=True,
)