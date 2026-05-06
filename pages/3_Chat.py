import streamlit as st

from components.styles import inject_styles
from components.sidebar import render_sidebar
from utils.auth import is_authenticated, get_user_id
from utils.data_processor import get_connections
from utils.llm import get_chat_response

st.set_page_config(
    page_title="ConnectionsFun – Chat",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

if not is_authenticated():
    st.switch_page("pages/1_Login.py")

render_sidebar()

user_id = get_user_id()

# ── Load connections (count only — RAG pulls from DB at query time) ───────────
if (
    "connections_df" not in st.session_state
    or st.session_state.get("connections_user_id") != user_id
):
    with st.spinner("Loading your connections…"):
        st.session_state.connections_df = get_connections(user_id)
        st.session_state.connections_user_id = user_id

df = st.session_state.connections_df
total = len(df)

# ── Page header ──────────────────────────────────────────────────────────────
hdr_l, hdr_r = st.columns([5, 1])
with hdr_l:
    st.markdown(
        '<h1 style="margin:0;font-size:1.8rem;font-weight:800;color:#222222;">'
        "Chat with Your Network"
        "</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#717171;font-size:.95rem;margin:6px 0 0;">'
        "Ask anything about your LinkedIn connections. "
        "Answers are grounded in your actual data via RAG — no hallucinations."
        "</p>",
        unsafe_allow_html=True,
    )
with hdr_r:
    if st.button("📤 Upload CSV", key="upload_btn", use_container_width=True):
        st.switch_page("pages/2_Home.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── Empty state ──────────────────────────────────────────────────────────────
if df.empty:
    st.info(
        "📤 You haven't uploaded your connections yet. "
        "Head to the Dashboard first to upload your LinkedIn CSV."
    )
    if st.button("Go to Dashboard →", key="goto_dash"):
        st.switch_page("pages/2_Home.py")
    st.stop()

# ── Connection count badge ────────────────────────────────────────────────────
st.markdown(
    f'<div style="display:inline-flex;align-items:center;gap:8px;'
    f'background:#F7F7F7;border-radius:20px;padding:8px 18px;margin-bottom:20px;">'
    f'<span style="width:8px;height:8px;background:#FF385C;border-radius:50%;'
    f'display:inline-block;"></span>'
    f'<span style="color:#717171;font-size:.88rem;">Analyzing </span>'
    f'<span style="color:#FF385C;font-weight:700;font-size:.88rem;">'
    f"{total:,} connections</span>"
    f"</div>",
    unsafe_allow_html=True,
)

# ── Example prompts ───────────────────────────────────────────────────────────
st.markdown(
    '<p style="font-weight:600;font-size:.92rem;color:#484848;margin-bottom:10px;">'
    "Try asking:</p>",
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

ex_cols = st.columns(3)
for i, example in enumerate(EXAMPLES):
    with ex_cols[i % 3]:
        if st.button(example, key=f"ex_{i}", use_container_width=True):
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"role": "user", "content": example})
            st.session_state.pending_ai_response = True
            st.rerun()

st.markdown('<hr style="margin:22px 0 16px;">', unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Respond to example-button clicks (requires a rerun to render user msg first) ─
if st.session_state.get("pending_ai_response") and st.session_state.messages:
    st.session_state.pending_ai_response = False
    last_q = st.session_state.messages[-1]["content"]

    with st.chat_message("assistant"):
        with st.spinner("Searching your network…"):
            answer = get_chat_response(
                last_q, user_id, total, st.session_state.messages
            )
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

# ── Live chat input ───────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about your connections…"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching your network…"):
            answer = get_chat_response(
                prompt, user_id, total, st.session_state.messages
            )
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# ── Clear conversation ────────────────────────────────────────────────────────
if st.session_state.get("messages"):
    st.markdown("<br>", unsafe_allow_html=True)
    _, clear_col, _ = st.columns([5, 1, 5])
    with clear_col:
        if st.button("🗑️ Clear chat", key="clear_chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
