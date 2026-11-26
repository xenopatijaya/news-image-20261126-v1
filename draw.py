#!/usr/bin/env python3
"""Build the 26 November 2026 one-day world news front page (1024x1024 PNG).

Draws everything with Pillow primitives: masthead, big-number strip, six
illustrated lead stories, numbered regional briefs, a schematic pin map, a
UTC timeline and a DATE CHECK box naming the Wednesday stories left out.
Every story below happened, or was first reported, on Thursday 26 Nov 2026.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (27, 42, 74)
NAVY = (23, 36, 66)
RED = (179, 39, 30)
GOLD = (200, 155, 60)
GOLD_LT = (232, 196, 110)
TEAL = (31, 111, 104)
CREAM = (255, 251, 238)
GREY = (94, 98, 110)
LINE = (27, 42, 74)
SOFT = (226, 219, 199)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading):
    """Draw wrapped text; returns y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


LEADS = [
    {
        "kicker": "NEW YORK  •  THANKSGIVING",
        "head": "100th Macy's parade",
        "body": "A record 100 balloons float over New York for the parade's 100th year as 3M watch; 81.5M Americans travel for the holiday. US markets shut.",
        "icon": "balloon",
        "accent": RED,
    },
    {
        "kicker": "GAZA  •  MIDDLE EAST",
        "head": "Truce 'near collapse'",
        "body": "A Board of Peace report to the UN warns the 13-month Gaza ceasefire faces imminent collapse, faulting both Israel and Hamas for broken promises.",
        "icon": "olive",
        "accent": TEAL,
    },
    {
        "kicker": "GENEVA  •  WORLD CHESS",
        "head": "Game 3: 1–1",
        "body": "Sindarov, with White, meets champion Gukesh in Game 3 of the world title match at 15:00 CET, after Game 2's 20-move draw.",
        "icon": "chess",
        "accent": INK,
    },
    {
        "kicker": "TAIPEI  •  TRADE",
        "head": "US offers 15% tariff",
        "body": "Taipei says Washington has proposed a 15% tariff — the lowest tier, and not stacked on top of existing duties — at a briefing at 08:30 local.",
        "icon": "tariff",
        "accent": GOLD,
    },
    {
        "kicker": "SEOUL  •  RATES",
        "head": "Korea rate call",
        "body": "The Bank of Korea sets its last rate of 2026 today; 32 of 34 economists expect a rise to 3.25%, a third hike in a chip-boom year.",
        "icon": "bank",
        "accent": NAVY,
    },
    {
        "kicker": "BRUSSELS  •  EUROPE",
        "head": "EU summit opens",
        "body": "EU leaders meet for two days on Ukraine's 2027 funding and the 2028–34 budget; the ECB publishes October minutes as the euro nears a 19-month low.",
        "icon": "stars",
        "accent": (46, 78, 150),
    },
]

BRIEFS = [
    ("NORTH AMERICA", [
        ("7", "NFL tripleheader: Bears–Lions 1pm ET, Eagles–Cowboys 4:30pm, Chiefs–Bills 8:20pm."),
        ("8", "AAA: 81.5M travel for Thanksgiving — 72.9M by car, 5.96M by air."),
        ("9", "US markets closed for Thanksgiving; thin trading, early close on Friday."),
    ]),
    ("EUROPE", [
        ("10", "ECB publishes its 28–29 Oct meeting account at 12:30 GMT; rates unchanged."),
        ("11", "Bank of England releases its Financial Stability Report at 10:30 GMT."),
        ("12", "Germany's GfK consumer confidence for December is released."),
        ("13", "Eurozone October M3 money supply due today."),
        ("14", "German and Romanian foreign ministers speak to journalists in Berlin at 12:00 GMT."),
    ]),
    ("ASIA-PACIFIC", [
        ("15", "Taiwan's third-quarter GDP figures due."),
        ("16", "BOJ hawk Tamura speaks in Yamanashi; a December hike to 1.5% is now the base case."),
        ("17", "Asia shares steady after Wednesday's rout: Hang Seng +0.9% seen, Nikkei +0.4%."),
        ("18", "India marks Constitution Day — Samvidhan Divas — on 26 November."),
        ("19", "China's October industrial profits (year to date) due."),
        ("20", "Philippines' October trade balance and Singapore's October bank lending due."),
        ("21", "Mumbai marks 18 years since the 26/11 attacks that killed 166; NSG holds a remembrance at the Gateway of India."),
    ]),
    ("AFRICA", [
        ("22", "Ramaphosa keynotes the MSME and Cooperatives Breakfast in Sandton at 09:00."),
        ("23", "Tshwane holds its first council meeting after the local elections."),
        ("24", "Stats SA releases October's producer price index."),
        ("25", "Parliament's Phala Phala committee meets on its draft terms of reference."),
        ("26", "Deputy President Mashatile answers questions in the National Council of Provinces."),
    ]),
    ("WORLD", [
        ("27", "The UN marks World Sustainable Transport Day."),
    ]),
]

