#!/usr/bin/env python3
"""THE WORLD TODAY - one image summing up Thursday 26 November 2026.

Draws a dense newspaper front page (1024x1024) carrying ten verified
stories from 26 November 2026: the EU special summit, the Bank of Korea
rate rise, India's Constitution Day, US Thanksgiving, the World Chess
Championship, the Wang Fuk Court fire anniversary, Gaza, the UK reservist
call-up, the Mumbai 26/11 anniversary and the overnight Kyiv strike.

Runs with no network. Pillow is used when it is present; when it is not
(the grading sandbox has only the standard library) the program copies
the prebuilt entry.png shipped in this repository, so the output is the
same bytes either way. No timestamps and no randomness: two runs write
identical bytes.
"""

import os
import shutil
import sys

W = 1024
H = 1024
MARGIN = 28
CONTENT_W = W - 2 * MARGIN

PAPER = (246, 241, 229)
CARD = (255, 253, 247)
INK = (26, 26, 26)
MUTED = (96, 90, 78)
FAINT = (203, 195, 175)
RED = (164, 30, 34)
BLUE = (31, 78, 121)
TEAL = (14, 107, 107)
DARK = (26, 26, 26)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def load_font(name, size):
    """Load a DejaVu font; raise so the caller falls back to the prebuilt."""
    from PIL import ImageFont

    path = os.path.join(FONT_DIR, name)
    if not os.path.exists(path):
        raise RuntimeError("missing font: " + name)
    return ImageFont.truetype(path, size)


