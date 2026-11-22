#!/usr/bin/env python3
"""Fresh renderer for news-image-20261121 evolved candidate.
Original flat-shape art drawn in code; layout rebuilt from the brief spec."""
import json, math, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/truetype/noto"
FL = "/usr/share/fonts/truetype/liberation"

def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)
def FLF(name, size):
    return ImageFont.truetype(os.path.join(FL, name), size)

XC_B   = "NotoSans-ExtraCondensedBold.ttf"
XC_SB  = "NotoSans-ExtraCondensedSemiBold.ttf"
C_B    = "NotoSans-CondensedBold.ttf"
C_SB   = "NotoSans-CondensedSemiBold.ttf"
C_R    = "NotoSans-Condensed.ttf"
C_M    = "NotoSans-CondensedMedium.ttf"

CREAM = (243, 234, 211); PAPER = (247, 240, 219)
INK   = (26, 23, 18);    RED   = (158, 32, 22)
DRED  = (120, 24, 16);   GOLD  = (232, 179, 60)
WHITE = (250, 247, 238); GREY  = (90, 84, 72)

W, H, M = 1024, 1024, 14

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def fit_lines(d, text, font, maxw, max_lines=6):
    return wrap(d, text, font, maxw)[:max_lines]

# ---------------------------------------------------------------- art panels
def burst(d, cx, cy, r, col):
    for k in range(8):
        a = k * math.pi / 4
        d.line([cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)], fill=col, width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=col)

def art_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 74, 96))
    d.pieslice([x + w*0.28, y + h*0.25, x + w*0.72, y + h*1.15], 180, 360, fill=(214, 196, 150))
    d.rectangle([x + w*0.28, y + h*0.78, x + w*0.72, y + h], fill=(160, 140, 100))
    for i, c in enumerate([(200,60,50),(60,110,200),(240,200,60),(80,170,90),(230,230,230)]):
        fx = x + 14 + i * 26
        d.line([fx, y + h - 4, fx, y + 22], fill=WHITE, width=2)
        d.rectangle([fx, y + 22, fx + 18, y + 32], fill=c)
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(24, 48, 62))

def art_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 20, 44))
    for bx, bw, bh in [(0.05,0.10,0.45),(0.18,0.07,0.65),(0.28,0.12,0.35),(0.55,0.08,0.55),(0.66,0.13,0.40),(0.82,0.09,0.60)]:
        d.rectangle([x + w*bx, y + h*(1-bh), x + w*(bx+bw), y + h], fill=(8, 10, 26))
        for wy in range(3):
            d.point((x + w*bx + 4, y + h*(1-bh) + 5 + wy*7), fill=GOLD)
    for sx, sy in [(0.35, 0.30), (0.60, 0.22), (0.78, 0.38)]:
        d.arc([x + w*sx - 34, y + h*sy - 12, x + w*sx + 34, y + h*sy + 40], 200, 330, fill=(240, 120, 60), width=2)
        burst(d, x + w*sx, y + h*sy, 11, GOLD)
    d.line([x + 6, y + h - 8, x + w*0.33, y + h*0.32], fill=(200, 200, 210), width=1)

def art_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(104, 96, 92))
    for i, (bx, bh) in enumerate([(0.06,0.62),(0.24,0.78),(0.44,0.55),(0.62,0.72),(0.80,0.60)]):
        col = (70, 64, 60) if i % 2 else (84, 78, 74)
        d.rectangle([x + w*bx, y + h*(1-bh), x + w*bx + w*0.15, y + h], fill=col)
        d.polygon([(x + w*bx + 4, y + h*(1-bh)), (x + w*bx + w*0.07, y + h*(1-bh) - 8), (x + w*bx + w*0.13, y + h*(1-bh))], fill=(50, 46, 44))
    for gx, gy in [(0.30, 0.30), (0.52, 0.22), (0.72, 0.34)]:
        d.ellipse([x + w*gx, y + h*gy, x + w*gx + 26, y + h*gy + 12], fill=(150, 144, 138))
    hx, hy = x + w*0.86, y + h*0.52
    d.rectangle([hx - 9, hy - 9, hx + 9, hy + 9], fill=WHITE)
    d.rectangle([hx - 3, hy - 7, hx + 3, hy + 7], fill=(200, 40, 30))
    d.rectangle([hx - 7, hy - 3, hx + 7, hy + 3], fill=(200, 40, 30))
    d.rectangle([x, y + h - 5, x + w, y + h], fill=(52, 48, 46))

