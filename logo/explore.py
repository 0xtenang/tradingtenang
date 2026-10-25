# Eksplorasi enam arah logo Trading Tenang. Semua huruf diubah jadi path (tanpa font).
# Hasil: logo/explore/<id>-lockup.svg dan <id>-tile.svg
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "explore")
os.makedirs(OUT, exist_ok=True)

BLACK, RED, GOLD, IVORY = "#0A0A0A", "#B3121F", "#C9A45C", "#F4F3EF"


class Face:
    def __init__(self, file):
        self.f = TTFont(os.path.join(HERE, "src", file))
        self.gs = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm
        self.cap = self.f["OS/2"].sCapHeight

    def glyph(self, ch, cap_px, x, baseline):
        """Satu huruf: path, kotak batas (x0, y0, x1, y1) dalam px, lebar advance."""
        s = cap_px / self.cap
        name = self.cmap[ord(ch)]
        pen = SVGPathPen(self.gs)
        self.gs[name].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        bp = BoundsPen(self.gs)
        self.gs[name].draw(bp)
        xmin, ymin, xmax, ymax = bp.bounds
        box = (x + xmin * s, baseline - ymax * s, x + xmax * s, baseline - ymin * s)
        return pen.getCommands(), box, self.gs[name].width * s

    def text(self, text, cap_px, x, baseline, tracking=0.3):
        size = cap_px * self.upm / self.cap
        parts, cx = [], x
        for i, ch in enumerate(text):
            if ch == " ":
                cx += size * 0.28 + tracking * size
                continue
            d, _, adv = self.glyph(ch, cap_px, cx, baseline)
            parts.append(d)
            cx += adv + (tracking * size if i < len(text) - 1 else 0)
        return " ".join(parts), cx - x


BODONI = Face("bodoni-display.ttf")
CINZEL = Face("cinzel-500.ttf")
BODONI_TEXT = Face("bodoni-text.ttf")
BODONI_MID = Face("bodoni-mid.ttf")
SWITZER = Face("switzer-600.ttf")


def web_word(cx, baseline):
    # Tulisan seperti di website: Switzer semibold, huruf besar-kecil, jarak antarhuruf rapat.
    return centered_word(SWITZER, "Trading Tenang", 46, cx, baseline, IVORY, -0.05)


def svg(w, h, body, bg=BLACK, defs=""):
    bgr = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img">'
            f'<title>Trading Tenang</title>{defs}{bgr}{body}</svg>\n')


def save(name, s):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(s)


def centered_word(face, text, cap, cx, baseline, color, tracking=0.32):
    _, w = face.text(text, cap, 0, 0, tracking)
    d, _ = face.text(text, cap, cx - w / 2, baseline, tracking)
    return f'<path d="{d}" fill="{color}"/>', w


W, H = 1200, 760


# A. Maison: T Bodoni emas, batangnya diteruskan sumbu merah setipis rambut.
def a_mark(cx, top, cap):
    d, (x0, y0, x1, y1), _ = BODONI.glyph("T", cap, 0, 0)
    w = x1 - x0
    d, (x0, y0, x1, y1), _ = BODONI.glyph("T", cap, cx - w / 2 - (x0), top + cap)
    stem_x = cx
    wick = f'<rect x="{stem_x - cap * 0.012:.2f}" y="{y1 + cap * 0.06:.2f}" width="{cap * 0.024:.2f}" height="{cap * 0.42:.2f}" fill="{RED}"/>'
    return f'<path d="{d}" fill="{GOLD}"/>' + wick, y1 + cap * 0.48


def a():
    m, bottom = a_mark(W / 2, 150, 300)
    wm, _ = web_word(W / 2, bottom + 112)
    save("a-lockup.svg", svg(W, H, m + wm))
    m, _ = a_mark(256, 92, 250)
    save("a-tile.svg", svg(512, 512, m))


# B. Koin: cincin emas tipis, T Cinzel di tengah, titik merah sebagai harga penutupan.
def b_mark(cx, cy, r):
    ring = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="{r * 0.035:.2f}"/>'
    ring2 = f'<circle cx="{cx}" cy="{cy}" r="{r * 0.9:.2f}" fill="none" stroke="{GOLD}" stroke-width="{r * 0.01:.2f}"/>'
    cap = r * 0.95
    d, (x0, y0, x1, y1), _ = CINZEL.glyph("T", cap, 0, 0)
    w = x1 - x0
    d, box, _ = CINZEL.glyph("T", cap, cx - w / 2 - x0, cy + cap / 2 - r * 0.08)
    dot = f'<rect x="{cx - r * 0.045:.2f}" y="{box[3] + r * 0.1:.2f}" width="{r * 0.09:.2f}" height="{r * 0.09:.2f}" fill="{RED}" transform="rotate(45 {cx:.2f} {box[3] + r * 0.145:.2f})"/>'
    return ring + ring2 + f'<path d="{d}" fill="{GOLD}"/>' + dot


def b():
    m = b_mark(W / 2, 300, 170)
    wm, _ = web_word(W / 2, 612)
    save("b-lockup.svg", svg(W, H, m + wm))
    save("b-tile.svg", svg(512, 512, b_mark(256, 256, 190)))


