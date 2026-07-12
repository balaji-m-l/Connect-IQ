import os
import streamlit as st
from utils.supabase_client import get_supabase_client

# Server-side cache: {streamlit_session_id -> {access_token, refresh_token}}
# Keyed by the internal Streamlit session ID so tokens are isolated per browser
# tab but survive HTML-link page navigations (which reconnect the same session).
_token_cache: dict[str, dict] = {}


def _sid() -> str | None:
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        return ctx.session_id if ctx else None
    except Exception:
        return None


def login(email: str, password: str) -> tuple[bool, str | None]:
    try:
        client = get_supabase_client()
        response = client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        st.session_state.user = response.user
        st.session_state.session = response.session
        if response.session:
            sid = _sid()
            if sid:
                _token_cache[sid] = {
                    "access_token":  response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                }
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
    sid = _sid()
    try:
        client = get_supabase_client()
        client.auth.sign_out()
    except Exception:
        pass
    if sid:
        _token_cache.pop(sid, None)
    if user_id:
        _clear_chat(user_id)
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def is_authenticated() -> bool:
    if st.session_state.get("user") is not None:
        return True
    # Restore from server-side token cache (keyed by Streamlit session ID).
    # This survives HTML-link page navigation because Streamlit reconnects
    # the same session ID for the same browser tab.
    sid = _sid()
    if sid and sid in _token_cache:
        tokens = _token_cache[sid]
        try:
            client = get_supabase_client()
            resp = client.auth.set_session(
                tokens["access_token"], tokens["refresh_token"]
            )
            if resp and getattr(resp, "user", None):
                st.session_state.user = resp.user
                st.session_state.session = resp.session
                _token_cache[sid] = {
                    "access_token":  resp.session.access_token,
                    "refresh_token": resp.session.refresh_token,
                }
                return True
        except Exception:
            pass
        _token_cache.pop(sid, None)
    return False


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
