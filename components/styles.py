import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Reset Streamlit chrome ── */
#MainMenu, footer, .stDeployButton { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Design tokens ── */
:root {
    --cf-red:         #FF385C;
    --cf-red-dark:    #E31C5F;
    --cf-red-tint:    #FFE8EE;
    --cf-text:        #222222;
    --cf-text-mid:    #484848;
    --cf-text-muted:  #717171;
    --cf-text-faint:  #AAAAAA;
    --cf-bg:          #FFFFFF;
    --cf-bg-soft:     #F7F7F7;
    --cf-border:      #EBEBEB;
    --cf-border-md:   #DDDDDD;
    --cf-teal:        #00A699;
    --shadow-sm:      0 2px 12px rgba(0,0,0,.07);
    --shadow-md:      0 4px 20px rgba(0,0,0,.08);
    --shadow-lg:      0 8px 32px rgba(0,0,0,.12);
}

/* ── Base ── */
.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #FFFFFF;
    color: var(--cf-text);
}

/* ── Primary buttons ── */
.stButton > button {
    background: var(--cf-red) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 10px 22px !important;
    transition: background .18s ease, transform .1s ease !important;
    box-shadow: none !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: var(--cf-red-dark) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Nav link buttons (ghost style) ── */
div[data-testid="stHorizontalBlock"] .stButton > button {
    background: transparent !important;
    color: var(--cf-text-muted) !important;
    border: none !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 8px 14px !important;
    border-radius: 8px !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: var(--cf-bg-soft) !important;
    color: var(--cf-text) !important;
    transform: none !important;
}

/* ── Restore primary button style inside horizontal blocks ── */
div[data-testid="stHorizontalBlock"] [data-testid="baseButton-primary"] {
    background: var(--cf-red) !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
div[data-testid="stHorizontalBlock"] [data-testid="baseButton-primary"]:hover {
    background: var(--cf-red-dark) !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs ── */
.stTextInput input {
    border-radius: 8px !important;
    border: 1.5px solid var(--cf-border-md) !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
    background: #FFFFFF !important;
    color: var(--cf-text) !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput input:focus {
    border-color: var(--cf-text) !important;
    box-shadow: 0 0 0 3px rgba(34,34,34,.05) !important;
}
.stTextInput input::placeholder { color: var(--cf-text-faint) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 2px solid var(--cf-border);
}
.stTabs [data-baseweb="tab"] {
    font-size: 15px;
    font-weight: 500;
    color: var(--cf-text-muted);
    padding: 10px 16px;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    font-family: 'Inter', sans-serif;
}
.stTabs [aria-selected="true"] {
    color: var(--cf-text) !important;
    border-bottom-color: var(--cf-text) !important;
    font-weight: 600 !important;
}

/* ── Metrics ── */
div[data-testid="metric-container"] {
    background: var(--cf-bg-soft);
    border: 1px solid var(--cf-border);
    border-radius: 12px;
    padding: 20px 22px;
}
div[data-testid="metric-container"] label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--cf-text-muted) !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: var(--cf-text) !important;
    letter-spacing: -0.5px !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--cf-border-md) !important;
    border-radius: 12px !important;
    background: var(--cf-bg-soft) !important;
}

/* ── Chat messages ── */
.stChatMessage {
    border-radius: 12px !important;
}
[data-testid="stChatMessageContent"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 14.5px !important;
    line-height: 1.6 !important;
}

/* ── Progress bar ── */
.stProgress > div > div { background: var(--cf-red) !important; }

/* ── Expander ── */
details {
    border: 1px solid var(--cf-border) !important;
    border-radius: 10px !important;
    background: var(--cf-bg-soft) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #DDD; border-radius: 3px; }

/* ── Divider ── */
hr { border-color: var(--cf-border) !important; margin: 16px 0 !important; }

/* ── Alert / info ── */
.stAlert { border-radius: 10px !important; font-family: 'Inter', sans-serif !important; }
</style>
"""

_HIDE_SIDEBAR = """
<style>section[data-testid="stSidebar"] { display: none !important; }</style>
"""


def inject_styles(hide_sidebar: bool = True) -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
    if hide_sidebar:
        st.markdown(_HIDE_SIDEBAR, unsafe_allow_html=True)
