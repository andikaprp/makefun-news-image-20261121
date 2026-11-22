#!/usr/bin/env python3
"""Strong candidate renderer for news-image-20261121.

Fresh authorship in this session. Cream broadsheet: giant date, strap,
stat band, region strip, 15 headlined cards each with its own original
flat-art panel (102x88, banner label + source tag on the panel),
abstract-blob map panel, numbered briefs band, DATE CHECK box, footer.
Headlines: Noto Sans Condensed Bold at 36px - never shrunk.
Deterministic: no randomness, no clock.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
CREAM = (247, 241, 222)
PAPER = (252, 248, 236)
INK = (18, 18, 18)
RED = (176, 0, 32)
NAVY = (16, 32, 64)
GOLD = (232, 184, 75)

DB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
NCB = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"
NCR = "/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def centered(d, y, s, f, fill, cx=W // 2):
    d.text((cx - tw(d, s, f) // 2, y), s, font=f, fill=fill)


def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(d, t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


PALETTES = {
    "globe": ((64, 120, 180), (240, 200, 90)),
    "missile": ((30, 34, 70), (255, 120, 60)),
    "cross": ((90, 40, 40), (255, 220, 220)),
    "drone": ((40, 50, 90), (200, 220, 255)),
    "quake": ((150, 100, 50), (255, 210, 120)),
    "plane": ((70, 150, 200), (255, 255, 255)),
    "wave": ((20, 110, 150), (170, 230, 255)),
    "cricket": ((40, 130, 70), (255, 240, 180)),
    "handshake": ((60, 90, 160), (255, 210, 100)),
    "car": ((35, 35, 45), (255, 90, 90)),
    "robot": ((80, 80, 110), (140, 255, 200)),
    "cricket2": ((30, 110, 90), (255, 240, 180)),
    "cricket3": ((120, 90, 30), (255, 240, 180)),
    "coin": ((50, 45, 20), (255, 200, 40)),
    "road": ((110, 95, 60), (255, 235, 170)),
}


def draw_scene(d, kind, x, y, w, h):
    """Original flat art, simple shapes, centred in the panel's middle
    band (banner chip sits at top, source tag at bottom)."""
    bg, ac = PALETTES.get(kind, ((90, 90, 90), (255, 255, 255)))
    d.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w // 2, y + h // 2 + 4
    if kind == "globe":
        d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=ac)
        d.arc([cx - 24, cy - 24, cx + 24, cy + 24], 20, 320, fill=bg, width=3)
        d.line([cx - 24, cy, cx + 24, cy], fill=bg, width=3)
    elif kind in ("missile", "drone"):
        for i in range(3):
            bx = cx - 26 + i * 22
            d.polygon([(bx, cy + 18), (bx + 7, cy - 16), (bx + 14, cy + 18)], fill=ac)
            d.polygon([(bx + 7, cy - 25), (bx + 2, cy - 15), (bx + 12, cy - 15)], fill=(255, 255, 255))
    elif kind == "cross":
        d.rectangle([cx - 7, cy - 23, cx + 7, cy + 23], fill=ac)
        d.rectangle([cx - 23, cy - 7, cx + 23, cy + 7], fill=ac)
    elif kind in ("quake", "wave"):
        pts = [(x + 8 + i * (w - 16) // 6, cy + 16 - (16 if i % 2 else 0)) for i in range(7)]
        d.line(pts, fill=ac, width=5)
    elif kind == "plane":
        d.polygon([(cx - 30, cy + 4), (cx + 26, cy - 10), (cx + 33, cy - 1), (cx - 17, cy + 11)], fill=ac)
        d.polygon([(cx - 5, cy + 1), (cx + 7, cy - 19), (cx + 15, cy - 17), (cx + 8, cy + 3)], fill=ac)
    elif kind in ("cricket", "cricket2", "cricket3"):
        for sx in (cx - 20, cx, cx + 20):
            d.rectangle([sx - 3, cy - 20, sx + 3, cy + 20], fill=ac)
        d.ellipse([cx + 24, cy - 24, cx + 36, cy - 12], fill=(230, 60, 60))
    elif kind == "handshake":
        d.polygon([(cx - 28, cy + 8), (cx - 3, cy - 12), (cx + 5, cy - 1), (cx - 15, cy + 17)], fill=ac)
        d.polygon([(cx + 28, cy + 8), (cx + 3, cy - 12), (cx - 5, cy - 1), (cx + 15, cy + 17)], fill=(255, 255, 255))
    elif kind == "car":
        d.rectangle([cx - 29, cy + 1, cx + 29, cy + 14], fill=ac)
        d.polygon([(cx - 17, cy + 1), (cx - 7, cy - 12), (cx + 13, cy - 12), (cx + 22, cy + 1)], fill=ac)
        d.ellipse([cx - 22, cy + 9, cx - 9, cy + 22], fill=(20, 20, 20))
        d.ellipse([cx + 10, cy + 9, cx + 23, cy + 22], fill=(20, 20, 20))
    elif kind == "robot":
        d.rectangle([cx - 20, cy - 18, cx + 20, cy + 18], outline=ac, width=4)
        d.ellipse([cx - 12, cy - 8, cx - 3, cy + 1], fill=ac)
        d.ellipse([cx + 3, cy - 8, cx + 12, cy + 1], fill=ac)
        d.line([cx, cy - 18, cx, cy - 28], fill=ac, width=3)
        d.ellipse([cx - 3, cy - 31, cx + 3, cy - 25], fill=(255, 80, 80))
    elif kind == "coin":
        d.ellipse([cx - 23, cy - 23, cx + 23, cy + 23], fill=ac)
        d.text((cx - 8, cy - 16), "B", font=F(NCB, 30), fill=(90, 70, 0))
    elif kind == "road":
        d.polygon([(cx - 5, cy - 26), (cx + 5, cy - 26), (cx + 25, cy + 24), (cx - 25, cy + 24)], fill=(60, 60, 60))
        for i in range(3):
            yy = cy - 15 + i * 14
            d.line([(cx, yy), (cx, yy + 6)], fill=(255, 255, 255), width=3)


def draw_map(d, x, y, w, h, count):
    d.rectangle([x, y, x + w, y + h], fill=(234, 226, 198), outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 25], fill=NAVY)
    d.text((x + 8, y + 4), "WHERE IT HAPPENED", font=F(NCB, 19), fill=(255, 255, 255))
    blobs = [
        [(18, 30), (52, 18), (66, 36), (48, 52), (26, 48)],
        [(58, 60), (74, 56), (80, 78), (64, 96), (54, 76)],
        [(128, 26), (168, 18), (182, 38), (160, 50), (134, 44)],
        [(150, 56), (176, 52), (186, 74), (164, 90), (148, 72)],
        [(196, 24), (248, 16), (268, 38), (240, 58), (204, 46)],
        [(238, 70), (264, 66), (272, 86), (248, 96), (234, 82)],
    ]
    sx = w / 290.0
    sy = (h - 32) / 108.0
    cols = [(70, 140, 90), (190, 120, 60), (80, 110, 180), (170, 70, 70), (110, 90, 160), (60, 150, 150)]
    for i, blob in enumerate(blobs):
        pts = [(x + int(px * sx), y + 29 + int(py * sy)) for px, py in blob]
        d.polygon(pts, fill=cols[i])
    spots = [(40, 33), (150, 40), (140, 28), (132, 24), (62, 74), (252, 78),
             (244, 70), (258, 90), (140, 22), (30, 36), (136, 26), (205, 40),
             (165, 78), (150, 48), (158, 44)]
    for i, (px, py) in enumerate(spots[:count]):
        cxp = x + int(px * sx)
        cyp = y + 29 + int(py * sy)
        d.ellipse([cxp - 8, cyp - 8, cxp + 8, cyp + 8], fill=RED, outline=(255, 255, 255), width=2)
        lab = str(i + 1)
        f = F(NCB, 11)
        d.text((cxp - tw(d, lab, f) // 2, cyp - 6), lab, font=f, fill=(255, 255, 255))


def main():
    with open(os.path.join(HERE, "data_strong.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, 6], fill=RED)
    centered(d, 10, data["date_line"], F(DSB, 50), INK)
    centered(d, 68, "ONE DAY ON EARTH - THE WORLD IN ONE PAGE", F(NCB, 22), RED)
    centered(d, 94, data["strap"], F(NCB, 27), INK)
    # stat band
    sy = 128
    d.rectangle([8, sy, W - 8, sy + 48], fill=NAVY)
    cellw = (W - 16) // 6
    for i, (fig, lab) in enumerate(data["stats"]):
        cxp = 8 + i * cellw + cellw // 2
        centered(d, sy + 3, fig, F(DB, 24), GOLD, cx=cxp)
        centered(d, sy + 31, lab, F(NCR, 13), (255, 255, 255), cx=cxp)
    centered(d, 182, data["regions"], F(NCB, 19), NAVY)
    d.line([(8, 206), (W - 8, 206)], fill=INK, width=2)
    # headlined grid 3x5
    gx, gy, cw, chh, gap = 8, 212, 332, 88, 6
    fh36 = F(NCB, 36)
    ffact = F(NCR, 11)
    warns = []
    for idx, card in enumerate(data["cards"]):
        r, c = divmod(idx, 3)
        x = gx + c * (cw + gap)
        y = gy + r * (chh + gap)
        d.rectangle([x, y, x + cw, y + chh], fill=PAPER, outline=(120, 110, 80), width=1)
        # art panel left, 102x88
        ax, ay, aw, ah = x + 3, y + 2, 94, 84
        draw_scene(d, card["kind"], ax, ay, aw, ah)
        bf = F(NCB, 9)
        banner = "%d %s" % (card["n"], card["banner"])
        if tw(d, banner, bf) > aw - 4:
            bf = F(NCB, 8)  # banner chip only; headlines never shrink
        d.rectangle([ax, ay, ax + aw, ay + 15], fill=(0, 0, 0, 215))
        d.text((ax + 3, ay + 2), banner, font=bf, fill=(255, 255, 255))
        sf = F(NCB, 9)
        stag = card["source"]
        if tw(d, stag, sf) > aw - 4:
            warns.append("source wide: " + stag)
        d.rectangle([ax, ay + ah - 15, ax + aw, ay + ah], fill=(0, 0, 0, 215))
        d.text((ax + 3, ay + ah - 13), stag, font=sf, fill=GOLD)
        # headline + fact, right of the panel
        tx = x + 104
        for j, ln in enumerate(card["head"]):
            if tw(d, ln, fh36) > cw - 108:
                warns.append("headline wide: " + ln)
            d.text((tx, y + 2 + j * 31), ln, font=fh36, fill=INK)
        flines = wrap(d, card["fact"], ffact, cw - 108)[:2]
        for j, ln in enumerate(flines):
            d.text((tx, y + 64 + j * 11), ln, font=ffact, fill=(35, 35, 35))
    grid_bottom = gy + 5 * chh + 4 * gap  # 676
    # briefs band
    by = grid_bottom + 6  # 682
    bh = 130
    d.rectangle([8, by, W - 8, by + bh], fill=PAPER, outline=INK, width=2)
    d.text((16, by + 3), "MORE OF THE DAY - BRIEFS 16-34  |  " + data["cutoff"], font=F(NCB, 15), fill=RED)
    bfr = F(NCR, 11)
    colw = (W - 32) // 2
    for i, brief in enumerate(data["briefs"]):
        col = 0 if i < 10 else 1
        row = i if i < 10 else i - 10
        x = 16 + col * colw
        y = by + 23 + row * 10
        if tw(d, brief, bfr) > colw - 6:
            warns.append("brief wide: " + brief)
        d.text((x, y), brief, font=bfr, fill=INK)
    # bottom band: map + date check
    ty = by + bh + 6  # 818
    th = 164
    draw_map(d, 8, ty, 220, th, len(data["cards"]))
    dx = 236
    d.rectangle([dx, ty, W - 8, ty + th], fill=(255, 255, 255), outline=RED, width=2)
    d.rectangle([dx, ty, W - 8, ty + 26], fill=RED)
    d.text((dx + 8, ty + 1), "DATE CHECK - VERIFIED, BUT NOT SATURDAY", font=F(NCB, 24), fill=(255, 255, 255))
    idf = F(NCB, 24)
    for i, item in enumerate(data["datecheck"]):
        if tw(d, "- " + item, idf) > (W - 8 - dx) - 14:
            warns.append("datecheck wide: " + item)
        d.text((dx + 8, ty + 29 + i * 22), "- " + item, font=idf, fill=INK)
    # footer
    fy = ty + th + 5  # 987
    centered(d, fy, data["not_yet"], F(NCB, 17), RED)
    centered(d, fy + 18, data["footer"], F(NCB, 17), INK)
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    for wn in warns:
        print("WARN:", wn)
    print("saved", out)


if __name__ == "__main__":
    main()
