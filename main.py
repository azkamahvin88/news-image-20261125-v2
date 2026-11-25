#!/usr/bin/env python3
"""news-image-20261125 round 2 — one-page newspaper of Wednesday 25 Nov 2026.

Draws entry.png (1024x1024) deterministically with Pillow from the story
data embedded below. No network, no wall-clock, no unseeded randomness.
If Pillow is unavailable, falls back to copying the shipped entry.png.
Run:  MAKEFUN_OUTPUT_DIR=. python3 main.py   (writes ./entry.png)
"""
import os
import shutil
import sys

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (20, 20, 20)
MAROON = (122, 31, 31)
NAVY = (29, 53, 87)
GOLD = (150, 110, 20)
RULE = (120, 110, 90)

BADGE = {
    "OFFICIAL": (29, 53, 87),
    "CONFIRMED": (30, 107, 52),
    "REPORTED": (138, 90, 0),
    "CLAIM": (178, 34, 34),
}

REGION_COLORS = {
    "EUROPE": (29, 53, 87),
    "ASIA": (122, 31, 31),
    "MIDDLE EAST": (179, 84, 30),
    "AFRICA": (46, 107, 52),
    "AMERICAS": (106, 76, 147),
    "OCEANIA": (14, 124, 123),
    "GLOBAL": (85, 85, 85),
}

# ---- story data -----------------------------------------------------------
# lead: 1-3 big; medium: 4-13; also: 14-38 one-liners.
# rep = first reported, UTC. conf = OFFICIAL / CONFIRMED / REPORTED / CLAIM.

LEADS = [
    dict(n=1, region="ASIA", conf="OFFICIAL", rep="00:18",
         head="PAKISTAN'S FIRST ASTRONAUT REACHES TIANGONG",
         body=("Shenzhou-24 lifted off from Jiuquan at 00:18 UTC and docked with China's "
               "Tiangong station at 03:56 UTC. Payload specialist Muhammad Zeeshan Ali, "
               "40, is the first Pakistani in orbit and the first foreigner ever to "
               "board Tiangong."),
         src="CMSA / Xinhua / Reuters", scene="rocket"),
    dict(n=2, region="ASIA", conf="CONFIRMED", rep="06:30",
         head="KOSPI CRASHES 6.2% AS THE CHIP RALLY UNWINDS",
         body=("Seoul's Kospi closed at 4,697.51, down 6.16% to a 10-month low, erasing "
               "Tuesday's rebound. Samsung fell 9.9% and SK Hynix 11.1%; "
               "SoftBank slid 14.8%."),
         src="Korea Exchange / Reuters / WSJ", scene="chart"),
    dict(n=3, region="MIDDLE EAST", conf="CLAIM", rep="09:46",
         head="TWO TANKERS HIT MINES IN HORMUZ, IRGC SAYS",
         body=("Iran's Revolutionary Guards Navy said two oil tankers struck naval mines, "
               "exploded and caught fire off the southern and eastern coasts of the "
               "strait. No names or casualty details were given."),
         src="IRGC via IRNA / Reuters", scene="tanker"),
]

