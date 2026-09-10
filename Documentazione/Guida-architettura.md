# Architettura: sito statico + Supabase

Guida per costruire un'app con la stessa struttura tecnologica di «Ricettario».
Scritta per essere passata a un assistente che deve partire da zero.

---

## Lo stack in una riga

**Sito statico** (HTML/CSS/JS, nessun build step) su **Vercel**, codice su **GitHub**,
che parla **direttamente** a **PostgreSQL su Supabase** via HTTP. Nessun backend scritto
da noi: PostgREST espone le tabelle come API, e le **Row Level Security policy** sono
l'unico strato di sicurezza.

```
TU ──push──▶ GITHUB ──webhook──▶ VERCEL ──file statici──▶ BROWSER / IPHONE
                                                              │        │
                                            email+password ───┘        └─── Bearer JWT
                                                    ▼                          ▼
                                          SUPABASE /auth/v1            SUPABASE /rest/v1
                                                                               │
                                                                    POSTGRESQL + RLS
```

## Quando usarlo e quando no

**Adatto a:** app per poche persone fidate, dati semplici, nessun segreto, CRUD.

**Da scartare se serve:**
- un **segreto** (chiave di terzi, invio email, pagamenti) → serve una funzione serverless
  (Vercel Functions o Supabase Edge Functions);
- **logica di cui non fidarsi del client**: qui la validazione lato client è cortesia,
  le sole regole applicate sono RLS + vincoli di tabella;
- **query complesse** (aggregazioni, join) → viste SQL o funzioni RPC;
- **upload di file** → Supabase Storage, servizio a parte con regole proprie;
- **scrittura offline** con riconciliazione dei conflitti.

---

## 1. Struttura del repository

```
index.html          markup + TUTTO il CSS (un file: senza build non c'è nulla da assemblare)
app.js              stato, rendering, gestori eventi
supabase.js         unico punto che conosce la rete: URL, chiave anon, una funzione per operazione
manifest.json       PWA
assets/             immagini e icone
schema.sql          struttura del database, da eseguire su installazione pulita
migrazione-NN.sql   modifiche successive, numerate e idempotenti
```

Tenere `supabase.js` separato serve a un fine preciso: il resto dell'app non sa nulla di
HTTP, e cambiare backend tocca un file solo.

---

## 2. Supabase: setup

### 2.1 Tabella + RLS

```sql
create extension if not exists pgcrypto;

create table if not exists elementi (
  id          uuid primary key default gen_random_uuid(),
  titolo      text not null,
  categoria   text not null,
  testo       text not null default '',
  -- liste che appartengono a UNA riga: jsonb, non tabella figlia.
  -- Niente join, scrittura in una sola richiesta.
  -- Tabella separata solo se quei dati vanno cercati o ordinati da soli.
  passi       jsonb not null default '[]'::jsonb,
  created_by  uuid default auth.uid(),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

alter table elementi enable row level security;

-- ARCHIVIO CONDIVISO: ogni utente autenticato vede e modifica tutto
create policy "condiviso tra autenticati" on elementi
  for all to authenticated using (true) with check (true);

-- Variante DATI PRIVATI: basta cambiare la condizione
-- create policy "solo i propri" on elementi
--   for all to authenticated using (created_by = auth.uid())
--   with check (created_by = auth.uid());
```

### 2.2 Impostazioni Authentication

- Se l'app è per poche persone: **Authentication → Sign In / Providers → Email →
  disattiva «Allow new users to sign up»**, poi crea gli account a mano da
  **Authentication → Users → Add user** con *Auto Confirm User*.
- Senza questo, chiunque trovi l'URL può registrarsi e — con una policy `to authenticated`
  — scrivere nei dati.

### 2.3 Verificare che le RLS proteggano davvero

⚠️ **Un accesso non autorizzato risponde `200 OK` con `[]`, non con un errore.**
Quindi «non dà errori» non significa «è protetto», e «non vedo dati» non significa
«è rotto». Va controllato il **corpo** della risposta:

```bash
curl -s "https://<progetto>.supabase.co/rest/v1/elementi?select=id" \
     -H "apikey: <chiave-anon>"
# atteso: []      → RLS attive
# se esce una lista di righe → la tabella è aperta a tutti
```

### 2.4 Le due chiavi

| Chiave | Dove sta | Cosa fa |
|---|---|---|
| `anon` / *publishable* | nel client, in chiaro | identifica il progetto; passa **attraverso** le RLS |
| `service_role` | **mai** nel client né in un repo | **scavalca** le RLS; solo server o pannello |

