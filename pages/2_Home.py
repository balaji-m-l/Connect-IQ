import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.styles import inject_styles
from components.nav import render_nav
from utils.auth import is_authenticated, get_user_id
from utils.data_processor import process_linkedin_file, save_connections, get_connections

st.set_page_config(
    page_title="Connect-IQ – Dashboard",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles(hide_sidebar=True)

if not is_authenticated():
    st.switch_page("pages/1_Login.py")

render_nav(active="home")

user_id = get_user_id()

# ── Load / cache connections ──────────────────────────────────────────────────
if (
    "connections_df" not in st.session_state
    or st.session_state.get("connections_user_id") != user_id
):
    with st.spinner("Loading your connections…"):
        st.session_state.connections_df = get_connections(user_id)
        st.session_state.connections_user_id = user_id

df: pd.DataFrame = st.session_state.connections_df

# ── Page header ───────────────────────────────────────────────────────────────
hdr_l, hdr_r = st.columns([5, 1])
with hdr_l:
    st.markdown(
        '<h1 style="margin:0;font-size:1.8rem;font-weight:800;color:#222222;">'
        "Your Network Dashboard"
        "</h1>",
        unsafe_allow_html=True,
    )
with hdr_r:
    if st.button("📤 Upload CSV", key="upload_toggle", use_container_width=True, type="primary"):
        st.session_state.show_uploader = not st.session_state.get("show_uploader", False)

# ── Upload panel ──────────────────────────────────────────────────────────────
if st.session_state.get("show_uploader", False):
    st.markdown(
        '<div style="background:#F7F7F7;border-radius:14px;padding:28px 32px;'
        'margin:16px 0;border:1.5px dashed #DDDDDD;">',
        unsafe_allow_html=True,
    )
    st.markdown("#### Upload LinkedIn Connections Export")
    st.markdown(
        '<p style="color:#717171;font-size:.88rem;margin-bottom:16px;">'
        "Export path: <b>LinkedIn → Settings & Privacy → Data Privacy → "
        "Get a copy of your data → Connections</b>. "
        "New connections are appended; duplicates are skipped automatically."
        "</p>",
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Choose your connections file (CSV or Excel)",
        type=["csv", "xlsx", "xls"],
        key="file_uploader",
    )

    btn_col, cancel_col, _ = st.columns([1, 1, 5])
    with btn_col:
        process_clicked = st.button(
            "Process & Save",
            key="process_btn",
            use_container_width=True,
            type="primary",
            disabled=not uploaded,
        )
    with cancel_col:
        if st.button("Cancel", key="cancel_upload", use_container_width=True):
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

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Refresh reference after possible upload
df = st.session_state.get("connections_df", pd.DataFrame())

# ── Empty state ───────────────────────────────────────────────────────────────
if df.empty:
    st.markdown(
        '<div style="text-align:center;padding:80px 20px;background:#F7F7F7;border-radius:16px;">'
        '<div style="font-size:3.5rem;margin-bottom:16px;">📤</div>'
        '<h2 style="color:#222222;font-weight:800;margin-bottom:10px;">Upload your LinkedIn connections</h2>'
        '<p style="color:#717171;max-width:400px;margin:0 auto;">'
        "Click the <b>Upload CSV</b> button above to get started. "
        "Your connections will be embedded and stored securely."
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.stop()

# ── Metrics row ───────────────────────────────────────────────────────────────
st.markdown("#### Network Overview")
m1, m2, m3, m4 = st.columns(4)

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

with m1:
    st.metric("Total Connections", f"{total:,}")
with m2:
    st.metric("Companies", f"{n_companies:,}")
with m3:
    st.metric("Unique Titles", f"{n_titles:,}")
with m4:
    st.metric("Top Company", top_co, f"{top_co_n} people")

st.markdown("<br>", unsafe_allow_html=True)

# ── Shared Plotly layout ───────────────────────────────────────────────────────
_LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Inter, sans-serif", color="#222222", size=12),
    margin=dict(l=10, r=20, t=30, b=10),
    height=380,
)

# ── Row 1: Companies | Job Titles ─────────────────────────────────────────────
r1l, r1r = st.columns(2, gap="medium")

with r1l:
    st.markdown("##### Top Companies")
    if "company" in df.columns:
        co_df = (
            df[df["company"].str.strip() != ""]["company"]
            .value_counts()
            .head(15)
            .reset_index()
        )
        co_df.columns = ["Company", "Connections"]
        fig = px.bar(
            co_df,
            x="Connections",
            y="Company",
            orientation="h",
            color_discrete_sequence=["#FF385C"],
        )
        fig.update_layout(**_LAYOUT, yaxis=dict(autorange="reversed"))
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

with r1r:
    st.markdown("##### Top Job Titles")
    if "position" in df.columns:
        pos_df = (
            df[df["position"].str.strip() != ""]["position"]
            .value_counts()
            .head(15)
            .reset_index()
        )
        pos_df.columns = ["Title", "Connections"]
        fig = px.bar(
            pos_df,
            x="Connections",
            y="Title",
            orientation="h",
            color_discrete_sequence=["#00A699"],
        )
        fig.update_layout(**_LAYOUT, yaxis=dict(autorange="reversed"))
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Timeline | Company donut ───────────────────────────────────────────
r2l, r2r = st.columns(2, gap="medium")

with r2l:
    st.markdown("##### Connections Over Time")
    if "connected_on" in df.columns:
        df_t = df[df["connected_on"].str.strip() != ""].copy()
        try:
            df_t["date"] = pd.to_datetime(df_t["connected_on"], errors="coerce", dayfirst=True)
            df_t = df_t.dropna(subset=["date"])
            if not df_t.empty:
                monthly = (
                    df_t.groupby(df_t["date"].dt.to_period("M").dt.to_timestamp())
                    .size()
                    .reset_index(name="count")
                )
                monthly.columns = ["date", "count"]
                monthly["cumulative"] = monthly["count"].cumsum()

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=monthly["date"],
                        y=monthly["cumulative"],
                        mode="lines",
                        line=dict(color="#FF385C", width=2.5),
                        fill="tozeroy",
                        fillcolor="rgba(255,56,92,0.10)",
                        hovertemplate="%{x|%b %Y}: %{y} total<extra></extra>",
                    )
                )
                fig.update_layout(
                    **_LAYOUT,
                    showlegend=False,
                    yaxis=dict(gridcolor="#F0F0F0"),
                    xaxis=dict(gridcolor="#F0F0F0"),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No parseable dates found in your connections file.")
        except Exception:
            st.info("Could not render the timeline — connection dates may be in an unrecognised format.")

with r2r:
    st.markdown("##### Network by Company (Top 10)")
    if "company" in df.columns:
        co_vc = df[df["company"].str.strip() != ""]["company"].value_counts()
        top10 = co_vc.head(10)
        other_n = int(co_vc.iloc[10:].sum()) if len(co_vc) > 10 else 0

        labels = list(top10.index) + (["Others"] if other_n else [])
        values = list(map(int, top10.values)) + ([other_n] if other_n else [])

        fig = go.Figure(
            go.Pie(
                labels=labels,
                values=values,
                hole=0.42,
                marker_colors=px.colors.qualitative.Pastel,
                hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
            )
        )
        fig.update_layout(**_LAYOUT, legend=dict(orientation="v", x=1.01, y=0.5))
        st.plotly_chart(fig, use_container_width=True)

# ── Full connections table ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📋  View all connections", expanded=False):
    display = df.copy()
    display.columns = [c.replace("_", " ").title() for c in display.columns]
    st.dataframe(display, use_container_width=True, hide_index=True)