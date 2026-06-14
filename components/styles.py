"""
styles.py — ConnectionsFun (Connect-IQ) design system for Streamlit
"""

import streamlit as st
from contextlib import contextmanager

# ───────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ───────────────────────────────────────────────────────────────
COLORS = {
    "red":          "#FF385C",
    "red_dark":     "#E31C5F",
    "red_tint":     "#FFE8EE",
    "text":         "#222222",
    "text_mid":     "#484848",
    "text_muted":   "#717171",
    "text_faint":   "#AAAAAA",
    "bg":           "#FFFFFF",
    "bg_soft":      "#F7F7F7",
    "bg_light":     "#FAFAFA",
    "page":         "#EEF0F3",
    "border":       "#EBEBEB",
    "border_strong":"#DDDDDD",
    "teal":         "#00A699",
    "dark":         "#222222",
    "darker":       "#1A1A1A",
}

SHADOWS = {
    "sm": "0 2px 12px rgba(0,0,0,.07)",
    "md": "0 4px 20px rgba(0,0,0,.08)",
    "lg": "0 8px 32px rgba(0,0,0,.12)",
}

FONT_STACK = "'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif"

# ───────────────────────────────────────────────────────────────
# CSS BLOCK
# ───────────────────────────────────────────────────────────────
CSS = f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

<style>
/* ── Design tokens ── */
:root {{
  --cf-red:          {COLORS['red']};
  --cf-red-dark:     {COLORS['red_dark']};
  --cf-red-tint:     {COLORS['red_tint']};
  --cf-text:         {COLORS['text']};
  --cf-text-mid:     {COLORS['text_mid']};
  --cf-text-muted:   {COLORS['text_muted']};
  --cf-text-faint:   {COLORS['text_faint']};
  --cf-bg:           {COLORS['bg']};
  --cf-bg-soft:      {COLORS['bg_soft']};
  --cf-bg-light:     {COLORS['bg_light']};
  --cf-border:       {COLORS['border']};
  --cf-border-strong:{COLORS['border_strong']};
  --cf-teal:         {COLORS['teal']};
  --cf-dark:         {COLORS['dark']};
  --cf-darker:       {COLORS['darker']};
  --shadow-sm:       {SHADOWS['sm']};
  --shadow-md:       {SHADOWS['md']};
  --shadow-lg:       {SHADOWS['lg']};
}}

/* ── Global Streamlit overrides ── */
html, body, [class*="css"] {{
  font-family: {FONT_STACK} !important;
  color: var(--cf-text);
  -webkit-font-smoothing: antialiased;
}}
.stApp {{ background: {COLORS['page']}; }}

#MainMenu, footer, header {{ visibility: hidden; }}

.block-container {{
  padding-top: 2rem !important;
  padding-bottom: 4rem !important;
  max-width: 1180px;
}}

