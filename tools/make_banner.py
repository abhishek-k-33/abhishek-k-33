"""Generate the profile banner (assets/banner-light.svg, assets/banner-dark.svg).

A flat-colour desk scene: code on the laptop, coffee, a chessboard, and a cat
who occasionally knocks the knight over. Light mode is daytime (sun), dark mode
is night-time (moon and stars). No gradients anywhere.

Run from the repo root:  python3 tools/make_banner.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"
SYMBOL = "'DejaVu Sans', 'Segoe UI Symbol', 'Apple Symbols', 'Noto Sans Symbols 2', sans-serif"

THEMES = {
    "light": dict(
        bg="#fbf6ee", ink="#2f3142", muted="#6b6f80", line="#e6dccb",
        terracotta="#e07a5f", sage="#5f9a7e", mustard="#e0a93b",
        desk="#e8d5b7", desk_edge="#d6bd96",
        lid="#3d405b", screen="#262838", code="#f4efe6", code_muted="#8a8ea3",
        mug="#81b29a", cat="#e8a35c", cat_dark="#c47a37", belly="#f8dcb8", cat_eye="#2f3142",
        sq_light="#f3e3c3", sq_dark="#b98a60", board_edge="#8a6243",
        sky="#cfe6ea", frame="#d6bd96", night=False,
    ),
    "dark": dict(
        bg="#1c2030", ink="#f4efe6", muted="#a3a8b8", line="#2e3347",
        terracotta="#ee8b70", sage="#86c0a4", mustard="#f2c66d",
        desk="#2c3042", desk_edge="#3a3f55",
        lid="#4a4e6a", screen="#131622", code="#f4efe6", code_muted="#7d8299",
        mug="#86c0a4", cat="#eaa968", cat_dark="#c4823f", belly="#f6dcbc", cat_eye="#1c2030",
        sq_light="#e9d8b8", sq_dark="#a97e57", board_edge="#6f4f36",
        sky="#262c45", frame="#3a3f55", night=True,
    ),
}

STYLE = """
  .caret{animation:blink 1.1s steps(1) infinite}
  @keyframes blink{50%{opacity:0}}
  .type{transform-box:fill-box;transform-origin:right;animation:type 9s steps(14) infinite}
  .l2{animation-name:type2}.l3{animation-name:type3}.l4{animation-name:type4}
  @keyframes type {0%{transform:scaleX(1)}8%,92%{transform:scaleX(0)}100%{transform:scaleX(1)}}
  @keyframes type2{0%,8%{transform:scaleX(1)}26%,92%{transform:scaleX(0)}100%{transform:scaleX(1)}}
  @keyframes type3{0%,26%{transform:scaleX(1)}38%,92%{transform:scaleX(0)}100%{transform:scaleX(1)}}
  @keyframes type4{0%,38%{transform:scaleX(1)}42%,92%{transform:scaleX(0)}100%{transform:scaleX(1)}}
  .steam{animation:steam 3s ease-in-out infinite;opacity:0}
  .steam.s2{animation-delay:-1.5s}
  @keyframes steam{0%{transform:translateY(6px);opacity:0}40%{opacity:.7}100%{transform:translateY(-14px);opacity:0}}
  .tail{transform-origin:1094px 252px;animation:tail 2.6s ease-in-out infinite}
  @keyframes tail{0%,100%{transform:rotate(0)}50%{transform:rotate(-14deg)}}
  .blink{transform-box:fill-box;transform-origin:center;animation:eyes 5s infinite}
  @keyframes eyes{0%,94%,100%{transform:scaleY(1)}96%{transform:scaleY(.1)}}
  .paw{animation:paw 6s ease-in-out infinite}
  @keyframes paw{0%,38%,62%,100%{transform:translate(0,0)}46%,52%{transform:translate(-22px,4px)}}
  .knight{transform-box:fill-box;transform-origin:bottom center;animation:knight 6s ease-in-out infinite}
  @keyframes knight{0%,46%,90%,100%{transform:translate(0,0) rotate(0)}
    52%{transform:translate(-10px,-16px) rotate(-30deg)}60%,82%{transform:translate(-18px,0) rotate(-90deg)}}
  .oops{animation:oops 6s ease-in-out infinite;opacity:0}
  @keyframes oops{0%,48%,70%,100%{opacity:0}52%,66%{opacity:1}}
  .twinkle{animation:twinkle 3s ease-in-out infinite}
  .twinkle.t2{animation-delay:-1s}.twinkle.t3{animation-delay:-2s}
  @keyframes twinkle{0%,100%{opacity:.25}50%{opacity:1}}
  @media (prefers-reduced-motion:reduce){*{animation:none!important}.type{transform:scaleX(0)}.steam{opacity:.6}}
