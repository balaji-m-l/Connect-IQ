"""
nav.py — Pure-HTML top navigation bar for Connect-IQ.

IMPORTANT: the HTML block is kept at zero indentation inside st.markdown.
Streamlit's markdown processor treats any line with 4+ leading spaces as a
fenced code block, which would render raw HTML tags as visible text.
"""

import streamlit as st
from utils.auth import get_display_name, get_user_email, logout as _do_logout

_PAGE_MAP = {
    "dashboard": "pages/2_Home.py",
    "chat":      "pages/3_Chat.py",
    "settings":  "pages/5_Settings.py",
    "about":     "pages/4_About.py",
}

_VALID_SECTIONS = {"profile", "password", "data", "privacy", "delete"}

# CSS lives in its own call so brace-escaping doesn't bleed into the HTML f-string.
_NAV_CSS = """<style>
[data-testid="stHeader"],[data-testid="stDecoration"],#stDecoration{display:none!important}
.block-container{padding-top:0!important;overflow:visible!important}
.stMarkdown,[data-testid="stMarkdownContainer"],[data-testid="stVerticalBlock"],.main{overflow:visible!important}
.cf-main-nav{display:flex;align-items:center;justify-content:space-between;background:#fff;border-bottom:1px solid #EBEBEB;padding:14px 32px;margin-bottom:28px;font-family:Inter,system-ui,sans-serif;position:relative;z-index:200}
.cf-main-nav a,.cf-main-nav a:visited,.cf-main-nav a:hover,.cf-main-nav a:active{text-decoration:none!important;color:inherit}
.cf-mn-logo{display:inline-flex;align-items:center;gap:8px;font-size:19px;font-weight:800;color:#FF385C!important;white-space:nowrap;line-height:1}
.cf-mn-logo .ico{font-size:22px;line-height:1}
.cf-nav-right{display:flex;align-items:center;gap:4px}
.cf-nav-link{display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:500;color:#717171!important;padding:8px 14px;border-radius:8px;cursor:pointer;white-space:nowrap;transition:background .15s,color .15s;line-height:1.2}
.cf-nav-link:hover{background:#F7F7F7;color:#222!important}
.cf-nav-link.active{background:#FFE8EE;color:#FF385C!important;font-weight:600}
.cf-nav-link.active:hover{background:#FFE0EA;color:#FF385C!important}
.cf-nav-avatar-wrap{position:relative;margin-left:8px}
.cf-nav-avatar{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#FF385C,#E31C5F);display:inline-flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:13px;line-height:1;cursor:pointer;flex-shrink:0;transition:box-shadow .15s;user-select:none}
.cf-nav-avatar-wrap:hover .cf-nav-avatar{box-shadow:0 0 0 2.5px #FF385C}
.cf-av-dd{display:none;position:absolute;top:calc(100% + 8px);right:0;background:#fff;border:1px solid #EBEBEB;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,.10);min-width:220px;z-index:9999;overflow:hidden}
.cf-nav-avatar-wrap:hover .cf-av-dd{display:block}
.cf-av-dd-hdr{padding:14px 16px 12px;border-bottom:1px solid #EBEBEB}
.cf-av-dd-name{font-size:13.5px;font-weight:600;color:#222}
.cf-av-dd-email{font-size:12px;color:#717171;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:188px}
.cf-av-dd-grp{padding:6px 8px;border-bottom:1px solid #EBEBEB}
.cf-av-dd-grp:last-child{border-bottom:none}
.cf-dd-item{display:block;padding:9px 16px;font-size:14px;font-weight:400;color:#222!important;border-radius:6px;white-space:nowrap;transition:background .15s;cursor:pointer}
.cf-dd-item:hover{background:#F7F7F7;color:#222!important}
.cf-dd-item.danger{color:#D92D20!important}
.cf-dd-item.danger:hover{background:#FEE4E2;color:#D92D20!important}
</style>"""


def _handle_params() -> None:
    if st.query_params.get("_logout") == "1":
        _do_logout()
        st.switch_page("app.py")
    nav = st.query_params.get("_nav", "")
    if nav in _PAGE_MAP:
        st.switch_page(_PAGE_MAP[nav])
    section = st.query_params.get("_section", "")
    if section in _VALID_SECTIONS:
        st.session_state.settings_section = section
        st.switch_page("pages/5_Settings.py")


def render_app_nav(active: str = "") -> None:
    """Render the top nav bar as a single HTML block. Call once per authenticated page."""
    _handle_params()

    name     = get_display_name()
    email    = get_user_email()
    initials = "".join(w[0].upper() for w in name.split() if w)[:2] if name else "U"
    dash_cls = "cf-nav-link active" if active == "dashboard" else "cf-nav-link"
    chat_cls = "cf-nav-link active" if active == "chat"      else "cf-nav-link"

    # HTML lines must have < 4 leading spaces — 4+ spaces = markdown code block.
    # Keep every line at 0 or 2 spaces of indentation only.
    nav_html = (
        '<div class="cf-main-nav">'
        f'<a class="cf-mn-logo" href="?_nav=dashboard" target="_self"><span class="ico">🔗</span> Connect-IQ</a>'
        '<div class="cf-nav-right">'
        f'<a class="{dash_cls}" href="?_nav=dashboard" target="_self">📊 Dashboard</a>'
        f'<a class="{chat_cls}" href="?_nav=chat" target="_self">💬 Chat</a>'
        '<div class="cf-nav-avatar-wrap">'
        f'<div class="cf-nav-avatar">{initials}</div>'
        '<div class="cf-av-dd">'
        '<div class="cf-av-dd-hdr">'
        f'<div class="cf-av-dd-name">{name or "User"}</div>'
        f'<div class="cf-av-dd-email">{email}</div>'
        '</div>'
        '<div class="cf-av-dd-grp">'
        '<a class="cf-dd-item" href="?_nav=settings" target="_self">👤&nbsp; Profile settings</a>'
        '<a class="cf-dd-item" href="?_section=password" target="_self">🔑&nbsp; Change password</a>'
        '</div>'
        '<div class="cf-av-dd-grp">'
        '<a class="cf-dd-item" href="?_section=data" target="_self">🗑️&nbsp; Clear all connections</a>'
        '</div>'
        '<div class="cf-av-dd-grp">'
        '<a class="cf-dd-item" href="?_section=privacy" target="_self">🔒&nbsp; Privacy &amp; data controls</a>'
        '<a class="cf-dd-item" href="?_logout=1" target="_self">↪&nbsp; Log out</a>'
        '</div>'
        '<div class="cf-av-dd-grp">'
        '<a class="cf-dd-item danger" href="?_section=delete" target="_self">⚠️&nbsp; Delete account</a>'
        '</div>'
        '</div>'  # .cf-av-dd
        '</div>'  # .cf-nav-avatar-wrap
        '</div>'  # .cf-nav-right
        '</div>'  # .cf-main-nav
    )

    st.markdown(_NAV_CSS, unsafe_allow_html=True)
    st.markdown(nav_html, unsafe_allow_html=True)


# Backwards-compatible alias
render_nav = render_app_nav
