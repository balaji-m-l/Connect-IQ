import streamlit as st
from utils.supabase_client import get_supabase_client


def login(email: str, password: str) -> tuple[bool, str | None]:
    try:
        client = get_supabase_client()
        response = client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        st.session_state.user = response.user
        st.session_state.session = response.session
        return True, None
    except Exception as e:
        return False, str(e)


def signup(email: str, password: str, full_name: str = "") -> tuple[bool, str]:
    try:
        client = get_supabase_client()
        credentials: dict = {"email": email, "password": password}
        if full_name.strip():
            credentials["options"] = {"data": {"full_name": full_name.strip()}}
        response = client.auth.sign_up(credentials)
        if response.user:
            return True, "Account created! Please check your email to verify, then sign in."
        return False, "Signup failed. Please try again."
    except Exception as e:
        return False, str(e)


def get_display_name() -> str:
    user = st.session_state.get("user")
    if not user:
        return ""
    meta = getattr(user, "user_metadata", {}) or {}
    return meta.get("full_name", "").strip()


def logout() -> None:
    try:
        client = get_supabase_client()
        client.auth.sign_out()
    except Exception:
        pass
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def is_authenticated() -> bool:
    if st.session_state.get("user") is not None:
        return True
    # Restore from the Supabase client's in-memory session (survives page reloads
    # within the same server process, e.g. after HTML-link navigation).
    try:
        client = get_supabase_client()
        session = client.auth.get_session()
        if session and getattr(session, "user", None):
            st.session_state.user = session.user
            st.session_state.session = session
            return True
    except Exception:
        pass
    return False


def get_user_id() -> str | None:
    user = st.session_state.get("user")
    return str(user.id) if user else None
