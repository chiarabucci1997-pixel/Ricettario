-- ═══════════════════════════════════════════════════════════════
-- Importazione delle 30 ricette dal file "Ricette 🍰 .docx"
--
-- PRIMA di questo file esegui, se non lo hai già fatto:
--   migrazione-01.sql  (dosi, rinomina Sfizietà)
--   migrazione-02.sql  (autore)
--   migrazione-03.sql  (strumenti)
--   migrazione-04.sql  (note)
--
-- Rieseguirlo è innocuo: ogni ricetta viene inserita solo se non esiste
-- già una con lo stesso titolo nella stessa tabella.
--
-- Dove il Word aveva solo il link, ingredienti e procedimento sono il
-- riassunto della pagina originale. Il link resta salvato in ogni caso.
-- ═══════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────
--  DOLCI — 19 ricette
-- ─────────────────────────────────────────────────────────────
insert into ricette_dolci
  (categoria, titolo, link, dosi, autore, prep_time, cook_time, total_time,
   tools, ingredienti, procedimento, strumenti, note)
select v.* from (values

('Torte', 'Torta zucca e mele',
 'https://www.contemporaneofood.com/torta-sofficissima-alla-zucca-con-mele-e-mandorlato-alla-vaniglia-e-cannella/',
 '6 porzioni', 'Chiara e Ale', '0:25', '1:05', '1:30',
 '{"forno":"150° ventilato, 50-55 min + 10 min a forno spento"}'::jsonb,
 E'BASE ALLA ZUCCA\n130 g burro\n130 g farina\n130 g zucca pulita\n100 g zucchero di canna\n50 g maizena\n20 g zucchero a velo\n2 uova\n12 g lievito\n1/2 stecca di vaniglia\n\nMANDORLATO\n120 g farina\n100 g mandorle\n50 g burro\n40 g zucchero di canna\n3 cucchiai di miele\n2 cucchiaini di cannella\n1/2 stecca di vaniglia\n\nCOMPOSIZIONE\n450 g mele\nZucchero a velo q.b.',
 '["Accendi il forno a 150° ventilato e trita le mandorle grossolanamente","Fondi miele e burro a fiamma bassissima, poi mescola con farina, cannella, vaniglia, zucchero e mandorle","Riduci la zucca in purea e lavora il burro morbido con lo zucchero di canna fino a spumoso","Aggiungi le uova, poi metà amido, lievito, vaniglia e zucchero a velo; unisci zucca, farina e amido restante","Versa in teglia imburrata da 20 cm, aggiungi le mele a cubetti e finisci col mandorlato spezzettato","Cuoci 50-55 minuti proteggendo la superficie verso la fine, poi spegni e lascia lo sportello aperto 10 minuti","Fai raffreddare del tutto e servi a temperatura ambiente con zucchero a velo"]'::jsonb,
 '["ciotola","teglia","coltello","sbattitore"]'::jsonb,
 'Particolare, bella strutturata.'),

('Torte', 'Torta di mele Princi',
 '', '', 'Princi', '', '0:45', '0:45',
 '{"forno":"170°, 40-45 min (forse un po'' di più)"}'::jsonb,
 E'1 misurino di yogurt alla vaniglia\n3 misurini di farina\n2 misurini di zucchero\n1 bustina di lievito\n3 uova\n1 misurino di olio di semi\n1 pizzico di sale\n1 cucchiaio di amido di mais (rende tutto più soffice)\n2 mele renette (1 sopra a raggiera, 1 a cubetti nell''impasto)\n1 limone per il succo (tieni le mele in ammollo mentre fai il resto)\nCannella q.b.',
 '["Taglia le mele e mettile in ammollo nel succo di limone","Monta zucchero e uova","Aggiungi farina, amido, lievito, sale, cannella, olio e yogurt","Incorpora le mele a cubetti","Imburra e infarina uno stampo da torta","Versa il composto e disponi le mele a raggiera sopra","Inforna 40-45 minuti a 170°"]'::jsonb,
 '["ciotola","tortiera","sbattitore","coltello"]'::jsonb,
 E'Da capire se coprire le mele in superficie per non farle bruciare.\nStatico o ventilato? Da provare.'),

('Biscotti', 'Biscotti Nonna Maria',
 '', '', 'Nonna Maria', '', '0:15', '0:15',
 '{"forno":"180°, 15 min"}'::jsonb,
 E'550 g farina\n2 uova\n200 g zucchero\n1/2 bicchiere di olio di semi\n1/2 bicchiere di latte\n1 bustina di lievito',
 '["Impasta tutti gli ingredienti","Forma delle striscette","Spolvera lo zucchero su ogni biscotto prima di cuocere","Inforna a 180° per 15 minuti"]'::jsonb,
 '["ciotola","teglia"]'::jsonb, ''),

('Torte', 'Ciambellone di Nonna Maria',
 '', '', 'Nonna Maria', '', '0:40', '0:40',
 '{"forno":"140° per 20 min, poi 180° per altri 20 min"}'::jsonb,
 E'4 uova\n4 bicchieri di farina\n1 bicchiere di zucchero (abbonda)\n1 bicchiere di olio\n1,5 bicchieri di latte\n1 bustina di lievito\nScorza di un limone',
 '["Sbatti le uova con lo zucchero","Aggiungi olio, latte, farina, lievito e scorza di limone","Versa nello stampo da ciambellone","Cuoci a 140° per 20 minuti, poi a 180° per altri 20"]'::jsonb,
 '["ciotola","tortiera"]'::jsonb, ''),

('Biscotti', 'Sfogliette per consumare albumi',
 'https://blog.giallozafferano.it/cuochinprogress/sfogliette-di-albumi-e-mandorle/',
 '', 'Chiara e Ale', '0:10', '0:35', '0:45',
 '{"forno":"180° ventilato 25 min, poi 150° ventilato 15 min"}'::jsonb,
 E'100 g albumi a temperatura ambiente\n100 g zucchero\n1 pizzico di sale\n100 g farina 00\n100 g mandorle non pelate',
 '["Monta gli albumi con il sale, aggiungi metà zucchero e mescola un minuto","Aggiungi il resto dello zucchero e monta 5 minuti fino a composto spumoso","Incorpora la farina setacciata con movimenti dal basso verso l''alto","Unisci le mandorle e mescola bene","Versa nello stampo rivestito di carta forno bagnata e strizzata","Inforna a 180° ventilato per 25 minuti, poi fai raffreddare","Taglia in sfoglie di 2 mm e ripassa in forno a 150° per 15 minuti fino a croccantezza"]'::jsonb,
 '["sbattitore","ciotola","setaccio","teglia","coltello"]'::jsonb, ''),

('Biscotti', 'Mikado',
 'https://www.ricetteperbimby.it/ricette/mikado-bimby',
 '300 g', 'Chiara e Ale', '0:15', '0:15', '0:30',
 '{"forno":"160° statico, 15-17 min","frigo":"fino a raffreddamento completo","frullatore":"30 sec, vel. 4"}'::jsonb,
 E'250 g farina 00\n40 g zucchero a velo\n40 g burro\n100 g acqua\n1 pizzico di sale fino\nCioccolato fondente e bianco q.b.',
 '["Frulla tutti gli ingredienti 30 secondi a velocità 4","Forma una palla e stendi l''impasto a 1-2 mm","Taglia striscioline lunghe 10 cm e arrotolale su se stesse","Disponile sulla teglia con carta forno","Inforna a 160° per 15-17 minuti","Sforna, fai intiepidire e ricopri ogni bastoncino di cioccolato fuso","Fai raffreddare del tutto in frigorifero"]'::jsonb,
 '["mattarello","teglia","coltello"]'::jsonb, ''),

('Vario', 'Pancake',
 '', '', 'Chiara e Ale', '', '', '',
 '{"pentola":"pentolino per fondere il burro","frigo":"1 ora di riposo, facoltativo"}'::jsonb,
 E'177 ml latte\n2 cucchiai di aceto di vino\n190 g farina 00\n2 cucchiai di zucchero\n1 cucchiaino di lievito\n0,5 cucchiaino di bicarbonato\n0,5 cucchiaino di sale\n1 uovo\n2 cucchiai di burro fuso',
 '["Fai fondere il burro in un pentolino","Unisci aceto e latte e lascia fermentare qualche minuto","Setaccia tutte le polveri","Unisci l''uovo al latte fermentato","Mescola polveri e liquidi con la frusta","Aggiungi per ultimo il burro fuso"]'::jsonb,
 '["frusta","ciotola","setaccio"]'::jsonb,
 'Se l''impasto riposa in frigo 1 ora è meglio.'),

('Vario', 'Crepes',
 'https://www.soniaperonaci.it/crepes/', '', 'Chiara e Ale', '', '', '',
 '{}'::jsonb, '', '[]'::jsonb, '[]'::jsonb, ''),

('Torte', 'Torta noci pecan',
 'https://www.lucake.it/pecan-pie/',
 '10 fette', 'Chiara e Ale', '0:35', '0:50', '1:25',
 '{"forno":"175-180°, 45-50 min","frigo":"2 ore di riposo per la frolla"}'::jsonb,
 E'230 g farina 00\n130 g burro freddo + 50 g fuso\n70 g acqua fredda\n5 g zucchero\n2 g sale + 1 pizzico\n3 uova\n100 g zucchero di canna scuro\n100 g miele\n100 g sciroppo d''acero\n180 g noci pecan tritate\n65-70 gherigli di noci pecan interi',
 '["Impasta farina, zucchero, sale e burro freddo fino a consistenza sabbiosa","Aggiungi l''acqua fredda e compatta l''impasto","Forma un panetto, avvolgilo nella pellicola e fallo riposare 2 ore in frigo","Prepara il ripieno: sbatti uova, zucchero di canna, miele, sciroppo d''acero, burro fuso e sale, poi unisci le noci tritate","Stendi la pasta a 4 mm, fodera una teglia da 22 cm, bucherella il fondo e crea il bordo ondulato","Versa il ripieno e copri con le noci pecan intere","Cuoci a 175-180° per 45-50 minuti e fai raffreddare prima di sformare"]'::jsonb,
 '["mattarello","tortiera","ciotola","coltello"]'::jsonb,
 'Servono 2 ore di riposo in frigo per la frolla, oltre ai tempi indicati.'),

('Torte', 'Carrot cake',
 'https://www.lucake.it/torta-di-carote/',
 '10 fette', 'Chiara e Ale', '0:20', '0:45', '1:05',
 '{"forno":"175° statico, 40-45 min, ripiano basso","frullatore":"carote e olio fino a polpa omogenea"}'::jsonb,
 E'375 g carote\n120 g olio di semi\n190 g zucchero\n3 uova\nScorza d''arancia grattugiata\n1 pizzico di sale\n190 g farina 00\n50 g fecola\n16 g lievito per dolci',
 '["Frulla le carote a rondelle con l''olio fino a ottenere una polpa omogenea","Monta zucchero, uova intere, scorza d''arancia e sale per 5-10 minuti fino a spumoso","Aggiungi il composto di carote e olio e mescola","Incorpora farina, fecola e lievito setacciati","Versa in una tortiera da 22 cm unta e infarinata","Cuoci in forno a 175° per 40-45 minuti nel ripiano basso","Fai raffreddare e sforma"]'::jsonb,
 '["planetaria","tortiera","setaccio"]'::jsonb,
 'Versione Ale: 300 g di carote e la polpa di 1/2 arancia al posto di 75 g di carote.'),

('Creme e basi', 'Tiramisu Lella',
 '', '', 'Lella', '', '', '',
 '{"frullatore":"per montare tutto"}'::jsonb,
 E'500 g mascarpone\n200 g panna\n6 tuorli\n6 cucchiai di zucchero',
 '["Monta bene zucchero e tuorli per almeno 5 minuti","Aggiungi il mascarpone","Aggiungi per ultima la panna, sempre col frullatore"]'::jsonb,
 '["ciotola","sbattitore"]'::jsonb, ''),

('Creme e basi', 'Crema chantilly Lella',
 '', '', 'Lella', '', '0:05', '0:05',
 '{"pentola":"latte a inizio bollore, poi addensare 5 min a fiamma moderata","frigo":"raffredda la pasticciera"}'::jsonb,
 E'3 tuorli\n3 cucchiai di zucchero\n1/2 litro di latte\n1 cucchiaio e 1/2 di farina\nVanillina o buccia di limone per aromatizzare\n+ 250 ml di panna (per la chantilly)',
 '["Scalda il latte in pentola con vanillina o buccia di limone fino a inizio bollore","In una ciotola monta bene tuorli, zucchero e farina con la frusta a mano","Aggiungi il latte caldo, amalgama e rimetti in pentola a fiamma moderata","Addensa circa 5 minuti girando sempre, finché è bella densa","Fai raffreddare la pasticciera in frigo","Monta 250 ml di panna e uniscila lentamente con la spatola alla crema fredda"]'::jsonb,
 '["frusta","ciotola","spatola"]'::jsonb,
 E'Pasticciera + 250 ml di panna montata = chantilly.\nGira sempre con un cucchiaio: si attacca e brucia facilmente.'),

('Torte', 'Brownies',
 'https://www.tavolartegusto.it/ricetta/brownies-al-cioccolato-fondente-ricetta-originale/',
 '9 brownies', 'Chiara e Ale', '0:15', '0:30', '0:45',
 '{"forno":"180° statico o 160° ventilato, 30 min, ripiano medio-alto","pentola":"bagnomaria per cioccolato e burro"}'::jsonb,
 E'225 g cioccolato fondente\n225 g burro\n225 g zucchero semolato\n4 uova grandi\n135 g farina 00\n15 g cacao amaro in polvere\n1/2 cucchiaino di lievito per dolci\n1 pizzico di sale',
 '["Sciogli cioccolato e burro a bagnomaria a fuoco basso e lascia raffreddare","Mescola farina, lievito, sale e cacao in una ciotola","Monta uova e zucchero fino a triplicare il volume","Versa il cioccolato nelle uova e amalgama dal basso verso l''alto con la spatola","Setaccia le polveri in due riprese e mescola delicatamente","Versa in una teglia 24x24 cm rivestita di carta forno","Cuoci a 180° statico per 30 minuti"]'::jsonb,
 '["ciotola","spatola","setaccio","teglia","sbattitore"]'::jsonb, ''),

('Creme e basi', 'Frolla mamma Dora',
 '', '', 'mamma Dora', '', '', '',
 '{}'::jsonb,
 E'300 g farina\n150 g zucchero\n150 g burro\n2 tuorli + 1 uovo intero',
 '[]'::jsonb, '["ciotola"]'::jsonb, ''),

('Torte', 'Crostata di ricotta (Pasqua)',
 '', '', 'Chiara e Ale', '', '', '',
 '{}'::jsonb,
 E'250 g ricotta\n3 tuorli\n200 g gocce di cioccolato fondente',
 '[]'::jsonb, '["ciotola"]'::jsonb, ''),

('Biscotti', 'Biscotti al Limone (Palline)',
 'https://www.facebook.com/buonidearicette/videos/1894778907406508/',
 '', 'Chiara e Ale', '', '', '',
 '{}'::jsonb, '', '[]'::jsonb, '[]'::jsonb,
 E'Varianti:\nLimone e rosmarino\nArancia\nArancia e cacao\nFarina d''arachidi e gocce di cioccolato'),

('Creme e basi', 'Lemon Curd',
 'https://www.lucake.it/lemon-meringue-pie/',
 '', 'Chiara e Ale', '', '', '',
 '{"frigo":"2-3 ore di riposo"}'::jsonb, '',
 '["Prepara una dose di lemon curd","Trasferisci la crema in una pirofila e copri con pellicola a contatto","Fai raffreddare a temperatura ambiente, poi in frigo almeno 2-3 ore","Prima di usarlo mescola con un leccapentole"]'::jsonb,
 '["spatola","ciotola"]'::jsonb,
 'La ricetta del lemon curd sta dentro la ricetta della crostata (lemon meringue pie).'),

('Torte', 'Muffin al cioccolato',
 'https://www.instagram.com/p/B2Ylfk_niya/', '', 'Chiara e Ale', '', '', '',
 '{}'::jsonb, '', '[]'::jsonb, '[]'::jsonb, ''),

('Creme e basi', 'Coulisse di lamponi',
 '', '', 'Chiara e Ale', '', '0:15', '0:15',
 '{"padella":"15 min finché si addensa"}'::jsonb,
 E'1 scatola di lamponi\n2 cucchiai di zucchero',
 '["Metti i lamponi in padella con lo zucchero","Fai andare circa 15 minuti finché si sciolgono e si addensa","Filtra per levare i semini"]'::jsonb,
 '["setaccio","spatola"]'::jsonb, '')

) as v(categoria, titolo, link, dosi, autore, prep_time, cook_time, total_time,
       tools, ingredienti, procedimento, strumenti, note)
