import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

_admin_client: Client | None = None


def get_supabase_client() -> Client:
    if "_supabase_client" not in st.session_state:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_ANON_KEY", "")
        if not url or not key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_ANON_KEY must be set in your .env file."
            )
        st.session_state["_supabase_client"] = create_client(url, key)
    return st.session_state["_supabase_client"]


def get_supabase_admin_client() -> Client:
    global _admin_client
    if _admin_client is None:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
        if not url or not key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in your .env file."
            )
        _admin_client = create_client(url, key)
    return _admin_client
