"""Genera le icone dell'app da assets/../icona.png.

L'immagine di partenza ha il fondo bianco e non è quadrata. Qui si fa:
  1. scontorno del bianco con un riempimento a partire dai BORDI — non una
     soglia globale, altrimenti si bucherebbero i bianchi interni (i funghi,
     l'etichetta "My Recipe", le cipolle);
  2. composizione su un quadrato con la carta dell'app come fondo, invece del
     bianco: iOS arrotonda gli angoli e il bianco stonerebbe;
  3. tre file: due icone normali e una "maskable" con più margine, perché
     Android ritaglia a cerchio e mangerebbe il disegno.

    pip install pymupdf
    python mkicona.py
"""
import fitz, os
from collections import deque

QUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(QUI, '..', 'icona.png'))
ASSETS = os.path.normpath(os.path.join(QUI, '..', 'assets'))
CARTA_PIATTA = (209 / 255, 220 / 255, 184 / 255)   # #d1dcb8, la carta salata
# Il fondo dell'immagine non è bianco puro ma grigio chiaro (229,229,229), e i
# 2 px più esterni sono una cornice scura che bloccherebbe il riempimento:
# quindi si ritaglia il bordo e si cerca "grigio chiaro e desaturato".
MARGINE = 4
CHIARO = 212          # da qui in su è fondo
ALONE = 190           # sfumatura antialias a contatto col fondo
GRIGIO = 14           # massimo scarto fra i canali per dirlo desaturato


def scontorna(path):
    """RGBA con il fondo reso trasparente, partendo dai bordi."""
    pix = fitz.Pixmap(path)
    if pix.alpha:                                  # scarta l'alpha esistente
        pix = fitz.Pixmap(pix, 0)
    n, sw, src = pix.n, pix.width, pix.samples
    w, h = pix.width - 2 * MARGINE, pix.height - 2 * MARGINE

    def rgb(x, y):
        i = ((y + MARGINE) * sw + (x + MARGINE)) * n
        return src[i], src[i + 1], src[i + 2]

    def desaturato(c):
        return max(c) - min(c) <= GRIGIO

    def fondo(x, y):
        c = rgb(x, y)
        return min(c) >= CHIARO and desaturato(c)

    fuori = bytearray(w * h)                       # 1 = da rendere trasparente
    coda = deque()
    for x in range(w):
        for y in (0, h - 1):
            if fondo(x, y) and not fuori[y * w + x]:
                fuori[y * w + x] = 1
                coda.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if fondo(x, y) and not fuori[y * w + x]:
                fuori[y * w + x] = 1
                coda.append((x, y))

    while coda:
        x, y = coda.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not fuori[ny * w + nx] and fondo(nx, ny):
                fuori[ny * w + nx] = 1
                coda.append((nx, ny))

    # una passata in più per l'alone antialias: pixel desaturati e chiarissimi
    # a contatto col fondo già tolto
    for y in range(h):
        for x in range(w):
            if fuori[y * w + x]:
                continue
            c = rgb(x, y)
            if min(c) >= ALONE and desaturato(c):
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and fuori[ny * w + nx] == 1:
                        fuori[y * w + x] = 2
                        break

    out = bytearray(w * h * 4)
    tolti = 0
    for y in range(h):
        for x in range(w):
            i = y * w + x
            o = i * 4
            out[o], out[o + 1], out[o + 2] = rgb(x, y)
            if fuori[i]:
                out[o + 3] = 0
                tolti += 1
            else:
                out[o + 3] = 255
    print(f'scontorno: rimosso il {100*tolti/(w*h):.1f}% come fondo')
    return fitz.Pixmap(fitz.csRGB, w, h, bytes(out), True), w, h


ritagliata, W, H = scontorna(SRC)
tmp = os.path.join(QUI, '_icona_scontornata.png')
ritagliata.save(tmp)


def componi(lato, quota, nome):
    """Quadrato di `lato` px: carta come fondo, disegno al `quota` per cento."""
    doc = fitz.open()
    pg = doc.new_page(width=lato, height=lato)
    # colore piatto e non la texture: a dimensione icona la grana non si vede,
    # e in PNG la texture costava 337 KB contro una cinquantina.
    pg.draw_rect(fitz.Rect(0, 0, lato, lato), color=None, fill=CARTA_PIATTA)
    box = lato * quota
    scala = min(box / W, box / H)
    dw, dh = W * scala, H * scala
    x, y = (lato - dw) / 2, (lato - dh) / 2
    pg.insert_image(fitz.Rect(x, y, x + dw, y + dh), filename=tmp, keep_proportion=True)
    p = os.path.join(ASSETS, nome)
    pg.get_pixmap(dpi=72).save(p)
    print(f'{nome}: {lato}x{lato}, disegno al {int(quota*100)}%, {os.path.getsize(p)//1024} KB')


componi(512, 0.88, 'icon-512.png')
componi(192, 0.88, 'icon-192.png')
componi(512, 0.62, 'icon-maskable-512.png')   # Android ritaglia a cerchio
os.remove(tmp)