MEDIUM = [
    dict(n=4, region="MIDDLE EAST", conf="CONFIRMED", rep="00:10",
         head="SAUDI COALITION STRIKES HODEIDAH PORT",
         body="Six strikes hit the Yemeni port after an evacuation warning; Saada and Amran hit too.",
         src="SPA / AFP", scene="strike"),
    dict(n=5, region="OCEANIA", conf="OFFICIAL", rep="06:30",
         head="SOLOMONS PICK AUSTRALIA AS TOP SECURITY PARTNER",
         body="Canberra treaty: no foreign base on Solomons soil; A$740m over a decade.",
         src="PM of Australia / Reuters", scene="treaty"),
    dict(n=6, region="ASIA", conf="CONFIRMED", rep="07:20",
         head="GARMENT WORKERS WIN 36% PAY RISE",
         body="Minimum wage rises to 17,000 taka ($136) after weeks of protests.",
         src="Reuters / AP", scene="sewing"),
    dict(n=7, region="ASIA", conf="CONFIRMED", rep="04:00",
         head="26 TRAPPED IN FLOODED JAVA GOLD MINE",
         body="Illegal 100m pit near Bogor flooded Monday; three bodies found, 11 escaped.",
         src="Reuters / West Java police", scene="mine"),
    dict(n=8, region="AMERICAS", conf="CONFIRMED", rep="06:45",
         head="HUAWEI GUILTY ON 10 OF 12 US COUNTS",
         body="Brooklyn jury convicts on fraud, sanctions and trade-secret theft; verdict Tue.",
         src="Reuters / US DOJ", scene="court"),
    dict(n=9, region="AFRICA", conf="OFFICIAL", rep="10:30",
         head="WHO PULLS EBOLA TEAMS FROM CONGO HOSPITAL",
         body="Staff left Akwe hospital in Ituri after three days sheltering from fighting.",
         src="WHO", scene="clinic"),
    dict(n=10, region="EUROPE", conf="REPORTED", rep="08:00",
         head="KYIV SEA DRONES SINK RUSSIAN WARSHIP OFF LIBYA",
         body="Ukrainian naval drones strike a Russian warship off the Libyan coast.",
         src="Reuters", scene="drone"),
    dict(n=11, region="EUROPE", conf="CONFIRMED", rep="09:00",
         head="NATO SENDS EARLY-WARNING JETS TO POLAND",
         body="Alliance moves AWACS jets east to watch skies over Poland and the Baltic.",
         src="Reuters", scene="jet"),
    dict(n=12, region="AMERICAS", conf="OFFICIAL", rep="15:00",
         head="TRUMP PARDONS TURKEYS FREEDOM AND FEATHERS",
         body="The White House Thanksgiving pardon spares two birds; both retire to a farm.",
         src="AP", scene="turkey"),
    dict(n=13, region="AFRICA", conf="CONFIRMED", rep="11:00",
         head="SENEGAL GET AFCON TITLE BACK AFTER CAS RULING",
         body="Sport's top court restores Senegal's Africa Cup of Nations crown.",
         src="AFP", scene="trophy"),
]

ALSO = [
    (14, "EUROPE", "Putin vows retaliation over refinery strikes", "Kremlin"),
    (15, "EUROPE", "700,000+ Russian soldiers killed, leak finds", "RFE/RL"),
    (16, "EUROPE", "Russian strike on Kyiv-region flats kills 11", "RFE/RL"),
    (17, "EUROPE", "Zelenskyy: US \u201caligning with Russia\u201d", "Bloomberg"),
    (18, "AMERICAS", "Fort Hood gunman seeks stay of execution", "Reuters"),
    (19, "EUROPE", "Sarkozy and Bruni ordered to stand trial", "Reuters"),
    (20, "ASIA", "Indonesia's vice-president resigns", "Wire reports"),
    (21, "ASIA", "Xiamen Airlines orders 50 Boeing 737-8", "Reuters"),
    (22, "OCEANIA", "England beat Australia by 8 wickets, 2nd T20I", "AP"),
    (23, "AMERICAS", "Colombia car bomb wounds 23; 25 held hostage", "Reuters"),
    (24, "MIDDLE EAST", "Iran winter gas shortages bite", "DW"),
    (25, "MIDDLE EAST", "Iraq seizes Kurdish oilfields", "Reuters"),
    (26, "MIDDLE EAST", "Israeli strike kills Hamas security chief in Gaza", "BBC"),
    (27, "MIDDLE EAST", "Israel: Iran building chemical weapons", "Israel says"),
    (28, "EUROPE", "EU adopts 22nd sanctions package", "EU"),
    (29, "EUROPE", "Denmark upholds \u201cghetto\u201d evictions", "Reuters"),
    (30, "AFRICA", "Cameroon separatist leader war-crimes trial opens in Norway", "Reuters"),
    (31, "ASIA", "RFE/RL shortwave lessons for Afghan girls", "RFE/RL"),
    (32, "AMERICAS", "FBI crime database suspected breach", "Reuters"),
    (33, "AMERICAS", "O'Hare radar delays snarl US flights", "Reuters"),
    (34, "AMERICAS", "US envoy \u201cnot certain\u201d Israel military aid ends this year", "Reuters"),
    (35, "EUROPE", "NATO vows to defend against space threats", "Reuters"),
    (36, "GLOBAL", "Asteroid eclipse imaged; Vera Rubin's first pictures", "NASA"),
    (37, "GLOBAL", "Landmine victims hit five-year high", "Landmine Monitor"),
    (38, "AFRICA", "DR Congo rebels pull back from front line", "Reuters"),
]

TIMELINE = [
    ("00:10", "Coalition strikes Hodeidah port"),
    ("00:18", "Shenzhou-24 lifts off from Jiuquan"),
    ("04:00", "Java mine: 26 trapped confirmed"),
    ("06:30", "Kospi closes down 6.2%"),
    ("07:20", "Bangladesh agrees 36% wage rise"),
    ("09:46", "IRGC: two tankers hit mines"),
]