NUMBERS = [
    ("100", "balloons in the\n100th Macy's parade"),
    ("81.5M", "Americans travelling\nfor Thanksgiving"),
    ("3M", "spectators lining\nthe parade route"),
    ("15%", "US tariff offered\nto Taiwan"),
    ("3.25%", "Bank of Korea rate\nexpected today"),
    ("1–1", "chess title match\nafter Game 2"),
]

TIMELINE = [
    ("00:30", "Taipei"),
    ("01:00", "BOK"),
    ("07:00", "Ramaphosa"),
    ("10:30", "BoE"),
    ("12:30", "ECB"),
    ("13:30", "Macy's"),
    ("14:00", "Chess"),
    ("18:00", "NFL"),
]

PINS = [
    # (name, x fraction, y fraction, lead number or None, label dx, dy, anchor)
    ("New York", 0.20, 0.42, "1", 10, -6, "la"),
    ("Geneva", 0.50, 0.34, "3", 10, 4, "la"),
    ("Gaza", 0.545, 0.52, "2", 10, -6, "la"),
    ("Taipei", 0.84, 0.50, "4", 10, -6, "la"),
    ("Seoul", 0.83, 0.34, "5", 10, -6, "la"),
    ("Brussels", 0.455, 0.20, "6", 10, -6, "la"),
    ("Joburg", 0.55, 0.82, None, 10, -6, "la"),
    ("New Delhi", 0.70, 0.52, None, 10, -6, "la"),
]

DATE_CHECK = (
    "NOT 26 NOV — left out: US Section 301 tariff plan (Wed) · "
    "Asia chip rout (Wed) · Houthi Ras Tanura attack (Wed) · Hera "
    "Dimorphos photos (Wed) · N. Korea shuts Swiss office (Wed) · "
    "Shenzhou-24 launch (Wed) · Canary record arrivals (Wed) · "
    "Bogor mine deaths (Wed) · Russia death-toll leak (Wed)."
)


