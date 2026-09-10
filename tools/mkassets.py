import fitz, os

PDF = r'C:\Users\alessia.giacobbe\Downloads\FilesRic\Render.pdf'
OUT = r'C:\Users\alessia.giacobbe\Downloads\FilesRic\assets'
os.makedirs(OUT, exist_ok=True)
doc = fitz.open(PDF)


def save(pix, name):
    p = os.path.join(OUT, name)
    pix.save(p)
    print(name, pix.width, 'x', pix.height, os.path.getsize(p) // 1024, 'KB')


def crop(page_i, rect, dpi, name):
    pg = doc[page_i]
    pix = pg.get_pixmap(dpi=dpi, clip=fitz.Rect(*rect))
    save(pix, name)


def mask(page_i, rect, dpi, name):
    """Line art -> black RGB + alpha from darkness, for CSS mask-image."""
    pg = doc[page_i]
    pix = pg.get_pixmap(dpi=dpi, clip=fitz.Rect(*rect))
    src = pix.samples
    n = pix.n
    w, h = pix.width, pix.height
    out = bytearray(w * h * 4)
    for i in range(w * h):
        r, g, b = src[i * n], src[i * n + 1], src[i * n + 2]
        lum = (r * 299 + g * 587 + b * 114) // 1000
        if lum >= 190:
            a = 0
        elif lum <= 110:
            a = 255
        else:
            a = int((190 - lum) * 255 / 80)
        o = i * 4
        out[o] = out[o + 1] = out[o + 2] = 0
        out[o + 3] = a
    save(fitz.Pixmap(fitz.csRGB, w, h, bytes(out), True), name)


# ── sfondi carta ──────────────────────────────────────────────
for xref, name in ((171, 'bg-salato.jpg'), (192, 'bg-dolce.jpg')):
    info = doc.extract_image(xref)
    pix = fitz.Pixmap(info['image'])
    scale = 820 / max(pix.width, pix.height)
    pix = fitz.Pixmap(pix, int(pix.width * scale), int(pix.height * scale), None)
    save(pix, name)

# ── fascia decorativa laterale (illustrazioni + carta) ────────
crop(0, (0, 0, 186, 842.25), 110, 'deco-salato.jpg')
crop(2, (0, 0, 200, 842.25), 110, 'deco-dolce.jpg')

# ── barra di ricerca ──────────────────────────────────────────
crop(0, (212.2, 129.0, 535.6, 207.1), 150, 'search-salato.jpg')
crop(2, (192.8, 129.9, 516.2, 207.9), 150, 'search-dolce.jpg')

# ── numeri del procedimento (1..5) ────────────────────────────
NUMS = {1: (29, 503, 50, 547), 2: (27, 565, 53, 618),
        3: (29, 637, 54, 688), 4: (29, 701, 56, 748), 5: (29, 764, 55, 816)}
for k, r in NUMS.items():
    crop(1, r, 300, f'num{k}.png')

# ── icone strumenti (maschere alpha) ──────────────────────────
ICONS = {'forno': (65, 266, 113, 314), 'frigo': (119, 251, 159, 314),
         'pentola': (166, 266, 241, 315), 'padella': (248, 273, 332, 314)}
for k, r in ICONS.items():
    mask(1, r, 300, f'ic-{k}.png')

# ── icone PWA ─────────────────────────────────────────────────
base = doc[0].get_pixmap(dpi=300, clip=fitz.Rect(5, 5, 205, 205))
for size, name in ((192, 'icon-192.png'), (512, 'icon-512.png')):
    save(fitz.Pixmap(base, size, size, None), name)