STATS = [
    ("38", "STORIES"),
    ("7", "REGIONS"),
    ("-6.2%", "KOSPI"),
    ("26", "MINERS TRAPPED"),
    ("10 of 12", "HUAWEI COUNTS"),
    ("00:18", "UTC LIFTOFF"),
]

REGIONS = [("EUROPE", 10), ("ASIA", 7), ("AMERICAS", 7), ("MIDDLE EAST", 6),
           ("AFRICA", 4), ("OCEANIA", 2), ("GLOBAL", 2)]

DATE_CHECK = [
    "Houthi drone hit on a Riyadh tower, 11 hurt \u2014 TUE 24 Nov, not today.",
    "Champions League results (Real Madrid 5-1 PSV) \u2014 TUESDAY's football.",
    "Nvidia's 31.5% surge \u2014 MONDAY 23 Nov; it fell 5.9% on Tuesday.",
    "Wed-night ties (Liverpool at Club Brugge) \u2014 not yet played at press time.",
]

FOOTER = ("Sources: Reuters, AP, AFP, Bloomberg, Xinhua/CMSA, WHO, Korea Exchange, SPA, US DOJ, "
          "RFE/RL, BBC, NASA, EU. All 38 stories happened or were first reported Wed 25 Nov 2026. "
          "Drawn from wire reports; claims are labelled as claims.")

# ---- fonts -----------------------------------------------------------------
def _font(name, size):
    from PIL import ImageFont
    cands = [
        "/usr/share/fonts/truetype/dejavu/%s" % name,
        "/usr/share/fonts/truetype/liberation/%s" % name,
        "/usr/share/fonts/truetype/noto/%s" % name,
    ]
    for p in cands:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


class Fonts:
    def __init__(self):
        self.serif_b = lambda s: _font("DejaVuSerif-Bold.ttf", s)
        self.serif = lambda s: _font("DejaVuSerif.ttf", s)
        self.serif_i = lambda s: _font("DejaVuSerif-Italic.ttf", s)
        self.sans_b = lambda s: _font("DejaVuSans-Bold.ttf", s)
        self.sans = lambda s: _font("DejaVuSans.ttf", s)


def wrap(text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if font.getlength(t) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, lines, font, fill=INK, leading=None, align="left", width=None):
    if leading is None:
        leading = font.size + 2
    for ln in lines:
        if align == "center":
            d.text((x + (width or 0) / 2, y), ln, font=font, fill=fill, anchor="ma")
        elif align == "right":
            d.text((x + (width or 0), y), ln, font=font, fill=fill, anchor="ra")
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def badge(d, x, y, label, font):
    w = int(font.getlength(label)) + 10
    h = font.size + 6
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=BADGE[label])
    d.text((x + 5, y + 3), label, font=font, fill=(255, 255, 255))
    return w


def meta_line(d, x, y, story, font):
    """'rep HH:MM · SOURCE' small caps line; returns width used."""
    s = "rep %s UTC \u00b7 %s" % (story["rep"], story["src"])
    d.text((x, y), s, font=font, fill=(90, 80, 60))
    return font.getlength(s)


# ---- scenes ----------------------------------------------------------------
STARS = [(12, 8), (60, 20), (110, 6), (150, 26), (200, 10), (250, 18), (300, 8),
         (350, 24), (400, 12), (40, 40), (180, 44), (320, 42), (90, 14), (230, 34),
         (380, 36), (140, 30), (270, 6), (30, 28), (210, 22), (360, 16)]


