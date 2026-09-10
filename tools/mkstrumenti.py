"""Genera le maschere alpha delle icone della sezione STRUMENTAZIONE.

Stesso stile delle icone in cima alla ricetta: line art nero su carta bianca,
convertito in maschera alpha così il colore lo decide il CSS (nero / rosso).
Ogni icona sta in una scatola quadrata di 40x40 pt -> 167x167 px a 300 dpi.

    pip install pymupdf
    python mkstrumenti.py
"""
import fitz, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
BOX = 40
SW = 1.3                      # spessore del tratto, come le altre icone
NERO = (0, 0, 0)


class Disegno:
    def __init__(self, pg):
        self.pg = pg

    def _fin(self, sh, chiusa=False):
        sh.finish(color=NERO, width=SW, lineJoin=1, lineCap=1, closePath=chiusa)
        sh.commit()

    def linea(self, *pts, chiusa=False):
        sh = self.pg.new_shape()
        sh.draw_polyline([fitz.Point(*p) for p in pts])
        self._fin(sh, chiusa)

    def rett(self, x0, y0, x1, y1, r=None):
        sh = self.pg.new_shape()
        sh.draw_rect(fitz.Rect(x0, y0, x1, y1), radius=r)
        self._fin(sh)

    def cerchio(self, cx, cy, rad):
        sh = self.pg.new_shape()
        sh.draw_circle(fitz.Point(cx, cy), rad)
        self._fin(sh)

    def ovale(self, x0, y0, x1, y1):
        sh = self.pg.new_shape()
        sh.draw_oval(fitz.Rect(x0, y0, x1, y1))
        self._fin(sh)

    def curva(self, p0, c1, c2, p1):
        sh = self.pg.new_shape()
        sh.draw_bezier(fitz.Point(*p0), fitz.Point(*c1), fitz.Point(*c2), fitz.Point(*p1))
        self._fin(sh)


# ── un disegno per strumento ─────────────────────────────────────
def coltello(d):
    d.rett(3.5, 15.8, 15, 22.6, r=0.35)                                # manico
    d.linea((16.5, 15.8), (16.5, 22.6))                                # ghiera
    d.linea((15, 16.2), (29, 17.6), (36, 20.2), (15, 22.4), chiusa=True)   # lama
    d.cerchio(7, 19.2, 1.0)                                            # rivetto


def tagliere(d):
    d.rett(5, 7, 29, 31, r=0.07)                                       # tavola
    d.linea((9, 11), (9, 27))                                          # venature
    d.linea((12, 11), (12, 27))
    d.linea((29, 16.5), (35.5, 17.5), (35.5, 22.5), (29, 23.5), chiusa=True)   # manico
    d.cerchio(32.5, 20, 1.0)                                           # foro


def ciotola(d):
    d.ovale(6.5, 12, 33.5, 18)
    d.curva((6.5, 15), (7.5, 29), (32.5, 29), (33.5, 15))


def bilancia(d):
    d.ovale(8, 8, 32, 14)                                              # piatto
    d.rett(6.5, 15.5, 33.5, 30, r=0.22)                                # corpo
    d.rett(11, 19.5, 29, 25.5, r=0.12)                                 # display
    d.linea((14, 27.5), (26, 27.5))


def frusta(d):
    d.rett(17.4, 24, 22.6, 36, r=0.45)                                 # manico
    d.linea((20, 24), (20, 4))                                         # filo centrale
    d.curva((20, 23.5), (10.5, 19), (10.5, 8), (20, 4))                # anelli esterni
    d.curva((20, 23.5), (29.5, 19), (29.5, 8), (20, 4))
    d.curva((20, 23.5), (15, 19.5), (15, 9), (20, 4))                  # anelli interni
    d.curva((20, 23.5), (25, 19.5), (25, 9), (20, 4))


def planetaria(d):
    d.rett(9, 4, 34.5, 12, r=0.3)                                      # testa
    d.rett(27, 12, 34.5, 31)                                           # colonna
    d.linea((15, 12), (15, 15.5))                                      # albero
    d.linea((11.5, 15.5), (18.5, 15.5), (15, 23), chiusa=True)         # frusta a foglia
    d.ovale(4, 17.5, 24, 22)                                           # bordo ciotola
    d.curva((4, 19.7), (5, 31), (23, 31), (24, 19.7))                  # ciotola
    d.rett(4, 31, 34.5, 35.5, r=0.35)                                  # base


def sbattitore(d):
    d.rett(11, 2.5, 25.5, 7, r=0.45)                                   # impugnatura
    d.linea((13.5, 7), (13.5, 9.5))                                    # montanti
    d.linea((23, 7), (23, 9.5))
    d.rett(6.5, 9.5, 29, 19, r=0.28)                                   # corpo
    d.rett(22.5, 12, 27, 16.5, r=0.3)                                  # tasto velocità
    d.linea((11.5, 19), (10.5, 30), (14, 30), (13, 19), chiusa=True)   # fruste
    d.linea((17.5, 19), (16.5, 30), (20, 30), (19, 19), chiusa=True)
    d.linea((11, 24.5), (13.5, 24.5))
    d.linea((17, 24.5), (19.5, 24.5))


