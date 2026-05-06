-- ============================================================
-- ConnectionsFun - Supabase Schema
-- Run this entire file in your Supabase SQL Editor
-- ============================================================

-- 1. Enable pgvector extension (required for embeddings)
create extension if not exists vector;

-- 2. Connections table
create table if not exists public.connections (
    id            uuid        default gen_random_uuid() primary key,
    user_id       uuid        references auth.users(id) on delete cascade not null,
    first_name    text        default '',
    last_name     text        default '',
    email         text        default '',
    company       text        default '',
    "position"    text        default '',
    connected_on  text        default '',
    embedding     vector(768),
    created_at    timestamptz default now()
);

-- 3. Row Level Security
alter table public.connections enable row level security;

create policy "Users can view own connections"
    on public.connections for select
    using (auth.uid() = user_id);

create policy "Users can insert own connections"
    on public.connections for insert
    with check (auth.uid() = user_id);

create policy "Users can delete own connections"
    on public.connections for delete
    using (auth.uid() = user_id);

-- 4. Indexes
create index if not exists connections_user_id_idx
    on public.connections(user_id);

create index if not exists connections_embedding_idx
    on public.connections using hnsw (embedding vector_cosine_ops);

-- 5. Vector similarity search function (used by RAG)
create or replace function match_connections(
    query_embedding  vector(768),
    match_count      int,
    filter_user_id   uuid
)
returns table (
    id           uuid,
    first_name   text,
    last_name    text,
    company      text,
    "position"   text,
    connected_on text,
    similarity   float
)
language plpgsql
as $$
begin
    return query
    select
        c.id,
        c.first_name,
        c.last_name,
        c.company,
        c."position",
        c.connected_on,
        1 - (c.embedding <=> query_embedding) as similarity
    from public.connections c
    where c.user_id = filter_user_id
      and c.embedding is not null
    order by c.embedding <=> query_embedding
    limit match_count;
end;
$$;
