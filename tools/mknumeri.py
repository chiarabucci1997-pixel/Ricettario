"""Genera le cifre 0, 6, 7, 8, 9 nello stile dei numeri dipinti del PDF.

Il Render.pdf contiene solo 1-5, disegnati a pennello asciutto: tratto spesso
con bordi sfilacciati e striature interne. Qui le cifre mancanti vengono
ricostruite con le stesse metriche misurate sugli originali
(tratto ~22 px su 200 px di altezza, copertura 29-39%) e poi "sporcate" con
una texture procedurale, così stanno accanto alle originali senza stonare.

Le originali NON vengono toccate: num1-num5.png restano quelle del PDF.

    pip install pymupdf
    python mknumeri.py
"""
import fitz, math, os

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(QUI, '..', 'assets'))

H = 200.0                 # altezza di riferimento del disegno
TRATTO = 22.0             # spessore misurato sugli originali
SCALA = 3                 # si disegna in grande e si riduce, per l'antialias
ALTEZZA_FINALE = 213      # come num3, in mezzo alle originali

# Quanto mordere i bordi, in unità del disegno (il tratto è 22): gli originali
# sono NERI PIENI con i bordi consumati, non righati da parte a parte.
MORSO_U = 6.0
MORSO = MORSO_U * SCALA
SOGLIA_STRIATURA = 0.985      # striature interne: rare


# ── percorsi delle cifre, in una scatola 100 x 200 ───────────────
def anello(d, cx, cy, rx, ry, incl=0.0):
    """Occhiello chiuso come due archi che bombano in fuori: così il buco
    interno resta aperto. Prima li disegnavo passando per il centro e si
    chiudevano tutti."""
    top = (cx + incl, cy - ry)
    bot = (cx - incl, cy + ry)
    d.curva(top, (cx - rx + incl, cy - ry), (cx - rx - incl, cy + ry), bot)
    d.curva(bot, (cx + rx - incl, cy + ry), (cx + rx + incl, cy - ry), top)


def cifra_0(d):
    anello(d, 50, 101, 37, 87, incl=3)


def cifra_6(d):
    d.curva((78, 16), (44, 40), (18, 86), (13, 128))     # gambo
    anello(d, 49, 145, 37, 45)                           # ciotola


def cifra_7(d):
    d.linea((11, 27), (46, 21), (88, 19))                # barra alta
    d.curva((88, 19), (67, 88), (49, 148), (41, 190))    # diagonale


def cifra_8(d, ):
    anello(d, 50, 57, 30, 41)                            # occhiello alto
    anello(d, 50, 146, 36, 44)                           # occhiello basso


def cifra_9(d):
    anello(d, 51, 59, 36, 43)                            # occhiello
    d.curva((86, 63), (83, 120), (70, 168), (52, 190))   # gambo


# alcune cifre hanno il tratto un filo più sottile, o il buco si chiude
CIFRE = {'0': (cifra_0, 1.0), '6': (cifra_6, 1.0), '7': (cifra_7, 1.05),
         '8': (cifra_8, 0.86), '9': (cifra_9, 0.95)}


class Penna:
    """Disegna con un tratto spesso a punta tonda."""

    def __init__(self, pg, k, spessore=1.0):
        self.pg = pg
        self.k = k
        self.spessore = spessore

    def _fin(self, sh):
        sh.finish(color=(0, 0, 0), width=TRATTO * self.k * self.spessore,
                  lineCap=1, lineJoin=1)
        sh.commit()

    def linea(self, *pts):
        sh = self.pg.new_shape()
        sh.draw_polyline([fitz.Point(x * self.k, y * self.k) for x, y in pts])
        self._fin(sh)

    def curva(self, p0, c1, c2, p1):
        sh = self.pg.new_shape()
        sh.draw_bezier(*[fitz.Point(x * self.k, y * self.k) for x, y in (p0, c1, c2, p1)])
        self._fin(sh)


