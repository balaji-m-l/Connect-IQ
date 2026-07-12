"""
nav.py — Top navigation bar for Connect-IQ.

Navigation uses hidden Streamlit buttons triggered by JavaScript onclick
handlers instead of HTML <a href> links. This ensures st.switch_page() is
used for all navigation, which preserves st.session_state across page changes.
HTML <a href> links cause browser navigation → new WebSocket session →
session_state lost → user gets kicked out.
"""

import streamlit as st
from utils.auth import get_display_name, get_user_email, logout as _do_logout

_VALID_SECTIONS = {"profile", "password", "data", "privacy", "delete"}

_NAV_CSS = """<style>
[data-testid="stHeader"],[data-testid="stDecoration"],#stDecoration{display:none!important}
.block-container{padding-top:0!important;overflow:visible!important}
.stMarkdown,[data-testid="stMarkdownContainer"],[data-testid="stVerticalBlock"],.main{overflow:visible!important}
.cf-main-nav{display:flex;align-items:center;justify-content:space-between;background:#fff;border-bottom:1px solid #EBEBEB;padding:14px 32px;margin-bottom:28px;font-family:Inter,system-ui,sans-serif;position:relative;z-index:200}
.cf-main-nav a,.cf-main-nav a:visited,.cf-main-nav a:hover,.cf-main-nav a:active{text-decoration:none!important;color:inherit}
.cf-mn-logo{display:inline-flex;align-items:center;gap:8px;font-size:19px;font-weight:800;color:#FF385C!important;white-space:nowrap;line-height:1;cursor:pointer}
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
.cf-nav-avatar-wrap::after{content:'';position:absolute;top:100%;left:-10px;right:-10px;height:8px}
.cf-av-dd-hdr{padding:14px 16px 12px;border-bottom:1px solid #EBEBEB}
.cf-av-dd-name{font-size:13.5px;font-weight:600;color:#222}
.cf-av-dd-email{font-size:12px;color:#717171;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:188px}
.cf-av-dd-grp{padding:6px 8px;border-bottom:1px solid #EBEBEB}
.cf-av-dd-grp:last-child{border-bottom:none}
.cf-dd-item{display:block;padding:9px 16px;font-size:14px;font-weight:400;color:#222!important;border-radius:6px;white-space:nowrap;transition:background .15s;cursor:pointer}
.cf-dd-item:hover{background:#F7F7F7;color:#222!important}
.cf-dd-item.danger{color:#D92D20!important}
.cf-dd-item.danger:hover{background:#FEE4E2;color:#D92D20!important}
.st-key-nav_btn_home,.st-key-nav_btn_dash,.st-key-nav_btn_chat,
.st-key-nav_btn_logout,.st-key-nav_btn_s_profile,.st-key-nav_btn_s_password,
.st-key-nav_btn_s_data,.st-key-nav_btn_s_privacy,.st-key-nav_btn_s_delete{
display:none!important}
</style>"""

# JS helper — clicks a hidden Streamlit button by its st-key CSS class
def _js(key: str) -> str:
    return f"(function(){{var b=document.querySelector('.st-key-{key} button');if(b){{b.click();}}}})();"


def _handle_params() -> None:
    """Handle legacy deep-link query params (e.g. emailed links with ?_nav=xxx)."""
    logout = st.query_params.get("_logout")
    if logout == "1":
        _do_logout()
        st.switch_page("app.py")

    nav = st.query_params.get("_nav", "")
    page_map = {
        "dashboard": "pages/2_Home.py",
        "chat":      "pages/3_Chat.py",
        "settings":  "pages/5_Settings.py",
        "about":     "pages/4_About.py",
    }
    if nav in page_map:
        st.switch_page(page_map[nav])

    section = st.query_params.get("_section", "")
    if section in _VALID_SECTIONS:
        st.session_state.settings_section = section
        scroll = st.query_params.get("_scroll", "")
        if scroll:
            st.session_state.settings_scroll = scroll
        st.switch_page("pages/5_Settings.py")


def render_app_nav(active: str = "") -> None:
    """Render the top nav bar. Call once per authenticated page."""
    _handle_params()

    name     = get_display_name()
    email    = get_user_email()
    initials = "".join(w[0].upper() for w in name.split() if w)[:2] if name else "U"
    dash_cls = "cf-nav-link active" if active == "dashboard" else "cf-nav-link"
    chat_cls = "cf-nav-link active" if active == "chat"      else "cf-nav-link"

    st.markdown(_NAV_CSS, unsafe_allow_html=True)

    # ── Hidden navigation buttons ─────────────────────────────────────────────
    # These are positioned off-screen via CSS and clicked programmatically by
    # the JavaScript onclick handlers in the HTML nav below.
    if st.button("home",     key="nav_btn_home"):
        st.switch_page("app.py")
    if st.button("dash",     key="nav_btn_dash"):
        st.switch_page("pages/2_Home.py")
    if st.button("chat",     key="nav_btn_chat"):
        st.switch_page("pages/3_Chat.py")
    if st.button("logout",   key="nav_btn_logout"):
        _do_logout()
        st.switch_page("app.py")

    for sec in ("profile", "password", "data", "privacy", "delete"):
        if st.button(sec, key=f"nav_btn_s_{sec}"):
            st.session_state.settings_section = sec
            if sec == "data":
                st.session_state.settings_scroll = "clear"
            st.switch_page("pages/5_Settings.py")

    # ── HTML nav (appearance only — onclick triggers hidden buttons above) ────
    nav_html = (
        '<div class="cf-main-nav">'
        f'<span class="cf-mn-logo" onclick="{_js("nav_btn_home")}"><span class="ico">🔗</span> Connect-IQ</span>'
        '<div class="cf-nav-right">'
        f'<span class="{dash_cls}" onclick="{_js("nav_btn_dash")}">📊 Dashboard</span>'
        f'<span class="{chat_cls}" onclick="{_js("nav_btn_chat")}">💬 Chat</span>'
        '<div class="cf-nav-avatar-wrap">'
        f'<div class="cf-nav-avatar">{initials}</div>'
        '<div class="cf-av-dd">'
        '<div class="cf-av-dd-hdr">'
        f'<div class="cf-av-dd-name">{name or "User"}</div>'
        f'<div class="cf-av-dd-email">{email}</div>'
        '</div>'
        '<div class="cf-av-dd-grp">'
        f'<span class="cf-dd-item" onclick="{_js("nav_btn_s_profile")}">👤&nbsp; Profile settings</span>'
        f'<span class="cf-dd-item" onclick="{_js("nav_btn_s_password")}">🔑&nbsp; Change password</span>'
        '</div>'
        '<div class="cf-av-dd-grp">'
        f'<span class="cf-dd-item" onclick="{_js("nav_btn_s_data")}">🗑️&nbsp; Clear all data</span>'
        '</div>'
        '<div class="cf-av-dd-grp">'
        f'<span class="cf-dd-item" onclick="{_js("nav_btn_s_privacy")}">🔒&nbsp; Privacy &amp; data controls</span>'
        f'<span class="cf-dd-item" onclick="{_js("nav_btn_logout")}">↪&nbsp; Log out</span>'
        '</div>'
        '<div class="cf-av-dd-grp">'
        f'<span class="cf-dd-item danger" onclick="{_js("nav_btn_s_delete")}">⚠️&nbsp; Delete account</span>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(nav_html, unsafe_allow_html=True)


# Backwards-compatible alias
render_nav = render_app_nav