/* ── Typography ── */
.cf-h1      {{ font-size: 56px; font-weight: 800; line-height: 1.05; letter-spacing: -1.5px; color: var(--cf-text); }}
.cf-h1-dark {{ font-size: 56px; font-weight: 800; line-height: 1.05; letter-spacing: -1.5px; color: #fff; }}
.cf-h2      {{ font-size: 32px; font-weight: 800; line-height: 1.15; letter-spacing: -0.5px; color: var(--cf-text); }}
.cf-h3      {{ font-size: 20px; font-weight: 700; color: var(--cf-text); letter-spacing: -0.2px; }}
.cf-h4      {{ font-size: 16px; font-weight: 600; color: var(--cf-text); }}
.cf-body    {{ font-size: 16px; color: var(--cf-text-muted); line-height: 1.65; font-weight: 400; }}
.cf-small   {{ font-size: 13px; color: var(--cf-text-muted); }}
.cf-tiny    {{ font-size: 11px; color: var(--cf-text-faint); letter-spacing: 0.5px; text-transform: uppercase; font-weight: 600; }}

/* ── App container / artboard ── */
.cf-app {{
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
  font-family: {FONT_STACK};
  color: var(--cf-text);
}}

/* ── Buttons (cf-* HTML classes) ── */
.cf-btn, button.cf-btn {{
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  background: var(--cf-red); color: #fff; border: none;
  font-family: {FONT_STACK}; font-weight: 600; font-size: 15px;
  padding: 12px 24px; border-radius: 8px; cursor: pointer;
  transition: all .18s ease; text-decoration: none;
}}
.cf-btn:hover {{ background: var(--cf-red-dark); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(255,56,92,.25); }}
.cf-btn-lg {{ padding: 14px 32px; font-size: 16px; }}
.cf-btn-sm {{ padding: 8px 16px; font-size: 14px; border-radius: 6px; }}
.cf-btn-block {{ width: 100%; padding: 14px; }}

.cf-btn-outline {{
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  background: transparent; color: var(--cf-text);
  border: 1.5px solid var(--cf-border-strong);
  font-family: {FONT_STACK}; font-weight: 600; font-size: 15px;
  padding: 12px 24px; border-radius: 8px; cursor: pointer; transition: all .15s;
  text-decoration: none;
}}
.cf-btn-outline:hover {{ border-color: var(--cf-text); background: var(--cf-bg-soft); }}

.cf-btn-ghost {{
  display: inline-flex; align-items: center; gap: 6px;
  background: transparent; color: var(--cf-text-muted); border: none;
  font-family: {FONT_STACK}; font-weight: 500; font-size: 14px;
  padding: 8px 14px; border-radius: 6px; cursor: pointer; transition: all .15s;
}}
.cf-btn-ghost:hover {{ background: var(--cf-bg-soft); color: var(--cf-text); }}

.cf-btn-dark {{
  background: #fff; color: var(--cf-darker);
  font-family: {FONT_STACK}; font-weight: 600; font-size: 15px;
  padding: 12px 24px; border-radius: 8px; border: none; cursor: pointer; transition: all .15s;
}}
.cf-btn-dark:hover {{ background: #f0f0f0; transform: translateY(-1px); }}

/* ── Streamlit st.button → cf-btn by default ── */
.stButton > button {{
  background: var(--cf-red) !important;
  color: #fff !important;
  border: none !important;
  font-family: {FONT_STACK} !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  padding: 12px 24px !important;
  border-radius: 8px !important;
  transition: all .18s ease !important;
  box-shadow: none !important;
  width: 100%;
}}
.stButton > button:hover {{
  background: var(--cf-red-dark) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255,56,92,.25) !important;
}}
.stButton > button:focus:not(:active) {{
  border: none !important;
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(255,56,92,.18) !important;
  color: #fff !important;
}}

/* Secondary buttons → cf-btn-outline style */
.stButton > button[kind="secondary"] {{
  background: transparent !important;
  color: var(--cf-text) !important;
  border: 1.5px solid var(--cf-border-strong) !important;
}}
.stButton > button[kind="secondary"]:hover {{
  border-color: var(--cf-text) !important;
  background: var(--cf-bg-soft) !important;
  color: var(--cf-text) !important;
  transform: none !important;
  box-shadow: none !important;
}}

/* ── Inputs ── */
.cf-input {{
  width: 100%;
  background: #fff; border: 1.5px solid var(--cf-border-strong);
  border-radius: 8px; padding: 12px 14px;
  font-family: {FONT_STACK}; font-size: 15px; color: var(--cf-text);
  transition: border-color .15s, box-shadow .15s;
}}
.cf-input::placeholder {{ color: var(--cf-text-faint); }}
.cf-input:focus {{ outline: none; border-color: var(--cf-text); box-shadow: 0 0 0 3px rgba(34,34,34,.05); }}
.cf-label {{ display: block; font-size: 14px; font-weight: 500; color: var(--cf-text); margin-bottom: 6px; }}

/* Streamlit text_input → cf-input style */
[data-testid="stTextInput"] label,
[data-testid="stTextArea"]  label {{
  font-size: 14px !important;
  font-weight: 500 !important;
  color: var(--cf-text) !important;
  margin-bottom: 6px !important;
}}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"]  textarea {{
  background: #fff !important;
  border: 1.5px solid var(--cf-border-strong) !important;
  border-radius: 8px !important;
  padding: 12px 14px !important;
  font-family: {FONT_STACK} !important;
  font-size: 15px !important;
  color: var(--cf-text) !important;
  transition: border-color .15s, box-shadow .15s !important;
  box-shadow: none !important;
}}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"]  textarea:focus {{
  border-color: var(--cf-text) !important;
  box-shadow: 0 0 0 3px rgba(34,34,34,.05) !important;
  outline: none !important;
}}

/* ── Cards ── */
.cf-card {{
  background: #fff; border: 1px solid var(--cf-border);
  border-radius: 16px; padding: 24px;
  transition: box-shadow .18s, transform .18s;
}}
.cf-card-hover:hover {{ box-shadow: var(--shadow-md); transform: translateY(-2px); }}
.cf-card-soft {{ background: var(--cf-bg-soft); border-radius: 16px; padding: 24px; }}