def scene_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 44))
    for sx, sy in STARS:
        if sx < w and sy < h:
            d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(255, 255, 220))
    # moon
    mx, my, mr = x + w - 52, y + 16, 15
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(235, 230, 200))
    d.ellipse([mx - 6, my - 4, mx + 2, my + 4], fill=(210, 205, 175))
    # station
    sx, sy = x + w - 150, y + h - 78
    d.rectangle([sx, sy, sx + 96, sy + 10], fill=(180, 190, 205))
    d.rectangle([sx + 12, sy + 3, sx + 40, sy + 7], fill=(40, 90, 160))
    d.rectangle([sx + 56, sy + 3, sx + 84, sy + 7], fill=(40, 90, 160))
    d.rectangle([sx + 40, sy - 4, sx + 56, sy + 14], fill=(220, 225, 235))
    # rocket, diagonal up
    rx, ry = x + 30, y + h - 18
    d.polygon([(rx, ry), (rx + 14, ry - 52), (rx + 28, ry)], fill=(240, 240, 240))
    d.polygon([(rx + 14, ry - 52), (rx + 20, ry - 66), (rx + 26, ry - 52)], fill=(178, 34, 34))
    d.polygon([(rx, ry), (rx - 12, ry + 12), (rx + 6, ry + 4)], fill=(178, 34, 34))
    d.polygon([(rx + 28, ry), (rx + 40, ry + 12), (rx + 22, ry + 4)], fill=(178, 34, 34))
    d.polygon([(rx + 6, ry + 4), (rx + 14, ry + 30), (rx + 22, ry + 4)], fill=(255, 170, 40))
    d.polygon([(rx + 10, ry + 4), (rx + 14, ry + 20), (rx + 18, ry + 4)], fill=(255, 230, 120))
    d.ellipse([rx + 9, ry - 40, rx + 19, ry - 30], fill=(40, 90, 160))
    # ground glow
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(255, 170, 40))


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 30))
    for i in range(1, 4):
        gy = y + i * h // 4
        d.line([x, gy, x + w, gy], fill=(70, 70, 80), width=1)
    pts = [(x + 8, y + 14), (x + w * 0.25, y + 30), (x + w * 0.45, y + 22),
           (x + w * 0.6, y + 52), (x + w * 0.75, y + 66), (x + w - 10, y + h - 14)]
    d.line(pts, fill=(230, 60, 60), width=4, joint="curve")
    for px, py in pts[1:-1]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 60))
    d.text((x + 10, y + h - 22), "-6.2%", font=_font("DejaVuSans-Bold.ttf", 20),
           fill=(255, 90, 90))
    d.text((x + w - 92, y + 6), "KOSPI", font=_font("DejaVuSans-Bold.ttf", 13),
           fill=(200, 200, 210))


def scene_tanker(d, x, y, w, h):
    # dusk sky bands
    bands = [(255, 150, 60), (240, 110, 70), (200, 70, 60), (120, 50, 70)]
    bh = h * 0.55 / len(bands)
    for i, c in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=c)
    # sun
    d.ellipse([x + w - 70, y + 8, x + w - 30, y + 48], fill=(255, 220, 130))
    # sea
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(30, 60, 90))
    d.line([x, y + h * 0.62, x + w, y + h * 0.62], fill=(90, 140, 180), width=1)
    d.line([x, y + h * 0.78, x + w, y + h * 0.78], fill=(70, 120, 160), width=1)
    # tanker hull
    hx, hy, hw, hh = x + w * 0.08, y + h * 0.62, w * 0.84, h * 0.2
    d.polygon([(hx, hy), (hx + hw, hy), (hx + hw - 14, hy + hh), (hx + 14, hy + hh)],
              fill=(40, 40, 46))
    d.rectangle([hx + hw * 0.62, hy - h * 0.16, hx + hw * 0.78, hy], fill=(220, 220, 220))
    d.rectangle([hx + hw * 0.66, hy - h * 0.16, hx + hw * 0.74, hy - h * 0.10],
                fill=(40, 90, 160))
    # fire + smoke on deck
    fx, fy = hx + hw * 0.3, hy - 6
    d.polygon([(fx - 22, fy), (fx - 8, fy - 34), (fx + 4, fy - 12), (fx + 16, fy - 30),
               (fx + 26, fy)], fill=(255, 140, 20))
    d.polygon([(fx - 10, fy), (fx - 2, fy - 18), (fx + 10, fy)], fill=(255, 220, 80))
    for cx, cy, r in [(fx - 6, fy - 44, 9), (fx + 8, fy - 56, 11), (fx + 20, fy - 68, 8)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=(60, 60, 66))
    # mine in water
    mx, my = x + w * 0.9, y + h * 0.86
    d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(20, 20, 20))
    for ang in range(0, 360, 45):
        import math
        dx = math.cos(math.radians(ang)) * 10
        dy = math.sin(math.radians(ang)) * 10
        d.line([mx, my, mx + dx, my + dy], fill=(20, 20, 20), width=2)