def mattarello(d):
    d.rett(10, 15.5, 30, 24.5, r=0.1)
    d.rett(3, 18, 10, 22, r=0.5)
    d.rett(30, 18, 37, 22, r=0.5)


def teglia(d):
    d.linea((4, 13), (36, 13), (31.5, 28), (8.5, 28), chiusa=True)
    d.linea((8, 16.5), (32, 16.5), (29.5, 24.5), (10.5, 24.5), chiusa=True)


def tortiera(d):
    d.ovale(6.5, 10, 33.5, 16)
    d.linea((6.5, 13), (7.5, 26))
    d.linea((33.5, 13), (32.5, 26))
    d.curva((7.5, 26), (10, 31), (30, 31), (32.5, 26))
    d.rett(33, 16.5, 36.5, 22, r=0.4)                                  # chiusura a cerniera


def setaccio(d):
    d.ovale(4, 11, 28, 17)
    d.curva((4, 14), (5, 27), (27, 27), (28, 14))
    d.rett(28, 12.5, 37, 16, r=0.5)                                    # manico
    d.linea((8, 18.5), (24, 18.5))                                     # rete
    d.linea((10, 22), (22, 22))
    d.linea((12, 15), (13.5, 24))
    d.linea((20, 15), (18.5, 24))


def sacapoche(d):
    d.linea((9, 4.5), (28, 4.5), (22, 24), (16.5, 24), chiusa=True)    # sacca
    d.curva((9, 4.5), (13, 1), (24, 1), (28, 4.5))                     # sommità raccolta
    d.linea((16.5, 24), (22, 24), (23, 30), (15.5, 30), chiusa=True)   # bocchetta
    d.linea((15.5, 30), (17, 32.5), (18.5, 30), (20, 32.5), (21.5, 30), (23, 32.5))  # punta a stella


def spatola(d):
    d.rett(12, 4.5, 28, 20, r=0.3)
    d.rett(17.5, 20, 22.5, 35, r=0.4)


def grattugia(d):
    d.linea((11.5, 7), (28.5, 7), (32.5, 32), (7.5, 32), chiusa=True)
    d.curva((14, 7), (15, 1.5), (25, 1.5), (26, 7))                    # maniglia
    for i, y in enumerate((13, 18, 23, 28)):
        off = 1.0 * i
        d.linea((13 - off * 0.5, y), (16 - off * 0.5, y))
        d.linea((19, y), (22, y))
        d.linea((25 + off * 0.5, y), (28 + off * 0.5, y))


def scolapasta(d):
    d.ovale(7, 11, 33, 17)
    d.curva((7, 14), (8, 29), (32, 29), (33, 14))
    d.curva((7, 13), (3, 12), (3, 18), (6.5, 17.5))                    # manici
    d.curva((33, 13), (37, 12), (37, 18), (33.5, 17.5))
    for cx, cy in ((15, 19), (20, 20.5), (25, 19), (17.5, 24), (22.5, 24)):
        d.cerchio(cx, cy, 1.2)


def microonde(d):
    d.rett(3.5, 10, 36.5, 30, r=0.1)
    d.rett(6.5, 13, 25, 27, r=0.06)
    d.linea((26.5, 15), (26.5, 25))                                    # maniglia
    d.cerchio(31.5, 16.5, 2)                                           # manopola
    d.rett(29, 21, 34, 22.5)
    d.rett(29, 24, 34, 25.5)


def pennello(d):
    d.rett(17, 3.5, 23, 20, r=0.45)                                    # manico
    d.rett(15.5, 20, 24.5, 25)                                         # ghiera
    for x0, x1 in ((16.2, 14.5), (18.6, 18.0), (21.4, 22.0), (23.8, 25.5)):
        d.linea((x0, 25), (x1, 35))                                    # setole
    d.curva((14.5, 35), (18, 37.5), (22, 37.5), (25.5, 35))


def tostapane(d):
    d.rett(6, 12.5, 34, 31, r=0.16)                                    # corpo
    d.rett(10.5, 9, 29.5, 12.5, r=0.35)                                # fessura
    d.rett(34, 16, 37.5, 19.5, r=0.45)                                 # leva
    d.cerchio(28.5, 24, 2.2)                                           # manopola
    d.rett(10, 21, 22, 27, r=0.15)                                     # sportellino
    d.linea((9.5, 31), (9.5, 34))
    d.linea((30.5, 31), (30.5, 34))


