#!/usr/bin/env python3
"""Draw the news-image entry: a one-page newspaper front page summing up
Wednesday 25 November 2026, rendered with Pillow. Output: entry.png (1024x1024).

Stories (all reported on 25 Nov 2026):
 1. Ukraine confirms drone strikes on Russian ships (Gulf of Finland; warship
    sunk off Benghazi, Libya) - Zelenskyy confirms, Norway urges caution.
 2. Houthi drone hits Riyadh's tallest tower, 11 wounded.
 3. Trump awards Rudy Giuliani the Presidential Medal of Freedom.
 4. Huawei convicted in US criminal trial over Iran business.
 5. Nvidia shares jump 31.5% as Jensen Huang is reinstated as CEO.
 6. BJP and Shiromani Akali Dal reunite for the 2027 Punjab polls.
Footer: Trump meets NATO chief Rutte; UN Day for the Elimination of
Violence against Women; England level the T20 series 1-1.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (23, 48, 84)
TEAL = (14, 92, 92)
GOLD = (176, 128, 20)
GREY = (90, 88, 80)
LIGHT = (233, 227, 211)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", max_w=None):
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        if align == "center":
            tw = draw.textlength(ln, font=fnt)
            draw.text((x + (max_w - tw) / 2, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def panel(draw, x, y, w, h, tag, tag_color, headline, body, art, headline_size=30):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=3)
    draw.rectangle([x, y, x + w, y + 34], fill=tag_color)
    draw.text((x + 12, y + 5), tag, font=font(SANS, 20), fill=WHITE)
    # panel() art height 96 keeps headline + 2-line body inside rh=296
    ay = y + 44
    art(draw, x + 14, ay, w - 28, 84)
    hy = ay + 92
    hl = wrap(draw, headline, font(SANS, headline_size), w - 28)
    hy = text_block(draw, x + 14, hy, hl, font(SANS, headline_size),
                    leading=headline_size + 6)
    hy += 4
    bl = wrap(draw, body, font(SANS_R, 19), w - 28)
    text_block(draw, x + 14, hy, bl, font(SANS_R, 19), leading=24)
    return hy


# ---- pictograms (flat, simple shapes) ----
def art_ship(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(178, 216, 232))
    # waves
    for i in range(4):
        wx = x + 8 + i * (w // 4)
        draw.arc([wx, y + h - 22, wx + 56, y + h - 2], 0, 180, fill=(23, 68, 110), width=3)
    # hull: dark trapezoid with a bow
    draw.polygon([(x + 10, y + h - 52), (x + w - 10, y + h - 52),
                  (x + w - 44, y + h - 14), (x + 44, y + h - 14)], fill=(40, 40, 48))
    draw.rectangle([x + 10, y + h - 52, x + w - 10, y + h - 46], fill=(178, 34, 34))
    # deck + bridge tower
    draw.rectangle([x + w // 2 - 52, y + h - 96, x + w // 2 + 52, y + h - 52],
                   fill=(226, 226, 220))
    draw.rectangle([x + w // 2 - 52, y + h - 96, x + w // 2 + 52, y + h - 88],
                   fill=(23, 48, 84))
    for i in range(4):
        wx = x + w // 2 - 40 + i * 24
        draw.rectangle([wx, y + h - 82, wx + 14, y + h - 70], fill=(23, 48, 84))
    # funnel with smoke
    draw.rectangle([x + w // 2 + 64, y + h - 128, x + w // 2 + 84, y + h - 96], fill=RED)
    for cx, cy, r in [(x + w // 2 + 74, y + h - 138, 8),
                      (x + w // 2 + 88, y + h - 152, 6),
                      (x + w // 2 + 66, y + h - 164, 5)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 150))
    # drone above
    dx, dy = x + w - 40, y + 18
    draw.ellipse([dx - 9, dy - 4, dx + 9, dy + 4], fill=INK)
    draw.line([dx - 20, dy - 9, dx + 20, dy - 9], fill=INK, width=3)
    draw.line([dx - 20, dy + 9, dx + 20, dy + 9], fill=INK, width=3)


def art_tower(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 226, 190))
    cx = x + w // 2
    draw.rectangle([cx - 34, y + 34, cx + 34, y + h], fill=(120, 110, 96))
    draw.rectangle([cx - 22, y + 18, cx + 22, y + 34], fill=(90, 82, 70))
    draw.line([cx, y + 4, cx, y + 18], fill=INK, width=4)
    for r in range(5):
        yy = y + 44 + r * 14
        draw.rectangle([cx - 26, yy, cx + 26, yy + 6], fill=(250, 226, 190))
    # blast burst top-right
    bx, by = x + w - 34, y + 22
    for ang in range(0, 360, 45):
        import math
        ex = bx + int(20 * math.cos(math.radians(ang)))
        ey = by + int(20 * math.sin(math.radians(ang)))
        draw.line([bx, by, ex, ey], fill=(220, 120, 20), width=5)
    draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(255, 190, 40))


def art_medal(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 228, 245))
    cx, cy = x + w // 2, y + h // 2 + 12
    draw.polygon([(cx - 26, y + 6), (cx - 8, y + 6), (cx - 2, cy - 18), (cx - 20, cy - 18)],
                 fill=(178, 34, 34))
    draw.polygon([(cx + 26, y + 6), (cx + 8, y + 6), (cx + 2, cy - 18), (cx + 20, cy - 18)],
                 fill=(23, 48, 84))
    draw.ellipse([cx - 40, cy - 34, cx + 40, cy + 46], fill=GOLD, outline=(120, 84, 10), width=3)
    draw.ellipse([cx - 26, cy - 20, cx + 26, cy + 32], outline=(120, 84, 10), width=2)
    draw.text((cx - 9, cy - 12), "★", font=font(SANS, 30), fill=(120, 84, 10))


def art_chip(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 214))
    cx, cy = x + w // 2, y + h // 2
    for i in range(5):
        px = cx - 44 + i * 22
        draw.line([px, y + 22, px, y + 42], fill=INK, width=3)
        draw.line([px, y + h - 42, px, y + h - 22], fill=INK, width=3)
        py = cy - 44 + i * 22
        draw.line([x + 22, py, x + 42, py], fill=INK, width=3)
        draw.line([x + w - 42, py, x + w - 22, py], fill=INK, width=3)
    draw.rectangle([cx - 46, cy - 46, cx + 46, cy + 46], fill=INK)
    draw.rectangle([cx - 30, cy - 30, cx + 30, cy + 30], outline=GOLD, width=3)
    draw.text((cx - 22, cy - 14), "AI", font=font(SANS, 30), fill=GOLD)


def art_chart(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    base = y + h - 14
    heights = [30, 46, 40, 66, 84]
    bw = (w - 28) // 5
    for i, bh in enumerate(heights):
        bx = x + 14 + i * bw
        draw.rectangle([bx, base - bh, bx + bw - 8, base], fill=NAVY)
    draw.line([(x + 10, base - 16), (x + w - 12, y + 12)], fill=(34, 139, 34), width=6)
    draw.polygon([(x + w - 12, y + 12), (x + w - 34, y + 10), (x + w - 16, y + 30)],
                 fill=(34, 139, 34))


def art_ballot(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(240, 224, 200))
    cx, cy = x + w // 2, y + h // 2 + 8
    draw.rectangle([cx - 52, cy - 30, cx + 52, cy + 44], fill=(250, 246, 236),
                   outline=INK, width=3)
    draw.rectangle([cx - 26, cy - 44, cx + 26, cy - 28], fill=INK)
    # check mark
    draw.line([(cx - 34, cy + 4), (cx - 12, cy + 26), (cx + 38, cy - 26)],
              fill=(34, 139, 34), width=9)
    # two flags
    draw.line([x + 26, y + 14, x + 26, y + 52], fill=INK, width=3)
    draw.polygon([(x + 26, y + 14), (x + 52, y + 21), (x + 26, y + 28)], fill=RED)
    draw.line([x + w - 26, y + 14, x + w - 26, y + 52], fill=INK, width=3)
    draw.polygon([(x + w - 26, y + 14), (x + w - 52, y + 21), (x + w - 26, y + 28)],
                 fill=NAVY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 8], fill=RED)
    y = 16
    t = "THE WORLD IN ONE DAY"
    tw = d.textlength(t, font=font(SERIF, 58))
    d.text(((W - tw) / 2, y), t, font=font(SERIF, 58), fill=INK)
    y += 72
    d.line([40, y, W - 40, y], fill=INK, width=3)
    y += 10
    t2 = "WEDNESDAY  25  NOVEMBER  2026"
    tw = d.textlength(t2, font=font(SANS, 44))
    d.text(((W - tw) / 2, y), t2, font=font(SANS, 44), fill=RED)
    y += 56
    t3 = "One day's world news — in one image"
    tw = d.textlength(t3, font=font(SERIF_R, 26))
    d.text(((W - tw) / 2, y), t3, font=font(SERIF_R, 26), fill=GREY)
    y += 40
    d.line([40, y, W - 40, y], fill=INK, width=3)

    # ---- lead story ----
    ly = y + 12
    lh = 244
    d.rectangle([40, ly, W - 40, ly + lh], outline=INK, width=3)
    d.rectangle([40, ly, W - 40, ly + 40], fill=NAVY)
    d.text((56, ly + 7), "LEAD  •  EUROPE — WAR AT SEA", font=font(SANS, 22), fill=WHITE)
    ax, ay, aw, ah = 56, ly + 54, 300, 176
    art_ship(d, ax, ay, aw, ah)
    tx = ax + aw + 22
    twd = W - 40 - tx - 16
    hl = wrap(d, "Ukraine strikes Russian ships at sea", font(SANS, 38), twd)
    hy = text_block(d, tx, ly + 56, hl, font(SANS, 38), leading=44)
    hy += 8
    body = ("Zelenskyy confirms Kyiv's drones hit a Russian cargo ship in the "
            "Gulf of Finland and sank a warship off Libya. Norway urges caution.")
    bl = wrap(d, body, font(SANS_R, 21), twd)
    text_block(d, tx, hy, bl, font(SANS_R, 21), leading=28)

    # ---- row of three ----
    ry = ly + lh + 14
    rh = 296
    pw = (W - 80 - 2 * 16) // 3
    panel(d, 40, ry, pw, rh, "MIDDLE EAST", RED,
          "Houthi drone hits Riyadh tower",
          "Eleven wounded in the strike on the tower.",
          art_tower, headline_size=26)
    panel(d, 40 + pw + 16, ry, pw, rh, "UNITED STATES", NAVY,
          "Giuliani gets Medal of Freedom",
          "The ex-New York mayor receives the honour.",
          art_medal, headline_size=26)
    panel(d, 40 + 2 * (pw + 16), ry, pw, rh, "TECH  •  CHINA", TEAL,
          "Huawei convicted in US Iran trial",
          "Guilty over Iran business; racketeering charge fails.",
          art_chip, headline_size=26)

    # ---- row of two ----
    ry2 = ry + rh + 14
    rh2 = 178
    pw2 = (W - 80 - 16) // 2
    # business panel (custom, shorter art)
    def panel2(x, tag, color, headline, body, artfn):
        d.rectangle([x, ry2, x + pw2, ry2 + rh2], outline=INK, width=3)
        d.rectangle([x, ry2, x + pw2, ry2 + 34], fill=color)
        d.text((x + 12, ry2 + 5), tag, font=font(SANS, 20), fill=WHITE)
        artfn(d, x + 14, ry2 + 44, 150, 138)
        tx2 = x + 178
        tw2 = x + pw2 - tx2 - 14
        hl = wrap(d, headline, font(SANS, 27), tw2)
        hy2 = text_block(d, tx2, ry2 + 48, hl, font(SANS, 27), leading=32)
        bl = wrap(d, body, font(SANS_R, 20), tw2)
        text_block(d, tx2, hy2 + 6, bl, font(SANS_R, 20), leading=26)

    panel2(40, "BUSINESS", (34, 100, 34), "Nvidia soars as Huang returns",
           "Shares jump 31.5% as Huang returns as CEO.",
           art_chart)
    panel2(40 + pw2 + 16, "ASIA  •  INDIA", GOLD, "BJP and Akali Dal reunite",
           "Allies again after six years, for Punjab 2027.",
           art_ballot)

    # ---- footer ----
    fy = ry2 + rh2 + 12
    d.rectangle([40, fy, W - 40, fy + 42], fill=INK)
    foot = ("ALSO:  Trump meets NATO chief Rutte  •  UN day on violence against women  •  England level T20 1–1")
    fw = d.textlength(foot, font=font(SANS, 16))
    d.text(((W - fw) / 2, fy + 12), foot, font=font(SANS, 16), fill=WHITE)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
