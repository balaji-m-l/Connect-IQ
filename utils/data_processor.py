import io
import os
import time
from typing import Callable

import pandas as pd
import requests
from dotenv import load_dotenv

from utils.supabase_client import get_supabase_client

load_dotenv(override=True)

LINKEDIN_COLUMN_MAP = {
    "first name":    "first_name",
    "last name":     "last_name",
    "email address": "email",
    "company":       "company",
    "position":      "position",
    "connected on":  "connected_on",
    "url":           "profile_url",
}

CORE_COLS = ["first_name", "last_name", "email", "company", "position", "connected_on", "profile_url"]


# ---------------------------------------------------------------------------
# File parsing
# ---------------------------------------------------------------------------

def process_linkedin_file(uploaded_file) -> tuple[pd.DataFrame | None, str | None]:
    """Parse a LinkedIn CSV/Excel export. Returns (df, error)."""
    try:
        name = uploaded_file.name.lower()

        if name.endswith(".csv"):
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            lines = content.strip().split("\n")
            # LinkedIn CSVs sometimes include a preamble before the real header
            header_idx = 0
            for i, line in enumerate(lines):
                if any(k in line.lower() for k in ["first name", "first_name", "company"]):
                    header_idx = i
                    break
            df = pd.read_csv(io.StringIO("\n".join(lines[header_idx:])))

        elif name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        else:
            return None, "Unsupported format. Please upload a CSV or Excel file."

        # Normalise column names
        df.columns = [c.strip().lower() for c in df.columns]
        df = df.rename(columns={k: v for k, v in LINKEDIN_COLUMN_MAP.items() if k in df.columns})

        available = [c for c in CORE_COLS if c in df.columns]
        if not available:
            return None, (
                "Could not detect LinkedIn columns. "
                "Please make sure you are uploading a LinkedIn connections export."
            )

        df = df[available].dropna(how="all").fillna("").astype(str)
        return df, None

    except Exception as e:
        return None, f"Error reading file: {e}"


# ---------------------------------------------------------------------------
# Embedding helpers
# ---------------------------------------------------------------------------

_EMBED_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-embedding-001:embedContent"
)


