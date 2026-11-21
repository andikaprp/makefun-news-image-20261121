#!/usr/bin/env python3
"""One Day on Earth - Saturday 21 November 2026 - probe candidate renderer.
Fresh-authored for news-image-20261121. Draws a cream broadsheet page:
giant date, strap, stat band, region strip, 3 illustrated leads,
13 illustrated dispatches, a pin map, numbered briefs, DATE CHECK box.
Every headlined card carries its own flat illustration with an ALL-CAPS
banner label and a source tag on the art panel.
"""
import json, math, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "data_probe.json")))

W = 1024
MARGIN = 26
CW = W - 2 * MARGIN

CREAM = (247, 241, 227)
PAPER = (252, 249, 240)
INK = (26, 24, 20)
MUTED = (104, 94, 76)
RED = (168, 44, 34)
DARKRED = (120, 30, 24)
LINE = (198, 188, 164)
WHITE = (255, 253, 246)

FDIR = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

def F_cond_b(size):  return font("NotoSansDisplay-ExtraCondensedBold.ttf", size)
def F_cond_sb(size): return font("NotoSansDisplay-ExtraCondensedSemiBold.ttf", size)
def F_cond_bi(size): return font("NotoSansDisplay-ExtraCondensedBoldItalic.ttf", size)
def F_b(size):  return font("NotoSans-Bold.ttf", size)
def F_r(size):  return font("NotoSans-Regular.ttf", size)
def F_i(size):  return font("NotoSans-Italic.ttf", size)

def tw(d, s, f):
    return d.textlength(s, font=f)

def fit_font(d, s, name_fn, start, target_w, floor=10):
    size = start
    while size > floor and tw(d, s, name_fn(size)) > target_w:
        size -= 1
    return name_fn(size)

def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

# ---------------------------------------------------------------- art scenes
# Each scene draws into box (x0,y0,x1,y1) on draw d. Flat, bold shapes only.

