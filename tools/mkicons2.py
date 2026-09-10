import fitz, os

PDF = r'C:\Users\alessia.giacobbe\Downloads\FilesRic\Render.pdf'
OUT = r'C:\Users\alessia.giacobbe\Downloads\FilesRic\assets'
TMP = os.path.dirname(os.path.abspath(__file__))
doc = fitz.open(PDF)


def alpha_da_luminanza(pix, hi=190, lo=110):
    """Line art scuro su carta chiara -> maschera alpha."""
    src, n, w, h = pix.samples, pix.n, pix.width, pix.height
    a = bytearray(w * h)
    for i in range(w * h):
        r, g, b = src[i * n], src[i * n + 1], src[i * n + 2]
        lum = (r * 299 + g * 587 + b * 114) // 1000
        if lum >= hi:
            a[i] = 0
        elif lum <= lo:
            a[i] = 255
        else:
            a[i] = int((hi - lum) * 255 / (hi - lo))
    return a, w, h


def dilata(a, w, h, r):
    """Massimo su finestra quadrata (separabile): ispessisce il tratto."""
    if r <= 0:
        return a
    out = bytearray(w * h)
    for y in range(h):                                   # orizzontale
        base = y * w
        for x in range(w):
            m = 0
            for dx in range(max(0, x - r), min(w, x + r + 1)):
                v = a[base + dx]
                if v > m:
                    m = v
            out[base + x] = m
    fin = bytearray(w * h)
    for x in range(w):                                   # verticale
        for y in range(h):
            m = 0
            for dy in range(max(0, y - r), min(h, y + r + 1)):
                v = out[dy * w + x]
                if v > m:
                    m = v
            fin[y * w + x] = m
    return fin


def copertura(a):
    return 100.0 * sum(1 for v in a if v > 128) / len(a)


def salva_maschera(a, w, h, nome):
    buf = bytearray(w * h * 4)
    for i in range(w * h):
        buf[i * 4 + 3] = a[i]                            # RGB = 0 (nero)
    p = os.path.join(OUT, nome)
    fitz.Pixmap(fitz.csRGB, w, h, bytes(buf), True).save(p)
    print(f'  {nome}: {w}x{h}, copertura {copertura(a):.1f}%, {os.path.getsize(p)//1024} KB')


ICONS = {'forno': (65, 266, 113, 314), 'frigo': (119, 251, 159, 314),
         'pentola': (166, 266, 241, 315), 'padella': (248, 273, 332, 314)}

# Riferimento: la copertura media di forno e frigo, che sono le due che
# piacciono. Pentola e padella vengono ispessite fino ad avvicinarsi.
rif = []
for k in ('forno', 'frigo'):
    a, w, h = alpha_da_luminanza(doc[1].get_pixmap(dpi=300, clip=fitz.Rect(*ICONS[k])))
    rif.append(copertura(a))
    salva_maschera(a, w, h, f'ic-{k}.png')
target = sum(rif) / len(rif)
print(f'copertura di riferimento (forno/frigo): {target:.1f}%')

for k in ('pentola', 'padella'):
    a0, w, h = alpha_da_luminanza(doc[1].get_pixmap(dpi=300, clip=fitz.Rect(*ICONS[k])))
    migliore, scarto_migliore = 0, abs(copertura(a0) - target)
    for r in (1, 2, 3, 4):
        s = abs(copertura(dilata(a0, w, h, r)) - target)
        if s < scarto_migliore:
            migliore, scarto_migliore = r, s
    print(f'{k}: dilatazione scelta r={migliore}')
    salva_maschera(dilata(a0, w, h, migliore), w, h, f'ic-{k}.png')