La chiave `anon` nel JavaScript non è una falla: è pubblica per progetto e da sola non
apre nulla. La sicurezza sta nelle policy.

---

## 3. Il client: `supabase.js`

Contratto minimo, senza SDK, solo `fetch`:

```js
const SUPABASE_URL = 'https://<progetto>.supabase.co';
const SUPABASE_KEY = '<chiave-anon>';

const sb = {
  headers: { 'Content-Type': 'application/json',
             'apikey': SUPABASE_KEY,
             'Authorization': 'Bearer ' + SUPABASE_KEY },
  authHeaders(token) { return { ...this.headers, 'Authorization': 'Bearer ' + token }; },

  // L'errore porta con sé il codice HTTP: serve per distinguere
  // "token rifiutato" (da ritentare) da tutto il resto (ritentare è tempo perso).
  async errore(r, dove) {
    const testo = await r.text().catch(() => '');
    const e = new Error(dove + ' ' + r.status + (testo ? ': ' + testo.slice(0, 200) : ''));
    e.stato = r.status;
    return e;
  },

  signIn(email, password) { /* POST /auth/v1/token?grant_type=password */ },
  refresh(refreshToken)   { /* POST /auth/v1/token?grant_type=refresh_token */ },
  signOut(token)          { /* POST /auth/v1/logout */ },

  async list(token, tabella) {
    const r = await fetch(`${SUPABASE_URL}/rest/v1/${tabella}?select=*&order=created_at.asc`,
                          { headers: this.authHeaders(token) });
    if (!r.ok) throw await this.errore(r, 'lettura');
    return r.json();
  },

  // Solo id e updated_at: per il controllo periodico, senza riscaricare tutto
  async versions(token, tabella) { /* ?select=id,updated_at */ },

  async insert(token, tabella, riga) {
    const r = await fetch(`${SUPABASE_URL}/rest/v1/${tabella}`, {
      method: 'POST',
      headers: { ...this.authHeaders(token), 'Prefer': 'return=representation' },
      body: JSON.stringify(riga)
    });
    if (!r.ok) throw await this.errore(r, 'inserimento');
    return (await r.json())[0];
  },

  async update(token, tabella, id, patch) { /* PATCH ?id=eq.<id> */ },
  async remove(token, tabella, id)        { /* DELETE ?id=eq.<id> */ }
};
```

Note su PostgREST:
- filtri nella query string: `?id=eq.<v>`, `?categoria=eq.<v>`, `?select=a,b`, `?order=col.asc`;
- `Prefer: return=representation` fa tornare la riga creata/modificata in **una** richiesta;
- il body può essere un **array** per inserire più righe in una sola chiamata;
- `?on_conflict=col1,col2` + `Prefer: resolution=merge-duplicates` dà un upsert atomico
  (richiede un vincolo UNIQUE su quelle colonne).

---

## 4. Autenticazione: le due regole che contano

```js
function scadenza(res) {
  return res.expires_at || (Math.floor(Date.now() / 1000) + (res.expires_in || 3600));
}

// Rinnova PRIMA di usare il token, non dopo che la richiesta è già fallita.
async function assicuraToken() {
  if (!session) return false;
  const ora = Math.floor(Date.now() / 1000);
  if (!session.expiresAt || session.expiresAt - ora < 120) return rinnovaToken();
  return true;
}

async function salva(payload) {
  await assicuraToken();                      // caso normale: UNA richiesta
  try {
    return await sb.insert(session.token, tabella, payload);
  } catch (e) {
    if (e.stato !== 401 || !await rinnovaToken()) throw e;   // ritenta SOLO sul 401
    return await sb.insert(session.token, tabella, payload);
  }
}
```

**Perché conta.** Col rinnovo reattivo (prima provo, se 401 rinnovo e riprovo) ogni
salvataggio a token scaduto costa **tre viaggi di rete** invece di uno: su rete mobile
la differenza è ben percepibile e sembra che «l'app sia lenta». E ritentare su un errore
generico di rete allunga solo l'attesa prima di dire che non è andata.

**Sessione** in `localStorage`: `{ token, refreshToken, userId, email, expiresAt }`.
Su iOS i timer si fermano quando l'app va in background: non fidarsi di un
`setInterval` per il rinnovo, controllare la scadenza al momento dell'uso.

**Polling leggero.** Per accorgersi delle modifiche altrui senza riscaricare tutto ogni
30 secondi: chiedi solo `id,updated_at`, confronta una firma dei risultati, e scarica per
intero solo se è cambiata.

---

## 5. Dati e migrazioni

**Migrazioni numerate e idempotenti**, versionate accanto al codice:

