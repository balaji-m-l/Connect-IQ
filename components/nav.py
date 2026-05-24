import streamlit as st
from utils.auth import logout

_NAV_CSS = """
<style>
/* Restore primary button style when inside nav columns */
div[data-testid="stHorizontalBlock"] [data-testid="baseButton-primary"] {
    background: var(--cf-red) !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 8px 16px !important;
}
div[data-testid="stHorizontalBlock"] [data-testid="baseButton-primary"]:hover {
    background: var(--cf-red-dark) !important;
    transform: translateY(-1px) !important;
}
/* Shrink column gaps and vertically center all nav items */
div[data-testid="stHorizontalBlock"] { gap: 4px !important; align-items: center !important; }
</style>
"""


def render_nav(active: str = "") -> None:
    """Horizontal top navigation bar for authenticated pages."""
    st.markdown(_NAV_CSS, unsafe_allow_html=True)

    logo_c, _, dash_c, chat_c, about_c, fill_c, up_c, out_c = st.columns(
        [2.4, 0.2, 1.0, 0.8, 0.8, 5.4, 1.4, 1.0]
    )

    with logo_c:
        st.markdown(
            '<a href="/" target="_self" style="text-decoration:none;">'
            '<p style="font-size:20px;font-weight:800;color:#FF385C;'
            'margin:0;padding:4px 0 0;">🔗 Connect-IQ</p></a>',
            unsafe_allow_html=True,
        )

    with dash_c:
        if st.button("Dashboard", key="nav_dash"):
            st.switch_page("pages/2_Home.py")

    with chat_c:
        if st.button("Chat", key="nav_chat"):
            st.switch_page("pages/3_Chat.py")

    with about_c:
        if st.button("About", key="nav_about"):
            st.switch_page("pages/4_About.py")

    with up_c:
        if st.button("📤 Upload CSV", key="nav_upload", type="primary"):
            st.switch_page("pages/2_Home.py")

    with out_c:
        if st.button("Log out", key="nav_logout"):
            logout()
            st.switch_page("app.py")

    st.markdown('<hr style="margin:2px 0 24px;">', unsafe_allow_html=True)