def art_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(126, 96, 66))
    d.polygon([(x, y+h), (x+w*0.25, y+6), (x+w*0.45, y+h)], fill=(96, 70, 48))
    d.polygon([(x+w*0.30, y+h), (x+w*0.55, y+2), (x+w*0.80, y+h)], fill=(110, 82, 54))
    d.polygon([(x+w*0.58, y+h), (x+w*0.82, y+10), (x+w, y+h)], fill=(88, 64, 42))
    pts = [(x+w*0.42, y+h-3), (x+w*0.47, y+h-11), (x+w*0.45, y+h-17), (x+w*0.52, y+h-25)]
    d.line(pts, fill=(30, 22, 16), width=2)
    d.line([(x+w*0.47, y+h-11), (x+w*0.55, y+h-13)], fill=(30, 22, 16), width=1)

def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 110, 62))
    d.rectangle([x + w*0.38, y + 4, x + w*0.62, y + h - 4], fill=(206, 184, 130))
    for sx in (0.44, 0.56):
        for k in range(3):
            d.line([x + w*sx + k*4 - 4, y + 8, x + w*sx + k*4 - 4, y + 17], fill=(240, 230, 200), width=2)
    d.line([x + w*0.70, y + h - 10, x + w*0.78, y + 10], fill=(120, 80, 40), width=3)
    d.ellipse([x + w*0.30, y + h*0.45, x + w*0.30 + 7, y + h*0.45 + 7], fill=(200, 40, 40))

def art_davao(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 120, 168))
    d.rectangle([x, y + h - 9, x + w, y + h], fill=(60, 60, 64))
    d.polygon([(x+w*0.16, y+h*0.52), (x+w*0.62, y+h*0.34), (x+w*0.80, y+h*0.40), (x+w*0.66, y+h*0.55), (x+w*0.24, y+h*0.66)], fill=(228, 230, 234))
    d.polygon([(x+w*0.40, y+h*0.38), (x+w*0.52, y+h*0.16), (x+w*0.60, y+h*0.36)], fill=(200, 204, 210))
    d.ellipse([x+w*0.60, y+h*0.44, x+w*0.72, y+h*0.60], outline=(255, 140, 40), width=2)
    burst(d, x + w*0.66, y + h*0.52, 6, (255, 160, 50))
    d.polygon([(x+w*0.24, y+h*0.62), (x+w*0.34, y+h-9), (x+w*0.42, y+h-9)], fill=(240, 190, 60))

def art_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 22, 30))
    pts = [(x+6, y+8), (x+w*0.25, y+12), (x+w*0.42, y+7), (x+w*0.60, y+h*0.55), (x+w*0.78, y+h*0.62), (x+w-8, y+h-7)]
    d.line(pts, fill=(230, 70, 50), width=2)
    d.polygon([(x+w-8, y+h-7), (x+w-18, y+h-12), (x+w-14, y+h-2)], fill=(230, 70, 50))
    cx, cy, r = x + w*0.30, y + h*0.60, min(w, h)*0.25
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(240, 150, 30))
    fnt = F(XC_B, int(r*1.2))
    d.text((cx, cy), "B", font=fnt, fill=(60, 34, 4), anchor="mm")

def art_palisades(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 52, 44))
    d.polygon([(x, y+h), (x+w*0.4, y+h*0.30), (x+w, y+h*0.55), (x+w, y+h)], fill=(46, 36, 32))
    for hx, hy, s in [(0.16, 0.52, 16), (0.48, 0.42, 13), (0.74, 0.55, 15)]:
        d.rectangle([x+w*hx, y+h*hy, x+w*hx+s, y+h*hy+s*0.7], fill=(210, 200, 188))
        d.polygon([(x+w*hx-2, y+h*hy), (x+w*hx+s/2, y+h*hy-6), (x+w*hx+s+2, y+h*hy)], fill=(90, 40, 30))
        for fx in range(3):
            d.polygon([(x+w*hx+2+fx*5, y+h*hy-2), (x+w*hx+4+fx*5, y+h*hy-11), (x+w*hx+7+fx*5, y+h*hy-2)], fill=(245, 130, 30))

