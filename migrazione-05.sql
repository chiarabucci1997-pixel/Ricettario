-- ═══════════════════════════════════════════════════════════════
-- Migrazione 05 — da eseguire UNA VOLTA su Supabase (SQL Editor).
-- Nelle ricette dolci la categoria "Dolci" diventa "Vario".
--
-- Senza questo, le ricette già salvate con categoria "Dolci" comparirebbero
-- in fondo all'indice sotto il vecchio nome (l'app mostra le categorie
-- orfane invece di nascondere le ricette, ma è meglio sistemarle).
-- ═══════════════════════════════════════════════════════════════

update ricette_dolci set categoria = 'Vario' where categoria = 'Dolci';
