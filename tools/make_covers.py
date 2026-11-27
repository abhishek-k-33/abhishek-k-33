"""Generate the project cover SVGs in the banner's flat palette (no gradients).

Writes assets/osdagbridge-{light,dark}.svg and assets/boardscan-{light,dark}.svg.
Colours come from tools/make_banner.py so the covers always match the banner.

Run from the repo root:  python3 tools/make_covers.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_banner import MONO, OUT, SANS, SYMBOL, THEMES  # noqa: E402

GRID = {"light": "#ebe5ef", "dark": "#2b2930"}

STYLE = """
  .draw{stroke-dasharray:700;animation:draw 6s ease-in-out infinite}
  @keyframes draw{0%{stroke-dashoffset:700}45%,80%{stroke-dashoffset:0}100%{stroke-dashoffset:-700}}
  .bob{animation:bob 2.4s ease-in-out infinite}
  @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(5px)}}
  .scan{animation:scan 3.5s ease-in-out infinite}
  @keyframes scan{0%,100%{transform:translateY(0)}50%{transform:translateY(150px)}}
  @media (prefers-reduced-motion:reduce){*{animation:none!important}.draw{stroke-dasharray:none}}
"""


def shell(t, grid, title, kicker, sub, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360" role="img" aria-label="{title}: {sub}">
<style>{STYLE}</style>
<defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{grid}" stroke-width="1"/></pattern></defs>
<rect width="640" height="360" rx="14" fill="{t['bg']}"/>
<rect width="640" height="360" rx="14" fill="url(#grid)"/>
<text x="36" y="44" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{t['terracotta']}">{kicker}</text>
<text x="34" y="86" font-family="{SANS}" font-size="38" font-weight="800" letter-spacing="-1" fill="{t['ink']}">{title}<tspan fill="{t['terracotta']}">.</tspan></text>
<text x="36" y="112" font-family="{MONO}" font-size="13" fill="{t['muted']}">{sub}</text>
{body}
<rect x=".75" y=".75" width="638.5" height="358.5" rx="14" fill="none" stroke="{t['line']}" stroke-width="1.5"/>
</svg>
"""


def osdag(mode):
    t, grid = THEMES[mode], GRID[mode]
    fill, edge = t["desk"], t["desk_edge"]
    arrows = "".join(
        f'<path d="M{x} 176 v24 m-5 -7 l5 7 l5 -7" fill="none" stroke="{t["mustard"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        for x in range(80, 580, 36))
    hatch = "".join(f'<path d="M{x} 316 l-10 12" stroke="{edge}" stroke-width="1.5"/>' for x in range(46, 604, 14))
    body = f"""
<g class="bob">{arrows}</g>
<rect x="56" y="206" width="528" height="12" rx="2" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>
<rect x="64" y="218" width="512" height="20" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>
<path d="M56 238 h30 l14 78 h-58 z" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>
<path d="M584 238 h-30 l-14 78 h58 z" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>
<rect x="222" y="238" width="18" height="78" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>
<rect x="400" y="238" width="18" height="78" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>
<line x1="30" y1="316" x2="610" y2="316" stroke="{t['muted']}" stroke-width="1.5"/>{hatch}
<path class="draw" d="M86 240 Q158 290 231 240 Q320 296 409 240 Q482 290 554 240" fill="none" stroke="{t['terracotta']}" stroke-width="3" stroke-linecap="round"/>
<text x="148" y="300" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t['sage']}">span 1</text>
<text x="320" y="300" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t['sage']}">span 2</text>
<text x="492" y="300" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t['sage']}">span 3</text>
"""
    svg = shell(t, grid, "OsdagBridge", "STRUCTURAL ENGINEERING · PYTHON",
                "bridge analysis &amp; design · IRC codes · OpenSees", body)
    (OUT / f"osdagbridge-{mode}.svg").write_text(svg)


# Position after 1.e4 e5 2.Nf3 (rank 8 first)
BOARD = ["rnbqkbnr", "pppp.ppp", "........", "....p...", "....P...", ".....N..", "PPPP.PPP", "RNBQKB.R"]
GLYPH = dict(K="♔", Q="♕", R="♖", B="♗", N="♘", P="♙", k="♚", q="♛", r="♜", b="♝", n="♞", p="♟")
FEN = "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"


def piece(c, x, y, size):
    col = "#ffffff" if c.isupper() else "#1d1d1d"
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" font-size="{size:.1f}" '
            f'fill="{col}" stroke="#1d1d1d" stroke-width=".5">{GLYPH[c]}</text>')


