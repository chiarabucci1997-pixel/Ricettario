-- ═══════════════════════════════════════════════════════════════
-- Migrazione 02 — da eseguire UNA VOLTA su Supabase (SQL Editor).
-- Aggiunge il campo "autore" mostrato in fondo alla ricetta.
--
-- Se stai partendo da zero, esegui solo schema.sql: lo ha già dentro.
-- ═══════════════════════════════════════════════════════════════

alter table ricette_salate add column if not exists autore text not null default '';
alter table ricette_dolci  add column if not exists autore text not null default '';