def art_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 14, 26))
    for i in range(6):
        d.point((x + 10 + i*30, y + 6 + (i % 2)*4), fill=(220, 220, 235))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(30, 30, 38))
    d.line([x, y + h - 9, x + w, y + h - 9], fill=(200, 50, 40), width=1)
    bx, by = x + w*0.22, y + h*0.52
    d.polygon([(bx, by+8), (bx+w*0.14, by), (bx+w*0.34, by+1), (bx+w*0.46, by+7), (bx+w*0.40, by+11), (bx+6, by+11)], fill=(30, 90, 200))
    d.rectangle([bx-4, by+4, bx+2, by+13], fill=(16, 16, 20))
    d.rectangle([bx+w*0.44, by+3, bx+w*0.50, by+13], fill=(16, 16, 20))
    for wx in (bx + 8, bx + w*0.36):
        d.ellipse([wx, by+9, wx+11, by+18], fill=(10, 10, 12))

def art_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 26))
    for i in range(8):
        d.point((x + 8 + i*23, y + 5 + (i*7) % 12), fill=(210, 210, 225))
    cx, cy, r = x + w*0.34, y + h*0.55, min(h*0.34, 15)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(168, 152, 138))
    d.ellipse([cx-r*0.5, cy-r*0.4, cx-r*0.1, cy], fill=(140, 126, 114))
    d.arc([x+w*0.10, y+3, x+w*0.92, y+h-3], 300, 130, fill=(150, 180, 230), width=1)
    sx, sy = x + w*0.74, y + h*0.30
    d.rectangle([sx-7, sy-3, sx+7, sy+3], fill=(200, 204, 214))
    d.rectangle([sx-16, sy-2, sx-8, sy+2], fill=(70, 110, 200))
    d.rectangle([sx+8, sy-2, sx+16, sy+2], fill=(70, 110, 200))

