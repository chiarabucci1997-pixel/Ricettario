-- ═══════════════════════════════════════════════════════════════
-- Migrazione 03 — da eseguire UNA VOLTA su Supabase (SQL Editor).
-- Aggiunge la sezione STRUMENTAZIONE in fondo alla ricetta:
-- un elenco di chiavi, es. ["coltello","frusta","tortiera"].
--
-- Se stai partendo da zero, esegui solo schema.sql: lo ha già dentro.
-- ═══════════════════════════════════════════════════════════════

alter table ricette_salate add column if not exists strumenti jsonb not null default '[]'::jsonb;
alter table ricette_dolci  add column if not exists strumenti jsonb not null default '[]'::jsonb;
