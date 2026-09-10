"""Rigenera le texture di carta come piastrelle affiancabili senza cucitura.

Le immagini originali sono ritagli: ripetendole si vedrebbe la giunzione a ogni
bordo. Qui si costruisce una piastrella specchiata in quattro quadranti
(originale, ribaltato in orizzontale, in verticale, in entrambi): così la prima
colonna della piastrella è identica all'ultima, e la prima riga all'ultima,
quindi affiancandole non c'è alcuno stacco. Su una grana di carta la simmetria
non si nota.

Serve perché l'app usa `background-repeat: repeat` con una dimensione fissa in
pixel invece di `cover`: in questo modo la grana ha la stessa scala in ogni
punto, indipendentemente da quanto è alta la scatola che la contiene.

    pip install pymupdf
    python mkcarta.py
"""
import fitz, os

PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Render.pdf')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')

# xref dell'immagine di carta dentro il PDF, e dimensione finale della piastrella
CARTE = {
    'bg-salato.jpg': (171, 820, 820),
    'bg-dolce.jpg':  (192, 820, 582),
}


def specchia(pix):
    """Piastrella 2x specchiata nei quattro quadranti."""
    w, h, n = pix.width, pix.height, pix.n
    src = pix.samples
    W, H = w * 2, h * 2
    out = bytearray(W * H * 3)

    def leggi(x, y):
        i = (y * w + x) * n
        return src[i], src[i + 1], src[i + 2]

    for y in range(h):
        for x in range(w):
            r, g, b = leggi(x, y)
            # (x,y) originale · (X specchiato, y) · (x, Y specchiato) · entrambi
            for px, py in ((x, y), (W - 1 - x, y), (x, H - 1 - y), (W - 1 - x, H - 1 - y)):
                o = (py * W + px) * 3
                out[o], out[o + 1], out[o + 2] = r, g, b
    return fitz.Pixmap(fitz.csRGB, W, H, bytes(out), False)


doc = fitz.open(PDF)
for nome, (xref, tw, th) in CARTE.items():
    orig = fitz.Pixmap(doc.extract_image(xref)['image'])
    # il quadrante è metà della piastrella finale
    base = fitz.Pixmap(orig, tw // 2, th // 2, None)
    tile = specchia(base)

    p = os.path.normpath(os.path.join(OUT, nome))
    tile.save(p)

    # controllo: prima e ultima colonna/riga devono coincidere
    s, n2, W, H = tile.samples, tile.n, tile.width, tile.height
    col = all(s[(y * W + 0) * n2] == s[(y * W + W - 1) * n2] for y in range(0, H, 37))
    rig = all(s[(0 * W + x) * n2] == s[((H - 1) * W + x) * n2] for x in range(0, W, 37))
    print(f'{nome}: {W}x{H}, {os.path.getsize(p)//1024} KB — '
          f'bordi combacianti: colonne={col} righe={rig}')