def _sky(d, box, top, bot):
    x0, y0, x1, y1 = box
    steps = 24
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        yy = y0 + (y1 - y0) * i // steps
        d.rectangle([x0, yy, x1, y0 + (y1 - y0) * (i + 1) // steps + 1], fill=c)

def _sun(d, cx, cy, r, col=(250, 199, 92)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

def art_summit(d, box):
    _sky(d, box, (38, 54, 92), (214, 164, 96))
    x0, y0, x1, y1 = box
    _sun(d, x1 - 60, y0 + 34, 17)
    # conference hall: dome + columns
    cx = (x0 + x1) // 2
    d.pieslice([cx - 90, y1 - 118, cx + 90, y1 - 28], 180, 360, fill=(232, 226, 208))
    d.rectangle([x0 + 30, y1 - 62, x1 - 30, y1 - 40], fill=(44, 48, 60))
    for i in range(6):
        px = x0 + 52 + i * ((x1 - x0 - 104) // 5)
        d.rectangle([px - 5, y1 - 62, px + 5, y1 - 16], fill=(232, 226, 208))
    d.rectangle([x0 + 20, y1 - 16, x1 - 20, y1], fill=(30, 32, 40))
    # flags
    cols = [(200, 60, 50), (60, 120, 200), (70, 160, 90), (240, 180, 40), (150, 80, 180)]
    for i, c in enumerate(cols):
        fx = x0 + 34 + i * 26
        d.line([fx, y0 + 14, fx, y0 + 44], fill=(240, 238, 228), width=2)
        d.polygon([(fx, y0 + 14), (fx + 17, y0 + 19), (fx, y0 + 24)], fill=c)

def art_missiles(d, box):
    _sky(d, box, (16, 20, 44), (96, 60, 84))
    x0, y0, x1, y1 = box
    # skyline
    hs = [46, 70, 34, 88, 52, 64, 40, 76, 30]
    bw = (x1 - x0) // len(hs)
    for i, h in enumerate(hs):
        d.rectangle([x0 + i * bw + 2, y1 - h, x0 + (i + 1) * bw - 2, y1], fill=(24, 26, 40))
    d.rectangle([x0, y1 - 6, x1, y1], fill=(12, 12, 22))
    # incoming arcs + interceptor arcs
    for sx, ex, col in [(x0 + 30, x0 + 190, (244, 120, 90)), (x0 + 90, x0 + 250, (244, 120, 90))]:
        pts = []
        for t in range(21):
            u = t / 20
            px = sx + (ex - sx) * u
            py = (y0 + 8) + (y1 - 60 - y0) * (u * u)
            pts.append((px, py))
        d.line(pts, fill=col, width=3)
    for sx, ex in [(x1 - 40, x0 + 205), (x1 - 90, x0 + 262)]:
        pts = []
        for t in range(21):
            u = t / 20
            px = sx + (ex - sx) * u
            py = (y1 - 8) - (y1 - 66 - y0) * (u * (2 - u)) * 0.9
            pts.append((px, py))
        d.line(pts, fill=(140, 220, 250), width=3)
    # bursts
    for bx, by in [(x0 + 200, y1 - 62), (x0 + 258, y1 - 70)]:
        for a in range(0, 360, 45):
            dx, dy = 13 * math.cos(math.radians(a)), 13 * math.sin(math.radians(a))
            d.line([bx, by, bx + dx, by + dy], fill=(255, 214, 110), width=3)
        _sun(d, bx, by, 4, (255, 230, 150))

def art_strike(d, box):
    _sky(d, box, (70, 62, 66), (188, 132, 96))
    x0, y0, x1, y1 = box
    # apartment blocks, one damaged
    blocks = [(x0 + 16, 66), (x0 + 84, 84), (x0 + 160, 58), (x0 + 226, 78)]
    for i, (bx, bh) in enumerate(blocks):
        d.rectangle([bx, y1 - bh, bx + 58, y1], fill=(52, 48, 52) if i != 1 else (66, 56, 52))
        for wy in range(y1 - bh + 10, y1 - 12, 16):
            for wx in range(bx + 8, bx + 48, 15):
                if (wx + wy) % 3:
                    d.rectangle([wx, wy, wx + 7, wy + 8], fill=(250, 205, 110))
    # smoke plume from damaged block
    for r, ox, oy, a in [(26, 120, -64, 90), (20, 138, -88, 110), (15, 152, -106, 130)]:
        d.ellipse([x0 + ox - r, y1 + oy - r, x0 + ox + r, y1 + oy + r], fill=(a, a, a))
    d.rectangle([x0, y1 - 8, x1, y1], fill=(34, 30, 32))
    # red cross marker (hospital)
    hx, hy = x0 + 250, y1 - 96
    d.rectangle([hx - 12, hy - 12, hx + 12, hy + 12], fill=(240, 238, 230))
    d.rectangle([hx - 3, hy - 8, hx + 3, hy + 8], fill=(200, 50, 40))
    d.rectangle([hx - 8, hy - 3, hx + 8, hy + 3], fill=(200, 50, 40))

def art_quake(d, box):
    _sky(d, box, (64, 96, 128), (216, 188, 130))
    x0, y0, x1, y1 = box
    # andes ridges
    d.polygon([(x0, y1 - 30), (x0 + 80, y0 + 26), (x0 + 150, y1 - 30)], fill=(88, 84, 92))
    d.polygon([(x0 + 110, y1 - 30), (x0 + 210, y0 + 14), (x0 + 300, y1 - 30)], fill=(70, 68, 80))
    d.polygon([(x0 + 62, y0 + 40), (x0 + 80, y0 + 26), (x0 + 98, y0 + 42)], fill=(245, 244, 238))
    d.polygon([(x0 + 192, y0 + 28), (x0 + 210, y0 + 14), (x0 + 228, y0 + 30)], fill=(245, 244, 238))
    # cracked ground
    d.rectangle([x0, y1 - 30, x1, y1], fill=(120, 92, 66))
    pts = [(x0 + 30, y1 - 28), (x0 + 90, y1 - 18), (x0 + 130, y1 - 24), (x0 + 190, y1 - 12), (x0 + 250, y1 - 20), (x1 - 14, y1 - 10)]
    d.line(pts, fill=(30, 22, 16), width=4)
    pts2 = [(x0 + 90, y1 - 18), (x0 + 108, y1 - 4)]
    d.line(pts2, fill=(30, 22, 16), width=3)
    # houses, one tilted
    d.rectangle([x0 + 236, y1 - 56, x0 + 272, y1 - 30], fill=(226, 214, 188))
    d.polygon([(x0 + 232, y1 - 56), (x0 + 254, y1 - 70), (x0 + 276, y1 - 56)], fill=(150, 60, 44))
    d.polygon([(x0 + 36, y1 - 52), (x0 + 52, y1 - 62), (x0 + 70, y1 - 48), (x0 + 66, y1 - 28), (x0 + 40, y1 - 30)], fill=(210, 198, 172))

def art_cricket(d, box):
    _sky(d, box, (86, 140, 190), (196, 224, 200))
    x0, y0, x1, y1 = box
    h = y1 - y0
    g = y1 - int(h * 0.34)  # ground line
    d.rectangle([x0, g, x1, y1], fill=(74, 148, 84))
    # pitch strip
    d.polygon([(x0 + 118, y1), (x0 + 148, g), (x0 + 196, g), (x0 + 182, y1)], fill=(226, 208, 160))
    # stumps at both ends
    for sx in (x0 + 152, x0 + 186):
        for k in range(3):
            d.line([sx + k * 5, g + 4, sx + k * 5, y1 - 6], fill=(250, 220, 120), width=3)
    # batsman silhouette (compact)
    bx, by = x0 + 92, g + 2
    d.ellipse([bx - 6, by - 22, bx + 6, by - 10], fill=(30, 34, 44))
    d.line([bx, by - 10, bx - 3, by + 10], fill=(30, 34, 44), width=6)
    d.line([bx - 3, by + 10, bx - 13, y1 - 4], fill=(30, 34, 44), width=5)
    d.line([bx - 3, by + 10, bx + 10, y1 - 5], fill=(30, 34, 44), width=5)
    d.line([bx + 2, by - 6, bx + 28, by + 4], fill=(30, 34, 44), width=5)
    d.line([bx + 28, by + 4, bx + 38, by - 18], fill=(196, 160, 100), width=6)
    # ball in flight
    _sun(d, x0 + 238, y0 + int(h * 0.36), 5, (214, 48, 44))
    pts = [(x0 + 262 - t * 3, y0 + int(h * 0.18) + t) for t in range(9)]
    d.line(pts, fill=(240, 240, 235), width=2)
    # crowd dots along the boundary
    for i in range(26):
        cxp = x0 + 8 + i * 12
        d.ellipse([cxp, g - 7, cxp + 6, g - 1], fill=(40 + (i * 37) % 160, 60, 90))

def art_plane(d, box):
    _sky(d, box, (18, 30, 58), (70, 96, 138))
    x0, y0, x1, y1 = box
    d.rectangle([x0, y1 - 22, x1, y1], fill=(28, 30, 36))
    d.line([x0, y1 - 22, x1, y1 - 22], fill=(250, 200, 90), width=3)
    for i in range(7):
        lx = x0 + 20 + i * 44
        d.rectangle([lx, y1 - 12, lx + 16, y1 - 8], fill=(250, 200, 90))
    # aircraft body (side view, nose right)
    cy = y0 + int((y1 - y0) * 0.52)
    d.polygon([(x0 + 36, cy), (x0 + 210, cy - 13), (x0 + 262, cy - 4), (x0 + 268, cy + 6),
               (x0 + 210, cy + 13), (x0 + 44, cy + 11)], fill=(232, 234, 238))
    d.polygon([(x0 + 40, cy - 2), (x0 + 16, cy - 30), (x0 + 34, cy - 32), (x0 + 62, cy - 4)], fill=(200, 60, 48))
    d.polygon([(x0 + 120, cy + 8), (x0 + 150, cy + 30), (x0 + 168, cy + 30), (x0 + 150, cy + 8)], fill=(190, 196, 205))
    for i in range(9):
        wx = x0 + 84 + i * 17
        d.ellipse([wx, cy - 6, wx + 7, cy - 1], fill=(40, 70, 110))
    # engine warning glow
    _sun(d, x0 + 152, cy + 26, 9, (250, 140, 50))
    _sun(d, x0 + 152, cy + 26, 4, (255, 220, 130))
    # slide
    d.polygon([(x0 + 232, cy + 10), (x0 + 262, y1 - 22), (x0 + 248, y1 - 22), (x0 + 224, cy + 12)], fill=(240, 190, 60))

def art_bitcoin(d, box):
    _sky(d, box, (24, 22, 34), (64, 40, 60))
    x0, y0, x1, y1 = box
    # plunging chart
    pts = [(x0 + 16, y0 + 26), (x0 + 80, y0 + 34), (x0 + 130, y0 + 30), (x0 + 180, y0 + 62), (x0 + 232, y0 + 96), (x0 + 292, y1 - 26)]
    d.line(pts, fill=(240, 90, 70), width=4)
    for gx in range(x0 + 16, x1 - 8, 46):
        d.line([gx, y0 + 10, gx, y1 - 12], fill=(52, 48, 66), width=1)
    # coin
    r = min(27, (y1 - y0) // 2 - 4)
    cx, cy = x0 + 66, y1 - r - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(243, 168, 44), outline=(190, 120, 20), width=3)
    bf = F_b(34)
    bb = d.textbbox((0, 0), "B", font=bf)
    d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), "B", font=bf, fill=(120, 70, 10))
    d.polygon([(x0 + 268, y1 - 40), (x0 + 282, y1 - 22), (x0 + 254, y1 - 22)], fill=(240, 90, 70))

def art_fire(d, box):
    _sky(d, box, (52, 36, 40), (196, 110, 62))
    x0, y0, x1, y1 = box
    # ridge houses silhouettes
    for i, (hx, hh) in enumerate([(x0 + 14, 40), (x0 + 76, 52), (x0 + 150, 36), (x0 + 214, 48), (x0 + 272, 38)]):
        d.rectangle([hx, y1 - hh, hx + 44, y1], fill=(30, 24, 26))
        d.polygon([(hx - 3, y1 - hh), (hx + 22, y1 - hh - 13), (hx + 47, y1 - hh)], fill=(22, 18, 20))
    # flames behind
    for fx, fh in [(x0 + 58, 74), (x0 + 128, 92), (x0 + 198, 80), (x0 + 258, 66)]:
        d.polygon([(fx - 15, y1 - 30), (fx, y1 - 30 - fh), (fx + 15, y1 - 30)], fill=(238, 110, 40))
        d.polygon([(fx - 8, y1 - 30), (fx, y1 - 30 - fh * 0.62), (fx + 8, y1 - 30)], fill=(250, 190, 70))
    d.rectangle([x0, y1 - 10, x1, y1], fill=(20, 16, 18))
    # smoke
    for ox, oy, r in [(90, 18, 15), (140, 12, 19), (196, 16, 14)]:
        d.ellipse([x0 + ox - r, y0 + oy - r // 2, x0 + ox + r, y0 + oy + r // 2], fill=(90, 78, 76))

def art_f1(d, box):
    _sky(d, box, (20, 22, 48), (120, 70, 110))
    x0, y0, x1, y1 = box
    # neon strip lights
    for i, c in enumerate([(250, 90, 160), (90, 200, 250), (250, 200, 80)]):
        lx = x0 + 30 + i * 100
        d.rectangle([lx, y0 + 12, lx + 70, y0 + 17], fill=c)
    d.rectangle([x0, y1 - 26, x1, y1], fill=(26, 26, 32))
    d.line([x0, y1 - 26, x1, y1 - 26], fill=(240, 240, 235), width=2)
    # car silhouette
    cy = y1 - 30
    d.polygon([(x0 + 40, cy), (x0 + 74, cy - 12), (x0 + 120, cy - 14), (x0 + 138, cy - 26),
               (x0 + 168, cy - 26), (x0 + 182, cy - 14), (x0 + 238, cy - 10), (x0 + 262, cy)], fill=(178, 34, 40))
    d.rectangle([x0 + 30, cy - 20, x0 + 52, cy - 4], fill=(140, 26, 32))
    d.rectangle([x0 + 246, cy - 16, x0 + 272, cy - 4], fill=(140, 26, 32))
    d.ellipse([x0 + 66, cy - 12, x0 + 98, cy + 8], fill=(16, 16, 20))
    d.ellipse([x0 + 206, cy - 12, x0 + 238, cy + 8], fill=(16, 16, 20))
    d.ellipse([x0 + 146, cy - 34, x0 + 162, cy - 20], fill=(240, 200, 90))
    # speed lines
    for k in range(3):
        d.line([x0 + 8, cy - 22 + k * 8, x0 + 34, cy - 22 + k * 8], fill=(200, 210, 230), width=2)

def art_space(d, box):
    _sky(d, box, (8, 10, 26), (30, 34, 66))
    x0, y0, x1, y1 = box
    for i in range(40):
        sx = x0 + (i * 67) % (x1 - x0)
        sy = y0 + (i * 41) % (y1 - y0)
        d.point((sx, sy), fill=(230, 232, 240))
    # mercury
    mr = (y1 - y0 - 12) // 2
    mx, my = x0 + 58, y0 + (y1 - y0) // 2
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(168, 148, 128))
    for ox, oy, r in [(-14, -8, 9), (12, 10, 12), (16, -16, 6), (-4, 18, 7)]:
        d.ellipse([mx + ox - r, my + oy - r, mx + ox + r, my + oy + r], fill=(146, 126, 106))
    d.pieslice([mx - mr, my - mr, mx + mr, my + mr], 90, 270, fill=(140, 120, 98))
    # orbit ellipse + craft
    d.ellipse([x0 + 120, y0 + 16, x1 - 14, y1 - 8], outline=(120, 170, 230), width=2)
    cx, cy = x0 + 226, y0 + 30
    d.rectangle([cx - 9, cy - 6, cx + 9, cy + 6], fill=(226, 228, 232))
    d.rectangle([cx - 30, cy - 4, cx - 12, cy + 4], fill=(70, 110, 190))
    d.rectangle([cx + 12, cy - 4, cx + 30, cy + 4], fill=(70, 110, 190))
    _sun(d, x1 - 30, y0 + 22, 11, (250, 220, 150))

def art_servers(d, box):
    _sky(d, box, (26, 34, 48), (44, 58, 76))
    x0, y0, x1, y1 = box
    h = y1 - y0
    top, bot = y0 + int(h * 0.16), y1 - int(h * 0.1)
    for i in range(4):
        rx = x0 + 22 + i * 76
        d.rectangle([rx, top, rx + 58, bot], fill=(52, 66, 84), outline=(96, 120, 148), width=2)
        for k in range(5):
            ry = top + 5 + k * max(4, (bot - top - 10) // 5)
            if ry + 5 > bot - 2:
                break
            d.rectangle([rx + 8, ry, rx + 50, ry + 5], fill=(38, 48, 62))
            d.ellipse([rx + 12, ry + 1, rx + 16, ry + 5], fill=(90, 220, 140) if k % 2 else (250, 170, 60))
    # flag stripe on top rack
    d.rectangle([x0 + 22, y0 + 3, x0 + 80, y0 + 9], fill=(178, 44, 40))

def art_train(d, box):
    _sky(d, box, (96, 128, 168), (208, 200, 168))
    x0, y0, x1, y1 = box
    d.rectangle([x0, y1 - 34, x1, y1], fill=(110, 100, 88))
    # rails: one straight, one bent
    d.line([x0, y1 - 14, x1, y1 - 14], fill=(60, 58, 56), width=3)
    d.line([(x0, y1 - 26), (x0 + 170, y1 - 26), (x0 + 205, y1 - 18), (x1, y1 - 20)], fill=(60, 58, 56), width=3)
    # wagons: three level, two tipped
    for i, (wx, tip) in enumerate([(x0 + 14, 0), (x0 + 76, 0), (x0 + 138, 0), (x0 + 200, 7), (x0 + 256, 13)]):
        wy = y1 - 58 + tip
        d.rectangle([wx, wy, wx + 52, wy + 26], fill=(120, 74, 44) if i % 2 else (96, 96, 104), outline=(40, 38, 36), width=2)
        d.ellipse([wx + 8, wy + 24, wx + 18, wy + 34], fill=(30, 30, 32))
        d.ellipse([wx + 34, wy + 24, wx + 44, wy + 34], fill=(30, 30, 32))
    # signal pole snapped
    d.line([x0 + 282, y1 - 30, x0 + 282, y0 + 30], fill=(50, 48, 46), width=4)
    d.line([x0 + 282, y0 + 30, x0 + 300, y0 + 44], fill=(50, 48, 46), width=4)
    _sun(d, x0 + 40, y0 + 24, 13)

def art_weather(d, box):
    _sky(d, box, (70, 110, 150), (170, 190, 200))
    x0, y0, x1, y1 = box
    d.rectangle([x0, y1 - 26, x1, y1], fill=(52, 110, 140))
    # islands
    for ix, iw in [(x0 + 40, 70), (x0 + 140, 92), (x0 + 252, 56)]:
        d.pieslice([ix, y1 - 44, ix + iw, y1 - 8], 180, 360, fill=(88, 150, 92))
    # four cloud systems
    for cx, cy, s in [(x0 + 60, y0 + 26, 1.0), (x0 + 150, y0 + 18, 0.8), (x0 + 226, y0 + 30, 0.9), (x0 + 282, y0 + 16, 0.7)]:
        for ox, oy, r in [(-16, 4, 12), (0, -4, 16), (16, 4, 12)]:
            d.ellipse([cx + ox * s - r * s, cy + oy * s - r * s * 0.6, cx + ox * s + r * s, cy + oy * s + r * s * 0.6], fill=(238, 240, 242))
        for rx in range(-14, 16, 9):
            d.line([cx + rx * s, cy + 16 * s, cx + rx * s - 3, cy + 26 * s], fill=(90, 150, 220), width=2)

def art_jail(d, box):
    _sky(d, box, (58, 62, 74), (150, 140, 118))
    x0, y0, x1, y1 = box
    h = y1 - y0
    water = y1 - int(h * 0.16)
    top = y0 + int(h * 0.14)
    # island jail block
    d.rectangle([x0 + 60, top + 8, x1 - 60, water], fill=(96, 94, 90))
    d.rectangle([x0 + 60, top, x1 - 60, top + 8], fill=(70, 68, 66))
    for r_ in range(2):
        for c_ in range(6):
            wx = x0 + 78 + c_ * 32
            wy = top + 14 + r_ * int((water - top - 20) / 2)
            d.rectangle([wx, wy, wx + 16, wy + 11], fill=(250, 205, 110) if (r_ + c_) % 3 else (52, 54, 58))
            for b_ in range(3):
                d.line([wx + 3 + b_ * 5, wy, wx + 3 + b_ * 5, wy + 11], fill=(30, 30, 32), width=1)
    # tower + water
    d.rectangle([x0 + 22, top + 16, x0 + 44, water], fill=(80, 78, 76))
    d.rectangle([x0, water, x1, y1], fill=(52, 90, 120))
    _sun(d, x1 - 44, y0 + int(h * 0.2), 11, (240, 190, 110))

def art_court(d, box):
    _sky(d, box, (40, 48, 70), (120, 116, 104))
    x0, y0, x1, y1 = box
    h = y1 - y0
    # courthouse: pediment + columns (fractions of panel height)
    cx = (x0 + x1) // 2
    ped_y = y0 + int(h * 0.52)
    d.polygon([(x0 + 40, ped_y), (x1 - 40, ped_y), (cx, y0 + int(h * 0.14))], fill=(226, 220, 204))
    d.rectangle([x0 + 40, ped_y + 3, x1 - 40, ped_y + 8], fill=(200, 194, 178))
    for i in range(5):
        px = x0 + 62 + i * 48
        d.rectangle([px, ped_y + 8, px + 14, y1 - int(h * 0.16)], fill=(232, 226, 210))
    d.rectangle([x0 + 30, y1 - int(h * 0.16), x1 - 30, y1 - int(h * 0.08)], fill=(200, 194, 178))
    d.rectangle([x0 + 20, y1 - int(h * 0.08), x1 - 20, y1], fill=(90, 86, 80))
    # gavel
    gx, gy = x0 + 238, y1 - int(h * 0.42)
    d.polygon([(gx, gy), (gx + 34, gy + 22), (gx + 28, gy + 30), (gx - 6, gy + 8)], fill=(146, 100, 56))
    d.rectangle([gx - 8, gy - 6, gx + 16, gy + 8], fill=(120, 80, 40))

def art_gaza(d, box):
    _sky(d, box, (120, 84, 74), (226, 168, 110))
    x0, y0, x1, y1 = box
    _sun(d, x0 + 52, y0 + 30, 15, (250, 214, 140))
    # dense skyline, some blocks broken
    hs = [58, 84, 44, 96, 66, 52, 88, 40, 70, 56]
    bw = (x1 - x0) // len(hs)
    for i, h in enumerate(hs):
        col = (74, 62, 58) if i % 3 else (88, 74, 66)
        d.rectangle([x0 + i * bw + 2, y1 - h, x0 + (i + 1) * bw - 2, y1], fill=col)
        if i == 3:
            d.polygon([(x0 + i * bw + 2, y1 - h), (x0 + i * bw + bw // 2, y1 - h + 16), (x0 + (i + 1) * bw - 2, y1 - h)], fill=(120, 84, 74))
    d.rectangle([x0, y1 - 8, x1, y1], fill=(48, 40, 38))
    # smoke columns
    for ox in (120, 236):
        for r, oy in [(16, -70), (12, -92), (9, -110)]:
            d.ellipse([x0 + ox - r, y1 + oy - r, x0 + ox + r, y1 + oy + r], fill=(104, 94, 90))

ART = {
    "summit": art_summit, "missiles": art_missiles, "strike": art_strike,
    "quake": art_quake, "cricket": art_cricket, "plane": art_plane,
    "bitcoin": art_bitcoin, "fire": art_fire, "f1": art_f1,
    "space": art_space, "servers": art_servers, "train": art_train,
    "weather": art_weather, "jail": art_jail, "court": art_court,
    "gaza": art_gaza,
}

# ---------------------------------------------------------------- page layout

def draw_art_panel(img, story, x, y, w, h, lead=False):
    """Illustrated panel with ALL-CAPS banner label + source tag on the art.
    Overlay strips scale with panel height so the art stays visible."""
    panel = Image.new("RGB", (w, h), (200, 200, 200))
    pd = ImageDraw.Draw(panel)
    ART[story["art"]](pd, (0, 0, w, h))
    bf_size = 17 if h >= 80 else (14 if h >= 52 else 12)
    bh = bf_size + 7
    bf = F_b(bf_size)
    label = story["banner"]
    lw = tw(pd, label, bf) + 14
    pd.rectangle([0, 0, lw, bh], fill=(16, 15, 13))
    pd.text((7, 3), label, font=bf, fill=(255, 214, 110))
    sf_size = 11 if h >= 52 else 9
    sf = F_b(sf_size)
    stag = story["source"]
    sw = tw(pd, stag, sf) + 10
    pd.rectangle([w - sw, h - (sf_size + 6), w, h], fill=(16, 15, 13))
    pd.text((w - sw + 5, h - (sf_size + 4)), stag, font=sf, fill=(245, 242, 232))
    nf = F_b(bf_size)
    n = str(story["num"])
    nw = tw(pd, n, nf) + 12
    pd.rectangle([w - nw, 0, w, bh], fill=RED)
    pd.text((w - nw + 6, 3), n, font=nf, fill=WHITE)
    img.paste(panel, (x, y))

def draw_lead(img, d, story, x, y, w):
    ah = 78
    draw_art_panel(img, story, x, y, w, ah, lead=True)
    cy = y + ah + 5
    d.text((x, cy), story["place"], font=F_b(13), fill=RED)
    cy += 17
    hf = F_cond_b(37)
    for ln in wrap(d, story["headline"], hf, w)[:2]:
        d.text((x, cy), ln, font=hf, fill=INK)
        cy += 34
    ff = fit_font(d, story["fact"], F_b, 15, w, floor=11)
    d.text((x, cy + 1), story["fact"], font=ff, fill=DARKRED)
    cy += 19
    sf = F_r(13)
    for ln in wrap(d, story["summary"], sf, w)[:2]:
        d.text((x, cy), ln, font=sf, fill=(52, 48, 42))
        cy += 15
    return cy

def draw_dispatch(img, d, story, x, y, w):
    ah = 47
    draw_art_panel(img, story, x, y, w, ah)
    cy = y + ah + 4
    d.text((x, cy), story["place"], font=F_b(11), fill=RED)
    cy += 15
    hf = F_cond_b(36)
    for ln in wrap(d, story["headline"], hf, w)[:2]:
        d.text((x, cy), ln, font=hf, fill=INK)
        cy += 33
    ff = fit_font(d, story["fact"], F_b, 13, w, floor=10)
    d.text((x, cy + 1), story["fact"], font=ff, fill=DARKRED)
    return cy + 15

def main():
    img = Image.new("RGB", (W, 1024), CREAM)
    d = ImageDraw.Draw(img)

    # ---- header
    y = 14
    d.text((MARGIN, y), DATA["kicker_left"], font=F_b(18), fill=INK)
    kr = DATA["kicker_right"]
    d.text((W - MARGIN - tw(d, kr, F_b(18)), y), kr, font=F_b(18), fill=RED)
    y += 22
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=3)
    y += 6
    df = fit_font(d, DATA["date_line"], F_cond_b, 78, CW, floor=60)
    d.text((MARGIN, y), DATA["date_line"], font=df, fill=INK)
    y += 76
    sf = fit_font(d, DATA["strap"], F_cond_bi, 26, CW, floor=18)
    d.text((MARGIN, y), DATA["strap"], font=sf, fill=DARKRED)
    y += 26
    d.line([MARGIN, y, W - MARGIN, y], fill=LINE, width=1)
    y += 6
    stats = DATA["stats"]
    cellw = CW // 6
    for i, s in enumerate(stats):
        sx = MARGIN + i * cellw
        if i:
            d.line([sx - 8, y + 2, sx - 8, y + 44], fill=LINE, width=1)
        vf = fit_font(d, s["value"], F_cond_b, 28, cellw - 14, floor=20)
        d.text((sx, y), s["value"], font=vf, fill=INK)
        d.text((sx, y + 29), s["label"], font=F_r(12), fill=MUTED)
    y += 38
    d.line([MARGIN, y, W - MARGIN, y], fill=LINE, width=1)
    y += 5
    rf = fit_font(d, DATA["regions"], F_b, 18, CW, floor=13)
    d.text((MARGIN + (CW - tw(d, DATA["regions"], rf)) / 2, y), DATA["regions"], font=rf, fill=INK)
    y += 19
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 7

    # ---- leads
    leads = DATA["leads"]
    lw = (CW - 24) // 3
    lend = y
    for i, st in enumerate(leads):
        lend = max(lend, draw_lead(img, d, st, MARGIN + i * (lw + 12), y, lw))
    y = lend + 5
    d.line([MARGIN, y, W - MARGIN, y], fill=LINE, width=1)
    y += 5

    # ---- dispatch grid: two rows of five
    disp = DATA["dispatches"]
    for row in [disp[0:5], disp[5:10]]:
        n = len(row)
        gap = 12
        cw_ = (CW - gap * (n - 1)) // n
        rend = y
        for i, st in enumerate(row):
            rend = max(rend, draw_dispatch(img, d, st, MARGIN + i * (cw_ + gap), y, cw_))
        y = rend + 5

    # ---- DATE CHECK box (full width, two columns)
    d.line([MARGIN, y, W - MARGIN, y], fill=LINE, width=1)
    y += 5
    box_top = y
    d.rectangle([MARGIN, box_top, W - MARGIN, box_top + 30], fill=RED)
    hf = fit_font(d, "DATE CHECK - VERIFIED, BUT NOT SATURDAY", F_b, 24, CW - 20, floor=16)
    d.text((MARGIN + 10, box_top + 3), "DATE CHECK - VERIFIED, BUT NOT SATURDAY", font=hf, fill=WHITE)
    iy = box_top + 36
    d.text((MARGIN + 10, iy), DATA["box_sub"], font=F_i(12), fill=DARKRED)
    iy += 17
    items = DATA["box"]
    colw = (CW - 26) // 2
    col_ends = []
    for ci, chunk in enumerate([items[:3], items[3:]]):
        bx = MARGIN + 10 + ci * (colw + 6)
        cy = iy
        itf = F_cond_sb(24)
        for item in chunk:
            for ln in wrap(d, item, itf, colw):
                d.text((bx, cy), ln, font=itf, fill=INK)
                cy += 23
            cy += 0
        col_ends.append(cy)
    box_bot = max(col_ends) + 3
    d.rectangle([MARGIN, box_top, W - MARGIN, box_bot], outline=RED, width=2)
    y = box_bot + 8

    # ---- briefs, four columns
    d.text((MARGIN, y), "ALSO SATURDAY - IN BRIEF", font=F_b(14), fill=INK)
    y += 19
    bf = F_r(11)
    briefs = DATA["briefs"]
    ncol = 4
    per = (len(briefs) + ncol - 1) // ncol
    colw = (CW - 18 * (ncol - 1)) // ncol
    bend = y
    for ci in range(ncol):
        chunk = briefs[ci * per:(ci + 1) * per]
        bx = MARGIN + ci * (colw + 18)
        cy = y
        for j, btext in enumerate(chunk):
            num = ci * per + j + 1
            lines = wrap(d, btext, bf, colw - 22)
            d.text((bx, cy), str(num) + ".", font=F_b(11), fill=RED)
            for ln in lines:
                d.text((bx + 20, cy), ln, font=bf, fill=(52, 48, 42))
                cy += 11
            cy += 2
        bend = max(bend, cy)
    y = bend + 4
    # not-yet line + footer
    nf = fit_font(d, DATA["notyet"], F_b, 12, CW, floor=10)
    d.text((MARGIN, y), DATA["notyet"], font=nf, fill=DARKRED)
    y += 16
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 4
    ff = fit_font(d, DATA["footer"], F_r, 11, CW, floor=9)
    d.text((MARGIN, y), DATA["footer"], font=ff, fill=MUTED)
    y += 12
    print("layout height:", y)

    img.convert("P", palette=Image.ADAPTIVE, colors=192).save(os.path.join(HERE, "entry.png"))
    img.resize((512, 512), Image.LANCZOS).save(os.path.join(HERE, "entry-512.png"))
    img.resize((300, 300), Image.LANCZOS).save(os.path.join(HERE, "entry-300.png"))
    print("entry.png bytes:", os.path.getsize(os.path.join(HERE, "entry.png")))

if __name__ == "__main__":
    main()