def mini_scene(d, x, y, w, h, kind):
    """Small pictorial strip for medium stories."""
    skies = {"strike": (90, 40, 40), "treaty": (29, 53, 87), "sewing": (120, 70, 40),
             "mine": (70, 55, 40), "court": (60, 60, 70), "clinic": (40, 100, 90),
             "drone": (40, 70, 110), "jet": (50, 80, 120), "turkey": (140, 90, 30),
             "trophy": (120, 95, 20)}
    d.rectangle([x, y, x + w, y + h], fill=skies.get(kind, (80, 80, 80)))
    d.rectangle([x, y + h - 5, x + w, y + h], fill=(30, 30, 30))
    cx, cy = x + w // 2, y + h // 2 - 2
    if kind == "strike":
        d.polygon([(cx - 26, cy + 8), (cx + 26, cy + 8), (cx + 20, cy - 8), (cx - 20, cy - 8)],
                  fill=(40, 40, 44))
        d.polygon([(cx - 12, cy - 8), (cx - 2, cy - 26), (cx + 8, cy - 8)], fill=(255, 140, 20))
        d.ellipse([cx + 14, cy - 22, cx + 24, cy - 12], fill=(70, 70, 74))
    elif kind == "treaty":
        d.rectangle([cx - 26, cy - 10, cx - 2, cy + 8], fill=(240, 240, 240))
        d.rectangle([cx + 2, cy - 10, cx + 26, cy + 8], fill=(240, 240, 240))
        d.line([cx - 2, cy - 2, cx + 2, cy - 2], fill=(122, 31, 31), width=2)
        d.polygon([(cx, cy - 22), (cx + 6, cy - 12), (cx - 6, cy - 12)], fill=(255, 200, 60))
    elif kind == "sewing":
        d.ellipse([cx - 14, cy - 12, cx + 14, cy + 12], fill=(240, 240, 240))
        d.ellipse([cx - 4, cy - 3, cx + 4, cy + 3], fill=(40, 40, 40))
        d.line([cx + 14, cy, cx + 30, cy], fill=(240, 240, 240), width=2)
    elif kind == "mine":
        d.polygon([(cx - 28, cy + 10), (cx - 20, cy - 14), (cx + 20, cy - 14), (cx + 28, cy + 10)],
                  fill=(50, 40, 30))
        d.rectangle([cx - 4, cy - 22, cx + 4, cy - 12], fill=(255, 200, 60))
        d.ellipse([cx - 8, cy - 26, cx + 8, cy - 18], fill=(255, 220, 100))
    elif kind == "court":
        for i in (-20, 0, 20):
            d.rectangle([cx + i - 3, cy - 12, cx + i + 3, cy + 10], fill=(240, 240, 240))
        d.rectangle([cx - 28, cy - 18, cx + 28, cy - 12], fill=(240, 240, 240))
        d.rectangle([cx - 28, cy + 10, cx + 28, cy + 14], fill=(240, 240, 240))
    elif kind == "clinic":
        d.rectangle([cx - 16, cy - 12, cx + 16, cy + 12], fill=(240, 240, 240))
        d.rectangle([cx - 3, cy - 8, cx + 3, cy + 8], fill=(200, 40, 40))
        d.rectangle([cx - 8, cy - 3, cx + 8, cy + 3], fill=(200, 40, 40))
    elif kind == "drone":
        d.ellipse([cx - 12, cy - 6, cx + 12, cy + 6], fill=(220, 220, 220))
        for sx in (-22, 22):
            d.ellipse([cx + sx - 8, cy - 14, cx + sx + 8, cy - 6], fill=(180, 180, 180))
            d.line([cx + sx, cy - 8, cx, cy - 2], fill=(180, 180, 180), width=2)
        d.line([cx, cy + 6, cx, cy + 14], fill=(255, 200, 60), width=2)
    elif kind == "jet":
        d.polygon([(cx - 28, cy + 4), (cx + 20, cy - 6), (cx + 30, cy + 2), (cx + 20, cy + 8)],
                  fill=(230, 230, 230))
        d.polygon([(cx - 6, cy - 2), (cx + 2, cy - 16), (cx + 8, cy - 2)], fill=(200, 200, 200))
    elif kind == "turkey":
        d.ellipse([cx - 12, cy - 4, cx + 12, cy + 14], fill=(120, 70, 30))
        d.ellipse([cx - 2, cy - 14, cx + 12, cy + 2], fill=(140, 85, 40))
        d.polygon([(cx + 10, cy - 10), (cx + 18, cy - 6), (cx + 10, cy - 4)], fill=(255, 170, 40))
    elif kind == "trophy":
        d.polygon([(cx - 10, cy - 14), (cx + 10, cy - 14), (cx + 6, cy + 2), (cx - 6, cy + 2)],
                  fill=(255, 210, 60))
        d.rectangle([cx - 4, cy + 2, cx + 4, cy + 10], fill=(255, 210, 60))
        d.rectangle([cx - 10, cy + 10, cx + 10, cy + 14], fill=(255, 210, 60))