def rumore(x, y, k):
    """Striature verticali nette, come un pennello scarico: alta frequenza
    attraverso il tratto, bassissima lungo il tratto. Un campo isotropo dava
    un alone sfumato invece dei solchi sottili degli originali."""
    x, y = x / k, y / k                      # ragiona in unità del disegno
    v = 0.5 + 0.5 * math.sin(x * 0.78 + math.sin(y * 0.090) * 3.0)
    v = 0.62 * v + 0.38 * (0.5 + 0.5 * math.sin(x * 1.85 + math.sin(y * 0.052) * 5.0))
    v = v * v * (3 - 2 * v)                  # un solo smoothstep: denti meno regolari
    # inviluppo lento: in certi punti il bordo resta pieno, in altri si consuma.
    # Senza questo il contorno risultava seghettato in modo uniforme, da sega.
    e = 0.30 + 0.70 * (0.5 + 0.5 * math.sin(y * 0.043 + x * 0.11 + 1.7))
    return v * e


def distanza_dal_fondo(mask, w, h):
    """Chamfer distance transform in due passate: per ogni pixel di inchiostro,
    quanto è lontano dal bordo. Serve a mordere solo i bordi."""
    INF = 10 ** 9
    dt = [0 if not mask[i] else INF for i in range(w * h)]
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if dt[i] == 0:
                continue
            best = dt[i]
            for dx, dy, c in ((-1, 0, 10), (0, -1, 10), (-1, -1, 14), (1, -1, 14)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    best = min(best, dt[ny * w + nx] + c)
            dt[i] = best
    for y in range(h - 1, -1, -1):
        for x in range(w - 1, -1, -1):
            i = y * w + x
            if dt[i] == 0:
                continue
            best = dt[i]
            for dx, dy, c in ((1, 0, 10), (0, 1, 10), (1, 1, 14), (-1, 1, 14)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    best = min(best, dt[ny * w + nx] + c)
            dt[i] = best
    return [v / 10.0 for v in dt]


def genera(ch, fn, spessore):
    k = SCALA
    W, Hp = int(100 * k), int(H * k)
    doc = fitz.open()
    pg = doc.new_page(width=W, height=Hp)
    pg.draw_rect(fitz.Rect(0, 0, W, Hp), color=None, fill=(1, 1, 1))
    fn(Penna(pg, k, spessore))
    pix = pg.get_pixmap(dpi=72)
    w, h, n, s = pix.width, pix.height, pix.n, pix.samples

    mask = [s[i * n] < 128 for i in range(w * h)]
    dt = distanza_dal_fondo(mask, w, h)

    # morso dei bordi + striature interne
    alpha = bytearray(w * h)
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if not mask[i]:
                continue
            r = rumore(x, y, k)
            if dt[i] < MORSO * r:
                continue                                  # bordo sfilacciato
            if r > SOGLIA_STRIATURA and dt[i] < MORSO * 1.3:
                continue                                  # striatura vicino al bordo
            alpha[i] = 255

    # riduzione con media dei blocchi: dà i bordi morbidi
    fh = ALTEZZA_FINALE
    fw = max(1, round(w * fh / h))
    buf = bytearray(fw * fh * 4)
    for fy in range(fh):
        y0, y1 = fy * h // fh, max(fy * h // fh + 1, (fy + 1) * h // fh)
        for fx in range(fw):
            x0, x1 = fx * w // fw, max(fx * w // fw + 1, (fx + 1) * w // fw)
            tot = cnt = 0
            for y in range(y0, y1):
                base = y * w
                for x in range(x0, x1):
                    tot += alpha[base + x]
                    cnt += 1
            buf[(fy * fw + fx) * 4 + 3] = tot // cnt

    p = os.path.join(OUT, f'num{ch}.png')
    fitz.Pixmap(fitz.csRGB, fw, fh, bytes(buf), True).save(p)
    inch = sum(1 for i in range(fw * fh) if buf[i * 4 + 3] > 128)
    print(f'num{ch}.png: {fw}x{fh}, copertura {100*inch/(fw*fh):4.1f}%, '
          f'{os.path.getsize(p)//1024} KB')


if __name__ == '__main__':
    for ch, (fn, spessore) in CIFRE.items():
        genera(ch, fn, spessore)