def boardscan(mode):
    t, grid = THEMES[mode], GRID[mode]
    lsq, dsq = t["sq_light"], t["sq_dark"]
    FL, FR, NR, NL = (96, 158), (236, 158), (270, 318), (40, 318)

    def pt(u, v):
        lx = FL[0] + (NL[0] - FL[0]) * v; ly = FL[1] + (NL[1] - FL[1]) * v
        rx = FR[0] + (NR[0] - FR[0]) * v; ry = FR[1] + (NR[1] - FR[1]) * v
        return lx + (rx - lx) * u, ly + (ry - ly) * u

    persp = []
    for r in range(8):
        for f in range(8):
            q = [pt(f / 8, r / 8), pt((f + 1) / 8, r / 8), pt((f + 1) / 8, (r + 1) / 8), pt(f / 8, (r + 1) / 8)]
            persp.append('<polygon points="%s" fill="%s"/>' % (
                " ".join(f"{x:.1f},{y:.1f}" for x, y in q), lsq if (r + f) % 2 == 0 else dsq))
    for r in range(8):
        for f in range(8):
            c = BOARD[r][f]
            if c != ".":
                x, y = pt((f + .5) / 8, (r + .72) / 8)
                persp.append(piece(c, x, y, 11 + 9 * (r / 7)))

    flat = []
    ox, oy, s = 392, 142, 20
    for r in range(8):
        for f in range(8):
            flat.append(f'<rect x="{ox + f * s}" y="{oy + r * s}" width="{s}" height="{s}" fill="{lsq if (r + f) % 2 == 0 else dsq}"/>')
            c = BOARD[r][f]
            if c != ".":
                flat.append(piece(c, ox + f * s + s / 2, oy + r * s + 15.5, 16))

    corners = "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{t["terracotta"]}"/>' for x, y in (FL, FR, NR, NL))
    body = f"""
<g font-family="{SYMBOL}">
  <polygon points="{FL[0]},{FL[1]} {FR[0]},{FR[1]} {NR[0]},{NR[1]} {NL[0]},{NL[1]}" fill="none" stroke="{t['mustard']}" stroke-width="2" stroke-dasharray="5 4"/>
  {''.join(persp)}
  {corners}
  <g class="scan"><line x1="40" y1="164" x2="270" y2="164" stroke="{t['terracotta']}" stroke-width="2" opacity=".85"/></g>
  {''.join(flat)}
  <rect x="{ox}" y="{oy}" width="160" height="160" fill="none" stroke="{t['board_edge']}" stroke-width="2"/>
</g>
<path d="M292 232 h70 m-9 -8 l9 8 l-9 8" fill="none" stroke="{t['sage']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<text x="326" y="220" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t['muted']}">homography</text>
<text x="326" y="256" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t['muted']}">+ CNN</text>
<rect x="558" y="142" width="72" height="24" rx="12" fill="{t['bg']}" stroke="{t['sage']}" stroke-width="1.5"/>
<text x="594" y="158" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{t['sage']}">stockfish</text>
<text x="34" y="344" font-family="{MONO}" font-size="11.5" fill="{t['terracotta']}">FEN  <tspan fill="{t['muted']}">{FEN}</tspan></text>
"""
    svg = shell(t, grid, "BoardScan", "COMPUTER VISION · PYTHON",
                "chessboard photo → FEN → engine evaluation", body)
    (OUT / f"boardscan-{mode}.svg").write_text(svg)


if __name__ == "__main__":
    for mode in ("light", "dark"):
        osdag(mode)
        boardscan(mode)
    print("wrote covers to", OUT)