SCENES = {"rocket": scene_rocket, "chart": scene_chart, "tanker": scene_tanker}

# ---- schematic world map ---------------------------------------------------
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 62), (-55, 47),
     (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-150, 60), (-168, 66)],
    # South America
    [(-80, 10), (-62, 10), (-50, 0), (-35, -8), (-40, -22), (-48, -28), (-58, -38),
     (-65, -45), (-70, -54), (-73, -37), (-70, -18), (-80, -5), (-80, 10)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (12, 55), (18, 56),
     (21, 59), (28, 71), (40, 68), (40, 60), (30, 60), (28, 55), (30, 46), (23, 40),
     (19, 42), (12, 44), (8, 44), (3, 43), (-10, 36)],
    # Africa
    [(-6, 35), (10, 37), (20, 32), (32, 31), (43, 12), (51, 11), (48, 0), (40, -10),
     (36, -20), (32, -29), (20, -35), (15, -27), (12, -18), (9, -1), (-8, 4), (-17, 15),
     (-16, 28), (-6, 35)],
    # Asia
    [(40, 68), (50, 70), (68, 73), (90, 75), (110, 74), (130, 72), (160, 70),
     (178, 66), (162, 60), (158, 52), (142, 50), (140, 40), (130, 33), (122, 30),
     (120, 22), (108, 18), (105, 8), (100, 8), (97, 16), (92, 21), (88, 22),
     (80, 13), (77, 8), (72, 20), (66, 25), (61, 25), (57, 26), (52, 28), (48, 30),
     (44, 29), (40, 36), (36, 36), (30, 36), (27, 40), (30, 46), (40, 50), (40, 60),
     (40, 68)],
    # Australia
    [(114, -22), (122, -14), (132, -12), (142, -11), (150, -22), (153, -27),
     (150, -37), (140, -38), (132, -32), (124, -33), (115, -35), (114, -22)],
]


def draw_map(d, x, y, w, h, f_small):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 235))
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h) for lon, lat in poly]
        d.polygon(pts, fill=(190, 200, 170), outline=(120, 130, 110))
    pins = [(1, 112, 35), (2, 127, 37), (3, 56, 26), (4, 43, 15), (5, 160, -9),
            (6, 90, 24), (7, 107, -7), (8, -74, 41), (9, 25, 0), (10, 15, 33),
            (11, 19, 52), (12, -77, 39), (13, -17, 15)]
    # nudge overlapping pins
    nudge = {1: (-8, -6), 2: (8, 4), 8: (-6, 6), 12: (7, -7), 10: (-8, 4)}
    for n, lon, lat in pins:
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        dx, dy = nudge.get(n, (0, 0))
        px, py = px + dx, py + dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=MAROON, outline=(255, 255, 255))
        d.text((px, py - 1), str(n), font=f_small, fill=(255, 255, 255), anchor="mm")


