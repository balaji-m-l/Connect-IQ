# ConnectionsFun 🔗

A Streamlit web app that lets you upload your LinkedIn connections export, visualize your professional network through interactive charts, and chat with an AI assistant to get grounded, hallucination-free answers about your connections.

---

## Features

- **Interactive Dashboard** — visualize your network by company, job title, and connection growth over time
- **RAG-Powered AI Chat** — ask natural language questions like *"List all recruiters in Finance"* or *"Who do I know at Google?"* — answers are grounded in your actual data
- **Additive Uploads** — upload multiple CSV files over time; duplicates are skipped automatically
- **Secure by Design** — Supabase Row Level Security ensures only you can access your data

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (multi-page) |
| Database & Auth | Supabase (PostgreSQL + pgvector) |
| Embeddings | Google `gemini-embedding-001` via REST API |
| LLM | Google Gemini 2.5 Flash |
| Charts | Plotly |
| Data processing | pandas |

---

## Prerequisites

- Python 3.11 or 3.12
- A [Supabase](https://supabase.com) project
- A [Google AI Studio](https://aistudio.google.com) API key (Gemini)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/connection_is_fun.git
cd connection_is_fun
```

### 2. Create a virtual environment

```bash
py -3.11 -m venv venv311
venv311\Scripts\activate      # Windows
source venv311/bin/activate   # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt --prefer-binary
```

### 4. Configure environment variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Set up the Supabase database

1. Open your Supabase project → **SQL Editor**
2. Run the full contents of `supabase_schema.sql`
3. Then run the following grants:

```sql
grant usage on schema public to anon, authenticated;
grant select, insert, delete on public.connections to authenticated;
grant execute on function match_connections to authenticated;
```

---

## Running the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How to export your LinkedIn connections

1. Go to LinkedIn → **Me** → **Settings & Privacy**
2. **Data Privacy** → **Get a copy of your data**
3. Select **Connections** → **Request archive**
4. Download the ZIP and extract `Connections.csv`
5. Upload it via the **Upload CSV** button on the Dashboard

---

## Project Structure

```
connection_is_fun/
├── app.py                  # Landing page
├── pages/
│   ├── 1_Login.py          # Login & sign up
│   ├── 2_Home.py           # Dashboard with charts
│   └── 3_Chat.py           # AI chat interface
├── utils/
│   ├── supabase_client.py  # Supabase singleton
│   ├── auth.py             # Login / signup / logout
│   ├── data_processor.py   # CSV parsing, embeddings, Supabase CRUD
│   └── llm.py              # RAG pipeline + Gemini chat
├── components/
│   ├── styles.py           # Shared CSS (Airbnb-inspired)
│   └── sidebar.py          # Navigation sidebar
├── supabase_schema.sql     # Database schema (run once in Supabase)
├── requirements.txt
└── .env.example
```

---

## RAG Architecture

```
Upload CSV
    │
    ▼
Parse connections → Generate embeddings (gemini-embedding-001, 768-dim)
    │
    ▼
Store in Supabase pgvector (vector(768) + HNSW index)

Chat query
    │
    ▼
Embed question → Cosine similarity search (top-100)
    + Keyword stem boost (recruiter → recruit → "Digital Recruiter" ✓)
    │
    ▼
Retrieved connections → Gemini 2.5 Flash → Grounded answer
```

---

## Deployment Notes

Before deploying to production:

- [ ] Re-enable Supabase email confirmation: **Authentication → Providers → Email → Confirm email: ON**
- [ ] Update `_RPM = 1500` in `utils/data_processor.py` (already set for paid tier)
- [ ] Set environment variables in your hosting platform (not in `.env`)
- [ ] Ensure `.env` is in `.gitignore` and never committed

---

## License

MIT