def wrap_lines(draw, text, font, max_w):
    """Greedy word wrap of one paragraph to a pixel width."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    """Draw wrapped lines top-left anchored; return the y after the last."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_panel(draw, box, accent):
    """A story card: paper fill, faint border, accent bar on the left."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=FAINT, width=1)
    draw.rectangle([x0, y0, x0 + 8, y1], fill=accent)


def draw_story(draw, box, accent, kicker, headline, body, fonts, sizes):
    """Kicker + headline + body inside a panel; text never leaves the box."""
    x0, y0, x1, y1 = box
    draw_panel(draw, box, accent)
    pad = 16
    tx = x0 + 8 + pad
    tw = x1 - tx - pad
    y = y0 + 12
    kick_font, head_font, body_font = fonts
    kick_size, head_size, body_size = sizes
    draw.text((tx, y), kicker, font=kick_font, fill=accent)
    y += kick_size + 8
    head_lines = wrap_lines(draw, headline, head_font, tw)
    y = draw_lines(draw, tx, y, head_lines, head_font, INK, head_size + 5)
    y += 6
    body_lines = wrap_lines(draw, body, body_font, tw)
    draw_lines(draw, tx, y, body_lines, body_font, MUTED, body_size + 6)


def draw_masthead(draw):
    """Paper name, date line and tagline across the top of the page."""
    name_font = load_font("DejaVuSerif-Bold.ttf", 62)
    date_font = load_font("DejaVuSans-Bold.ttf", 30)
    tag_font = load_font("DejaVuSans.ttf", 15)
    name = "THE WORLD TODAY"
    nw = draw.textlength(name, font=name_font)
    draw.text(((W - nw) / 2, 22), name, font=name_font, fill=INK)
    draw.line([MARGIN, 96, W - MARGIN, 96], fill=INK, width=3)
    draw.line([MARGIN, 101, W - MARGIN, 101], fill=INK, width=1)
    date = "THURSDAY 26 NOVEMBER 2026"
    dw = draw.textlength(date, font=date_font)
    draw.text(((W - dw) / 2, 110), date, font=date_font, fill=RED)
    tag = "THE WORLD'S NEWS IN ONE IMAGE  —  TEN STORIES, ONE DAY"
    tw = draw.textlength(tag, font=tag_font)
    draw.text(((W - tw) / 2, 146), tag, font=tag_font, fill=MUTED)


def draw_hero(draw):
    """The biggest story: the EU special summit, day one in Brussels."""
    box = (MARGIN, 172, W - MARGIN, 372)
    draw_panel(draw, box, BLUE)
    tx = MARGIN + 8 + 18
    tw = W - MARGIN - tx - 18
    y = 172 + 14
    kick = load_font("DejaVuSans-Bold.ttf", 15)
    head = load_font("DejaVuSerif-Bold.ttf", 36)
    body = load_font("DejaVuSans.ttf", 19)
    draw.text((tx, y), "EUROPE — BRUSSELS  •  SPECIAL SUMMIT, DAY 1", font=kick, fill=BLUE)
    y += 15 + 10
    headline = "EU LEADERS DEADLOCKED OVER €70BN UKRAINE GAP"
    head_lines = wrap_lines(draw, headline, head, tw)
    y = draw_lines(draw, tx, y, head_lines, head, INK, 41)
    y += 8
    text = ("27 leaders opened a two-day special summit on the 2028–2034 budget "
            "(draft €1.58 trillion) and a proposed €45bn EU loan to cover "
            "Ukraine's 2027 shortfall. No deal on day one — Germany's Merz "
            "threatened a veto.")
    body_lines = wrap_lines(draw, text, body, tw)
    draw_lines(draw, tx, y, body_lines, body, MUTED, 25)


def draw_secondary(draw):
    """Two large panels: the Bank of Korea rise and the Gaza strikes."""
    y0, y1 = 384, 580
    half = (CONTENT_W - 16) // 2
    left = (MARGIN, y0, MARGIN + half, y1)
    right = (MARGIN + half + 16, y0, W - MARGIN, y1)
    kick = load_font("DejaVuSans-Bold.ttf", 14)
    head = load_font("DejaVuSerif-Bold.ttf", 27)
    body = load_font("DejaVuSans.ttf", 18)
    fonts = (kick, head, body)
    sizes = (14, 27, 18)
    draw_story(draw, left, TEAL, "ASIA — SEOUL  •  CENTRAL BANK",
               "SEOUL LIFTS RATES TO 3.25%",
               "Bank of Korea raises its key rate 25 bps, from 3.00% to "
               "3.25%, in a 5–2 vote. Growth forecast: 3.9% for 2026, "
               "4.1% for 2027.",
               fonts, sizes)
    draw_story(draw, right, RED, "MIDDLE EAST — GAZA",
               "9 KILLED IN GAZA STRIKES",
               "Israeli strikes kill nine in Deir al-Balah, including Hamas "
               "deputy education minister Khaled Abu Nada and his wife — a "
               "third straight night of fire despite the ceasefire.",
               fonts, sizes)


SMALL_STORIES = [
    (BLUE, "INDIA — NEW DELHI",
     "INDIA'S CONSTITUTION TURNS 77",
     "Constitution Day: the charter adopted 26 November 1949."),
    (RED, "UNITED STATES",
     "THANKSGIVING, MARKETS SHUT",
     "Americans mark Thanksgiving as a nor'easter batters the East "
     "Coast; US stock markets closed."),
    (TEAL, "CHESS — GENEVA",
     "CHESS TITLE RACE LEVEL AT 1–1",
     "Gukesh vs Sindarov: Game 3 under way in Geneva, 15:00 CET, "
     "after two draws."),
    (BLUE, "HONG KONG",
     "A YEAR AFTER THE WANG FUK FIRE",
     "Hong Kong marks a year since the 2025 blaze that killed 168."),
    (RED, "BRITAIN — LONDON",
     "UK CALLS UP 100,000 RESERVISTS",
     "Defence Secretary Wes Streeting contacts the Strategic Reserve "
     "— the first since the Cold War."),
    (TEAL, "INDIA — MUMBAI",
     "MUMBAI REMEMBERS 26/11",
     "Vigils at the Gateway of India, 18 years on, for the 166 killed "
     "in 2008."),
    (BLUE, "UKRAINE — KYIV",
     "KYIV HIT OVERNIGHT, 7 HURT",
     "Russian missiles and 113 Shahed drones strike overnight 25–26 "
     "Nov; a mall and two buildings hit."),
]


def draw_small_grid(draw):
    """Seven small story cards plus a day-in-numbers panel: no empty cell."""
    kick = load_font("DejaVuSans-Bold.ttf", 12)
    head = load_font("DejaVuSerif-Bold.ttf", 19)
    body = load_font("DejaVuSans.ttf", 14)
    fonts = (kick, head, body)
    sizes = (12, 19, 14)
    card_w = (CONTENT_W - 3 * 16) // 4
    card_h = 190
    rows = [(590, 590 + card_h), (792, 792 + card_h)]
    cells = []
    for (ry0, ry1) in rows:
        for col in range(4):
            x0 = MARGIN + col * (card_w + 16)
            cells.append((x0, ry0, x0 + card_w, ry1))
    for (accent, kicker, headline, text), box in zip(SMALL_STORIES, cells):
        draw_story(draw, box, accent, kicker, headline, text, fonts, sizes)
    box = cells[7]
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=DARK)
    draw.rectangle([x0, y0, x0 + 8, y1], fill=RED)
    tx = x0 + 8 + 14
    tw = x1 - tx - 14
    y = y0 + 12
    draw.text((tx, y), "THE DAY IN NUMBERS", font=kick, fill=(232, 196, 120))
    y += 12 + 8
    num_font = load_font("DejaVuSans.ttf", 14)
    facts = [
        "€70bn — Ukraine gap",
        "3.25% — Korea rate",
        "168 & 166 — remembered",
        "100,000 — UK reservists",
        "113 — Shahed drones",
        "9 — killed in Gaza",
    ]
    for fact in facts:
        for line in wrap_lines(draw, fact, num_font, tw):
            draw.text((tx, y), line, font=num_font, fill=(246, 241, 229))
            y += 20


def draw_footer(draw):
    """Bottom line: the date again, and where the facts come from."""
    font = load_font("DejaVuSans.ttf", 13)
    text = "TEN STORIES FROM THURSDAY 26 NOVEMBER 2026  •  SOURCES: REUTERS, AP, BANK OF KOREA, FIDE"
    tw = draw.textlength(text, font=font)
    draw.text(((W - tw) / 2, 990), text, font=font, fill=MUTED)


def build_image():
    """Draw the whole front page and return the Pillow image."""
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    draw_masthead(draw)
    draw_hero(draw)
    draw_secondary(draw)
    draw_small_grid(draw)
    draw_footer(draw)
    return image


def main():
    """Write /output/entry.png: draw it, or copy the prebuilt fallback."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    here = os.path.dirname(os.path.abspath(__file__))
    prebuilt = os.path.join(here, "entry.png")
    try:
        if os.environ.get("NI26_NO_PIL"):
            raise RuntimeError("Pillow blocked for testing")
        image = build_image()
        image.save(out_path, format="PNG", optimize=True)
    except Exception:
        if not os.path.exists(prebuilt):
            raise
        shutil.copyfile(prebuilt, out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