def draw_icon(draw, kind, box, accent):
    """Small pictogram drawn with primitives inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w, h = x1 - x0, y1 - y0
    if kind == "balloon":
        draw.ellipse([cx - 26, y0 + 2, cx + 26, y0 + 52], fill=accent)
        draw.ellipse([cx - 26, y0 + 2, cx + 26, y0 + 52], outline=INK, width=2)
        draw.polygon([(cx - 8, y0 + 50), (cx + 8, y0 + 50), (cx, y0 + 60)], fill=accent)
        draw.line([(cx, y0 + 60), (cx - 6, y1 - 4), (cx + 6, y1 - 8), (cx, y1 - 2)],
                  fill=INK, width=2)
        draw.line([(x0 + 4, y1 - 2), (x1 - 4, y1 - 2)], fill=GREY, width=2)
    elif kind == "olive":
        draw.ellipse([x0 + 4, y0 + 4, x1 - 4, y1 - 4], outline=accent, width=3)
        for i, (lx, ly, ang) in enumerate([(0.42, 0.30, -35), (0.60, 0.28, 35),
                                           (0.38, 0.52, -30), (0.64, 0.50, 30),
                                           (0.50, 0.68, 0)]):
            ex, ey = x0 + lx * w, y0 + ly * h
            draw.ellipse([ex - 13, ey - 6, ex + 13, ey + 6], fill=accent)
        draw.line([(cx - 16, y1 - 16), (cx + 16, y0 + 18)], fill=accent, width=3)
    elif kind == "chess":
        s = 15
        bx, by = cx - 2 * s, cy - 2 * s
        for r in range(4):
            for c in range(4):
                col = INK if (r + c) % 2 == 0 else CREAM
                draw.rectangle([bx + c * s, by + r * s, bx + (c + 1) * s,
                                by + (r + 1) * s], fill=col)
        draw.rectangle([bx, by, bx + 4 * s, by + 4 * s], outline=INK, width=2)
        draw.ellipse([bx + 1.1 * s, by + 0.6 * s, bx + 2.1 * s, by + 1.6 * s],
                     fill=RED, outline=INK, width=1)
        draw.rectangle([bx + 1.0 * s, by + 1.6 * s, bx + 2.2 * s, by + 2.0 * s],
                       fill=RED, outline=INK, width=1)
        draw.ellipse([bx + 2.4 * s, by + 2.5 * s, bx + 3.4 * s, by + 3.5 * s],
                     fill=GOLD, outline=INK, width=1)
    elif kind == "tariff":
        draw.rounded_rectangle([x0 + 6, y0 + 14, x1 - 6, y1 - 14], radius=8,
                               fill=CREAM, outline=accent, width=3)
        draw.text((cx, cy - 4), "%", font=font(SANS_B, 34), fill=accent,
                  anchor="mm")
        draw.line([(x0 + 14, y1 - 6), (x1 - 14, y1 - 6)], fill=accent, width=3)
    elif kind == "bank":
        draw.polygon([(cx - 30, y0 + 18), (cx + 30, y0 + 18), (cx, y0 + 2)],
                     fill=accent)
        draw.rectangle([x0 + 6, y0 + 18, x1 - 6, y0 + 24], fill=accent)
        for i in range(4):
            px = x0 + 12 + i * 14
            draw.rectangle([px, y0 + 26, px + 7, y1 - 14], fill=accent)
        draw.rectangle([x0 + 6, y1 - 14, x1 - 6, y1 - 8], fill=accent)
    elif kind == "stars":
        draw.ellipse([x0 + 4, y0 + 4, x1 - 4, y1 - 4], fill=(46, 78, 150))
        for i in range(12):
            ang = -math.pi / 2 + i * math.pi / 6
            sx, sy = cx + 24 * math.cos(ang), cy + 24 * math.sin(ang)
            star(draw, sx, sy, 5, GOLD_LT)


def masthead(draw):
    draw.rectangle([0, 0, W, 112], fill=NAVY)
    draw.rectangle([0, 112, W, 116], fill=GOLD)
    draw.text((28, 16), "THE WORLD IN ONE DAY",
              font=font(SERIF, 40), fill=CREAM)
    draw.text((28, 66), "Thursday 26 November 2026  •  27 stories  •  6 regions",
              font=font(SANS, 17), fill=GOLD_LT)
    draw.rounded_rectangle([W - 268, 18, W - 28, 92], radius=6, fill=RED)
    draw.text((W - 148, 38), "26 NOV", font=font(SERIF, 30), fill=CREAM,
              anchor="mm")
    draw.text((W - 148, 70), "2026", font=font(SANS_B, 16), fill=CREAM,
              anchor="mm")


def numbers_strip(draw):
    y0, y1 = 124, 180
    draw.rectangle([0, y0, W, y1], fill=CREAM)
    draw.line([(0, y1), (W, y1)], fill=LINE, width=2)
    cw = W / 6
    for i, (num, label) in enumerate(NUMBERS):
        x = i * cw
        if i:
            draw.line([(x, y0 + 8), (x, y1 - 8)], fill=SOFT, width=2)
        draw.text((x + cw / 2, y0 + 4), num, font=font(SERIF, 22),
                  fill=RED, anchor="ma")
        for j, ln in enumerate(label.split("\n")):
            draw.text((x + cw / 2, y0 + 30 + j * 12), ln,
                      font=font(SANS, 11), fill=GREY, anchor="ma")


def leads(draw):
    y0 = 182
    cell_w, cell_h = 322, 146
    gap = 9
    x0 = 28
    for idx, lead in enumerate(LEADS):
        row, col = divmod(idx, 3)
        x = x0 + col * (cell_w + gap)
        y = y0 + row * (cell_h + gap)
        draw.rounded_rectangle([x, y, x + cell_w, y + cell_h], radius=8,
                               fill=(255, 255, 255), outline=LINE, width=2)
        draw.rounded_rectangle([x, y, x + cell_w, y + 26], radius=8,
                               fill=lead["accent"])
        draw.rectangle([x, y + 18, x + cell_w, y + 26], fill=lead["accent"])
        draw.text((x + 10, y + 5), lead["kicker"], font=font(SANS_B, 11),
                  fill=(255, 255, 255))
        draw.text((x + cell_w - 12, y + 2), str(idx + 1),
                  font=font(SERIF, 22), fill=(255, 255, 255), anchor="ra")
        draw_icon(draw, lead["icon"], (x + 12, y + 34, x + 92, y + 100),
                  lead["accent"])
        draw.text((x + 100, y + 32), lead["head"], font=font(SERIF, 19),
                  fill=INK)
        body_lines = wrap(draw, lead["body"], font(SANS, 13), cell_w - 112)
        for i, ln in enumerate(body_lines[:3]):
            draw.text((x + 100, y + 58 + i * 16), ln, font=font(SANS, 13),
                      fill=INK)
        if len(body_lines) > 3:
            rest = " ".join(body_lines[3:])
            text_block(draw, (x + 12, y + 106), rest, font(SANS, 13), INK,
                       cell_w - 24, 16)


def briefs(draw):
    y = 492
    draw.text((28, y), "THE REST OF THE DAY", font=font(SERIF, 20), fill=INK)
    draw.text((W - 28, y + 4), "numbered 7–27", font=font(SANS, 12),
              fill=GREY, anchor="ra")
    draw.line([(28, y + 28), (W - 28, y + 28)], fill=LINE, width=2)
    col_w = 313
    xs = [28, 355, 682]

    def column(draw, groups, x, y):
        for region, items in groups:
            draw.text((x, y), region, font=font(SANS_B, 13), fill=RED)
            y += 20
            for num, txt in items:
                draw.text((x, y), num, font=font(SANS_B, 12), fill=INK)
                y = text_block(draw, (x + 28, y), txt, font(SANS, 12), INK,
                               col_w - 28, 14)
                y += 4
            y += 4
        return y

    ends = [
        column(draw, BRIEFS[0:2], xs[0], y + 38),
        column(draw, BRIEFS[2:3], xs[1], y + 38),
        column(draw, BRIEFS[3:5], xs[2], y + 38),
    ]
    return max(ends)


def world_map(draw, x0, y0, x1, y1):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=(214, 230, 240),
                           outline=LINE, width=2)
    draw.text((x0 + 10, y0 + 6), "WHERE IT HAPPENED", font=font(SANS_B, 12),
              fill=INK)
    mw, mh = x1 - x0, y1 - y0
    # rough continent blobs (schematic, not to scale)
    blobs = [
        [(0.06, 0.30), (0.10, 0.22), (0.18, 0.20), (0.24, 0.26), (0.22, 0.38),
         (0.16, 0.48), (0.10, 0.44)],  # N America
        [(0.26, 0.52), (0.30, 0.48), (0.34, 0.52), (0.33, 0.62), (0.28, 0.64)],
        [(0.44, 0.20), (0.48, 0.14), (0.55, 0.16), (0.56, 0.26), (0.50, 0.30),
         (0.45, 0.28)],  # Europe
        [(0.52, 0.42), (0.56, 0.38), (0.60, 0.44), (0.58, 0.58), (0.54, 0.60),
         (0.51, 0.50)],  # Africa
        [(0.60, 0.22), (0.68, 0.16), (0.82, 0.18), (0.88, 0.30), (0.84, 0.44),
         (0.74, 0.48), (0.66, 0.40), (0.60, 0.32)],  # Asia
        [(0.84, 0.62), (0.88, 0.58), (0.92, 0.62), (0.90, 0.68), (0.85, 0.68)],
    ]
    for blob in blobs:
        pts = [(x0 + fx * mw, y0 + 24 + fy * (mh - 30)) for fx, fy in blob]
        draw.polygon(pts, fill=(250, 246, 232), outline=GREY)
    for name, fx, fy, num, dx, dy, anch in PINS:
        px, py = x0 + fx * mw, y0 + 24 + fy * (mh - 30)
        if num:
            draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                         outline=(255, 255, 255), width=2)
            draw.text((px, py), num, font=font(SANS_B, 9), fill=(255, 255, 255),
                      anchor="mm")
        else:
            draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=INK,
                         outline=(255, 255, 255), width=1)
        draw.text((px + dx, py + dy), name, font=font(SANS, 9), fill=INK,
                  anchor=anch)


def timeline(draw, y0, y1):
    draw.rectangle([0, y0, W, y1], fill=NAVY)
    draw.text((28, y0 + 5), "THE DAY IN UTC", font=font(SANS_B, 12),
              fill=GOLD_LT)
    x0, x1 = 28, W - 28
    line_y = y0 + 30
    draw.line([(x0, line_y), (x1, line_y)], fill=GOLD_LT, width=2)
    n = len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        fx = i / (n - 1)
        x = x0 + fx * (x1 - x0)
        draw.ellipse([x - 5, line_y - 5, x + 5, line_y + 5], fill=RED,
                     outline=(255, 255, 255), width=1)
        draw.text((min(max(x, 82), W - 82), y0 + 40), t + "  " + label,
                  font=font(SANS, 10), fill=CREAM, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    numbers_strip(draw)
    leads(draw)
    bottom = briefs(draw)
    # bottom row: map left, date check right
    map_y0 = bottom + 6
    map_y1 = 930
    world_map(draw, 28, map_y0, 470, map_y1)
    draw.rounded_rectangle([482, map_y0, W - 28, map_y1], radius=8,
                           fill=(255, 251, 238), outline=RED, width=2)
    draw.text((496, map_y0 + 8), "DATE CHECK — WHAT IS NOT TODAY'S NEWS",
              font=font(SANS_B, 12), fill=RED)
    end_y = text_block(draw, (496, map_y0 + 30), DATE_CHECK, font(SANS, 10),
                       INK, W - 28 - 496 - 14, 13)
    timeline(draw, 938, 998)
    draw.text((28, 1004), "All events happened or were first reported on Thursday 26 November 2026. "
              "Sources: Reuters, AP, BBC, FIDE, ECB, Bank of Korea, Al Jazeera.",
              font=font(SANS, 10), fill=GREY)
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
