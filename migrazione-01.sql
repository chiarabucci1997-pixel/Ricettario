-- ═══════════════════════════════════════════════════════════════
-- Migrazione 01 — da eseguire UNA VOLTA su Supabase (SQL Editor)
-- se hai già creato le tabelle con la prima versione di schema.sql.
--
-- Se invece stai partendo da zero, esegui direttamente schema.sql:
-- lo ha già dentro tutto.
-- ═══════════════════════════════════════════════════════════════

-- 1. nuovo campo "Dosi / Persone"
alter table ricette_salate add column if not exists dosi text not null default '';
alter table ricette_dolci  add column if not exists dosi text not null default '';

-- 2. categoria rinominata: Sfizietà → Sfiziosità
update ricette_salate set categoria = 'Sfiziosità' where categoria = 'Sfizietà';
