import streamlit as st
import streamlit.components.v1

from components.styles import inject_styles, metric_tile
from components.nav import render_app_nav
from utils.auth import (
    require_auth, get_user_id, get_display_name, get_user_email,
    get_user_headline, logout, update_profile, update_password, delete_account,
)
from utils.data_processor import (
    get_connection_stats, clear_connections, export_connections_csv,
    process_linkedin_file, save_connections,
)

st.set_page_config(
    page_title="Connect-IQ – Settings",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles(hide_sidebar=True)

require_auth()

render_app_nav(active="")

user_id  = get_user_id()
name     = get_display_name()
email    = get_user_email()
initials = "".join(w[0].upper() for w in name.split() if w)[:2] if name else "U"

# ── Page CSS ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp { background: #FFFFFF !important; }
    .main, .block-container {
        background: transparent !important;
        padding-top: 0 !important;
        max-width: 1180px;
    }
    [data-testid="column"], [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > div { background: transparent !important; }

    /* Settings row helpers */
    .cf-row-label { font-size: 14px; font-weight: 600; color: var(--cf-text); }
    .cf-row-hint  { font-size: 12.5px; color: var(--cf-text-muted); margin-top: 3px; line-height: 1.5; }

    /* Read-only email */
    .cf-input-disabled {
        width: 100%; background: var(--cf-border); opacity: .65;
        border: 1.5px solid var(--cf-border-strong); border-radius: 8px;
        padding: 12px 14px; font-size: 15px; color: var(--cf-text);
        cursor: not-allowed; font-family: Inter, sans-serif;
    }

    /* Privacy reassurance banner */
    .cf-banner {
        display: flex; gap: 12px; align-items: flex-start;
        background: var(--cf-bg-soft); border: 1px solid var(--cf-border);
        border-radius: 12px; padding: 16px 18px; margin-bottom: 24px;
    }

    /* Sidebar nav — base (inactive) state.
       Streamlit adds .st-key-nav_<key> to every widget wrapper, so this
       selector reliably beats the global .stButton red-primary rule. */
    div[class*="st-key-nav_"] .stButton > button {
        background: transparent !important;
        color: var(--cf-text-mid) !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 10px 12px !important;
        border-radius: 8px !important;
        justify-content: flex-start !important;
        text-align: left !important;
        box-shadow: none !important;
        width: 100% !important;
        min-height: 0 !important;
        transform: none !important;
        transition: background .15s, color .15s !important;
    }
    div[class*="st-key-nav_"] .stButton > button:hover {
        background: var(--cf-bg-soft) !important;
        color: var(--cf-text) !important;
        transform: none !important;
    }
    /* ACTIVE item: type="primary" → pink pill, never solid red. */
    div[class*="st-key-nav_"] .stButton > button[kind="primary"],
    div[class*="st-key-nav_"] .stButton > button[kind="primary"]:hover,
    div[class*="st-key-nav_"] .stButton > button[kind="primary"]:focus {
        background: var(--cf-red-tint) !important;
        color: var(--cf-red) !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }
    /* Delete account: always destructive red. */
    div.st-key-nav_delete .stButton > button {
        color: #D92D20 !important;
    }
    div.st-key-nav_delete .stButton > button:hover {
        background: #FEF3F2 !important;
        color: #D92D20 !important;
    }

    /* Password strength meter */
    .cf-strength { display: flex; gap: 6px; margin: 6px 0 4px; }
    .cf-seg { flex: 1; height: 4px; border-radius: 4px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session defaults ───────────────────────────────────────────────────────────
if "settings_section" not in st.session_state:
    st.session_state.settings_section = st.session_state.pop("settings_tab", "profile")

SECTIONS = [
    ("profile",  "👤", "Profile"),
    ("password", "🔑", "Password & security"),
    ("data",     "🗄️", "Your data"),
    ("privacy",  "🔒", "Privacy"),
]

stats            = get_connection_stats(user_id)
CONNECTION_COUNT = stats["total"]
LAST_IMPORT      = stats["last_import"]


# ── Delete account dialog ──────────────────────────────────────────────────────
@st.dialog("Delete your account?")
def _delete_dialog():
    st.markdown(
        f'<div style="text-align:center;margin-bottom:12px;">'
        f'<div style="width:56px;height:56px;border-radius:50%;background:#FEE4E2;'
        f'display:inline-flex;align-items:center;justify-content:center;font-size:26px;">⚠️</div>'
        f'</div>'
        f'<p style="font-size:14.5px;text-align:center;color:#717171;line-height:1.6;">'
        f'This permanently deletes your account, all '
        f'<strong style="color:#222;">{CONNECTION_COUNT:,} connections</strong>, '
        f'embeddings, and chat history. '
        f'<strong style="color:#222;">This cannot be undone.</strong></p>',
        unsafe_allow_html=True,
    )
    confirm = st.text_input("Type **DELETE** to confirm", placeholder="DELETE",
                            key="delete_confirm_input")
    col_cancel, col_delete = st.columns(2)
    with col_cancel:
        if st.button("Cancel", key="delete_dlg_cancel", type="secondary",
                     use_container_width=True):
            st.rerun()
    with col_delete:
        if st.button("Delete account", key="delete_dlg_go", type="primary",
                     use_container_width=True, disabled=(confirm != "DELETE")):
            with st.spinner("Deleting all data…"):
                ok, err = delete_account(user_id)
            if ok:
                st.switch_page("app.py")
            else:
                st.error(f"Failed: {err}")


if st.session_state.get("settings_section") == "delete":
    st.session_state.settings_section = "profile"
    st.session_state.show_delete_dialog = True

if st.session_state.get("show_delete_dialog"):
    st.session_state.show_delete_dialog = False
    _delete_dialog()

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="padding:24px 0 12px;">'
    '<div style="font-size:13px;color:#717171;margin-bottom:6px;">Account</div>'
    '<div class="cf-h2" style="margin:0;">Settings</div>'
    '</div>'
    '<hr class="cf-hr" style="margin-bottom:24px;">',
    unsafe_allow_html=True,
)

# ── Two-pane layout ────────────────────────────────────────────────────────────
side, _gap, content = st.columns([0.26, 0.04, 0.70])

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with side:
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:12px;padding:4px 0 16px;'
        f'border-bottom:1px solid var(--cf-border);margin-bottom:12px;">'
        f'<div class="cf-avatar" style="width:42px;height:42px;font-size:15px;'
        f'background:linear-gradient(135deg,var(--cf-red),var(--cf-red-dark));">'
        f'{initials}</div>'
        f'<div style="min-width:0;">'
        f'<div style="font-size:14px;font-weight:700;color:var(--cf-text);">{name or "User"}</div>'
        f'<div class="cf-small" style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'
        f'{email}</div></div></div>',
        unsafe_allow_html=True,
    )

    section = st.session_state.settings_section

    for sid, icon, label in SECTIONS:
        is_active = section == sid
        if st.button(f"{icon}  {label}", key=f"nav_{sid}",
                     type="primary" if is_active else "secondary",
                     use_container_width=True):
            st.session_state.settings_section = sid
            st.rerun()

    st.markdown("<hr style='margin:8px 0;border-color:#EBEBEB;border-top:1px solid #EBEBEB;'>",
                unsafe_allow_html=True)
    if st.button("⚠️  Delete account", key="nav_delete", type="secondary",
                 use_container_width=True):
        st.session_state.show_delete_dialog = True
        st.rerun()


# ── Helper: row label ──────────────────────────────────────────────────────────
def settings_row(label: str, hint: str = "") -> None:
    hint_html = f'<div class="cf-row-hint">{hint}</div>' if hint else ""
    st.markdown(
        f'<div style="margin-top:20px;padding-bottom:4px;">'
        f'<span class="cf-row-label">{label}</span>{hint_html}</div>',
        unsafe_allow_html=True,
    )


# ── CONTENT ────────────────────────────────────────────────────────────────────
with content:
    section = st.session_state.settings_section

    # ── PROFILE ───────────────────────────────────────────────────────────────
    if section == "profile":
        st.markdown('<div class="cf-h3">Profile</div>', unsafe_allow_html=True)
        st.markdown('<p class="cf-small">How you appear in Connect-IQ.</p>',
                    unsafe_allow_html=True)

        current_name     = get_display_name()
        current_headline = get_user_headline()

        settings_row("Full name")
        new_name = st.text_input("Full name", value=current_name,
                                 placeholder="Your full name", key="profile_name",
                                 label_visibility="collapsed")

        settings_row("Email address",
                     "Used for sign-in and account notifications. Email can't be changed.")
        st.markdown(f'<div class="cf-input-disabled">{email}</div>', unsafe_allow_html=True)

        settings_row("Headline", "Optional — shown in your dashboard greeting.")
        new_headline = st.text_input("Headline", value=current_headline,
                                     placeholder="e.g. Building my network",
                                     key="profile_headline", label_visibility="collapsed")

        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        c1, c2, _ = st.columns([0.3, 0.25, 0.45])
        with c1:
            if st.button("Save changes", key="profile_save", type="primary",
                         use_container_width=True):
                ok, msg = update_profile(new_name, new_headline)
                if ok:
                    st.session_state["profile_saved"] = True
                    st.rerun()
                else:
                    st.error(msg)
        with c2:
            if st.button("Cancel", key="profile_cancel", type="secondary",
                         use_container_width=True):
                st.rerun()

        if st.session_state.pop("profile_saved", False):
            st.success("Profile saved successfully ✓")

    # ── PASSWORD & SECURITY ───────────────────────────────────────────────────
    elif section == "password":
        st.markdown('<div class="cf-h3">Password &amp; security</div>', unsafe_allow_html=True)
        st.markdown('<p class="cf-small">Keep your account protected.</p>',
                    unsafe_allow_html=True)

        current_pw = st.text_input("Current password", type="password", key="pw_current")
        new_pw     = st.text_input("New password",     type="password", key="pw_new")
        confirm_pw = st.text_input("Confirm new password", type="password", key="pw_confirm")

        def _strength(pw: str) -> int:
            if not pw: return 0
            s = 1
            if len(pw) >= 8: s += 1
            if any(c.isdigit() for c in pw): s += 1
            if any(not c.isalnum() for c in pw): s += 1
            return s

        s = _strength(new_pw)
        seg_colors = [
            ("#00A699" if s >= 3 else "#FF385C") if i < s else "var(--cf-border-strong)"
            for i in range(4)
        ]
        captions = {
            0: "", 1: "Weak", 2: "Weak — add a number and a symbol",
            3: "Good", 4: "Strong — at least 8 characters, 1 number, 1 symbol",
        }
        segs = "".join(
            f'<div class="cf-seg" style="background:{c};"></div>' for c in seg_colors
        )
        st.markdown(
            f'<div class="cf-strength">{segs}</div>'
            + (f'<p class="cf-small">{captions[s]}</p>' if new_pw else ""),
            unsafe_allow_html=True,
        )

        st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
        if st.button("Update password", key="pw_update", type="primary"):
            if not current_pw or not new_pw or not confirm_pw:
                st.error("Please fill in all password fields.")
            elif s < 2:
                st.error("Password must be at least 8 characters.")
            elif new_pw != confirm_pw:
                st.error("Passwords don't match.")
            else:
                with st.spinner("Updating…"):
                    ok, msg = update_password(current_pw, new_pw)
                if ok:
                    st.toast("Password updated ✓")
                else:
                    st.error(msg)

    # ── YOUR DATA ─────────────────────────────────────────────────────────────
    elif section == "data":
        st.markdown('<div class="cf-h3">Your data</div>', unsafe_allow_html=True)
        st.markdown('<p class="cf-small">Manage the connection data you\'ve imported.</p>',
                    unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(metric_tile("Connections stored", f"{CONNECTION_COUNT:,}"),
                        unsafe_allow_html=True)
        with m2:
            st.markdown(metric_tile("Last import", LAST_IMPORT), unsafe_allow_html=True)
        with m3:
            status = "Active" if CONNECTION_COUNT > 0 else "Empty"
            st.markdown(metric_tile("Status", status), unsafe_allow_html=True)

        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

        def _action_card(icon: str, title: str, desc: str, btn_label: str,
                         btn_key: str, destructive: bool = False) -> bool:
            title_color = "#D92D20" if destructive else "var(--cf-text)"
            st.markdown(
                f'<div class="cf-card" style="margin-bottom:12px;">'
                f'<div style="display:flex;gap:14px;align-items:flex-start;">'
                f'<div style="font-size:22px;">{icon}</div>'
                f'<div><div class="cf-h4" style="color:{title_color};">{title}</div>'
                f'<p class="cf-small" style="margin-top:3px;">{desc}</p>'
                f'</div></div></div>',
                unsafe_allow_html=True,
            )
            return st.button(btn_label, key=btn_key, type="secondary")

        if _action_card("📤", "Re-upload connections",
                        "Upload a newer LinkedIn export. New connections are appended; duplicates skipped.",
                        "Upload CSV", "data_reupload"):
            st.session_state["settings_show_reupload"] = not st.session_state.get(
                "settings_show_reupload", False
            )
            st.rerun()

        if st.session_state.get("settings_show_reupload"):
            uploaded = st.file_uploader("LinkedIn connections CSV",
                                        type=["csv", "xlsx", "xls"],
                                        key="settings_uploader",
                                        label_visibility="collapsed")
            st.caption("Supports CSV, XLSX, XLS · Up to 50 MB")
            p_col, c_col, _ = st.columns([1, 1, 4])
            with p_col:
                if st.button("Process & Save", key="settings_process", type="primary",
                             disabled=not uploaded):
                    parsed_df, err = process_linkedin_file(uploaded)
                    if err:
                        st.error(err)
                    else:
                        with st.spinner("Saving…"):
                            inserted, dups, save_err = save_connections(user_id, parsed_df)
                        if save_err:
                            st.error(f"Save failed: {save_err}")
                        else:
                            parts = [f"✅ Added **{inserted}** new connections."]
                            if dups:
                                parts.append(f"Skipped **{dups}** duplicate(s).")
                            st.success(" ".join(parts))
                            st.session_state["settings_show_reupload"] = False
                            st.rerun()
            with c_col:
                if st.button("Cancel", key="settings_cancel_upload", type="secondary"):
                    st.session_state["settings_show_reupload"] = False
                    st.rerun()

        csv_data = export_connections_csv(user_id)
        st.markdown(
            '<div class="cf-card" style="margin-bottom:12px;">'
            '<div style="display:flex;gap:14px;align-items:flex-start;">'
            '<div style="font-size:22px;">⬇️</div>'
            '<div><div class="cf-h4">Export my data</div>'
            '<p class="cf-small" style="margin-top:3px;">Download everything we hold about you as a CSV file.</p>'
            '</div></div></div>',
            unsafe_allow_html=True,
        )
        if csv_data:
            st.download_button("⬇️ Download CSV", data=csv_data,
                               file_name="my_connections.csv", mime="text/csv",
                               key="data_export_dl", type="secondary")
        else:
            st.caption("No data to export yet.")

        st.markdown('<div id="cf-data-clear"></div>', unsafe_allow_html=True)
        if _action_card("🗑️", "Clear all data",
                        "Remove every imported connection and its embeddings. Your account stays active.",
                        "Clear data", "data_clear", destructive=True):
            st.session_state["confirm_clear"] = True

        if st.session_state.get("confirm_clear"):
            st.warning(
                f"Remove all **{CONNECTION_COUNT:,} connections**? "
                "Your account stays active. **This cannot be undone.**",
                icon="⚠️",
            )
            cc1, cc2, _ = st.columns([0.25, 0.2, 0.55])
            with cc1:
                if st.button("Yes, clear data", key="clear_yes", type="primary",
                             use_container_width=True):
                    with st.spinner("Clearing…"):
                        ok, err = clear_connections(user_id)
                    if ok:
                        st.session_state.confirm_clear = False
                        st.session_state.pop("connections_df", None)
                        st.toast("All connections cleared ✓")
                        st.rerun()
                    else:
                        st.error(f"Failed: {err}")
            with cc2:
                if st.button("Cancel", key="clear_no", type="secondary",
                             use_container_width=True):
                    st.session_state.confirm_clear = False
                    st.rerun()

        if st.session_state.pop("settings_scroll", None) == "clear":
            st.components.v1.html(
                '<script>window.parent.document.getElementById("cf-data-clear")'
                '.scrollIntoView({behavior:"smooth",block:"start"});</script>',
                height=1,
            )

    # ── PRIVACY ───────────────────────────────────────────────────────────────
    elif section == "privacy":
        st.markdown('<div class="cf-h3">Privacy</div>', unsafe_allow_html=True)
        st.markdown('<p class="cf-small">Control how your data is stored and used.</p>',
                    unsafe_allow_html=True)

        st.markdown(
            '<div class="cf-banner">'
            '<div style="font-size:20px;">🔒</div>'
            '<div><div class="cf-h4">Your data stays yours</div>'
            '<p class="cf-small" style="margin-top:3px;">'
            'Connections are stored in your own database with Row-Level Security. '
            'We never sell your data or use it to train AI models.'
            '</p></div></div>',
            unsafe_allow_html=True,
        )

        # Exactly one toggle on this page — do not add more
        st.markdown('<div class="cf-tiny" style="margin-bottom:4px;">CHAT HISTORY</div>',
                    unsafe_allow_html=True)
        st.toggle(
            "Save chat history",
            value=st.session_state.get("save_chat_history", True),
            key="privacy_history",
            help="Keep your past questions so you can revisit them. "
                 "Turn off to keep chats ephemeral.",
        )
        st.session_state["save_chat_history"] = st.session_state.get("privacy_history", True)

        settings_row("Data retention",
                     "How long we keep inactive data before automatic deletion.")
        ret_options = ["Keep until I delete", "12 months", "6 months"]
        st.selectbox(
            "Data retention",
            ret_options,
            index=ret_options.index(
                st.session_state.get("data_retention", "Keep until I delete")
            ),
            key="privacy_retention",
            label_visibility="collapsed",
        )
        st.session_state["data_retention"] = st.session_state.get(
            "privacy_retention", "Keep until I delete"
        )

        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
        p1, p2, _ = st.columns([0.32, 0.36, 0.32])
        with p1:
            st.download_button(
                "⬇️ Download my data",
                data=export_connections_csv(user_id) or "",
                file_name="my_connections.csv", mime="text/csv",
                key="privacy_dl", type="secondary", use_container_width=True,
                disabled=not CONNECTION_COUNT,
            )
        with p2:
            if st.button("Request data deletion", key="privacy_delete_req",
                         type="secondary", use_container_width=True):
                st.info("Deletion request noted. Your account will be removed within 30 days.")
