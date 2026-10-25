# Membuat semua varian logo Trading Tenang sebagai SVG murni (huruf sudah jadi garis, tanpa font).
# Simbol: satu huruf T, T dari Tenang. Palangnya lengkung tipis yang meruncing di kedua ujung,
# batangnya meruncing ke bawah seperti badan candle, dan ujungnya sumbu merah: harga pernah jatuh,
# tapi batangnya tetap berdiri.
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "svg")
os.makedirs(OUT, exist_ok=True)

BLACK = "#0A0A0A"
RED = "#B3121F"
GOLD = "#C9A45C"
GOLD_ON_LIGHT = "#9E7A34"
IVORY = "#F4F3EF"

FONT = TTFont(os.path.join(HERE, "src", "switzer-400.ttf"))
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UPM = FONT["head"].unitsPerEm
CAP = FONT["OS/2"].sCapHeight


def text_path(text, cap_px, x0, baseline, tracking=0.42):
    """Huruf jadi path. cap_px = tinggi huruf kapital dalam px."""
    size = cap_px * UPM / CAP
    s = size / UPM
    x = x0
    parts = []
    for i, ch in enumerate(text):
        name = CMAP[ord(ch)]
        pen = SVGPathPen(GLYPHS)
        GLYPHS[name].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        parts.append(pen.getCommands())
        x += GLYPHS[name].width * s
        if i < len(text) - 1:
            x += tracking * size
    return " ".join(p for p in parts if p), x - x0


# Simbol dalam kotak 100x100.
CROSSBAR = "M5 27.5 C 20 13, 80 13, 95 27.5 C 77 21.5, 23 21.5, 5 27.5 Z"
STEM = "M41.8 26.4 C 47 25.2, 53 25.2, 58.2 26.4 L 52.1 73 L 47.9 73 Z"
WICK = "M48.3 76.5 L 51.7 76.5 L 50 97 Z"


def mark(red=RED, gold=GOLD, dx=0, dy=0, k=1.0):
    return (f'<g transform="translate({dx:.2f} {dy:.2f}) scale({k:.4f})">'
            f'<path d="{CROSSBAR}" fill="{gold}"/><path d="{STEM}" fill="{gold}"/><path d="{WICK}" fill="{red}"/></g>')


def svg(w, h, body, bg=None, title="Trading Tenang"):
    bgrect = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img">'
            f'<title>{title}</title>{bgrect}{body}</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


def wordmark(x, baseline, cap, c1, c2):
    # TRADING dan TENANG dalam satu baris, jarak antarhuruf lebar.
    d1, w1 = text_path("TRADING", cap, x, baseline)
    gap = cap * 1.6
    d2, w2 = text_path("TENANG", cap, x + w1 + gap, baseline)
    return f'<path d="{d1}" fill="{c1}"/><path d="{d2}" fill="{c2}"/>', w1 + gap + w2


def horizontal(bg, c1, c2, red=RED, gold=GOLD, pad=56):
    mk = 112
    x_text = pad + mk + 24
    cap = 17
    body_text, tw = wordmark(x_text, pad + mk * 0.5 + cap / 2, cap, c1, c2)
    w = x_text + tw + pad
    h = mk + pad * 2
    return svg(w, h, mark(red, gold, pad, pad, mk / 100) + body_text, bg)


def stacked(bg, c1, c2, red=RED, gold=GOLD, pad=64):
    mk = 200
    cap = 15
    _, tw = wordmark(0, 0, cap, c1, c2)
    w = max(tw, mk) + pad * 2
    h = pad + mk + 44 + cap + pad
    body_text, _ = wordmark((w - tw) / 2, pad + mk + 44 + cap, cap, c1, c2)
    return svg(w, h, mark(red, gold, (w - mk) / 2, pad, mk / 100) + body_text, bg)


def tile(bg, red=RED, gold=GOLD, size=512, inset=0.18):
    k = size * (1 - inset * 2) / 100
    return svg(size, size, mark(red, gold, size * inset, size * inset, k), bg)


save("trading-tenang-logo-dark.svg", horizontal(BLACK, IVORY, GOLD))
save("trading-tenang-logo-light.svg", horizontal(IVORY, BLACK, GOLD_ON_LIGHT, gold=GOLD_ON_LIGHT))
save("trading-tenang-logo-stacked-dark.svg", stacked(BLACK, IVORY, GOLD))
save("trading-tenang-logo-gold-mono.svg", horizontal(BLACK, GOLD, GOLD, red=GOLD))
save("trading-tenang-logo-transparent.svg", horizontal(None, IVORY, GOLD))
save("trading-tenang-mark.svg", svg(100, 100, mark()))
save("trading-tenang-mark-tile.svg", tile(BLACK))
save("trading-tenang-mark-tile-red.svg", tile(RED, red=BLACK, gold=GOLD))
print("ok:", sorted(os.listdir(OUT)))