def _embed_text(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in .env")
    resp = requests.post(
        _EMBED_URL,
        params={"key": api_key},
        json={
            "content": {"parts": [{"text": text}]},
            "taskType": task_type,
            "outputDimensionality": 768,
        },
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(f"Embedding API error {resp.status_code}: {resp.text}")
    return resp.json()["embedding"]["values"]


def _connection_to_text(row: dict) -> str:
    """Convert a connection row to a natural-language sentence for embedding."""
    name = f"{row.get('first_name', '')} {row.get('last_name', '')}".strip()
    position = row.get("position", "").strip()
    company = row.get("company", "").strip()
    connected_on = row.get("connected_on", "").strip()

    parts = [name] if name else []
    if position:
        parts.append(f"works as {position}")
    if company:
        parts.append(f"at {company}")
    if connected_on:
        parts.append(f"connected on {connected_on}")
    return ", ".join(parts)


_RPM = 1500
_DELAY = 60 / _RPM


def _embed_with_retry(text: str, max_retries: int = 3) -> list[float]:
    """Embed a single text, retrying automatically on 429 rate-limit errors."""
    for attempt in range(max_retries):
        try:
            return _embed_text(text)
        except RuntimeError as e:
            if "429" in str(e) and attempt < max_retries - 1:
                time.sleep(5)
            else:
                raise


def _generate_embeddings(
    texts: list[str],
    progress_cb: Callable[[float, str], None] | None = None,
) -> list[list[float]]:
    """
    Embed a list of texts at ~80 req/min to stay under the free-tier limit.
    Retries automatically if a 429 is hit despite throttling.
    """
    embeddings: list[list[float]] = []
    total = len(texts)

    for i, text in enumerate(texts):
        embeddings.append(_embed_with_retry(text))
        time.sleep(_DELAY)

        if progress_cb and (i + 1) % 10 == 0:
            pct = 0.2 + 0.6 * ((i + 1) / total)
            progress_cb(pct, f"Embedding {i + 1}/{total} connections…")

    return embeddings


# ---------------------------------------------------------------------------
# Supabase CRUD
# ---------------------------------------------------------------------------

def _get_existing_rows(user_id: str) -> dict[tuple[str, str, str], str]:
    """Return a mapping of (first_name, last_name, company) → profile_url for existing rows."""
    try:
        client = get_supabase_client()
        resp = (
            client.table("connections")
            .select("first_name,last_name,company,profile_url")
            .eq("user_id", user_id)
            .execute()
        )
        return {
            (r["first_name"], r["last_name"], r["company"]): r.get("profile_url", "")
            for r in resp.data
        }
    except Exception:
        return {}


def save_connections(
    user_id: str,
    df: pd.DataFrame,
    progress_cb: Callable[[float, str], None] | None = None,
) -> tuple[int, int, str | None]:
    """
    Append new connections (with embeddings) to Supabase.
    Skips rows whose (first_name, last_name, company) already exist.
    Returns (inserted, duplicates_skipped, error).
    """
    try:
        if progress_cb:
            progress_cb(0.05, "Checking for duplicates…")

        existing = _get_existing_rows(user_id)
        all_rows = df.to_dict("records")

        new_rows = []
        url_updates = []  # existing rows whose profile_url is now available

        for row in all_rows:
            key = (row.get("first_name", ""), row.get("last_name", ""), row.get("company", ""))
            new_url = str(row.get("profile_url", "")).strip()
            if key not in existing:
                new_rows.append(row)
            elif new_url and not existing[key]:
                # Row exists but profile_url was empty — backfill it
                url_updates.append({"key": key, "profile_url": new_url})

        duplicates = len(all_rows) - len(new_rows)

        # Backfill profile_url for existing rows that now have a URL
        if url_updates:
            client = get_supabase_client()
            if progress_cb:
                progress_cb(0.08, f"Updating profile URLs for {len(url_updates)} existing connections…")
            for item in url_updates:
                fn, ln, co = item["key"]
                client.table("connections").update(
                    {"profile_url": item["profile_url"]}
                ).eq("user_id", user_id).eq("first_name", fn).eq("last_name", ln).eq("company", co).execute()

        if not new_rows:
            if progress_cb:
                progress_cb(1.0, "Done!")
            return 0, duplicates, None

        if progress_cb:
            progress_cb(0.15, f"Generating embeddings for {len(new_rows)} new connections…")

        texts = [_connection_to_text(r) for r in new_rows]
        embeddings = _generate_embeddings(texts, progress_cb=progress_cb)

        if progress_cb:
            progress_cb(0.85, "Saving to database…")

        client = get_supabase_client()
        records = []
        for row, emb in zip(new_rows, embeddings):
            rec = {"user_id": user_id}
            for col in CORE_COLS:
                rec[col] = str(row.get(col, ""))
            rec["embedding"] = emb
            records.append(rec)

        # Insert in chunks to avoid request-size limits
        chunk = 100
        for i in range(0, len(records), chunk):
            client.table("connections").insert(records[i : i + chunk]).execute()

        if progress_cb:
            progress_cb(1.0, "Done!")

        return len(records), duplicates, None

    except Exception as e:
        return 0, 0, str(e)


def get_connections(user_id: str) -> pd.DataFrame:
    """Load all connections for a user (without the embedding vector)."""
    try:
        client = get_supabase_client()
        all_rows = []
        page_size = 1000
        offset = 0

        while True:
            resp = (
                client.table("connections")
                .select("first_name,last_name,email,company,position,connected_on,profile_url")
                .eq("user_id", user_id)
                .range(offset, offset + page_size - 1)
                .execute()
            )
            batch = resp.data or []
            all_rows.extend(batch)
            if len(batch) < page_size:
                break
            offset += page_size

        if all_rows:
            return pd.DataFrame(all_rows).fillna("")
        return pd.DataFrame()
    except Exception as e:
        import streamlit as st
        st.error(f"Error loading connections: {e}")
        return pd.DataFrame()


def get_connection_stats(user_id: str) -> dict:
    """Return {total, last_import} for the Settings / Your data panel."""
    try:
        client = get_supabase_client()
        resp = (
            client.table("connections")
            .select("id,created_at")
            .eq("user_id", user_id)
            .execute()
        )
        rows = resp.data or []
        total = len(rows)
        last_import = "—"
        if rows:
            dates = [r["created_at"] for r in rows if r.get("created_at")]
            if dates:
                last_import = max(dates)[:10]
        return {"total": total, "last_import": last_import}
    except Exception:
        return {"total": 0, "last_import": "—"}


def clear_connections(user_id: str) -> tuple[bool, str | None]:
    """Delete all connections (and their embeddings) for a user."""
    try:
        client = get_supabase_client()
        client.table("connections").delete().eq("user_id", user_id).execute()
        return True, None
    except Exception as exc:
        return False, str(exc)


def export_connections_csv(user_id: str) -> str:
    """Return a CSV string of all connections for download."""
    try:
        client = get_supabase_client()
        resp = (
            client.table("connections")
            .select("first_name,last_name,email,company,position,connected_on")
            .eq("user_id", user_id)
            .execute()
        )
        rows = resp.data or []
        if not rows:
            return ""
        return pd.DataFrame(rows).to_csv(index=False)
    except Exception:
        return ""