"""


def board(t):
    """Chessboard on the desk seen at a shallow angle (8x8, perspective)."""
    FL, FR, NR, NL = (936, 262), (1106, 262), (1124, 290), (918, 290)

    def pt(u, v):
        lx = FL[0] + (NL[0] - FL[0]) * v; ly = FL[1] + (NL[1] - FL[1]) * v
        rx = FR[0] + (NR[0] - FR[0]) * v; ry = FR[1] + (NR[1] - FR[1]) * v
        return lx + (rx - lx) * u, ly + (ry - ly) * u

    out = []
    for r in range(8):
        for f in range(8):
            q = [pt(f / 8, r / 8), pt((f + 1) / 8, r / 8), pt((f + 1) / 8, (r + 1) / 8), pt(f / 8, (r + 1) / 8)]
            fill = t["sq_light"] if (r + f) % 2 == 0 else t["sq_dark"]
            out.append('<polygon points="%s" fill="%s"/>' % (" ".join(f"{x:.1f},{y:.1f}" for x, y in q), fill))
    out.append(f'<polygon points="{NL[0]},{NL[1]} {NR[0]},{NR[1]} {NR[0]},{NR[1] + 6} {NL[0]},{NL[1] + 6}" fill="{t["board_edge"]}"/>')
    return "\n  ".join(out)


def window(t):
    parts = [
        f'<rect x="876" y="40" width="92" height="84" rx="8" fill="{t["sky"]}" stroke="{t["frame"]}" stroke-width="5"/>',
    ]
    if t["night"]:
        parts += [
            f'<circle cx="938" cy="70" r="15" fill="{t["mustard"]}"/>',
            f'<circle cx="946" cy="64" r="13" fill="{t["sky"]}"/>',
            f'<circle class="twinkle" cx="896" cy="62" r="2" fill="{t["ink"]}"/>',
            f'<circle class="twinkle t2" cx="912" cy="98" r="1.6" fill="{t["ink"]}"/>',
            f'<circle class="twinkle t3" cx="952" cy="104" r="1.8" fill="{t["ink"]}"/>',
        ]
    else:
        parts += [
            f'<circle cx="934" cy="72" r="15" fill="{t["mustard"]}"/>',
            f'<rect x="886" y="96" width="34" height="10" rx="5" fill="#ffffff" opacity=".9"/>',
            f'<rect x="896" y="90" width="18" height="10" rx="5" fill="#ffffff" opacity=".9"/>',
        ]
    parts += [
        f'<line x1="922" y1="40" x2="922" y2="124" stroke="{t["frame"]}" stroke-width="4"/>',
        f'<line x1="876" y1="82" x2="968" y2="82" stroke="{t["frame"]}" stroke-width="4"/>',
    ]
    return "\n  ".join(parts)


def laptop(t):
    c = t
    lines = [
        # (y, [(text, colour), ...])
        (178, [("const", c["terracotta"]), (" me = {", c["code"])]),
        (198, [("  loves: [", c["code"]), ('"code"', c["sage"]), (",", c["code"]),
               ('"chess"', c["sage"]), (",", c["code"]), ('"cats"', c["sage"]), ("],", c["code"])]),
        (218, [("  fuel: ", c["code"]), ('"coffee"', c["mustard"]), (",", c["code"])]),
        (238, [("};", c["code"])]),
    ]
    widths = [96, 218, 120, 16]
    out = [
        f'<rect x="608" y="146" width="256" height="140" rx="10" fill="{c["lid"]}"/>',
        f'<rect x="618" y="156" width="236" height="118" rx="4" fill="{c["screen"]}"/>',
    ]
    for i, ((y, spans), w) in enumerate(zip(lines, widths), start=1):
        tsp = "".join(f'<tspan fill="{col}">{txt.replace("&", "&amp;")}</tspan>' for txt, col in spans)
        out.append(f'<text x="630" y="{y}" font-family="{MONO}" font-size="10.5" xml:space="preserve">{tsp}</text>')
        out.append(f'<rect class="type l{i}" x="628" y="{y - 11}" width="{w}" height="15" fill="{c["screen"]}"/>')
    out.append(f'<text x="630" y="262" font-family="{MONO}" font-size="10.5" fill="{c["code_muted"]}">// TODO: feed the cat<tspan class="caret" fill="{c["terracotta"]}">▍</tspan></text>')
    out.append(f'<path d="M594 286 H878 L870 296 H602 Z" fill="{c["lid"]}"/>')
    out.append(f'<rect x="712" y="286" width="48" height="4" rx="2" fill="{c["screen"]}"/>')
    return "\n  ".join(out)


def mug(t):
    return "\n  ".join([
        f'<path class="steam" d="M898 236 q-6 -8 0 -16 q6 -8 0 -16" fill="none" stroke="{t["muted"]}" stroke-width="2.5" stroke-linecap="round"/>',
        f'<path class="steam s2" d="M910 236 q-6 -8 0 -16 q6 -8 0 -16" fill="none" stroke="{t["muted"]}" stroke-width="2.5" stroke-linecap="round"/>',
        f'<path d="M920 252 h6 a10 10 0 0 1 0 22 h-6" fill="none" stroke="{t["mug"]}" stroke-width="5"/>',
        f'<rect x="888" y="244" width="34" height="46" rx="6" fill="{t["mug"]}"/>',
        f'<rect x="888" y="256" width="34" height="6" fill="{t["ink"]}" opacity=".12"/>',
    ])


def cat(t):
    c = t
    return "\n  ".join([
        # tail (behind body)
        f'<path class="tail" d="M1094 252 C1140 254 1152 214 1132 186" fill="none" stroke="{c["cat"]}" stroke-width="11" stroke-linecap="round"/>',
        # body
        f'<ellipse cx="1060" cy="222" rx="38" ry="46" fill="{c["cat"]}"/>',
        f'<path d="M1038 206 q8 4 16 0 M1036 222 q10 5 20 0" fill="none" stroke="{c["cat_dark"]}" stroke-width="4" stroke-linecap="round"/>',
        f'<ellipse cx="1066" cy="236" rx="16" ry="22" fill="{c["belly"]}"/>',
        # head
        f'<path d="M1036 146 L1030 110 L1056 132 Z" fill="{c["cat"]}"/>',
        f'<path d="M1084 146 L1090 110 L1064 132 Z" fill="{c["cat"]}"/>',
        f'<path d="M1037 140 L1034 120 L1049 133 Z" fill="{c["terracotta"]}" opacity=".7"/>',
        f'<path d="M1083 140 L1086 120 L1071 133 Z" fill="{c["terracotta"]}" opacity=".7"/>',
        f'<circle cx="1060" cy="160" r="31" fill="{c["cat"]}"/>',
        f'<path d="M1052 133 v9 M1060 131 v10 M1068 133 v9" stroke="{c["cat_dark"]}" stroke-width="3.5" stroke-linecap="round"/>',
        f'<ellipse class="blink" cx="1049" cy="160" rx="4" ry="5.5" fill="{c["cat_eye"]}"/>',
        f'<ellipse class="blink" cx="1071" cy="160" rx="4" ry="5.5" fill="{c["cat_eye"]}"/>',
        f'<path d="M1056 170 h8 l-4 5 z" fill="{c["terracotta"]}"/>',
        f'<path d="M1060 175 q-4 5 -9 3 M1060 175 q4 5 9 3" fill="none" stroke="{c["cat_eye"]}" stroke-width="1.6" stroke-linecap="round"/>',
        f'<path d="M1040 170 h-20 M1040 175 l-18 4 M1080 170 h20 M1080 175 l18 4" stroke="{c["cat_eye"]}" stroke-width="1.3" stroke-linecap="round" opacity=".6"/>',
    ])


def paw(t):
    c = t
    return (f'<g class="paw"><ellipse cx="1034" cy="262" rx="10" ry="7" fill="{c["cat"]}"/>'
            f'<path d="M1028 262 v3 M1034 263 v3 M1040 262 v3" stroke="{c["cat_dark"]}" stroke-width="1.5" stroke-linecap="round"/></g>')


def banner(name, t):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="340" viewBox="0 0 1200 340" role="img" aria-labelledby="t d">
<title id="t">Abhishek: code, chess and cats</title>
<desc id="d">A desk scene: a laptop typing out "loves: code, chess, cats", a mug of coffee, and an orange cat knocking a knight off a chessboard.</desc>
<style>{STYLE}</style>
<defs><clipPath id="frame"><rect x="1" y="1" width="1198" height="338" rx="22"/></clipPath></defs>
<g clip-path="url(#frame)">
  <rect width="1200" height="340" fill="{t['bg']}"/>
  {window(t)}
  <rect x="590" y="300" width="16" height="44" fill="{t['desk_edge']}"/>
  <rect x="548" y="296" width="680" height="18" rx="9" fill="{t['desk']}"/>
  <rect x="548" y="309" width="680" height="5" fill="{t['desk_edge']}"/>
</g>
<rect x="1" y="1" width="1198" height="338" rx="22" fill="none" stroke="{t['line']}" stroke-width="1.5"/>

<text x="64" y="96" font-family="{MONO}" font-size="16" fill="{t['muted']}">&gt; hello, world. i'm<tspan class="caret" fill="{t['terracotta']}"> ▍</tspan></text>
<text x="60" y="172" font-family="{SANS}" font-size="76" font-weight="800" letter-spacing="-2" fill="{t['ink']}">Abhishek<tspan fill="{t['terracotta']}">.</tspan></text>
<path d="M66 190 q40 -10 80 0 t80 0 t80 0" fill="none" stroke="{t['sage']}" stroke-width="5" stroke-linecap="round"/>
<text x="64" y="232" font-family="{SANS}" font-size="22" fill="{t['ink']}">I design &amp; build websites that feel <tspan font-style="italic" fill="{t['terracotta']}">crafted</tspan>.</text>
<text x="64" y="270" font-family="{MONO}" font-size="15" fill="{t['muted']}">CSE student  ·  India  ·  web dev + AIML</text>
<text x="64" y="300" font-family="{SANS}" font-size="15" font-style="italic" fill="{t['muted']}">powered by code, chess &amp; one very opinionated cat</text>

<g>
  <g transform="translate(-24 0)">
  {laptop(t)}
  {mug(t)}
  </g>
  {cat(t)}
  {board(t)}
  {paw(t)}
  <g font-family="{SYMBOL}">
    <text x="1078" y="284" font-size="24" fill="#1d1d1d" stroke="#1d1d1d" stroke-width=".4" text-anchor="middle">♛</text>
    <text x="1040" y="288" font-size="20" fill="#ffffff" stroke="#1d1d1d" stroke-width=".6" text-anchor="middle">♙</text>
    <text x="966" y="288" font-size="22" fill="#ffffff" stroke="#1d1d1d" stroke-width=".6" text-anchor="middle">♔</text>
    <text class="knight" x="1008" y="286" font-size="24" fill="#1d1d1d" stroke="#1d1d1d" stroke-width=".4" text-anchor="middle">♞</text>
  </g>
  <text class="oops" x="986" y="238" font-family="{SANS}" font-size="20" font-weight="800" fill="{t['terracotta']}">!</text>
</g>
</svg>
"""
    (OUT / name).write_text(svg)


if __name__ == "__main__":
    banner("banner-light.svg", THEMES["light"])
    banner("banner-dark.svg", THEMES["dark"])
    print("wrote", OUT / "banner-light.svg", OUT / "banner-dark.svg")
