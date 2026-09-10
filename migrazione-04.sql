-- ═══════════════════════════════════════════════════════════════
-- Migrazione 04 — da eseguire UNA VOLTA su Supabase (SQL Editor).
-- Aggiunge il campo "note", mostrato in fondo alla ricetta: serve per le
-- annotazioni che non sono passaggi ("Particolare, bella strutturata",
-- "Varianti: limone e rosmarino", "Da provare con coulisse di fragole").
--
-- Se stai partendo da zero, esegui solo schema.sql: lo ha già dentro.
-- ═══════════════════════════════════════════════════════════════

alter table ricette_salate add column if not exists note text not null default '';
alter table ricette_dolci  add column if not exists note text not null default '';
