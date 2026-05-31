import streamlit as st
from utils.auth import logout, get_display_name


def render_nav(active: str = "") -> None:
    """Horizontal top navigation bar for authenticated pages."""

    # User avatar initials
    name = get_display_name()
    initials = "".join(w[0].upper() for w in name.split() if w)[:2] if name else "U"

    # Column index (1-based) of the active button so we can highlight it.
    # Layout: logo(1) | gap(2) | dash(3) | chat(4) | fill(5) | upload(6) | logout(7) | avatar(8)
    _active_col = {"home": 3, "chat": 4}.get(active, 99)

    st.markdown(
        f"""
        <style>
        /* ── Nav row container ── */
        div[data-testid="stHorizontalBlock"]:first-of-type {{
            gap: 2px !important;
            align-items: center !important;
            padding: 10px 0 !important;
            background: #FFFFFF !important;
            border-bottom: 1px solid #EBEBEB !important;
            margin-bottom: 20px !important;
        }}

        /* ── All nav buttons: ghost style ── */
        div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {{
            background: transparent !important;
            color: #717171 !important;
            border: none !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            padding: 7px 14px !important;
            width: auto !important;
            white-space: nowrap !important;
            box-shadow: none !important;
            border-radius: 8px !important;
            transition: background .15s, color .15s !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:hover {{
            background: #F7F7F7 !important;
            color: #222222 !important;
            transform: none !important;
            box-shadow: none !important;
        }}

        /* ── Active nav button ── */
        div[data-testid="stHorizontalBlock"]:first-of-type
            > div:nth-child({_active_col}) .stButton > button {{
            background: #FFE8EE !important;
            color: #FF385C !important;
            font-weight: 600 !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type
            > div:nth-child({_active_col}) .stButton > button:hover {{
            background: #FFE8EE !important;
            color: #FF385C !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ── Column layout ─────────────────────────────────────────────
    # [logo | gap | Dashboard | Chat | fill | Upload CSV | Log out | avatar]
    logo_c, _, dash_c, chat_c, fill_c, up_c, out_c, av_c = st.columns(
        [2.2, 0.1, 1.2, 0.8, 5.2, 1.4, 1.0, 0.6]
    )

    with logo_c:
        st.markdown(
            '<a href="/" target="_self" style="text-decoration:none;">'
            '<p style="font-size:18px;font-weight:800;color:#FF385C;margin:0;padding:0;'
            'font-family:Inter,sans-serif;white-space:nowrap;line-height:1;">🔗 Connect-IQ</p>'
            '</a>',
            unsafe_allow_html=True,
        )

    with dash_c:
        if st.button("📊 Dashboard", key="nav_dash"):
            st.switch_page("pages/2_Home.py")

    with chat_c:
        if st.button("💬 Chat", key="nav_chat"):
            st.switch_page("pages/3_Chat.py")

    with up_c:
        if st.button("📤 Upload CSV", key="nav_upload"):
            st.switch_page("pages/2_Home.py")

    with out_c:
        if st.button("↪ Log out", key="nav_logout"):
            logout()
            st.switch_page("app.py")

    with av_c:
        st.markdown(
            f'<div style="display:flex;justify-content:center;align-items:center;height:38px;">'
            f'<div style="width:36px;height:36px;border-radius:50%;'
            f'background:linear-gradient(135deg,#FF385C,#E31C5F);'
            f'display:flex;align-items:center;justify-content:center;'
            f'color:#fff;font-weight:700;font-size:13px;flex-shrink:0;">'
            f'{initials}</div></div>',
            unsafe_allow_html=True,
        )