import streamlit as st
from components.styles import inject_styles
from utils.auth import login, signup, is_authenticated

st.set_page_config(
    page_title="ConnectionsFun – Sign In",
    page_icon="🔗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_styles(hide_sidebar=True)

if is_authenticated():
    st.switch_page("pages/2_Home.py")

# ── Back link ────────────────────────────────────────────────────────────────
if st.button("← Back to home", key="back_home"):
    st.switch_page("app.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── Card container ───────────────────────────────────────────────────────────
_, card, _ = st.columns([0.5, 3, 0.5])

with card:
    st.markdown(
        '<div style="text-align:center;margin-bottom:32px;">'
        '<p style="font-size:26px;font-weight:800;color:#FF385C;margin:0;">🔗 ConnectionsFun</p>'
        '<p style="color:#717171;font-size:.95rem;margin-top:6px;">Sign in to explore your network</p>'
        "</div>",
        unsafe_allow_html=True,
    )

    tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

    # ── Sign In tab ──────────────────────────────────────────────────────────
    with tab_login:
        st.markdown("<br>", unsafe_allow_html=True)
        email = st.text_input("Email address", key="li_email", placeholder="you@example.com")
        password = st.text_input(
            "Password", type="password", key="li_password", placeholder="Your password"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Sign In", key="login_btn", use_container_width=True):
            if not email or not password:
                st.error("Please fill in both fields.")
            else:
                with st.spinner("Signing in…"):
                    ok, err = login(email, password)
                if ok:
                    st.success("Welcome back!")
                    st.switch_page("pages/2_Home.py")
                else:
                    st.error(f"Sign-in failed: {err}")

    # ── Create Account tab ───────────────────────────────────────────────────
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

        if st.button("Create Account", key="signup_btn", use_container_width=True):
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
        '<div style="background:#F7F7F7;border-radius:10px;padding:14px 18px;text-align:center;">'
        '<p style="color:#AAAAAA;font-size:.8rem;margin:0;">'
        "🔒 Your data is encrypted and only accessible to you."
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )
