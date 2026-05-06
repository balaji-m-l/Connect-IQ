import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

from utils.supabase_client import get_supabase_client

load_dotenv(override=True)


def _configure() -> None:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in .env")
    genai.configure(api_key=api_key)


# ---------------------------------------------------------------------------
# Retrieval layer
# ---------------------------------------------------------------------------

_EMBED_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-embedding-001:embedContent"
)


def _embed_query(question: str) -> list[float]:
    api_key = os.getenv("GEMINI_API_KEY", "")
    resp = requests.post(
        _EMBED_URL,
        params={"key": api_key},
        json={
            "content": {"parts": [{"text": question}]},
            "taskType": "RETRIEVAL_QUERY",
            "outputDimensionality": 768,
        },
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(f"Embedding API error {resp.status_code}: {resp.text}")
    return resp.json()["embedding"]["values"]


def _vector_search(user_id: str, query_embedding: list[float], top_k: int = 100) -> list[dict]:
    """Cosine-similarity search via the match_connections Postgres function."""
    client = get_supabase_client()
    resp = client.rpc(
        "match_connections",
        {
            "query_embedding": query_embedding,
            "match_count": top_k,
            "filter_user_id": user_id,
        },
    ).execute()
    return resp.data or []


def _stem(word: str) -> str:
    """Strip common suffixes so plural/verb forms match their root (recruiters → recruit)."""
    for suffix in ("lers", "ers", "ing", "ed", "er", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            return word[: -len(suffix)]
    return word


def _keyword_boost(user_id: str, question: str, seen_ids: set) -> list[dict]:
    """
    Supplement vector results with keyword matches on position/company.
    Uses stemmed search terms so 'recruiters' also matches 'Digital Recruiter'.
    """
    client = get_supabase_client()
    raw_words = [w.strip("?.,!") for w in question.lower().split() if len(w.strip("?.,!")) > 3]

    # Build unique search terms: original + stemmed root (deduplicated)
    search_terms: list[str] = []
    for w in raw_words[:6]:
        if w not in search_terms:
            search_terms.append(w)
        root = _stem(w)
        if root != w and root not in search_terms:
            search_terms.append(root)

    extras: list[dict] = []
    for term in search_terms:
        try:
            for field in ("position", "company"):
                resp = (
                    client.table("connections")
                    .select("id,first_name,last_name,company,position,connected_on")
                    .eq("user_id", user_id)
                    .ilike(field, f"%{term}%")
                    .execute()
                )
                for row in resp.data or []:
                    if row["id"] not in seen_ids:
                        extras.append(row)
                        seen_ids.add(row["id"])
        except Exception:
            continue

    return extras


def _format_context(connections: list[dict]) -> str:
    if not connections:
        return "No relevant connections were found for this query."

    lines = [f"Relevant connections retrieved ({len(connections)} total):\n"]
    for c in connections:
        name = f"{c.get('first_name', '')} {c.get('last_name', '')}".strip()
        position = c.get("position", "").strip()
        company = c.get("company", "").strip()
        connected_on = c.get("connected_on", "").strip()

        line = f"• {name}"
        if position:
            line += f", {position}"
        if company:
            line += f" at {company}"
        if connected_on:
            line += f" (connected: {connected_on})"
        lines.append(line)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_chat_response(
    question: str,
    user_id: str,
    total_connections: int,
    history: list[dict],
) -> str:
    """
    RAG pipeline:
      1. Embed the question
      2. Vector-search the user's connections
      3. Keyword-boost for broad recall
      4. Pass retrieved context + history to Gemini Flash
    history items: {"role": "user"|"assistant", "content": str}
    """
    try:
        _configure()

        # --- Retrieval ---
        query_emb = _embed_query(question)
        retrieved = _vector_search(user_id, query_emb, top_k=100)
        seen_ids = {r["id"] for r in retrieved}
        retrieved += _keyword_boost(user_id, question, seen_ids)

        context = _format_context(retrieved)

        # --- Generation ---
        system_instruction = f"""You are a helpful assistant analyzing the user's LinkedIn professional network.

The user has {total_connections} total connections. The most relevant connections for this query were retrieved using semantic search and keyword matching:

{context}

Guidelines:
- Base your answer strictly on the connections listed above.
- When listing people, always include: full name, job title, company, and connection date.
- Format lists with bullet points for readability.
- If a query asks for "all" of a category, note that results reflect the closest semantic matches; some edge cases may not appear.
- If the data does not contain enough information to answer, say so honestly.
- Never invent or hallucinate connections that are not in the list above."""

        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            system_instruction=system_instruction,
        )

        # Convert stored history to Gemini format (exclude the last user message,
        # which is sent as the current turn)
        gemini_history = []
        for msg in history[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})

        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(question)
        return response.text

    except Exception as e:
        return f"⚠️ Error: {e}\n\nPlease check that your GEMINI_API_KEY is set correctly in .env."
