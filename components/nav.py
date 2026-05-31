import streamlit as st
from utils.auth import get_display_name

# ── Shared inline style strings ────────────────────────────────────────────────
_BASE_LINK = (
    "display:inline-flex;align-items:center;gap:6px;"
    "font-size:14px;font-weight:500;color:#717171;"
    "padding:8px 14px;border-radius:8px;"
    "text-decoration:none;white-space:nowrap;"
    "font-family:Inter,system-ui,sans-serif;cursor:pointer;"
    "transition:background .15s,color .15s;"
)
_ACTIVE_LINK = (
    "display:inline-flex;align-items:center;gap:6px;"
    "font-size:14px;font-weight:600;color:#FF385C;"
    "padding:8px 14px;border-radius:8px;"
    "background:#FFE8EE;text-decoration:none;white-space:nowrap;"
    "font-family:Inter,system-ui,sans-serif;cursor:pointer;"
)
_AVATAR = (
    "width:36px;height:36px;border-radius:50%;"
    "background:linear-gradient(135deg,#FF385C,#E31C5F);"
    "display:inline-flex;align-items:center;justify-content:center;"
    "color:#fff;font-weight:700;font-size:13px;"
    "margin-left:6px;flex-shrink:0;"
)


def render_app_nav(active: str = "") -> None:
    """Horizontal top navigation bar for authenticated pages."""
    name = get_display_name()
    initials = "".join(w[0].upper() for w in name.split() if w)[:2] if name else "U"

    def _s(page: str) -> str:
        return _ACTIVE_LINK if active == page else _BASE_LINK

    st.markdown(
        f"""
        <div style="display:flex;align-items:center;justify-content:space-between;
                    background:#fff;border-bottom:1px solid #EBEBEB;
                    padding:10px 0;margin-bottom:20px;">
          <a href="/" style="font-size:18px;font-weight:800;color:#FF385C;
             text-decoration:none;white-space:nowrap;
             font-family:Inter,system-ui,sans-serif;line-height:1;">
            🔗 Connect-IQ
          </a>
          <div style="display:flex;align-items:center;gap:4px;">
            <a href="/Home"         target="_self" style="{_s('dashboard')}">📊 Dashboard</a>
            <a href="/Chat"         target="_self" style="{_s('chat')}">💬 Chat</a>
            <a href="/Login?logout=1" target="_self" style="{_BASE_LINK}">↪ Log out</a>
            <div style="{_AVATAR}">{initials}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Backwards-compatible alias
render_nav = render_app_nav