# ---- layout ----------------------------------------------------------------
def draw(f):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14
    CW = W - 2 * M

    # top bar
    d.rectangle([0, 0, W, 26], fill=(20, 20, 20))
    d.text((M, 5), "THE WORLD IN ONE DAY", font=f.sans_b(13), fill=(255, 255, 255))
    d.text((W - M, 6), "WEDNESDAY'S NEWS  \u00b7  No. 25", font=f.sans(11),
           fill=(220, 220, 210), anchor="ra")

    # masthead
    d.text((W // 2, 30), "Wednesday 25 November 2026", font=f.serif_b(44),
           fill=INK, anchor="ma")
    d.line([M, 86, W - M, 86], fill=RULE, width=1)
    d.line([M, 88, W - M, 88], fill=RULE, width=2)

    # kicker
    d.text((W // 2, 92), "38 STORIES  \u00b7  7 REGIONS  \u00b7  EVERY ONE DATED "
           "WEDNESDAY 25 NOVEMBER 2026", font=f.sans_b(13), fill=MAROON, anchor="ma")

    # sub-headline
    d.text((W // 2, 112), "Shenzhou carries Pakistan's first astronaut to Tiangong  \u2014  "
           "Kospi crashes 6.2%  \u2014  two tankers hit mines in Hormuz",
           font=f.serif_i(15), fill=INK, anchor="ma")

    # timeline strip
    y = 132
    d.text((M, y), "THE DAY IN UTC", font=f.sans_b(10), fill=MAROON)
    d.text((W - M, y), "all times UTC", font=f.sans(9), fill=(90, 80, 60), anchor="ra")
    y += 14
    bw = CW // 6
    for i, (t, label) in enumerate(TIMELINE):
        bx = M + i * bw
        d.rectangle([bx, y, bx + bw - 3, y + 22], fill=(255, 255, 255),
                    outline=(180, 170, 150))
        d.text((bx + 5, y + 5), t, font=f.sans_b(11), fill=MAROON)
        lines = wrap(label, f.sans(8), bw - 52)
        text_lines(d, bx + 46, y + 2, lines[:2], f.sans(8), fill=INK, leading=10)

    # stat strip
    y = 172
    d.rectangle([M, y, W - M, y + 38], fill=(20, 20, 20))
    sw = CW // 6
    for i, (num, lab) in enumerate(STATS):
        cx = M + i * sw + sw // 2
        d.text((cx, y + 3), num, font=f.serif_b(20), fill=(255, 255, 255), anchor="ma")
        d.text((cx, y + 26), lab, font=f.sans_b(8), fill=(220, 200, 120), anchor="ma")

    # region bar
    y = 214
    total = sum(c for _, c in REGIONS)
    rx = M
    for name, c in REGIONS:
        seg = int(CW * c / total)
        d.rectangle([rx, y, rx + seg - 1, y + 20], fill=REGION_COLORS[name])
        d.text((rx + seg // 2, y + 5), "%s %d" % (name, c), font=f.sans_b(8),
               fill=(255, 255, 255), anchor="ma")
        rx += seg

    # ---- lead 1 ------------------------------------------------------------
    y = 238
    d.text((M, y), "LEAD STORY  \u00b7  1", font=f.sans_b(10), fill=MAROON)
    d.line([M + 92, y + 6, W - M, y + 6], fill=RULE, width=1)
    y += 14
    s = LEADS[0]
    SCENES[s["scene"]](d, M, y, 470, 118)
    tx, tw = M + 482, CW - 482
    bw_ = badge(d, tx, y + 1, s["conf"], f.sans_b(9))
    d.text((tx + bw_ + 8, y + 2), "rep %s UTC \u00b7 %s" % (s["rep"], s["src"]),
           font=f.sans(9), fill=(90, 80, 60))
    hl = wrap(s["head"], f.serif_b(20), tw)
    text_lines(d, tx, y + 18, hl[:2], f.serif_b(20), leading=23)
    bl = wrap(s["body"], f.sans(11), tw)
    text_lines(d, tx, y + 18 + 2 * 23 + 4, bl[:4], f.sans(11), leading=13)

    # ---- leads 2 & 3 ---------------------------------------------------------
    y = 374
    lw = (CW - 10) // 2
    for i, s in enumerate(LEADS[1:]):
        lx = M + i * (lw + 10)
        d.text((lx, y), "LEAD %d  \u00b7  %s" % (s["n"], s["region"]), font=f.sans_b(10),
               fill=MAROON)
        d.line([lx + 96, y + 6, lx + lw, y + 6], fill=RULE, width=1)
        sy = y + 14
        SCENES[s["scene"]](d, lx, sy, lw, 52)
        by = sy + 52 + 4
        bw_ = badge(d, lx, by, s["conf"], f.sans_b(9))
        d.text((lx + bw_ + 8, by + 1), "rep %s UTC \u00b7 %s" % (s["rep"], s["src"]),
               font=f.sans(9), fill=(90, 80, 60))
        hl = wrap(s["head"], f.serif_b(15), lw)
        text_lines(d, lx, by + 16, hl[:2], f.serif_b(15), leading=18)
        bl = wrap(s["body"], f.sans(10), lw)
        text_lines(d, lx, by + 16 + 2 * 18 + 3, bl[:2], f.sans(10), leading=12)

    # ---- medium grid ---------------------------------------------------------
    y = 526
    d.text((M, y), "TEN MORE STORIES  \u2014  EVERY ONE DATED TODAY", font=f.sans_b(10),
           fill=MAROON)
    d.text((W - M, y), "badges: HOW SURE, see foot of page", font=f.sans(9),
           fill=(90, 80, 60), anchor="ra")
    y += 16
    cw = (CW - 4 * 4) // 5
    ch = 86
    for idx, s in enumerate(MEDIUM):
        r, c = divmod(idx, 5)
        cx = M + c * (cw + 4)
        cy = y + r * (ch + 4)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=(255, 255, 255),
                    outline=(190, 180, 160))
        mini_scene(d, cx, cy, cw, 24, s["scene"])
        d.text((cx + 4, cy + 26), "%d" % s["n"], font=f.sans_b(11), fill=MAROON)
        bw_ = badge(d, cx + 22, cy + 27, s["conf"], f.sans_b(7))
        d.text((cx + 22 + bw_ + 5, cy + 28), "rep %s" % s["rep"], font=f.sans(7),
               fill=(90, 80, 60))
        hl = wrap(s["head"], f.sans_b(10), cw - 8)
        text_lines(d, cx + 4, cy + 40, hl[:2], f.sans_b(10), leading=11)
        bl = wrap(s["body"], f.sans(9), cw - 8)
        text_lines(d, cx + 4, cy + 40 + 2 * 11 + 1, bl[:2], f.sans(9), leading=10)

    # ---- map -----------------------------------------------------------------
    y = 726
    d.text((M, y), "WHERE IT HAPPENED  \u2014  13 PINNED STORIES (SCHEMATIC MAP, NOT TO SCALE)",
           font=f.sans_b(10), fill=MAROON)
    draw_map(d, M, y + 15, CW, 70, f.sans_b(8))

    # ---- also list -----------------------------------------------------------
    y = 816
    d.text((M, y), "ALSO ON WEDNESDAY 25 NOVEMBER  \u2014  25 MORE STORIES",
           font=f.sans_b(10), fill=MAROON)
    y += 15
    cols = [ALSO[0:9], ALSO[9:17], ALSO[17:25]]
    colw = CW // 3
    for ci, col in enumerate(cols):
        lx = M + ci * colw
        for j, (n, reg, head, src) in enumerate(col):
            ly = y + j * 12
            line = "%d. %s \u2014 %s" % (n, head, src)
            while f.sans(9).getlength(line) > colw - 8 and len(line) > 10:
                line = line[:-5] + "\u2026"
            d.text((lx, ly), "%d." % n, font=f.sans_b(9), fill=REGION_COLORS[reg])
            d.text((lx + 20, ly), line[3:], font=f.sans(9), fill=INK)

    # ---- how sure + date check ----------------------------------------------
    y = 944
    bw2 = 470
    d.rectangle([M, y, M + bw2, y + 56], fill=(255, 255, 255), outline=(180, 170, 150))
    d.text((M + 6, y + 4), "HOW SURE ARE WE?", font=f.sans_b(10), fill=MAROON)
    legend = [("OFFICIAL", "from an official statement"),
              ("CONFIRMED", "two or more major outlets"),
              ("REPORTED", "one major outlet"),
              ("CLAIM", "one side's claim, unverified")]
    d.rectangle([M, y, M + bw2, y + 56], fill=(255, 255, 255), outline=(180, 170, 150))
    d.text((M + 6, y + 4), "HOW SURE ARE WE?", font=f.sans_b(10), fill=MAROON)
    for k, (lab, desc) in enumerate(legend):
        colx = M + 6 + (k // 2) * 235
        rowy = y + 20 + (k % 2) * 17
        w_ = badge(d, colx, rowy, lab, f.sans_b(8))
        d.text((colx + w_ + 5, rowy + 1), desc, font=f.sans(8), fill=INK)

    dx = M + bw2 + 10
    dw = W - M - dx
    d.rectangle([dx, y, dx + dw, y + 56], fill=(255, 246, 246),
                outline=(178, 34, 34))
    d.text((dx + 6, y + 4), "DATE CHECK  \u2014  LEFT OUT ON PURPOSE", font=f.sans_b(10),
           fill=MAROON)
    ly = y + 19
    for item in DATE_CHECK:
        lines = wrap("\u2022  " + item, f.sans(8), dw - 12)
        ly = text_lines(d, dx + 6, ly, lines[:1], f.sans(8), leading=9)
        if len(lines) > 1:
            ly = text_lines(d, dx + 6, ly, lines[1:2], f.sans(8), leading=9)

    # footer
    fl = wrap(FOOTER, f.sans(8), CW)
    text_lines(d, M, 1006, fl[:2], f.sans(8), fill=(90, 80, 60), leading=10)
    return img


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "entry.png")
    try:
        from PIL import Image  # noqa: F401
    except Exception:
        here = os.path.dirname(os.path.abspath(__file__))
        shutil.copy(os.path.join(here, "entry.png"), out)
        return
    img = draw(Fonts())
    img.save(out, optimize=True)
    print("wrote %s %dx%d" % (out, img.width, img.height))


if __name__ == "__main__":
    main()
