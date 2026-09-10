import fitz, os, sys

OUT = r'C:\Users\alessia.giacobbe\Downloads\FilesRic\assets'
W, H = 40, 63          # stessa scatola del frigo (40x63 pt) -> stessa scala
SW = float(sys.argv[1]) if len(sys.argv) > 1 else 1.3
NERO = (0, 0, 0)

doc = fitz.open()
pg = doc.new_page(width=W, height=H)
pg.draw_rect(fitz.Rect(0, 0, W, H), color=None, fill=(1, 1, 1))   # carta bianca

def linea(pts, chiudi=False):
    p = [fitz.Point(*t) for t in pts]
    sh = pg.new_shape()
    sh.draw_polyline(p)
    if chiudi:
        sh.draw_line(p[-1], p[0])
    sh.finish(color=NERO, width=SW, lineJoin=1, lineCap=1)
    sh.commit()

def rett(x0, y0, x1, y1, r=0):
    sh = pg.new_shape()
    sh.draw_rect(fitz.Rect(x0, y0, x1, y1), radius=(r / (x1 - x0), r / (y1 - y0)) if r else None)
    sh.finish(color=NERO, width=SW, lineJoin=1)
    sh.commit()

def cerchio(cx, cy, r):
    sh = pg.new_shape()
    sh.draw_circle(fitz.Point(cx, cy), r)
    sh.finish(color=NERO, width=SW)
    sh.commit()

# ── coperchio ────────────────────────────────────────────────
rett(17.0, 1.8, 23.0, 5.0, r=1.0)          # pomello
rett(7.5, 5.0, 32.5, 10.0, r=1.6)          # tappo

# ── caraffa svasata, con beccuccio a destra ──────────────────
linea([(9.5, 10.0), (12.0, 37.0), (28.0, 37.0), (30.5, 10.0)])
linea([(30.5, 10.5), (34.0, 9.0), (32.8, 12.6)])          # beccuccio
linea([(11.2, 22.0), (28.8, 22.0)])                        # tacca di livello

# ── lame ─────────────────────────────────────────────────────
linea([(16.5, 31.5), (23.5, 35.0)])
linea([(23.5, 31.5), (16.5, 35.0)])
linea([(20.0, 35.0), (20.0, 37.0)])

# ── ghiera + corpo motore + zoccolo ──────────────────────────
rett(15.0, 37.0, 25.0, 40.2)
linea([(14.0, 40.2), (11.0, 56.5), (29.0, 56.5), (26.0, 40.2)])
rett(9.8, 56.5, 30.2, 60.0, r=1.2)
cerchio(22.8, 48.5, 2.6)                   # manopola
rett(13.6, 46.4, 17.6, 50.6, r=0.8)        # tasto

pix = pg.get_pixmap(dpi=300)

# stessa conversione in maschera alpha delle altre icone
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

p = os.path.join(OUT, 'ic-frullatore.png')
fitz.Pixmap(fitz.csRGB, w, h, bytes(buf), True).save(p)
print(f'ic-frullatore.png: {w}x{h}, tratto {SW}pt, copertura {100*scuri/(w*h):.1f}%, {os.path.getsize(p)//1024} KB')