```sql
alter table elementi add column if not exists note text not null default '';
update elementi set categoria = 'Nuovo nome' where categoria = 'Vecchio nome';
```

**Importazioni ripetibili** — inserisci solo se non esiste già:

```sql
insert into elementi (titolo, categoria)
select v.* from (values ('Uno', 'A'), ('Due', 'B')) as v(titolo, categoria)
where not exists (select 1 from elementi e where e.titolo = v.titolo);
```

**Il client va scritto tollerante:** codice e database si aggiornano in momenti diversi,
quindi il telefono può avere la versione nuova prima che la migrazione sia stata eseguita,
o viceversa. Il client deve sopportare campi mancanti e valori che non conosce invece di
rompersi. Per esempio: se una categoria viene rinominata, mostra comunque le righe rimaste
col vecchio nome sotto quel nome, invece di farle sparire dall'elenco.

---

## 6. Deploy

1. **GitHub**: repository (anche privato), carica tutti i file, **cartelle comprese**.
2. **Vercel**: *Add New → Project* → importa il repo → preset **Other**, nessun comando di
   build, nessuna cartella di output → *Deploy*.
3. Da qui in poi **il deploy è un commit**: niente da copiare a mano su un server.

Sviluppo locale: serve via HTTP, non aprendo il file con doppio clic.

```bash
python -m http.server 8000
```

---

## 7. PWA su iPhone: la parte che costa tempo scoprire

### Meta tag necessari

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0,
      maximum-scale=1.0, viewport-fit=cover" />
<link rel="manifest" href="manifest.json" />
<meta name="mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
<meta name="apple-mobile-web-app-title" content="Nome app" />
<link rel="apple-touch-icon" href="assets/icon-192.png" />
<!-- NESSUN <meta name="theme-color">: vedi sotto -->
```

### ⚠️ iOS legge manifest e meta una volta sola, all'installazione

Non li rilegge mai più, nemmeno ricaricando la pagina. Per cambiare icona, nome o colori
va **rimossa e riaggiunta l'icona dalla Home**. CSS e JavaScript invece si aggiornano
normalmente. Sapere questa differenza evita di inseguire modifiche che sembrano non fare
effetto.

### Le tre bande indesiderate, e perché

Andare davvero a schermo pieno richiede tre accorgimenti indipendenti. Ognuno corrisponde
a una banda che compare se manca:

**1. Nessun `theme_color`** — né nel manifest né in un meta tag. È quello a disegnare la
striscia opaca dietro l'orologio in standalone, e resta del colore letto
all'installazione: se l'app cambia tema a runtime, la banda no.

**2. Lo sfondo va sull'elemento radice `html`**, non solo su `body`:

```css
html, body { position: fixed; inset: 0; overflow: hidden; overscroll-behavior: none; }

/* Con body in position:fixed, WebKit non propaga il suo sfondo alla tela del
   documento: la tela resta trasparente e la riempie il sistema.
   Inoltre lo sfondo della radice è l'UNICO dipinto su tutta la superficie:
   qualunque altro elemento, anche position:fixed, viene ritagliato dal viewport
   e non può coprire la zona della barra home.
   bottom negativo: l'immagine è dimensionata sulla scatola di html, quindi la
   scatola deve sforare. */
