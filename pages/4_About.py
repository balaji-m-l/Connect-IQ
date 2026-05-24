import streamlit as st

from components.styles import inject_styles
from components.nav import render_nav
from utils.auth import is_authenticated

st.set_page_config(
    page_title="Connect-IQ – About",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles(hide_sidebar=True)

if not is_authenticated():
    st.switch_page("pages/1_Login.py")

render_nav(active="about")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    '<h1 style="margin:0 0 6px;font-size:1.8rem;font-weight:800;color:#222222;">About Connect-IQ</h1>'
    '<p style="color:#717171;font-size:.95rem;margin:0 0 36px;">'
    "Learn how the app works and what powers it under the hood."
    "</p>",
    unsafe_allow_html=True,
)

# ── Tech stack tiles ──────────────────────────────────────────────────────────
st.markdown(
    '<h2 style="font-size:1.2rem;font-weight:700;color:#222222;margin:0 0 20px;">Tech Stack</h2>',
    unsafe_allow_html=True,
)

t1, t2, t3, t4 = st.columns(4, gap="medium")

_TILE = (
    '<div style="background:#F7F7F7;border-radius:16px;padding:28px 22px;'
    'border:1px solid #EBEBEB;height:100%;">'
    '<div style="font-size:2rem;margin-bottom:14px;">{icon}</div>'
    '<h3 style="font-size:1rem;font-weight:700;color:#222222;margin:0 0 8px;">{name}</h3>'
    '<p style="color:#717171;font-size:.85rem;line-height:1.6;margin:0;">{desc}</p>'
    "</div>"
)

with t1:
    st.markdown(
        _TILE.format(
            icon="🎈",
            name="Streamlit",
            desc="Multi-page Python web framework that turns data scripts into shareable apps with zero front-end code.",
        ),
        unsafe_allow_html=True,
    )
with t2:
    st.markdown(
        _TILE.format(
            icon="🗄️",
            name="Supabase",
            desc="PostgreSQL database with Row Level Security, Supabase Auth, and pgvector for storing connection embeddings.",
        ),
        unsafe_allow_html=True,
    )
with t3:
    st.markdown(
        _TILE.format(
            icon="✨",
            name="Google Gemini",
            desc="gemini-embedding-001 generates 768-dim vector embeddings; Gemini 2.5 Flash powers the RAG chat responses.",
        ),
        unsafe_allow_html=True,
    )
with t4:
    st.markdown(
        _TILE.format(
            icon="🔍",
            name="pgvector",
            desc="PostgreSQL extension that stores and indexes embedding vectors with HNSW cosine-similarity search.",
        ),
        unsafe_allow_html=True,
    )

st.markdown("<br><br>", unsafe_allow_html=True)

# ── RAG architecture ──────────────────────────────────────────────────────────
st.markdown(
    '<h2 style="font-size:1.2rem;font-weight:700;color:#222222;margin:0 0 16px;">How the AI Chat Works (RAG)</h2>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div style="background:#18181B;border-radius:16px;padding:28px 32px;">'
    '<pre style="color:#A1A1AA;font-family:monospace;font-size:.82rem;line-height:1.8;margin:0;">'
    "Upload CSV\n"
    "    │\n"
    "    ▼\n"
    "Parse connections → Generate embeddings (gemini-embedding-001, 768-dim)\n"
    "    │\n"
    "    ▼\n"
    "Store in Supabase pgvector  (vector(768) + HNSW index)\n"
    "\n"
    "Chat query\n"
    "    │\n"
    "    ▼\n"
    "Embed question → Cosine similarity search (top-100)\n"
    "    + Keyword stem boost  (recruiter → recruit → 'Digital Recruiter' ✓)\n"
    "    │\n"
    "    ▼\n"
    "Retrieved connections → Gemini 2.5 Flash → Grounded answer"
    "</pre>"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── FAQ ────────────────────────────────────────────────────────────────────────
st.markdown(
    '<h2 style="font-size:1.2rem;font-weight:700;color:#222222;margin:0 0 16px;">Frequently Asked Questions</h2>',
    unsafe_allow_html=True,
)

FAQ = [
    (
        "Where does my data go?",
        "Your connections are stored in **your own** Supabase project — not on any shared server. "
        "Row Level Security (RLS) ensures only your authenticated account can read your data.",
    ),
    (
        "How do I export my LinkedIn connections?",
        "Go to **LinkedIn → Me → Settings & Privacy → Data Privacy → Get a copy of your data**, "
        "select **Connections**, then request the archive. You'll receive an email with a ZIP file "
        "containing `Connections.csv`.",
    ),
    (
        "Can I upload multiple CSV files?",
        "Yes — uploads are **additive**. Each new file is checked against existing records and only "
        "truly new connections (matched on first name + last name + company) are inserted. "
        "Duplicates are skipped automatically.",
    ),
    (
        "Why does the AI sometimes miss a connection?",
        "The RAG pipeline retrieves the top-100 closest matches by vector similarity, then adds "
        "keyword-boosted results using stemmed search terms. Very unusual job titles that don't "
        "appear anywhere in the query may still be missed — try rephrasing the question.",
    ),
    (
        "Is the app free to use?",
        "The app itself is open source and free. You'll need a **Supabase** account (free tier works) "
        "and a **Google AI Studio** API key (free tier: 15 req/min; paid tier: 1,500 req/min).",
    ),
    (
        "How do I delete my connections?",
        "You can delete all your connections directly from your Supabase dashboard by running: "
        "`DELETE FROM public.connections WHERE user_id = '<your-user-id>';`",
    ),
]

for question, answer in FAQ:
    with st.expander(question):
        st.markdown(answer)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<hr style="margin:0 0 12px;">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#AAAAAA;font-size:.82rem;padding:0 0 8px;">'
    "© 2025 Connect-IQ · MIT License · "
    '<a href="https://github.com" style="color:#AAAAAA;">GitHub</a>'
    "</p>",
    unsafe_allow_html=True,
)