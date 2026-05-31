import streamlit as st
from utils.auth import logout


def render_sidebar(active: str = "home") -> None:
    """Render the authenticated sidebar navigation."""
    with st.sidebar:
        st.markdown(
            '<div style="padding:8px 0 28px 0;">'
            '<span style="font-size:20px;font-weight:700;color:#FF385C;">🔗 ConnectionsFun</span>'
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p style="font-size:11px;font-weight:600;letter-spacing:.08em;'
            'color:#AAAAAA;text-transform:uppercase;margin-bottom:6px;">Navigation</p>',
            unsafe_allow_html=True,
        )

        if st.button("📊  Dashboard", width='stretch', key="sb_home"):
            st.switch_page("pages/2_Home.py")

        if st.button("💬  Chat with AI", width='stretch', key="sb_chat"):
            st.switch_page("pages/3_Chat.py")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:11px;font-weight:600;letter-spacing:.08em;'
            'color:#AAAAAA;text-transform:uppercase;margin-bottom:6px;">Account</p>',
            unsafe_allow_html=True,
        )

        if st.button("🚪  Log Out", width='stretch', key="sb_logout"):
            logout()
            st.switch_page("app.py")
