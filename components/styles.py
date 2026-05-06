import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset Streamlit chrome ── */
#MainMenu, footer, .stDeployButton { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }

/* ── Base ── */
.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background-color: #FFFFFF;
    color: #222222;
}

/* ── Buttons ── */
.stButton > button {
    background-color: #FF385C !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 10px 22px !important;
    transition: background-color 0.18s ease, transform 0.1s ease !important;
    box-shadow: none !important;
}
.stButton > button:hover {
    background-color: #E31C5F !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Secondary outlined button — add class "secondary" via markdown workaround not possible;
   we'll rely on key-based targeting via the outline variant */
button[kind="secondary"] {
    background-color: transparent !important;
    color: #222222 !important;
    border: 1.5px solid #DDDDDD !important;
}
button[kind="secondary"]:hover {
    background-color: #F7F7F7 !important;
    border-color: #AAAAAA !important;
}

/* ── Inputs ── */
.stTextInput input, .stTextInput textarea {
    border-radius: 8px !important;
    border: 1.5px solid #DDDDDD !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
    background: #FFFFFF !important;
    color: #222222 !important;
}
.stTextInput input:focus {
    border-color: #222222 !important;
    box-shadow: none !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 2px solid #EBEBEB;
}
.stTabs [data-baseweb="tab"] {
    font-size: 15px;
    font-weight: 500;
    color: #717171;
    padding: 10px 16px;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    color: #222222 !important;
    border-bottom-color: #222222 !important;
    font-weight: 600 !important;
}

/* ── Metrics ── */
div[data-testid="metric-container"] {
    background: #F7F7F7;
    border-radius: 12px;
    padding: 18px 20px;
    border: 1px solid #EBEBEB;
}
div[data-testid="metric-container"] label {
    color: #717171 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #222222 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #F7F7F7 !important;
    border-right: 1px solid #EBEBEB !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    text-align: left !important;
    justify-content: flex-start !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #1D4ED8 !important;
    transform: none !important;
}

/* Active nav item (logout) */
section[data-testid="stSidebar"] .stButton > button[data-testid*="logout"] {
    color: #FF385C !important;
    border-color: #FFD0D8 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed #DDDDDD !important;
    border-radius: 12px !important;
    background: #FAFAFA !important;
}

/* ── Chat ── */
.stChatMessage {
    border-radius: 12px !important;
    padding: 4px 0 !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background-color: #FF385C !important;
}

/* ── Expander ── */
details {
    border: 1px solid #EBEBEB !important;
    border-radius: 10px !important;
    background: #FAFAFA !important;
}

/* ── Divider ── */
hr {
    border-color: #EBEBEB !important;
    margin: 20px 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F7F7F7; }
::-webkit-scrollbar-thumb { background: #CCCCCC; border-radius: 3px; }
</style>
"""

# Additional CSS for landing page (no sidebar)
_HIDE_SIDEBAR = """
<style>
section[data-testid="stSidebar"] { display: none !important; }
</style>
"""


def inject_styles(hide_sidebar: bool = False) -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
    if hide_sidebar:
        st.markdown(_HIDE_SIDEBAR, unsafe_allow_html=True)
