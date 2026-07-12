import re
import streamlit as st

from components.styles import inject_styles
from components.nav import render_app_nav
from utils.auth import require_auth, get_user_id
from utils.data_processor import get_connections
from utils.llm import get_chat_response
from utils.chat_store import _MSG_STORE, clear_user as _clear_user_msgs

st.set_page_config(
    page_title="Connect-IQ – Chat",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles(hide_sidebar=True)

require_auth()

render_app_nav(active="chat")

user_id = get_user_id()

# ── Load connections ───────────────────────────────────────────────────────────
if (
    "connections_df" not in st.session_state
    or st.session_state.get("connections_user_id") != user_id
):
    with st.spinner("Loading your connections…"):
        st.session_state.connections_df = get_connections(user_id)
        st.session_state.connections_user_id = user_id

df = st.session_state.connections_df
total = len(df)

# ── Page-specific CSS ──────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp { background: #fff !important; }
    .main, .block-container {
      background: transparent !important;
      padding-top: 1.2rem !important;
      max-width: 1100px !important;
      margin-left: auto !important;
      margin-right: auto !important;
    }
    [data-testid="column"], [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > div { background: transparent !important; }

    /* Constrain bottom chat-input bar to match content column */
    [data-testid="stBottom"] { background:#fff; border-top:1px solid #EBEBEB; }
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"],
    [data-testid="stBottom"] .block-container {
      max-width: 1100px !important;
      margin: 0 auto !important;
      padding-left: 40px !important;
      padding-right: 40px !important;
    }
    /* Soft rounded input to match the design */
    [data-testid="stChatInput"] {
      background: #F7F7F7 !important;
      border: 1.5px solid transparent !important;
      border-radius: 12px !important;
    }
    [data-testid="stChatInput"]:focus-within { border-color: #FF385C !important; }

    /* Status chip */
    .status-chip {
      display:inline-flex; align-items:center; gap:8px;
      background:#F7F7F7; border-radius:20px; padding:8px 16px; white-space:nowrap;
    }
    .status-chip .dot { width:8px; height:8px; background:#FF385C; border-radius:50%; display:inline-block; flex-shrink:0; }
    .status-chip .muted { color:#717171; font-size:13px; }
    .status-chip .accent { color:#FF385C; font-weight:700; font-size:13px; }

    /* Chat bubbles */
    .row-user { display:flex; justify-content:flex-end; margin:8px 0; }
    .row-ai   { display:flex; justify-content:flex-start; gap:10px; margin:8px 0; align-items:flex-start; }
    .bubble-user {
      background:#FF385C; color:#fff; border-radius:18px 18px 4px 18px;
      padding:10px 16px; font-size:14.5px; line-height:1.5; max-width:70%;
    }
    .bubble-ai {
      background:#F7F7F7; color:#222; border-radius:18px 18px 18px 4px;
      padding:12px 16px; font-size:14.5px; line-height:1.6; max-width:85%;
    }
    .ai-avatar {
      width:32px; height:32px; border-radius:50%; flex-shrink:0;
      background:linear-gradient(135deg,#FF385C,#E31C5F);
      display:inline-flex; align-items:center; justify-content:center; font-size:14px;
    }

    /* Example prompt chips */
    #cf-ex-start ~ [data-testid="stHorizontalBlock"] .stButton > button {
      background: #fff !important;
      border: 1px solid #EBEBEB !important;
      border-radius: 8px !important;
      color: #484848 !important;
      font-weight: 500 !important;
      font-size: 12px !important;
      padding: 5px 10px !important;
      line-height: 1.3 !important;
      text-align: center !important;
      white-space: normal !important;
      min-height: 0 !important;
      box-shadow: none !important;
      transition: all .15s !important;
    }
    #cf-ex-start ~ [data-testid="stHorizontalBlock"] .stButton > button:hover {
      border-color: #FF385C !important;
      color: #FF385C !important;
      background: #FFE8EE !important;
      transform: none !important;
    }

</style>
    """,
    unsafe_allow_html=True,
)

# ── Empty state ────────────────────────────────────────────────────────────────
if df.empty:
    st.info(
        "📤 You haven't uploaded your connections yet. "
        "Head to the Dashboard first to upload your LinkedIn CSV."
    )
    if st.button("Go to Dashboard →", key="goto_dash", type="primary"):
        st.switch_page("pages/2_Home.py")
    st.stop()

# ── Header ─────────────────────────────────────────────────────────────────────
hdr_l, hdr_r = st.columns([4, 1.5])
with hdr_l:
    st.markdown(
        '<h1 style="margin:0 0 4px;font-size:26px;font-weight:800;letter-spacing:-.5px;color:#222;">'
        "Chat with AI to understand your network better</h1>"
        '<p style="color:#717171;font-size:14.5px;line-height:1.6;margin:0;">'
        "Ask anything about your LinkedIn connections. Answers are grounded in your "
        "actual data via RAG — no hallucinations.</p>",
        unsafe_allow_html=True,
    )
with hdr_r:
    st.markdown(
        f'<div style="display:flex;justify-content:flex-end;align-items:center;height:100%;padding-top:8px;">'
        f'<span class="status-chip">'
        f'<span class="dot"></span>'
        f'<span class="muted">Analyzing</span>&nbsp;'
        f'<span class="accent">{total:,} connections</span>'
        f'</span></div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr style="margin:16px 0;">', unsafe_allow_html=True)

# ── Example prompts ────────────────────────────────────────────────────────────
st.markdown(
    '<p style="font-size:13px;font-weight:600;color:#484848;margin:0 0 10px;">Try asking:</p>',
    unsafe_allow_html=True,
)

EXAMPLES = [
    "List all recruiters I'm connected with",
    "Who do I know at Google or Meta?",
    "Show connections in the Finance industry",
    "Who are the CEOs or founders in my network?",
    "List all software engineers I know",
    "Who works at startups or early-stage companies?",
]

st.markdown('<div id="cf-ex-start"></div>', unsafe_allow_html=True)
ex_cols = st.columns(3)
for i, example in enumerate(EXAMPLES):
    with ex_cols[i % 3]:
        if st.button(example, key=f"ex_{i}", width="stretch"):
            st.session_state.setdefault("messages", [])
            st.session_state.messages.append({"role": "user", "content": example})
            st.session_state.pending_ai_response = True
            st.rerun()

st.markdown('<hr style="margin:16px 0 12px;">', unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
def _md_to_html(text: str) -> str:
    """Convert common LLM markdown patterns to HTML for use inside chat bubbles."""
    # Markdown links must be converted before bold/italic to avoid conflicts
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^\)]+)\)",
        r'<a href="\2" target="_blank" rel="noopener noreferrer" '
        r'style="color:#0077B5;font-weight:600;text-decoration:none;">\1</a>',
        text,
    )
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*",     r"<em>\1</em>",         text)
    text = text.replace("\n", "<br>")
    return text


# ── Chat history ───────────────────────────────────────────────────────────────
# On a fresh session (new page load / page navigation), restore from the
# module-level store.  On subsequent reruns within the same session, the
# assignment below keeps the store reference in sync so that appends made
# later in this script are automatically visible to future fresh sessions.
if "messages" not in st.session_state:
    st.session_state.messages = list(_MSG_STORE.get(user_id, []))
_MSG_STORE[user_id] = st.session_state.messages

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="row-user"><div class="bubble-user">{msg["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="row-ai">'
            f'<div class="ai-avatar">🤖</div>'
            f'<div class="bubble-ai">{_md_to_html(msg["content"])}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Respond to example-button click ───────────────────────────────────────────
if st.session_state.get("pending_ai_response") and st.session_state.get("messages"):
    st.session_state.pending_ai_response = False
    last_q = st.session_state.messages[-1]["content"]
    with st.spinner("Searching your network…"):
        answer = get_chat_response(last_q, user_id, total, st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

# ── Live chat input ────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about your connections…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Searching your network…"):
        answer = get_chat_response(prompt, user_id, total, st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .chat-footer-row {
        display:flex; align-items:center; justify-content:space-between;
        margin-top:16px; padding-top:12px; border-top:1px solid #EBEBEB;
    }
    /* Clear chat = inline text link, not a full button */
    .chat-footer-row + div [data-testid="clear_chat_btn"] button,
    [data-testid="clear_chat_btn"] button {
        background: transparent !important;
        color: #717171 !important;
        border: none !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        padding: 2px 0 !important;
        width: auto !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        min-height: 0 !important;
        text-decoration: none !important;
        cursor: pointer !important;
    }
    [data-testid="clear_chat_btn"] button:hover {
        background: transparent !important;
        color: #D92D20 !important;
        transform: none !important;
        text-decoration: underline !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="chat-footer-row">'
    '<span style="font-size:13px;color:#717171;">'
    "Powered by Gemini 2.5 Flash · Grounded in your data"
    "</span>",
    unsafe_allow_html=True,
)
if st.button("🗑 Clear chat", key="clear_chat_btn"):
    st.session_state["confirm_clear_chat"] = True
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.get("confirm_clear_chat"):
    st.warning(
        "Clear all messages in this conversation? This cannot be undone.",
        icon="⚠️",
    )
    ok_col, cancel_col, _ = st.columns([1, 1, 5])
    with ok_col:
        if st.button("Yes, clear", key="confirm_clear_yes", type="primary"):
            st.session_state.messages = []
            _clear_user_msgs(user_id)
            st.session_state.pop("confirm_clear_chat", None)
            st.rerun()
    with cancel_col:
        if st.button("Cancel", key="confirm_clear_no", type="secondary"):
            st.session_state.pop("confirm_clear_chat", None)
            st.rerun()