html {
  background-color: var(--paper);
  background-image: url('assets/carta.jpg');
  background-repeat: repeat;          /* NON cover: vedi "texture" */
  background-position: top left;
  background-size: 820px 820px;
  bottom: -150px;
}
```

**3. Niente altezze in `vh`/`dvh`.** In standalone risultano più basse dello schermo e
lasciano scoperta una striscia in fondo. Ancorare invece a tutti i lati:

```css
.wrap { position: absolute; inset: 0; max-width: 460px; margin: 0 auto; overflow: hidden; }
```

### Zone sicure

```css
.barra-alto  { padding-top:    calc(8px + env(safe-area-inset-top)); }
.barra-basso { padding-bottom: calc(8px + env(safe-area-inset-bottom)); }
```

Non mettere testo o comandi dentro la fascia della barra home: lì iOS intercetta il gesto
di sistema, e le dita coprono il contenuto.

### Texture di sfondo

`background-size: cover` riscala l'immagine in base all'altezza della scatola: su elementi
di altezza diversa la grana cambia scala e le giunzioni si vedono. Una **piastrella
ripetuta a dimensione fissa in pixel** ha la stessa grana dappertutto per costruzione. Se
l'immagine non è affiancabile, la si rende tale **specchiandola nei quattro quadranti**:
prima colonna uguale all'ultima, prima riga uguale all'ultima, quindi nessuna cucitura.

### Icone monocromatiche colorabili

Per icone che devono cambiare colore (per esempio da nere a rosse quando selezionate),
usare **maschere alpha** invece di immagini colorate: il colore lo dà il CSS.

```css
.icona {
  width: 46px; height: 44px;
  background-color: var(--ink);              /* il colore sta qui */
  -webkit-mask: var(--m) center/contain no-repeat;
          mask: var(--m) center/contain no-repeat;
}
.icona.attiva { background-color: var(--red); }
```

```html
<div class="icona" style="--m:url(assets/ic-forno.png)"></div>
```

### Aprire un link esterno in Safari invece che dentro l'app

In standalone un link normale resta dentro l'app. Per forzare Safari:

```js
function hrefApribile(u) {
  if (!u || !window.navigator.standalone) return u;   // in Safari normale non toccare
  return u.replace(/^http(s?):\/\//i, 'x-safari-http$1://');
}
```

---

## 8. Export dei dati senza librerie

I dati sono l'unica cosa che **non** sta nel repository: prevedere un export dal primo
giorno. Due strade complementari:

**PDF leggibile, dall'app.** Comporre tutto il contenuto in un blocco nascosto e usare la
stampa di sistema (`window.print()`); su iPhone *Condividi → Stampa → Salva su File*.
Nessuna libreria.

```css
.stampa { display: none; }
@media print {
  /* sciogliere il position:fixed dell'app, altrimenti esce solo la prima pagina */
  html, body { position: static; inset: auto; height: auto; overflow: visible; background: #fff; }
  .app { display: none !important; }
  .stampa { display: block; }
  @page { margin: 14mm 13mm; }
  .ricetta { break-inside: avoid; }
}
```

**CSV grezzo, dal pannello.** Supabase → *Table Editor* → tabella → menu `⋮` →
*Export data* → *Download as CSV*.

---

## 9. Insidie verificate sul campo

| Sintomo | Causa | Rimedio |
|---|---|---|
| «Funziona ma non vedo dati» | RLS senza policy: risponde `200` con `[]` | scrivere la policy; verificare il corpo, non lo stato |
| Salvataggio lento | rinnovo del token reattivo: 3 viaggi di rete | `assicuraToken()` prima dell'uso; ritentare solo sul 401 |
| Banda colorata dietro l'orologio | `theme_color` nel manifest | togliere `theme_color` + `black-translucent` |
| Banda del colore giusto ma piatta in fondo | sfondo solo su `body`, o altezza in `dvh` | sfondo su `html` con `bottom` negativo; `inset: 0` |
| Modifiche a icona/nome senza effetto | iOS legge il manifest all'installazione | rimuovere e riaggiungere l'icona |
| Grana della texture disallineata | `background-size: cover` su scatole diverse | piastrella `repeat` a dimensione fissa |
| Accenti diventati `Ã ` | PowerShell 5.1 rilegge UTF-8 come ANSI | non usare `Get-Content`/`Set-Content` su file UTF-8; se accade, decodificare in cp1252 e rileggere come UTF-8 |

⚠️ **Il rischio strutturale:** le RLS sono l'unico strato di difesa. Una policy scritta
male non causa un errore visibile — apre i dati a tutti, in silenzio. Vanno riviste ogni
volta che si aggiunge una tabella.

---

## 10. Costi e alternative

Tutti e tre i servizi hanno un piano gratuito che basta per un'app familiare. I limiti
cambiano nel tempo e **vanno verificati al momento**; la voce a cui fare attenzione è che
sui piani gratuiti i progetti Supabase **inattivi vengono messi in pausa**, quindi la prima
apertura dopo un lungo silenzio può richiedere qualche secondo.

I pezzi sono sostituibili senza cambiare l'impianto: Netlify o Cloudflare Pages al posto di
Vercel; Firebase, Appwrite o PocketBase al posto di Supabase. Quello che conta è lo schema:
**file statici da una CDN, più un database che espone da sé un'API e applica le regole di
accesso al proprio interno.**

---

## Checklist per partire

1. Supabase: crea il progetto, annota URL e chiave `anon`.
2. SQL Editor: tabelle, `enable row level security`, policy.
3. Authentication: disattiva la registrazione libera, crea gli account a mano.
4. Verifica le RLS con `curl` senza token: deve uscire `[]`.
5. Scrivi `index.html`, `app.js`, `supabase.js`; prova con un server HTTP locale.
6. GitHub: repository e caricamento, cartelle comprese.
7. Vercel: importa, preset «Other», nessuna build, Deploy.
8. iPhone: Safari → Condividi → Aggiungi alla schermata Home.
9. Export dei dati: previsto dal primo giorno.