def art_euid(d, x, y, w, h):
    # NEW: EU star circle + Indonesian red/white flag over a signed document
    d.rectangle([x, y, x + w, y + h], fill=(36, 54, 96))
    cx, cy = x + w*0.24, y + h*0.50
    for k in range(8):
        a = k * math.pi / 4 - math.pi/2
        sx, sy = cx + 11*math.cos(a), cy + 11*math.sin(a)
        d.polygon([(sx, sy-3), (sx+3, sy+3), (sx-3, sy+3)], fill=GOLD)
    fx, fy, fw, fh = x + w*0.46, y + h*0.16, w*0.30, h*0.42
    d.rectangle([fx, fy, fx+fw, fy+fh//2], fill=(206, 40, 44))
    d.rectangle([fx, fy+fh//2, fx+fw, fy+fh], fill=(242, 242, 240))
    d.line([fx, fy, fx, fy+fh], fill=WHITE, width=2)
    dx, dy, dw, dh = x + w*0.52, y + h*0.60, w*0.42, h*0.34
    d.rectangle([dx, dy, dx+dw, dy+dh], fill=(244, 240, 228))
    d.line([dx+4, dy+5, dx+dw-10, dy+5], fill=(120, 116, 106), width=1)
    d.line([dx+4, dy+9, dx+dw-16, dy+9], fill=(120, 116, 106), width=1)
    d.arc([dx+dw-20, dy+dh-11, dx+dw-4, dy+dh-2], 200, 520, fill=RED, width=2)

def art_banda(d, x, y, w, h):
    # NEW: sea waves, island silhouettes, seismic ring/star (no mountains)
    d.rectangle([x, y, x + w, y + h], fill=(18, 84, 110))
    for row, off in enumerate((0.30, 0.52, 0.74)):
        pts = []
        for px in range(0, int(w)+8, 8):
            pts.append((x+px, y + h*off + 3*math.sin((px+off*40)/11.0)))
        d.line(pts, fill=(120, 205, 225), width=2)
    d.polygon([(x+w*0.08, y+h*0.30), (x+w*0.20, y+h*0.20), (x+w*0.34, y+h*0.30)], fill=(14, 52, 40))
    d.polygon([(x+w*0.66, y+h*0.28), (x+w*0.78, y+h*0.19), (x+w*0.92, y+h*0.28)], fill=(14, 52, 40))
    cx, cy = x + w*0.50, y + h*0.62
    for r in (5, 10, 15):
        d.ellipse([cx-r, cy-r*0.55, cx+r, cy+r*0.55], outline=(250, 200, 70), width=2)
    burst(d, cx, cy, 6, (250, 210, 80))

def art_geneva(d, x, y, w, h):
    # NEW: robot head silhouette with document / gavel
    d.rectangle([x, y, x + w, y + h], fill=(52, 56, 66))
    cx, cy = x + w*0.34, y + h*0.54
    d.rectangle([cx-13, cy-11, cx+13, cy+11], fill=(168, 176, 188))
    d.line([cx, cy-11, cx, cy-17], fill=(200, 204, 214), width=2)
    d.ellipse([cx-2, cy-19, cx+2, cy-15], fill=(230, 70, 50))
    d.ellipse([cx-8, cy-4, cx-3, cy+1], fill=(20, 30, 40))
    d.ellipse([cx+3, cy-4, cx+8, cy+1], fill=(20, 30, 40))
    d.rectangle([cx-6, cy+5, cx+6, cy+7], fill=(90, 96, 106))
    dx, dy = x + w*0.60, y + h*0.18
    d.rectangle([dx, dy, dx+w*0.30, dy+h*0.62], fill=(244, 240, 228))
    d.line([dx+4, dy+6, dx+w*0.30-5, dy+6], fill=(120, 116, 106), width=1)
    d.line([dx+4, dy+11, dx+w*0.30-9, dy+11], fill=(120, 116, 106), width=1)
    gx, gy = x + w*0.66, y + h*0.80
    d.line([gx, gy, gx+16, gy-8], fill=(150, 105, 55), width=3)
    d.rectangle([gx+13, gy-13, gx+21, gy-5], fill=(120, 82, 40))

ART = {"cop": art_cop, "riyadh": art_riyadh, "kryvyi": art_kryvyi, "peru": art_peru,
       "cricket": art_cricket, "davao": art_davao, "bitcoin": art_bitcoin,
       "palisades": art_palisades, "f1": art_f1, "mercury": art_mercury,
       "euid": art_euid, "banda": art_banda, "geneva": art_geneva}

def panel(d, card, x, y, w, h, lead=False):
    d.rectangle([x, y, x+w, y+h], fill=INK)
    ART[card["art"]](d, x, y, w, h)
    bh = 19 if lead else 15
    d.rectangle([x, y, x+w, y+bh], fill=(12, 11, 10))
    bf = F(C_B, 14 if lead else 11)
    d.text((x+5, y+bh//2), card["banner"], font=bf, fill=GOLD, anchor="lm")
    # number chip
    cf = F(XC_B, 15 if lead else 12)
    cw = d.textlength(str(card["num"]), font=cf) + 10
    d.rectangle([x+w-cw, y, x+w, y+bh], fill=RED)
    d.text((x+w-cw/2, y+bh//2), str(card["num"]), font=cf, fill=WHITE, anchor="mm")
    # source tag bottom right
    sf = F(C_B, 10 if lead else 8)
    sw = d.textlength(card["source"], font=sf) + 8
    d.rectangle([x+w-sw, y+h-13, x+w, y+h], fill=(12, 11, 10))
    d.text((x+w-4, y+h-6), card["source"], font=sf, fill=WHITE, anchor="rm")

def main():
    data = json.load(open(os.path.join(HERE, "data_evolved.json"), encoding="utf-8"))
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    y = 8
    # header
    kf = F(C_B, 16)
    d.text((M, y), data["kicker_left"], font=kf, fill=INK)
    d.text((W-M, y), data["kicker_right"], font=kf, fill=RED, anchor="ra")
    y += 22
    d.line([M, y, W-M, y], fill=INK, width=2); y += 4
    d.text((M, y), data["date_line"], font=F(XC_B, 78), fill=INK)
    y += 78
    d.text((M, y), data["strap"], font=FLF("LiberationSerif-BoldItalic.ttf", 21), fill=RED)
    y += 22
    d.line([M, y, W-M, y], fill=INK, width=1); y += 3
    # stat band
    sw = (W - 2*M) / 6.0
    vf, lf = F(XC_B, 29), F(C_R, 11)
    for i, s in enumerate(data["stats"]):
        sx = M + i*sw
        d.text((sx+2, y), s["value"], font=vf, fill=INK)
        d.text((sx+2, y+31), s["label"], font=lf, fill=GREY)
        if i: d.line([sx, y+2, sx, y+40], fill=(190, 178, 150), width=1)
    y += 43
    # region strip
    d.rectangle([M, y, W-M, y+21], fill=INK)
    d.text((W//2, y+10), data["region_strip"], font=F(XC_SB, 15), fill=CREAM, anchor="mm")
    y += 21
    # leads
    gap = 8; lw = (W - 2*M - 2*gap) / 3.0
    pf, hf = F(C_B, 12), F(XC_B, 37)
    ff, sf2 = F(C_SB, 12), F(C_R, 12)
    lead_h = 0
    rendered = []
    for i, c in enumerate(data["leads"]):
        hl = wrap(d, c["headline"], hf, lw)
        fl = wrap(d, c["fact"], ff, lw); sl = wrap(d, c["summary"], sf2, lw)
        hh = 52 + 15 + len(hl)*36 + 9 + len(fl)*14 + len(sl)*14
        rendered.append((hl, fl, sl)); lead_h = max(lead_h, hh)
    for i, c in enumerate(data["leads"]):
        x = M + i*(lw+gap); cy = y
        panel(d, c, x, cy, lw, 52, lead=True); cy += 55
        d.text((x, cy), c["place"], font=pf, fill=RED); cy += 15
        hl, fl, sl = rendered[i]
        for ln in hl: d.text((x, cy), ln, font=hf, fill=INK); cy += 36
        cy += 9
        for ln in fl: d.text((x, cy), ln, font=ff, fill=DRED); cy += 14
        for ln in sl: d.text((x, cy), ln, font=sf2, fill=INK); cy += 14
    y += lead_h + 3
    d.line([M, y, W-M, y], fill=INK, width=1); y += 5
    # dispatches: 2 rows of 5
    dgap = 6; dw = (W - 2*M - 4*dgap) / 5.0
    dpf, dhf, dff = F(C_B, 11), F(XC_B, 36), F(C_SB, 11)
    for row in range(2):
        cards = data["dispatches"][row*5:(row+1)*5]
        pre, rh = [], 0
        for c in cards:
            hl = wrap(d, c["headline"], dhf, dw)
            fl = wrap(d, c["fact"], dff, dw)
            hh = 36 + 14 + len(hl)*35 + 9 + len(fl)*13
            pre.append((hl, fl)); rh = max(rh, hh)
        for i, c in enumerate(cards):
            x = M + i*(dw+dgap); cy = y
            panel(d, c, x, cy, dw, 36); cy += 39
            pl = wrap(d, c["place"], dpf, dw)
            for ln in pl: d.text((x, cy), ln, font=dpf, fill=RED); cy += 13
            hl, fl = pre[i]
            for ln in hl: d.text((x, cy), ln, font=dhf, fill=INK); cy += 35
            cy += 2
            for ln in fl: d.text((x, cy), ln, font=dff, fill=DRED); cy += 13
        y += rh + 3
    # date check box
    d.rectangle([M, y, W-M, y+30], fill=RED)
    d.text((M+8, y+15), data["datecheck_heading"], font=F(XC_B, 24), fill=WHITE, anchor="lm")
    y += 30
    box_top = y
    d.rectangle([M, box_top, W-M, box_top+100], outline=RED, width=2)
    d.text((M+8, box_top+3), data["datecheck_sub"], font=FLF("LiberationSerif-Italic.ttf", 14), fill=DRED)
    itf = F(C_SB, 24)
    colw = (W - 2*M - 20) / 2.0
    for j, it in enumerate(data["datecheck_left"]):
        d.text((M+8, box_top+19+j*27), it, font=itf, fill=INK)
    for j, it in enumerate(data["datecheck_right"]):
        d.text((M+12+colw, box_top+19+j*27), it, font=itf, fill=INK)
    y = box_top + 103
    # briefs
    d.text((M, y), data["briefs_heading"], font=F(C_B, 13), fill=RED); y += 14
    bw = (W - 2*M - 2*10) / 3.0
    bf2 = F(C_R, 11)
    cols = [data["briefs"][0:4], data["briefs"][4:8], data["briefs"][8:12]]
    maxh = 0
    for ci, col in enumerate(cols):
        x = M + ci*(bw+10); cy = y
        for k, b in enumerate(col):
            n = ci*4 + k + 1
            lines = wrap(d, b, bf2, bw-16)
            d.text((x, cy), f"{n}.", font=F(C_B, 11), fill=RED)
            for ln in lines: d.text((x+16, cy), ln, font=bf2, fill=INK); cy += 13
            cy += 2
        maxh = max(maxh, cy-y)
    y += maxh + 1
    # not yet + footer
    nyf = F(XC_SB, 12)
    for ln in wrap(d, data["not_yet"], nyf, W-2*M):
        d.text((M, y), ln, font=nyf, fill=RED); y += 14
    y += 1
    ftf = F(C_R, 10)
    for ln in wrap(d, data["footer"], ftf, W-2*M):
        d.text((W//2, y), ln, font=ftf, fill=GREY, anchor="ma"); y += 12
    print("final_y:", y)
    assert y <= 1022, f"overflow: {y}"
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    img.resize((512, 512), Image.LANCZOS).save(os.path.join(HERE, "entry-512.png"), optimize=True)
    img.resize((300, 300), Image.LANCZOS).save(os.path.join(HERE, "entry-300.png"), optimize=True)

if __name__ == "__main__":
    main()
