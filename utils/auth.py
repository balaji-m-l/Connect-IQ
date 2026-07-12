import os
import uuid
import streamlit as st
import streamlit.components.v1 as _components
from utils.supabase_client import get_supabase_client

# Process-level cache: {marker_uuid -> {access_token, refresh_token}}
# Survives HTML-link navigation because it lives in the Python process,
# not in per-request session_state.
_restore_cache: dict[str, dict] = {}


def login(email: str, password: str) -> tuple[bool, str | None]:
    try:
        client = get_supabase_client()
        response = client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        st.session_state.user = response.user
        st.session_state.session = response.session
        if response.session:
            marker = str(uuid.uuid4())
            _restore_cache[marker] = {
                "access_token":  response.session.access_token,
                "refresh_token": response.session.refresh_token,
            }
            st.session_state["_cf_marker"] = marker
        return True, None
    except Exception as e:
        return False, str(e)


def signup(email: str, password: str, full_name: str = "") -> tuple[bool, str]:
    try:
        client = get_supabase_client()
        site_url = os.getenv("SITE_URL", "http://localhost:8501")
        credentials: dict = {
            "email": email,
            "password": password,
            "options": {
                "email_redirect_to": f"{site_url}/Login?verified=1",
            },
        }
        if full_name.strip():
            credentials["options"]["data"] = {"full_name": full_name.strip()}
        response = client.auth.sign_up(credentials)
        if response.user:
            return True, "Account created! Please check your email to verify, then sign in."
        return False, "Signup failed. Please try again."
    except Exception as e:
        return False, str(e)


def reset_password(email: str) -> tuple[bool, str]:
    try:
        client = get_supabase_client()
        client.auth.reset_password_for_email(email)
        return True, "Password reset link sent! Check your inbox."
    except Exception as e:
        return False, str(e)


def get_display_name() -> str:
    user = st.session_state.get("user")
    if not user:
        return ""
    meta = getattr(user, "user_metadata", {}) or {}
    return meta.get("full_name", "").strip()


def logout() -> None:
    from utils.chat_store import clear_user as _clear_chat
    user_id = get_user_id()
    marker = st.session_state.get("_cf_marker")
    try:
        client = get_supabase_client()
        client.auth.sign_out()
    except Exception:
        pass
    if marker:
        _restore_cache.pop(marker, None)
    if user_id:
        _clear_chat(user_id)
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    # Clear marker from browser sessionStorage
    _components.html(
        "<script>try{window.parent.sessionStorage.removeItem('cf_marker');}catch(e){}</script>",
        height=0,
    )


def is_authenticated() -> bool:
    if st.session_state.get("user") is not None:
        return True

    # Restore from process-level cache using a marker passed via URL param.
    # This fires after the browser sessionStorage JS redirects back here.
    marker = st.query_params.get("_cf_r")
    if marker and marker in _restore_cache:
        tokens = _restore_cache[marker]
        try:
            client = get_supabase_client()
            resp = client.auth.set_session(
                tokens["access_token"], tokens["refresh_token"]
            )
            if resp and getattr(resp, "user", None):
                st.session_state.user = resp.user
                st.session_state.session = resp.session
                st.session_state["_cf_marker"] = marker
                _restore_cache[marker] = {
                    "access_token":  resp.session.access_token,
                    "refresh_token": resp.session.refresh_token,
                }
                # Clean up both params on success
                for p in ("_cf_r", "_cf_tried"):
                    if p in st.query_params:
                        st.query_params.pop(p)
                return True
        except Exception:
            pass
        _restore_cache.pop(marker, None)
    # Only clean up _cf_r here; leave _cf_tried so require_auth() can see it.
    if "_cf_r" in st.query_params:
        st.query_params.pop("_cf_r")

    return False


def require_auth() -> None:
    """
    Drop-in replacement for `if not is_authenticated(): st.switch_page(login)`.

    On first auth failure, injects JS to read the restore marker from
    sessionStorage and redirect back to this page with ?_cf_r=MARKER.
    On the second load the marker is in the URL, is_authenticated() restores
    the session, and we return normally.  If sessionStorage has no marker
    (brand-new visitor), the JS redirects straight to Login.
    """
    # Read _cf_tried BEFORE is_authenticated() might mutate query params.
    already_tried = bool(st.query_params.get("_cf_tried"))

    if is_authenticated():
        return

    if already_tried:
        # Restore was already attempted and failed — send to Login.
        if "_cf_tried" in st.query_params:
            st.query_params.pop("_cf_tried")
        st.switch_page("pages/1_Login.py")
        st.stop()

    # First failure — ask the browser to look up the marker.
    _components.html(
        """<script>
        (function() {
          try {
            var m = window.parent.sessionStorage.getItem('cf_marker');
            var u = new URL(window.parent.location.href);
            if (m) { u.searchParams.set('_cf_r', m); }
            u.searchParams.set('_cf_tried', '1');
            window.parent.location.replace(u.toString());
          } catch(e) {
            window.parent.location.replace('/Login');
          }
        })();
        </script>""",
        height=0,
    )
    st.markdown(
        '<div style="display:flex;justify-content:center;align-items:center;'
        'height:60vh;font-family:Inter,sans-serif;color:#717171;font-size:14px;">'
        'Loading…</div>',
        unsafe_allow_html=True,
    )
    st.stop()


def write_session_marker() -> None:
    """Call this once after a successful login to persist the marker in sessionStorage."""
    marker = st.session_state.get("_cf_marker", "")
    if not marker:
        return
    _components.html(
        f"<script>try{{window.parent.sessionStorage.setItem('cf_marker','{marker}');}}catch(e){{}}</script>",
        height=0,
    )


def get_user_id() -> str | None:
    user = st.session_state.get("user")
    return str(user.id) if user else None


def get_user_email() -> str:
    user = st.session_state.get("user")
    return str(getattr(user, "email", "") or "") if user else ""


def get_user_headline() -> str:
    user = st.session_state.get("user")
    if not user:
        return ""
    meta = getattr(user, "user_metadata", {}) or {}
    return meta.get("headline", "").strip()


def update_profile(full_name: str, headline: str = "") -> tuple[bool, str]:
    try:
        client = get_supabase_client()
        meta: dict = {"full_name": full_name.strip(), "headline": headline.strip()}
        resp = client.auth.update_user({"data": meta})
        if resp.user:
            st.session_state.user = resp.user
            return True, "Profile updated."
        return False, "Update failed."
    except Exception as exc:
        return False, str(exc)


def delete_account(user_id: str) -> tuple[bool, str | None]:
    from utils.data_processor import clear_connections
    from utils.supabase_client import get_supabase_admin_client

    ok, err = clear_connections(user_id)
    if not ok:
        return False, err

    try:
        admin = get_supabase_admin_client()
        admin.auth.admin.delete_user(user_id)
    except Exception as exc:
        return False, str(exc)

    logout()
    return True, None


def update_password(current_pw: str, new_pw: str) -> tuple[bool, str]:
    email = get_user_email()
    if not email:
        return False, "No authenticated user found."
    ok, err = login(email, current_pw)
    if not ok:
        return False, "Current password is incorrect."
    try:
        client = get_supabase_client()
        resp = client.auth.update_user({"password": new_pw})
        if resp.user:
            return True, "Password updated."
        return False, "Password update failed."
    except Exception as exc:
        return False, str(exc)
