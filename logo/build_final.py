# Logo final Trading Tenang: tulisan persis seperti judul di website
# (Switzer 600, letter-spacing -0.055em, kerning aktif), plus favicon huruf T.
# Hasil: logo/final/*.svg
import os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = os.path.join(HERE, "src", "switzer-600.ttf")
OUT = os.path.join(HERE, "final")
os.makedirs(OUT, exist_ok=True)

# Warna website
GRAPHITE = "#18191B"
INK = "#EFF0F1"

FONT = TTFont(FONT_FILE)
GS = FONT.getGlyphSet()
ORDER = FONT.getGlyphOrder()
UPM = FONT["head"].unitsPerEm
CAP = FONT["OS/2"].sCapHeight
TRACKING = -0.055  # sama dengan .hero h1 di website

with open(FONT_FILE, "rb") as f:
    HB_FONT = hb.Font(hb.Face(hb.Blob(f.read())))


def shape(text):
    """Posisi glyph dengan kerning, dalam satuan font."""
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(HB_FONT, buf, {"kern": True, "liga": True})
    out, x = [], 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((ORDER[info.codepoint], x + pos.x_offset))
        x += pos.x_advance + TRACKING * UPM
    return out


def draw(glyphs, s, x, baseline):
    """Path SVG dan kotak batas (x0, y0, x1, y1) tulisan pada skala s."""
    parts, b = [], [1e9, 1e9, -1e9, -1e9]
    for name, gx in glyphs:
        pen = SVGPathPen(GS)
        GS[name].draw(TransformPen(pen, (s, 0, 0, -s, x + gx * s, baseline)))
        parts.append(pen.getCommands())
        bp = BoundsPen(GS)
        GS[name].draw(bp)
        if bp.bounds:
            x0, y0, x1, y1 = bp.bounds
            b = [min(b[0], x + (gx + x0) * s), min(b[1], baseline - y1 * s),
                 max(b[2], x + (gx + x1) * s), max(b[3], baseline - y0 * s)]
    return " ".join(p for p in parts if p), b


def svg(w, h, body, bg=None, rx=0):
    bgr = f'<rect width="{w:.0f}" height="{h:.0f}" rx="{rx}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img">'
            f'<title>Trading Tenang</title>{bgr}{body}</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


def wordmark(ink, bg, cap=160):
    s = cap / CAP
    glyphs = shape("Trading Tenang")
    _, b = draw(glyphs, s, 0, 0)
    pad = cap * 0.5
    w = (b[2] - b[0]) + pad * 2
    h = (b[3] - b[1]) + pad * 2
    d, _ = draw(glyphs, s, pad - b[0], pad - b[1])
    return svg(w, h, f'<path d="{d}" fill="{ink}"/>', bg)


def favicon(size=512, rx=0):
    # Huruf T di tengah kotak grafit, tinggi huruf 62% kotak
    cap = size * 0.62
    s = cap / CAP
    glyphs = shape("T")
    _, b = draw(glyphs, s, 0, 0)
    dx = (size - (b[2] - b[0])) / 2 - b[0]
    dy = (size - (b[3] - b[1])) / 2 - b[1]
    d, _ = draw(glyphs, s, dx, dy)
    return svg(size, size, f'<path d="{d}" fill="{INK}"/>', GRAPHITE, rx)


save("trading-tenang-logo-dark.svg", wordmark(INK, GRAPHITE))
save("trading-tenang-logo-light.svg", wordmark(GRAPHITE, INK))
save("trading-tenang-logo-white.svg", wordmark(INK, None))
save("trading-tenang-logo-black.svg", wordmark(GRAPHITE, None))
save("favicon.svg", favicon(512))
save("favicon-rounded.svg", favicon(512, rx=112))
print(sorted(os.listdir(OUT)))