where not exists (select 1 from ricette_dolci d where d.titolo = v.titolo);


-- ─────────────────────────────────────────────────────────────
--  SALATE — 11 ricette
-- ─────────────────────────────────────────────────────────────
insert into ricette_salate
  (categoria, titolo, link, dosi, autore, prep_time, cook_time, total_time,
   tools, ingredienti, procedimento, strumenti, note)
select v.* from (values

('Pane e Lievitati', 'Pane macchina del pane',
 'https://www.ricetteperlamacchinadelpane.it/ricetta-pane-bianco/',
 '1 pagnotta da circa 800 g', 'Chiara e Ale', '0:05', '', '',
 '{}'::jsonb,
 E'360 g farina 00\n190 g farina Manitoba\n300 ml acqua\n2 cucchiai di olio extravergine d''oliva\n12,5 g lievito fresco\n1 cucchiaino e 1/2 di sale\n1 cucchiaino di zucchero',
 '["Versa nel cestello prima i liquidi (acqua e olio), poi le farine","Fai un pozzo centrale per il lievito frantumato","Aggiungi sale e zucchero ai lati","Avvia il programma e controlla che l''impasto non resti attaccato ai bordi","Al termine estrai il cestello con cautela","Togli il pane con una spatola e fallo raffreddare prima di consumarlo"]'::jsonb,
 '["bilancia"]'::jsonb,
 E'Programma "Pane bianco" (di solito il numero 1), circa 3 ore, cottura media o elevata.\nSul sito ci sono tutte le ricette per la macchina del pane.'),

('Pane e Lievitati', 'Taralli papà',
 '', '', 'papà', '', '', '', '{}'::jsonb, '', '[]'::jsonb, '[]'::jsonb, ''),

('Pane e Lievitati', 'Impasto pizza Pigi',
 '', '', 'Pigi', '', '', '', '{}'::jsonb, '', '[]'::jsonb, '[]'::jsonb, ''),

('Pane e Lievitati', 'Impasto pizza Lella',
 '', '', 'Lella', '', '', '', '{}'::jsonb, '', '[]'::jsonb, '[]'::jsonb, ''),

('Primi Piatti', 'Vellutata porro-carote e patate',
 '', '', 'Chiara e Ale', '', '', '',
 '{"pentola":"verdure coperte d''acqua fino a cottura","frullatore":"frulla a fine cottura"}'::jsonb,
 'Porro, patate e carote in proporzione 1:1:1',
 '["Taglia le verdure a cubetti","Mettile in pentola e ricoprile d''acqua","Una volta cotte, frulla il tutto"]'::jsonb,
 '["coltello","tagliere"]'::jsonb, ''),

('Sfiziosità', 'Hummus',
 '', '', 'Chiara e Ale', '', '', '', '{}'::jsonb, '', '[]'::jsonb, '[]'::jsonb, ''),

('Primi Piatti', 'Vellutata di sedano e mele',
 '', '', 'Chiara e Ale', '', '', '',
 '{"pentola":"","frullatore":""}'::jsonb,
 E'1 mazzo di sedano\n2 mele',
 '[]'::jsonb, '["coltello","tagliere"]'::jsonb,
 'Per non buttare le foglie di sedano.'),

('Primi Piatti', 'Zuppa toscana',
 '', '', 'Chiara e Ale', '', '', '', '{}'::jsonb, '', '[]'::jsonb, '[]'::jsonb, ''),

('Secondi Piatti', 'Panino Melanzane',
 'https://www.instagram.com/reel/CqLScWmMAD2/', '', 'Chiara e Ale', '', '', '',
 '{}'::jsonb, '', '[]'::jsonb, '[]'::jsonb,
 'Da provare con coulisse di fragole.'),

('Secondi Piatti', 'Burritos',
 '', '', 'Chiara e Ale', '', '', '',
 '{"padella":"soffritto di carota e cipolla"}'::jsonb,
 E'1 barattolo di fagioli in salsa messicana\nCarota\nCipolla\nMais\nScamorza o halloumi\nHummus o guacamole\nMaionese\nRiso basmati',
 '["Fai un soffritto di carota e cipolla","Aggiungi i fagioli in salsa messicana e il mais","Grattugia la scamorza, oppure piastra l''halloumi","Prepara riso basmati, hummus, guacamole e maionese","Componi i burritos"]'::jsonb,
 '["coltello","tagliere","grattugia"]'::jsonb, ''),

('Sfiziosità', 'Ceci Croccanti',
 'https://www.ilcuoreinpentola.it/ricette/aperitivi/ceci-croccanti-al-forno/',
 '4 persone', 'Chiara e Ale', '0:05', '0:30', '0:35',
 '{"forno":"200° ventilato, 30 min, ripiano medio"}'::jsonb,
 E'400 g ceci precotti\n1 cucchiaio di farina 00\n1 cucchiaino di sale\n1 cucchiaino di paprika affumicata\nPepe e rosmarino\n3 cucchiai di olio d''oliva',
 '["Accendi il forno a 200° ventilato","Sgocciola, sciacqua e asciuga bene i ceci con uno strofinaccio","Mescola i ceci con farina, sale, pepe e paprika","Distribuisci l''olio nella teglia e aggiungi i ceci senza sovrapporli","Aggiungi il rosmarino e inforna sul ripiano medio","Muovi la teglia durante la cottura e verifica la croccantezza a 30 minuti","Sforna, fai intiepidire qualche minuto e servi"]'::jsonb,
 '["teglia","ciotola"]'::jsonb, '')

) as v(categoria, titolo, link, dosi, autore, prep_time, cook_time, total_time,
       tools, ingredienti, procedimento, strumenti, note)
where not exists (select 1 from ricette_salate s where s.titolo = v.titolo);