/* ── Pills / tags ── */
.cf-pill {{
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--cf-red-tint); color: var(--cf-red);
  font-size: 13px; font-weight: 600; padding: 6px 14px; border-radius: 20px;
}}
.cf-pill-light {{
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--cf-bg-soft); color: var(--cf-text-mid);
  font-size: 13px; font-weight: 500; padding: 6px 14px; border-radius: 20px;
}}
.cf-pill-dark {{
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(255,255,255,.1); color: rgba(255,255,255,.85);
  font-size: 12px; font-weight: 600; padding: 6px 14px; border-radius: 20px;
  border: 1px solid rgba(255,255,255,.15);
  letter-spacing: 0.5px; text-transform: uppercase;
}}

/* ── Logo ── */
.cf-logo     {{ display: inline-flex; align-items: center; gap: 8px; font-size: 19px; font-weight: 800; color: var(--cf-red); }}
.cf-logo-lg  {{ font-size: 28px; }}
.cf-logo-dark {{ color: #fff; }}
.cf-logo-icon {{ font-size: 22px; }}

/* ── Marketing nav (pre-login) ── */
.cf-nav {{
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 40px; border-bottom: 1px solid var(--cf-border); background: #fff;
}}
.cf-nav-links {{ display: flex; align-items: center; gap: 6px; }}
.cf-nav-link {{
  font-size: 14px; font-weight: 500; color: var(--cf-text-mid);
  padding: 8px 14px; border-radius: 6px; cursor: pointer; transition: background .15s;
}}
.cf-nav-link:hover {{ background: var(--cf-bg-soft); color: var(--cf-text); }}

/* ── App nav (post-login) ── */
.cf-appnav {{
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 32px; border-bottom: 1px solid var(--cf-border); background: #fff;
}}
.cf-appnav-right {{ display: flex; align-items: center; gap: 4px; }}
.cf-appnav-link {{
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 14px; font-weight: 500; color: var(--cf-text-muted);
  padding: 8px 14px; border-radius: 8px; cursor: pointer; transition: all .15s;
  text-decoration: none;
}}
.cf-appnav-link:hover {{ background: var(--cf-bg-soft); color: var(--cf-text); }}
.cf-appnav-link-active {{ background: var(--cf-red-tint); color: var(--cf-red); font-weight: 600; }}
.cf-appnav-avatar {{
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, var(--cf-red), var(--cf-red-dark));
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-weight: 700; font-size: 14px;
  margin-left: 6px; cursor: pointer;
}}

/* ── Tabs ── */
.cf-tabs {{ display: flex; border-bottom: 2px solid var(--cf-border); }}
.cf-tab {{
  padding: 12px 16px; font-size: 15px; font-weight: 500;
  color: var(--cf-text-muted); border-bottom: 2px solid transparent;
  margin-bottom: -2px; cursor: pointer; transition: color .15s;
}}
.cf-tab:hover {{ color: var(--cf-text); }}
.cf-tab-active {{ color: var(--cf-text); border-bottom-color: var(--cf-text); font-weight: 600; }}

/* Streamlit native tabs */
.stTabs [data-baseweb="tab-list"] {{ gap: 0; border-bottom: 2px solid var(--cf-border); }}
.stTabs [data-baseweb="tab"] {{
  padding: 12px 16px; font-size: 15px; font-weight: 500;
  color: var(--cf-text-muted); background: transparent;
}}
.stTabs [aria-selected="true"] {{ color: var(--cf-text) !important; font-weight: 600 !important; }}
.stTabs [data-baseweb="tab-highlight"] {{ background-color: var(--cf-text) !important; height: 2px !important; }}

/* ── Chat bubbles ── */
.cf-bubble-user {{
  background: var(--cf-red); color: #fff;
  border-radius: 18px 18px 4px 18px;
  padding: 10px 16px; font-size: 14.5px; line-height: 1.5;
  max-width: 70%; align-self: flex-end;
}}
.cf-bubble-ai {{
  background: var(--cf-bg-soft); color: var(--cf-text);
  border-radius: 18px 18px 18px 4px;
  padding: 10px 16px; font-size: 14.5px; line-height: 1.5;
  max-width: 78%; align-self: flex-start;
}}

/* ── Metric tile ── */
.cf-metric {{ background: var(--cf-bg-soft); border: 1px solid var(--cf-border); border-radius: 12px; padding: 20px 22px; }}
.cf-metric-label {{ font-size: 13px; font-weight: 500; color: var(--cf-text-muted); margin-bottom: 6px; }}
.cf-metric-value {{ font-size: 28px; font-weight: 700; color: var(--cf-text); letter-spacing: -0.5px; }}
.cf-metric-sub   {{ font-size: 12px; color: var(--cf-text-muted); margin-top: 2px; }}

/* ── Chart card (st.container border=True) ── */
[data-testid="stVerticalBlockBorderWrapper"] {{
  background: #fff !important;
  border: 1px solid var(--cf-border) !important;
  border-radius: 16px !important;
  padding: 20px 22px !important;
  box-shadow: none !important;
}}
.chart-head {{ margin-bottom: 8px; }}
.chart-head h4 {{ margin: 0 0 2px; font-size: 15px; font-weight: 700; color: var(--cf-text); }}
.sub {{ font-size: 13px; color: var(--cf-text-muted); margin: 0; }}

/* ── Misc ── */
.cf-hr {{ border: none; border-top: 1px solid var(--cf-border); margin: 0; }}
.cf-or-divider {{ display: flex; align-items: center; gap: 12px; margin: 4px 0; }}
.cf-or-divider .line {{ flex: 1; border-top: 1px solid var(--cf-border); }}
.cf-avatar {{ width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 700; font-size: 14px; }}
.cf-avatar-sm {{ width: 30px; height: 30px; font-size: 12px; }}
.cf-trust-strip {{ background: var(--cf-bg-soft); border-radius: 12px; padding: 12px 18px; margin-top: 18px; text-align: center; }}
.cf-connection-row {{ display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 8px; transition: background .15s; }}
.cf-connection-row:hover {{ background: var(--cf-bg-soft); }}

/* ── Progress bar ── */
.stProgress > div > div {{ background: var(--cf-red) !important; }}

/* ── Alerts ── */
.stAlert {{ border-radius: 10px !important; font-family: {FONT_STACK} !important; }}

/* ── Hide "Press Enter to apply" hint on text inputs ── */
[data-testid="InputInstructions"] {{ display: none !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: #DDD; border-radius: 3px; }}
</style>
"""

_HIDE_SIDEBAR = """<style>
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stHeader"],
[data-testid="stDecoration"],
#stDecoration {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none; }}
section[data-testid="stSidebar"] {{ display: none !important; }}
</style>"""


def inject_styles(hide_sidebar: bool = True) -> None:
    """Inject the full CSS theme into the current Streamlit page. Call once at app start."""
    st.markdown(CSS, unsafe_allow_html=True)
    if hide_sidebar:
        st.markdown(_HIDE_SIDEBAR, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
# HTML COMPONENT BUILDERS
# ───────────────────────────────────────────────────────────────
def logo(size: str = "md", dark: bool = False) -> str:
    cls = "cf-logo" + (" cf-logo-lg" if size == "lg" else "") + (" cf-logo-dark" if dark else "")
    return f'<div class="{cls}"><span class="cf-logo-icon">🔗</span> Connect-IQ</div>'


def pill(text: str, variant: str = "red") -> str:
    cls = {"red": "cf-pill", "light": "cf-pill-light", "dark": "cf-pill-dark"}[variant]
    return f'<span class="{cls}">{text}</span>'


def metric_tile(label: str, value: str, sub: str = "") -> str:
    sub_html = f'<div class="cf-metric-sub">{sub}</div>' if sub else ""
    return (
        f'<div class="cf-metric">'
        f'<div class="cf-metric-label">{label}</div>'
        f'<div class="cf-metric-value">{value}</div>'
        f"{sub_html}</div>"
    )


def card(content_html: str, soft: bool = False, padding: int = 24, radius: int = 16) -> str:
    cls = "cf-card-soft" if soft else "cf-card"
    return f'<div class="{cls}" style="padding:{padding}px;border-radius:{radius}px">{content_html}</div>'


def or_divider() -> str:
    return (
        '<div class="cf-or-divider">'
        '<div class="line"></div>'
        '<span class="cf-small">or</span>'
        '<div class="line"></div>'
        '</div>'
    )


def trust_strip(text: str = "🔒 Your data is encrypted and only accessible to you.") -> str:
    return f'<div class="cf-trust-strip"><span class="cf-small">{text}</span></div>'


@contextmanager
def chart_card(title: str, subtitle: str):
    """Bordered chart card with header. Use as: `with chart_card(title, subtitle): ...`"""
    with st.container(border=True):
        st.markdown(
            f'<div class="chart-head">'
            f'<h4>{title}</h4>'
            f'<p class="sub">{subtitle}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        yield


def marketing_nav() -> str:
    return f"""
    <div class="cf-nav">
      {logo()}
      <div class="cf-nav-links">
        <span class="cf-nav-link">Features</span>
        <span class="cf-nav-link">How it works</span>
        <span class="cf-nav-link">About</span>
        <span class="cf-nav-link">FAQ</span>
      </div>
      <div style="display:flex;gap:10px;align-items:center;">
        <button class="cf-btn-outline cf-btn-sm">Log in</button>
        <button class="cf-btn cf-btn-sm">Sign up free</button>
      </div>
    </div>
    """