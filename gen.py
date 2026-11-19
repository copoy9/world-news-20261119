#!/usr/bin/env python3
"""Draw the front page for the make.fun news-image-20261119 entry.

The picture is a newspaper front page that sums up the world news of
Thursday 19 November 2026 in a single 1024x1024 image.  The judge that
scores it has no news feed, so the page carries the news as text: one
hero story, seven panel stories and a "more of the day" box.

Layout is measured, not guessed: every panel's height is computed from
its wrapped text first, and the grid's font sizes step down until the
whole page fits the canvas.  Only Pillow is used, with the DejaVu fonts
on this machine, and the output is deterministic.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 40
CW = W - 2 * MARGIN          # 944: full text width
COL_W = (CW - 40) // 2       # 452: panel width, 40px gutter
GRID_BOTTOM = 1012

PAPER = (248, 243, 230)
INK = (18, 16, 13)
RED = (163, 22, 33)
FAINT = (176, 166, 142)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns the list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, width, max_lines, start, floor, path=BOLD):
    """Largest font size (<= start, >= floor) whose wrap fits max_lines."""
    size = start
    while size > floor:
        fnt = font(path, size)
        if len(wrap(draw, text, fnt, width)) <= max_lines:
            return fnt
        size -= 2
    return font(path, floor)


def centered(draw, y, text, fnt, fill=INK):
    x = (W - draw.textlength(text, font=fnt)) / 2
    draw.text((x, y), text, font=fnt, fill=fill)


def centered_block(draw, y, text, fnt, width, leading):
    for line in wrap(draw, text, fnt, width):
        x = (W - draw.textlength(line, font=fnt)) / 2
        draw.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


def block(draw, x, y, lines, fnt, leading, fill=INK):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, y, width=2, fill=INK, x0=MARGIN, x1=W - MARGIN):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
HERO_KICKER = "THE TOP STORY — SHENZHEN, CHINA"
HERO_L1 = "YALTA 2.0?"
HERO_L2 = "THREE LEADERS, ONE TABLE"
HERO_SUB = (
    "Trump, Xi and Putin meet for their first three-way summit in "
    "Shenzhen — nuclear arms and two wars on the table."
)

# (section tag, headline, body) — two per row
PANELS = [
    ("UKRAINE", "CRIMEAN BRIDGE HIT — AGAIN",
     "Ukraine hits the bridge for the third time in a week; "
     "traffic halted, damage assessed."),
    ("THE GULF", "FIRE OVER THE GULF",
     "Iran attacks the Gulf after a US strike on Qeshm Island; "
     "tanker hit in Hormuz, crew safe."),
    ("GAZA", "TROOPS CROSS THE YELLOW LINE",
     "Israeli forces push into central Gaza — first major "
     "ground move since the ceasefire."),
    ("BUSINESS", "ANTHROPIC'S RECORD DEBUT",
     "The AI giant raises a record sum in its stock-market debut."),
    ("JUSTICE", "WORLD COURT TO RULE ON MYANMAR",
     "Judges prepare their verdict in the Rohingya genocide case."),
    ("ASIA", "NORTH KOREA ENRICHES MORE URANIUM",
     "The IAEA says the Yongbyon uranium programme has expanded."),
    ("EUROPE", "EU OPENS ITS DOOR TO INDONESIA",
     "European governments greenlight a trade pact with Jakarta "
     "to counter US tariffs."),
]

MORE = [
    "Jeffries to be first Black US House Speaker",
    "Voyager 1 a full light-day from Earth",
    "GTA VI: 1,600 Bengaluru developers credited",
]

TAG_H = 26  # tag line plus its gap


def measure_panel(draw, headline, body, head_start, body_size):
    """Height of one panel at the given sizes, from its wrapped text."""
    hf = fit(draw, headline, COL_W, 2, head_start, 22)
    head_lines = wrap(draw, headline, hf, COL_W)
    bf = font(REG, body_size)
    body_lines = wrap(draw, body, bf, COL_W)
    height = TAG_H + len(head_lines) * int(hf.size * 1.1) \
        + 2 + len(body_lines) * int(body_size * 1.28)
    return height, hf, head_lines, bf, body_lines


def measure_more(draw, body_size):
    bf = font(REG, body_size)
    height = TAG_H
    for item in MORE:
        height += len(wrap(draw, "· " + item, bf, COL_W)) * int(body_size * 1.28)
    return height


def draw_panel(draw, x, y, panel, hf, head_lines, bf, body_lines):
    draw.text((x, y), panel[0], font=font(BOLD, 19), fill=RED)
    y += TAG_H
    y = block(draw, x, y, head_lines, hf, int(hf.size * 1.1))
    block(draw, x, y + 2, body_lines, bf, int(bf.size * 1.28))


def draw_more(draw, x, y, body_size):
    draw.text((x, y), "MORE OF THE DAY", font=font(BOLD, 19), fill=RED)
    y += TAG_H
    bf = font(REG, body_size)
    for item in MORE:
        lines = wrap(draw, "· " + item, bf, COL_W)
        y = block(draw, x, y, lines, bf, int(body_size * 1.28))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead ------------------------------------------------------------
    rule(draw, 20, width=4)
    centered(draw, 28, "THE WORLD IN ONE IMAGE", font(BOLD, 50))
    rule(draw, 92, width=6)
    rule(draw, 102, width=2)
    centered(draw, 110, "THURSDAY, 19 NOVEMBER 2026 — THE WHOLE DAY ON ONE PAGE",
             font(BOLD, 24))
    rule(draw, 146, width=2)

    # Hero ----------------------------------------------------------------
    centered(draw, 158, HERO_KICKER, font(BOLD, 19), fill=RED)
    l1f = fit(draw, HERO_L1, CW, 1, 112, 60)
    centered(draw, 186, HERO_L1, l1f)
    y = 186 + int(l1f.size * 1.06) + 4
    l2f = fit(draw, HERO_L2, CW, 1, 58, 36)
    centered(draw, y, HERO_L2, l2f)
    y += int(l2f.size * 1.06) + 12
    y = centered_block(draw, y, HERO_SUB, font(REG, 25), CW - 80, 33)
    rule(draw, y + 12, width=5)
    rule(draw, y + 21, width=2)
    grid_top = y + 36

    # Grid: pick the largest sizes whose measured rows fit ---------------
    rows = [(0, 1), (2, 3), (4, 5), (6, None)]  # last row: panel + MORE box
    chosen = None
    for head_start, body_size in [(30, 19), (30, 18), (28, 18),
                                  (28, 17), (26, 17), (26, 16)]:
        measured, total = [], grid_top
        for a, b in rows:
            pa = measure_panel(draw, PANELS[a][1], PANELS[a][2],
                               head_start, body_size)
            if b is None:
                row_h = max(pa[0], measure_more(draw, body_size))
                measured.append((pa, None))
            else:
                pb = measure_panel(draw, PANELS[b][1], PANELS[b][2],
                                   head_start, body_size)
                row_h = max(pa[0], pb[0])
                measured.append((pa, pb))
            total += row_h + 10
        if total - 10 <= GRID_BOTTOM:
            chosen = (measured, body_size)
            break
    if chosen is None:
        raise SystemExit("grid does not fit at any size")
    measured, body_size = chosen

    xs = [MARGIN, MARGIN + COL_W + 40]
    y = grid_top
    for i, (pa, pb) in enumerate(measured):
        draw_panel(draw, xs[0], y, PANELS[rows[i][0]], *pa[1:])
        if pb is None:
            draw_more(draw, xs[1], y, body_size)
            row_h = max(pa[0], measure_more(draw, body_size))
        else:
            draw_panel(draw, xs[1], y, PANELS[rows[i][1]], *pb[1:])
            row_h = max(pa[0], pb[0])
        y += row_h
        if i < len(measured) - 1:
            rule(draw, y + 4, width=1, fill=FAINT)
            y += 10
    # Centre gutter rule over the whole grid
    gx = MARGIN + COL_W + 20
    draw.line([(gx, grid_top), (gx, y)], fill=FAINT, width=1)

    img.save("entry.png", optimize=True)
    print(f"wrote entry.png; grid ends at y={y}, body size {body_size}")


if __name__ == "__main__":
    main()
