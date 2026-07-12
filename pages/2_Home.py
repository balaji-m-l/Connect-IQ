import streamlit as st
import pandas as pd

from charts import hbar_chart, area_chart, donut_chart
from components.styles import inject_styles, metric_tile, chart_card
from components.nav import render_app_nav
from utils.auth import require_auth, get_user_id, get_display_name
from utils.data_processor import process_linkedin_file, save_connections, get_connections

st.set_page_config(
    page_title="Connect-IQ – Dashboard",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles(hide_sidebar=True)

require_auth()

render_app_nav(active="dashboard")

# ── Page-level CSS ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp { background: #FFFFFF !important; }
    .main, .block-container {
        background: transparent !important;
        padding-top: 32px !important;
        padding-left: 40px !important;
        padding-right: 40px !important;
        padding-bottom: 40px !important;
    }
    [data-testid="column"], [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > div { background: transparent !important; }

    .upload-panel {
      background: var(--cf-bg-soft);
      border: 2px dashed var(--cf-border-strong);
      border-radius: 14px; padding: 20px 24px; margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

user_id = get_user_id()
display_name = get_display_name()

# ── Load / cache connections ───────────────────────────────────────────────────
if (
    "connections_df" not in st.session_state
    or st.session_state.get("connections_user_id") != user_id
):
    with st.spinner("Loading your connections…"):
        st.session_state.connections_df = get_connections(user_id)
        st.session_state.connections_user_id = user_id

df: pd.DataFrame = st.session_state.connections_df

# Pre-compute stats for the header
total = len(df)
n_companies = (
    df["company"].replace("", pd.NA).dropna().nunique()
    if "company" in df.columns else 0
)

# ── Page header ───────────────────────────────────────────────────────────────
hdr_l, hdr_r = st.columns([4, 1])
with hdr_l:
    welcome = f"Welcome back, {display_name}." if display_name else "Welcome back."
    summary = (
        f'You have <strong style="color:var(--cf-text);">{total:,} connections</strong> across '
        f'<strong style="color:var(--cf-text);">{n_companies:,} companies</strong>.'
        if total else "Upload your LinkedIn connections to get started."
    )
    st.markdown(
        f'<h1 style="margin:0 0 6px;font-size:1.8rem;font-weight:800;color:#222222;">'
        f'Your Network Dashboard</h1>'
        f'<p style="color:#717171;font-size:15px;margin:0;">{welcome} {summary}</p>',
        unsafe_allow_html=True,
    )
with hdr_r:
    st.write("")
    if st.button("📤 Upload CSV", key="upload_toggle", width='stretch', type="primary"):
        st.session_state.show_uploader = not st.session_state.get("show_uploader", False)

st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

# ── Upload panel ───────────────────────────────────────────────────────────────
if st.session_state.get("show_uploader", False):
    st.markdown(
        '<div class="upload-panel">'
        '<h4 style="margin:0 0 6px;font-size:15px;font-weight:700;">Upload LinkedIn Connections Export</h4>'
        '<p style="color:#717171;font-size:.88rem;margin:0;">'
        'Export path: <b>LinkedIn → Settings &amp; Privacy → Data Privacy → Download my data → '
        'Download larger data archive → Request Archive → upload the Connections.csv file here</b>. '
        'New connections are appended; duplicates are skipped automatically.'
        '</p></div>',
        unsafe_allow_html=True,
    )
    uploaded = st.file_uploader(
        "Drop your file here",
        type=["csv", "xlsx", "xls"],
        key="file_uploader",
        label_visibility="collapsed",
    )
    st.caption("Supports CSV, XLSX, XLS · Up to 50 MB")

    btn_col, cancel_col, _ = st.columns([1, 1, 4])
    with btn_col:
        process_clicked = st.button(
            "Process & Save", key="process_btn",
            width='stretch', type="primary", disabled=not uploaded,
        )
    with cancel_col:
        if st.button("Cancel", key="cancel_upload", width='stretch', type="secondary"):
            st.session_state.show_uploader = False
            st.rerun()

    if process_clicked and uploaded:
        parsed_df, parse_err = process_linkedin_file(uploaded)
        if parse_err:
            st.error(parse_err)
        else:
            progress_bar = st.progress(0.0, text="Starting…")
            status = st.empty()

            def _on_progress(pct: float, msg: str) -> None:
                progress_bar.progress(min(pct, 1.0), text=msg)
                status.markdown(
                    f'<p style="color:#717171;font-size:.84rem;">{msg}</p>',
                    unsafe_allow_html=True,
                )

            inserted, dups, save_err = save_connections(user_id, parsed_df, progress_cb=_on_progress)
            progress_bar.empty()
            status.empty()

            if save_err:
                st.error(f"Save failed: {save_err}")
            else:
                parts = [f"✅ Added **{inserted}** new connections."]
                if dups:
                    parts.append(f"Skipped **{dups}** duplicate(s).")
                st.success(" ".join(parts))
                st.session_state.connections_df = get_connections(user_id)
                st.session_state.connections_user_id = user_id
                st.session_state.show_uploader = False
                st.rerun()

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

# Refresh after possible upload
df = st.session_state.get("connections_df", pd.DataFrame())

# ── Empty state ───────────────────────────────────────────────────────────────
if df.empty:
    st.markdown(
        '<div style="text-align:center;padding:80px 20px;background:#F7F7F7;border-radius:16px;">'
        '<div style="font-size:3.5rem;margin-bottom:16px;">📤</div>'
        '<h2 style="color:#222222;font-weight:800;margin-bottom:10px;">Upload your LinkedIn connections</h2>'
        '<p style="color:#717171;max-width:400px;margin:0 auto;">'
        'Click the <b>Upload CSV</b> button above to get started. '
        'Your connections will be embedded and stored securely.'
        '</p></div>',
        unsafe_allow_html=True,
    )
    st.stop()

# ── Metrics ────────────────────────────────────────────────────────────────────
total = len(df)
n_companies = (
    df["company"].replace("", pd.NA).dropna().nunique() if "company" in df.columns else 0
)
n_titles = (
    df["position"].replace("", pd.NA).dropna().nunique() if "position" in df.columns else 0
)
if "company" in df.columns:
    vc = df[df["company"].str.strip() != ""]["company"].value_counts()
    top_co = vc.index[0] if len(vc) else "—"
    top_co_n = int(vc.iloc[0]) if len(vc) else 0
else:
    top_co, top_co_n = "—", 0

st.markdown('<h3 style="margin:8px 0 12px;font-size:15px;font-weight:700;color:#222222;">Network Overview</h3>',
            unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(metric_tile("Total Connections", f"{total:,}"), unsafe_allow_html=True)
with m2:
    st.markdown(metric_tile("Companies", f"{n_companies:,}"), unsafe_allow_html=True)
with m3:
    st.markdown(metric_tile("Unique Titles", f"{n_titles:,}"), unsafe_allow_html=True)
with m4:
    st.markdown(metric_tile("Top Company", top_co, f"{top_co_n} people"), unsafe_allow_html=True)

st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

# ── Row 1: Companies | Job Titles ──────────────────────────────────────────────
r1l, r1r = st.columns(2, gap="medium")

with r1l:
    with chart_card("Top Companies", "Where your connections work"):
        if "company" in df.columns:
            co_df = (
                df[df["company"].str.strip() != ""]["company"]
                .value_counts().head(15).reset_index()
            )
            co_df.columns = ["Company", "Connections"]
            st.plotly_chart(
                hbar_chart(co_df, "Company", "Connections", "#FF385C"),
                width="stretch", config={"displayModeBar": False},
            )

with r1r:
    with chart_card("Top Job Titles", "Most common roles in your network"):
        if "position" in df.columns:
            pos_df = (
                df[df["position"].str.strip() != ""]["position"]
                .value_counts().head(15).reset_index()
            )
            pos_df.columns = ["Title", "Connections"]
            st.plotly_chart(
                hbar_chart(pos_df, "Title", "Connections", "#00A699"),
                width="stretch", config={"displayModeBar": False},
            )

# ── Row 2: Timeline | Company donut ────────────────────────────────────────────
r2l, r2r = st.columns(2, gap="medium")

with r2l:
    with chart_card("Connections Over Time", "Your network growth"):
        if "connected_on" in df.columns:
            df_t = df[df["connected_on"].str.strip() != ""].copy()
            try:
                df_t["date"] = pd.to_datetime(df_t["connected_on"], errors="coerce", dayfirst=True)
                df_t = df_t.dropna(subset=["date"])
                if not df_t.empty:
                    monthly = (
                        df_t.groupby(df_t["date"].dt.to_period("M").dt.to_timestamp())
                        .size().reset_index(name="count")
                    )
                    monthly["cumulative"] = monthly["count"].cumsum()
                    st.plotly_chart(
                        area_chart(monthly),
                        width="stretch", config={"displayModeBar": False},
                    )
                else:
                    st.info("No parseable dates found.")
            except Exception:
                st.info("Could not render the timeline.")

with r2r:
    with chart_card("Network by Company (Top 10)", f"Distribution of your {total:,} connections"):
        if "company" in df.columns:
            co_vc = df[df["company"].str.strip() != ""]["company"].value_counts()
            top10 = co_vc.head(10)
            other_n = int(co_vc.iloc[10:].sum()) if len(co_vc) > 10 else 0
            labels = list(top10.index) + (["Others"] if other_n else [])
            values = list(map(int, top10.values)) + ([other_n] if other_n else [])
            st.plotly_chart(
                donut_chart(labels, values, total),
                width="stretch", config={"displayModeBar": False},
            )

# ── Full connections table ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.expander(f"📋  View all {total:,} connections", expanded=False):
    display = df.copy()
    display.columns = [c.replace("_", " ").title() for c in display.columns]
    st.dataframe(display, width='stretch', hide_index=True)