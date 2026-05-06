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


def signup(email: str, password: str) -> tuple[bool, str]:
    try:
        client = get_supabase_client()
        response = client.auth.sign_up({"email": email, "password": password})
        if response.user:
            return True, "Account created! Please check your email to verify, then sign in."
        return False, "Signup failed. Please try again."
    except Exception as e:
        return False, str(e)


def logout() -> None:
    try:
        client = get_supabase_client()
        client.auth.sign_out()
    except Exception:
        pass
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def is_authenticated() -> bool:
    return st.session_state.get("user") is not None


def get_user_id() -> str | None:
    user = st.session_state.get("user")
    return str(user.id) if user else None