def minipimer(d):
    d.rett(14, 3.5, 26, 20, r=0.3)                                     # corpo
    d.rett(16.8, 7, 23.2, 11.5, r=0.3)                                 # tasto
    d.rett(18, 20, 22, 28.5)                                           # asta
    d.linea((13.8, 28.5), (26.2, 28.5), (25, 34), (15, 34), chiusa=True)   # campana
    d.linea((17, 31), (23, 31))                                        # lama


def mandolina(d):
    d.linea((7.5, 32), (13.5, 8), (36, 8), (30, 32), chiusa=True)      # piano
    d.linea((12.5, 19.5), (31.5, 19.5))                                # lama
    d.linea((12, 22), (31, 22))
    d.linea((9, 32), (9, 35.5))                                        # piedini
    d.linea((28.5, 32), (28.5, 35.5))


def spremiagrumi(d):
    d.linea((20, 4.5), (13.5, 17), (26.5, 17), chiusa=True)            # cono
    d.linea((20, 6), (20, 17))                                         # scanalature
    d.linea((16.8, 11), (16.8, 17))
    d.linea((23.2, 11), (23.2, 17))
    d.ovale(7.5, 17, 32.5, 23)                                         # bordo bacinella
    d.curva((7.5, 20), (9, 30.5), (31, 30.5), (32.5, 20))
    d.linea((32.4, 21), (36.5, 23), (32.4, 25.5))                      # beccuccio


def pelapatate(d):
    # Forma a Y: lama larga in alto, due bracci che convergono, manico
    # verticale. Prima i bracci partivano dal manico e chiudevano l'area
    # in mezzo, e l'icona sembrava un imbuto.
    d.rett(8.5, 8.5, 31.5, 14, r=0.16)                                 # lama
    d.linea((11.5, 11.3), (28.5, 11.3))                                # fessura
    d.linea((13, 14), (18.2, 24))                                      # bracci
    d.linea((27, 14), (21.8, 24))
    d.rett(17.5, 24, 22.5, 35.5, r=0.4)                                # manico


def schiacciapatate(d):
    d.rett(17.4, 3, 22.6, 16, r=0.45)                                  # manico
    d.linea((20, 16), (20, 21))                                        # asta
    d.linea((8, 21.5), (32, 21.5))                                     # traversa
    for x0 in (10.2, 17.8, 25.4):                                      # filo a serpentina
        d.linea((x0, 21.5), (x0, 28.5), (x0 + 4.4, 28.5), (x0 + 4.4, 21.5))


def termometro(d):
    d.cerchio(20, 12, 7)                                               # quadrante
    d.linea((20, 12), (24, 8))                                         # lancetta
    d.rett(18.4, 19, 21.6, 33.5)                                       # gambo
    d.linea((18.4, 33.5), (20, 36.5), (21.6, 33.5), chiusa=True)       # punta


ICONE = {
    'coltello': coltello, 'tagliere': tagliere, 'ciotola': ciotola,
    'bilancia': bilancia, 'frusta': frusta, 'planetaria': planetaria,
    'sbattitore': sbattitore, 'mattarello': mattarello, 'teglia': teglia,
    'tortiera': tortiera, 'setaccio': setaccio, 'sacapoche': sacapoche,
    'spatola': spatola, 'grattugia': grattugia, 'scolapasta': scolapasta,
    'microonde': microonde,
    # aggiunte
    'pennello': pennello, 'tostapane': tostapane, 'minipimer': minipimer,
    'mandolina': mandolina, 'spremiagrumi': spremiagrumi, 'pelapatate': pelapatate,
    'schiacciapatate': schiacciapatate, 'termometro': termometro,
}


def genera(nome, fn):
    doc = fitz.open()
    pg = doc.new_page(width=BOX, height=BOX)
    pg.draw_rect(fitz.Rect(0, 0, BOX, BOX), color=None, fill=(1, 1, 1))
    fn(Disegno(pg))
    pix = pg.get_pixmap(dpi=300)

    src, n, w, h = pix.samples, pix.n, pix.width, pix.height
    buf = bytearray(w * h * 4)
    scuri = 0
    for i in range(w * h):
        r, g, b = src[i * n], src[i * n + 1], src[i * n + 2]
        lum = (r * 299 + g * 587 + b * 114) // 1000
        a = 0 if lum >= 190 else 255 if lum <= 110 else int((190 - lum) * 255 / 80)
        buf[i * 4 + 3] = a
        if a > 128:
            scuri += 1

    p = os.path.normpath(os.path.join(OUT, f'st-{nome}.png'))
    fitz.Pixmap(fitz.csRGB, w, h, bytes(buf), True).save(p)
    return w, h, 100 * scuri / (w * h), os.path.getsize(p)


if __name__ == '__main__':
    tot = 0
    for nome, fn in ICONE.items():
        w, h, cop, size = genera(nome, fn)
        tot += size
        print(f'st-{nome}.png  {w}x{h}  copertura {cop:4.1f}%  {size//1024} KB')
    print(f'-- {len(ICONE)} icone, {tot//1024} KB in totale')