# C. Air tenang: T emas berdiri di atas garis air, bayangannya merah dipecah riak.
def c_mark(cx, line_y, cap, uid):
    d, (x0, y0, x1, y1), _ = BODONI.glyph("T", cap, 0, 0)
    w = x1 - x0
    shift = cx - w / 2 - x0
    d, box, _ = BODONI.glyph("T", cap, shift, line_y - cap * 0.06)
    up = f'<path d="{d}" fill="{GOLD}"/>'
    # bayangan: huruf yang sama dibalik terhadap garis air, dipotong pita-pita mendatar
    depth = cap * 0.7
    bands, y, hgt, gap = [], line_y + cap * 0.035, cap * 0.16, cap * 0.022
    while y < line_y + depth:
        bands.append(f'<rect x="{box[0] - 10:.1f}" y="{y:.2f}" width="{box[2] - box[0] + 20:.1f}" height="{hgt:.2f}"/>')
        y += hgt + gap
        hgt *= 0.72
        gap *= 1.3
    clip = f'<clipPath id="rip{uid}">{"".join(bands)}</clipPath>'
    refl = (f'<g clip-path="url(#rip{uid})"><path d="{d}" fill="{RED}" '
            f'transform="translate(0 {2 * line_y:.2f}) scale(1 -1)"/></g>')
    line = f'<rect x="{cx - cap * 0.62:.2f}" y="{line_y - cap * 0.006:.2f}" width="{cap * 1.24:.2f}" height="{cap * 0.012:.2f}" fill="{GOLD}"/>'
    return up + line + refl, clip, line_y + depth


def c():
    m, clip, bottom = c_mark(W / 2, 360, 250, "a")
    wm, _ = web_word(W / 2, bottom + 100)
    save("c-lockup.svg", svg(W, H, m + wm, defs=f"<defs>{clip}</defs>"))
    m, clip, _ = c_mark(256, 300, 230, "b")
    save("c-tile.svg", svg(512, 512, m, defs=f"<defs>{clip}</defs>"))


# D. Cap emas: bingkai seperti hallmark pada perhiasan emas, T di dalam, tahun berdiri di bawah.
def d_mark(cx, cy, s):
    frame = (f'<rect x="{cx - s / 2:.2f}" y="{cy - s / 2:.2f}" width="{s:.2f}" height="{s:.2f}" fill="none" '
             f'stroke="{GOLD}" stroke-width="{s * 0.022:.2f}"/>')
    cap = s * 0.56
    d, (x0, y0, x1, y1), _ = BODONI.glyph("T", cap, 0, 0)
    w = x1 - x0
    d, box, _ = BODONI.glyph("T", cap, cx - w / 2 - x0, cy + cap / 2 - s * 0.06)
    year, yw = centered_word(CINZEL, "MMXVII", s * 0.07, cx, cy + s * 0.41, RED, 0.45)
    return frame + f'<path d="{d}" fill="{GOLD}"/>' + year


def d():
    m = d_mark(W / 2, 290, 300)
    wm, _ = web_word(W / 2, 580)
    save("d-lockup.svg", svg(W, H, m + wm))
    save("d-tile.svg", svg(512, 512, d_mark(256, 256, 340)))


# E. Hanya nama: "Trading Tenang" besar seperti di website, diakhiri titik merah.
def e():
    cap = 92
    _, bw = SWITZER.text("Trading Tenang", cap, 0, 0, -0.05)
    x = (W - bw) / 2 - 14
    big, bw = SWITZER.text("Trading Tenang", cap, x, 420, -0.05)
    dot = f'<rect x="{x + bw + 10:.2f}" y="{420 - 18:.2f}" width="18" height="18" fill="{RED}"/>'
    save("e-lockup.svg", svg(W, H, f'<path d="{big}" fill="{IVORY}"/>' + dot))
    # tile: T dan titik merah
    d, (x0, y0, x1, y1), adv = SWITZER.glyph("T", 250, 0, 0)
    w = x1 - x0
    d, box, _ = SWITZER.glyph("T", 250, 256 - w / 2 - x0 - 20, 381)
    dot = f'<rect x="{box[2] + 14:.2f}" y="{381 - 34:.2f}" width="34" height="34" fill="{RED}"/>'
    save("e-tile.svg", svg(512, 512, f'<path d="{d}" fill="{IVORY}"/>' + dot))


# F. Dua warna: T Bodoni, palang dan badan atas emas, bagian bawah batang merah, dipisah celah tipis.
def f_mark(cx, top, cap, uid):
    d, (x0, y0, x1, y1), _ = BODONI.glyph("T", cap, 0, 0)
    w = x1 - x0
    d, box, _ = BODONI.glyph("T", cap, cx - w / 2 - x0, top + cap)
    cut = box[1] + (box[3] - box[1]) * 0.66
    g = cap * 0.03
    defs = (f'<clipPath id="fu{uid}"><rect x="0" y="0" width="5000" height="{cut - g / 2:.2f}"/></clipPath>'
            f'<clipPath id="fd{uid}"><rect x="0" y="{cut + g / 2:.2f}" width="5000" height="5000"/></clipPath>')
    body = (f'<path d="{d}" fill="{GOLD}" clip-path="url(#fu{uid})"/>'
            f'<path d="{d}" fill="{RED}" clip-path="url(#fd{uid})"/>')
    return body, defs, box[3]


def f():
    m, defs, bottom = f_mark(W / 2, 150, 330, "a")
    wm, _ = web_word(W / 2, bottom + 120)
    save("f-lockup.svg", svg(W, H, m + wm, defs=f"<defs>{defs}</defs>"))
    m, defs, _ = f_mark(256, 96, 320, "b")
    save("f-tile.svg", svg(512, 512, m, defs=f"<defs>{defs}</defs>"))


for fn in (a, b, c, d, e, f):
    fn()
print(sorted(os.listdir(OUT)))
