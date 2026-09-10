// ─────────────────────────────────────────────────────────────────
// Client Supabase minimale (nessun npm, nessun build): solo fetch.
// Stesso progetto di AgendaBb, quindi gli account sono in comune.
// Per puntare a un progetto diverso basta cambiare queste due righe.
// ─────────────────────────────────────────────────────────────────
const SUPABASE_URL = 'https://grmfbbqujopstaagknuc.supabase.co';
const SUPABASE_KEY = 'sb_publishable_S5LYjuFe5m4ieS6BNZXz5A_-E7kuxuK';

const sb = {
  url: SUPABASE_URL,
  key: SUPABASE_KEY,

  headers: {
    'Content-Type': 'application/json',
    'apikey': SUPABASE_KEY,
    'Authorization': 'Bearer ' + SUPABASE_KEY
  },

  authHeaders(token) {
    return { ...this.headers, 'Authorization': 'Bearer ' + token };
  },

  // ── AUTH ───────────────────────────────────────────────────────
  async signUp(email, password) {
    const r = await fetch(SUPABASE_URL + '/auth/v1/signup', {
      method: 'POST', headers: this.headers,
      body: JSON.stringify({ email, password })
    });
    return r.json();
  },

  async signIn(email, password) {
    const r = await fetch(SUPABASE_URL + '/auth/v1/token?grant_type=password', {
      method: 'POST', headers: this.headers,
      body: JSON.stringify({ email, password })
    });
    return r.json();
  },

  async refresh(refreshToken) {
    const r = await fetch(SUPABASE_URL + '/auth/v1/token?grant_type=refresh_token', {
      method: 'POST', headers: this.headers,
      body: JSON.stringify({ refresh_token: refreshToken })
    });
    return r.json();
  },

  async signOut(token) {
    await fetch(SUPABASE_URL + '/auth/v1/logout', {
      method: 'POST', headers: this.authHeaders(token)
    });
  },

  // ── RICETTE (database condiviso: tutti leggono e scrivono tutto) ─
  // Errore che porta con sé il codice HTTP: serve a chi chiama per distinguere
  // "token rifiutato" (da ritentare dopo il rinnovo) da tutto il resto, che
  // ritentare è solo tempo perso.
  async errore(r, dove) {
    const testo = await r.text().catch(() => '');
    const e = new Error(dove + ' ' + r.status + (testo ? ': ' + testo.slice(0, 200) : ''));
    e.stato = r.status;
    return e;
  },

  // `table` è 'ricette_salate' oppure 'ricette_dolci'.
  async listRecipes(token, table) {
    const r = await fetch(SUPABASE_URL + '/rest/v1/' + table + '?select=*&order=created_at.asc', {
      headers: this.authHeaders(token)
    });
    if (!r.ok) throw await this.errore(r, 'lettura ' + table);
    return r.json();
  },

  // Solo id e updated_at: serve al controllo periodico per capire se qualcosa
  // è cambiato senza riscaricare tutte le ricette ogni trenta secondi.
  async listVersions(token, table) {
    const r = await fetch(SUPABASE_URL + '/rest/v1/' + table + '?select=id,updated_at', {
      headers: this.authHeaders(token)
    });
    if (!r.ok) throw await this.errore(r, 'versioni ' + table);
    return r.json();
  },

  async insertRecipe(token, table, row) {
    const r = await fetch(SUPABASE_URL + '/rest/v1/' + table, {
      method: 'POST',
      headers: { ...this.authHeaders(token), 'Prefer': 'return=representation' },
      body: JSON.stringify(row)
    });
    if (!r.ok) throw await this.errore(r, 'inserimento');
    const rows = await r.json();
    return rows[0];
  },

  async updateRecipe(token, table, id, patch) {
    const r = await fetch(SUPABASE_URL + '/rest/v1/' + table + '?id=eq.' + id, {
      method: 'PATCH',
      headers: { ...this.authHeaders(token), 'Prefer': 'return=representation' },
      body: JSON.stringify({ ...patch, updated_at: new Date().toISOString() })
    });
    if (!r.ok) throw await this.errore(r, 'modifica');
    const rows = await r.json();
    return rows[0];
  },

  async deleteRecipe(token, table, id) {
    const r = await fetch(SUPABASE_URL + '/rest/v1/' + table + '?id=eq.' + id, {
      method: 'DELETE', headers: this.authHeaders(token)
    });
    if (!r.ok) throw await this.errore(r, 'eliminazione');
    return true;
  }
};
