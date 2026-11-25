#!/usr/bin/env python3
"""draw24.py -- "Tuesday 24 November 2026" one-image news poster (1024x1024).

Single source of truth: story data + all art + layout. Deterministic: no
timestamps, no randomness (a tiny LCG is used only where texture is wanted).
Usage:  python3 draw24.py [out.png]
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = sys.argv[1] if len(sys.argv) > 1 else "entry.png"

# ----------------------------------------------------------------- fonts
FONT_R = "/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf"
FONT_B = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"
FONT_X = "/usr/share/fonts/truetype/noto/NotoSans-CondensedExtraBold.ttf"
_fc = {}
SIZES_USED = set()
MIN_SIZE = 10


def F(size, style="r"):
    assert size >= MIN_SIZE, "font size %s is below the %spx floor" % (size, MIN_SIZE)
    key = (size, style)
    if key not in _fc:
        path = {"r": FONT_R, "b": FONT_B, "x": FONT_X}[style]
        _fc[key] = ImageFont.truetype(path, size)
    SIZES_USED.add(size)
    return _fc[key]


WARN = []


def warn(msg):
    WARN.append(msg)
    print("WARN:", msg)


# ----------------------------------------------------------------- colours
INK = (24, 26, 32)
PAPER = (246, 242, 232)
PANEL = (255, 253, 247)
GREY = (96, 98, 106)
LINE = (170, 166, 154)
RED = (200, 22, 34)
REGION_COL = {
    "EUROPE": (30, 88, 178),
    "MIDDLE EAST": (118, 54, 168),
    "AMERICAS": (24, 128, 62),
    "ASIA-PACIFIC": (208, 40, 120),
    "AFRICA": (128, 84, 30),
    "OCEANIA": (236, 108, 18),
}
REGIONS = list(REGION_COL.keys())
EU, ME, AM, AP, AF, OC = REGIONS

# ----------------------------------------------------------------- stories
# id, region, lon, lat, source-line
# kind: 'lead' (1-3) | 'small' (4-13) | 'also' (14-32)
S = {}


def story(i, kind, region, lon, lat, head, body, src, also=None):
    S[i] = dict(id=i, kind=kind, region=region, lon=lon, lat=lat, head=head,
                body=body, src=src, also=also)


# ---- 3 leads
story(1, "lead", OC, 160.0, -9.4,
      "SOLOMONS SCRAP CHINA SECURITY PACT",
      "Honiara has told Beijing it will not renew the 2022 pact, which ends April 2027, ABC reports. "
      "China says its Pacific ties target no third party. PM Wale is due in Canberra to sign an Australia treaty on Wednesday.",
      "ABC (AU) · RNZ · REPORTED, unnamed sources")
story(2, "lead", ME, 34.5, 31.5,
      "ISRAEL KILLS HAMAS INTERNAL-SECURITY CHIEF",
      "A drone strike in Gaza killed Naim Abu Nahl, 50, who ran Hamas's Internal Security Service; four others were hurt. "
      "Hamas calls it a war crime (CLAIM). 1,680 killed since the Oct 2025 ceasefire.",
      "Al Jazeera · Washington Post · Reuters")
story(3, "lead", EU, 35.1, 47.8,
      "PUTIN VOWS RETALIATION; RUSSIA HITS ZAPORIZHZHIA",
      "Putin says retaliation for Ukraine's refinery strikes is \"inevitable\". Overnight a Russian strike hit a "
      "five-storey block in Zaporizhzhia: 2 dead, 40+ hurt, per Gov. Semikin (REPORTED).",
      "Al Jazeera · Kyiv Independent · AP")
# ---- 10 smalls
story(4, "small", AF, -17.4, 14.7,
      "COURT REINSTATES SENEGAL AS AFRICA CUP CHAMPION",
      "CAS overturned CAF: the referee's call to resume play stands, so Senegal's 1–0 final win counts.",
      "allAfrica (CAS release) · AP")
story(5, "small", AP, 121.5, 25.0,
      "ASIAN STOCKS SURGE: TAIWAN +9.1% IN A DAY",
      "KOSPI +7.1%, Nikkei +3.9% (4:13pm AEDT), ASX +1.8%: a rally after Nvidia's 23 Nov CEO reinstatement.",
      "ABC (AU)")
story(6, "small", EU, -0.1, 51.5,
      "UK RECORDS ITS DEADLIEST HEAT YEAR: 5,258",
      "UKHSA counts 5,258 heat-related deaths in 2026, the highest on record, above 2022.",
      "Reuters")
story(7, "small", AM, -75.5, 10.4,
      "ARMED MEN HOLD HOSTAGES IN CARTAGENA STORE",
      "Robbers fled into a supermarket after a failed armoured-van heist. CLAIM: ~25 held (president: 30, 5 freed).",
      "Al Jazeera")
story(8, "small", AM, -108.5, 25.6,
      "MEXICO WILL TRY \"EL CHAPO ISIDRO\" ITSELF",
      "Fausto Meza Flores, on the FBI's 10 Most Wanted list, faces trial in Mexico despite a US extradition request.",
      "Al Jazeera")
story(9, "small", AP, 90.4, 23.8,
      "GARMENT STRIKE HALTS 481 BANGLADESH FACTORIES",
      "Wage-dispute protests: police fired tear gas in Gazipur, Savar, Ashulia; 101 BGB platoons deployed.",
      "The Business Standard · Daily Star")
story(10, "small", AM, -91.1, 40.8,
      "ARMY TO BLOW UP LEAD EXPLOSIVES IN IOWA",
      "Detonation set for Wednesday after a court cleared it. CLAIM: green groups warn of a lead plume.",
      "Al Jazeera")
story(11, "small", ME, 46.7, 24.7,
      "DRONE HITS RIYADH FINANCIAL TOWER",
      "11 hurt, Saudi civil defence says: Saudis, Indians, Nepalis, Egyptians. Houthis blamed (CLAIM).",
      "Al Jazeera")
story(12, "small", AP, 101.7, 3.1,
      "MALAYSIA TO RETURN 6,500+ ROHINGYA TO MYANMAR",
      "PM Anwar Ibrahim says more than 6,500 refugees will be sent back across the border.",
      "Al Jazeera")
story(13, "small", AF, 6.1, 4.9,
      "NIGERIA BOAT DISASTER TOLL HITS 32",
      "Police blame overloading and no life jackets after the Bayelsa State boat accident.",
      "allAfrica")
# ---- 19 ALSO
story(14, "also", EU, 26.0, 59.8, "Zelensky confirms drone hit on cargo ship Sparta II, Gulf of Finland", "", "Kyiv Independent")
story(15, "also", EU, 12.6, 55.7, "Danish court backs \"ghetto law\" used to evict \"non-Western\" residents", "", "Al Jazeera")
story(16, "also", EU, 30.5, 39.8, "Turkish Air Force helicopter crashes in Eskişehir, 5 crew dead", "", "AP")
story(17, "also", ME, 44.2, 15.4, "UK sanctions Houthi group and four senior officials over abuses", "", "Al Jazeera")
story(18, "also", ME, 55.9, 25.8, "Ras Al Khaimah: bus hits stationary truck, 13 dead, 14 hurt", "", "Gulf News")
story(19, "also", AM, -73.6, 4.1, "Colombia: Villavicencio car bomb, 23+ hurt; ex-FARC rebels blamed", "", "Al Jazeera")
story(20, "also", AM, -77.0, 38.9, "US House counsel denies backing raid on Rep. Ilhan Omar's home", "", "Al Jazeera")
story(21, "also", AM, -77.5, 40.9, "Pennsylvania reports ninth measles death in ongoing outbreak", "", "Al Jazeera")
story(22, "also", AP, 105.8, 21.0, "Hanoi hot-pot restaurant gas blast: 7 dead, 9 hurt", "", "VnExpress")
story(23, "also", AP, 90.5, 23.7, "Sheikh Hasina says she will return to Bangladesh on Dec 16", "", "Reuters")
story(24, "also", AP, 130.9, 37.5, "Russian jets near Ulleung Island trigger South Korea air-raid alert", "", "Al Jazeera")
story(25, "also", AF, 39.5, 12.4, "Amnesty: Ethiopian shelling of Alamata killed 14+; seeks war-crimes probe", "", "allAfrica")
story(26, "also", AF, 32.5, 15.6, "Sudan: 19.5 million face crisis-level hunger or worse", "", "allAfrica")
story(27, "also", AF, 29.8, 1.6, "DR Congo: Ituri fighting traps Ebola responders in a maternity ward", "", "allAfrica")
story(28, "also", AF, -0.2, 5.6, "Ghana beat Morocco 1–0 to win the Amputee Football World Cup", "", "allAfrica")
story(29, "also", OC, 151.2, -33.9, "ASX 200 closes +1.8% at 8,726, first gain in nearly two weeks", "", "ABC (AU)")
story(30, "also", OC, -170.7, -14.3, "US leases 31.5M acres of American Samoa seabed for deep-sea mining", "", "RNZ")
story(31, "also", OC, 149.1, -35.3, "Labor–Greens deal gives Australians a right to sue social platforms", "", "ABC (AU)")
story(32, "also", OC, 174.8, -41.3, "Cyber attack on Allied Media delays New Zealand newspapers", "", "RNZ")

TOTAL = len(S)
assert sorted(S) == list(range(1, TOTAL + 1))
COUNTS = {r: sum(1 for s in S.values() if s["region"] == r) for r in REGIONS}
assert sum(COUNTS.values()) == TOTAL, "region counts must sum to the story total"
assert TOTAL >= 31 and all(COUNTS[r] >= 1 for r in REGIONS)
assert [s["kind"] for s in S.values()].count("lead") == 3
assert [s["kind"] for s in S.values()].count("small") == 10

DATA_STRIP = [
    ("9.1%", "Taiwan shares, one-day jump", "ABC"),
    ("5,258", "UK heat deaths, a record", "Reuters"),
    ("1,680", "Gaza dead since ceasefire", "Al Jazeera"),
    ("481", "Bangladesh factories halted", "TBS"),
    ("6,500+", "Rohingya Malaysia will return", "Al Jazeera"),
    ("31.5M", "acres Am. Samoa seabed leased", "RNZ"),
]
assert len(DATA_STRIP) == 6

DATE_CHECK = [
    ("22 NOV", "COP31 climate talks end with no deal"),
    ("22 NOV", "Ukraine drones sink corvette Merkury, Benghazi"),
    ("23 NOV", "Nvidia reinstates CEO Jensen Huang"),
    ("25 NOV", "Shenzhou-24 launches with a Pakistani astronaut"),
    ("25 NOV", "Australia–Solomons treaty signed in Canberra"),
]
assert len(DATE_CHECK) == 5

BEATS = [
    ("OVERNIGHT", "Russian strike hits Zaporizhzhia block: 2 dead"),
    ("~05:00 UTC", "Asian shares jump; ASX closes +1.8%"),
    ("DAYTIME", "Putin: retaliation \"inevitable\"; Solomons end China pact"),
    ("AFTERNOON", "Drone kills Hamas security chief Abu Nahl"),
    ("EVENING", "CAS reinstates Senegal as Africa Cup champion"),
]
assert len(BEATS) == 5

# ----------------------------------------------------------------- helpers
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

_seed = [12345]


def lcg():
    _seed[0] = (_seed[0] * 1103515245 + 12345) & 0x7FFFFFFF
    return _seed[0] / 0x7FFFFFFF


def tw(text, font):
    return font.getlength(text)


def wrap(text, font, maxw):
    words = text.split(" ")
    lines, cur = [], ""
    for wd in words:
        t = wd if not cur else cur + " " + wd
        if tw(t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def block(x, y, text, font, fill, maxw, maxlines, lh, name, dd=None):
    dd = dd or d
    lines = wrap(text, font, maxw)
    if len(lines) > maxlines:
        warn("%s: %d lines > %d (%r)" % (name, len(lines), maxlines, text[:40]))
    for ln in lines[:maxlines]:
        if tw(ln, font) > maxw + 0.5:
            warn("%s: line wider than box" % name)
        dd.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def grad(x, y, w, h, c1, c2, dd=None):
    dd = dd or d
    for i in range(h):
        t = i / max(1, h - 1)
        c = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        dd.line([(x, y + i), (x + w - 1, y + i)], fill=c)


def chip(x, y, n, region, r=9, font=None):
    """round number badge"""
    font = font or F(11, "b")
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=REGION_COL[region], outline=(255, 255, 255), width=1)
    s = str(n)
    d.text((x + r, y + r), s, font=font, fill=(255, 255, 255), anchor="mm")


def label(x, y, text, size=10, fill=(255, 255, 255), bg=None, style="b", anchor="la"):
    f = F(size, style)
    if bg:
        wtxt = tw(text, f)
        bx = x - (wtxt / 2 if anchor[0] == "m" else 0)
        d.rectangle([bx - 2, y - 1, bx + wtxt + 2, y + size + 2], fill=bg)
    d.text((x, y), text, font=f, fill=fill, anchor=anchor)


# ----------------------------------------------------------------- LEAD ART (w ~333, h ~92)
def art_solomons(x, y, w, h):
    grad(x, y, w, int(h * 0.50), (150, 200, 235), (214, 232, 244))
    grad(x, y + int(h * 0.50), w, h - int(h * 0.50), (24, 118, 176), (8, 52, 112))
    # islands (right)
    for (cx, base, sw, hh, col) in [(x + 232, y + int(h * 0.52), 70, 26, (46, 120, 62)),
                                    (x + 286, y + int(h * 0.52), 52, 20, (58, 136, 70)),
                                    (x + 190, y + int(h * 0.53), 34, 12, (40, 108, 58))]:
        d.polygon([(cx - sw // 2, base), (cx - sw // 4, base - hh), (cx, base - hh - 5),
                   (cx + sw // 4, base - hh + 2), (cx + sw // 2, base)], fill=col)
    d.ellipse([x + 296, y + 8, x + 316, y + 28], fill=(255, 226, 120))  # sun
    # waves
    for i in range(5):
        yy = y + int(h * 0.62) + i * 7
        for k in range(0, w, 22):
            d.arc([x + k + (i % 2) * 11, yy, x + k + 16 + (i % 2) * 11, yy + 6], 200, 340, fill=(120, 190, 230))
    # torn pact sheet (left) -- two halves, red cross, stamp
    sx, sy, sw_, sh_ = x + 14, y + 10, 118, 70
    d.polygon([(sx, sy), (sx + 64, sy), (sx + 52, sy + 20), (sx + 66, sy + 40), (sx + 56, sy + sh_), (sx, sy + sh_)],
              fill=(250, 248, 240), outline=(90, 90, 90))
    d.polygon([(sx + 72, sy + 4), (sx + sw_, sy + 8), (sx + sw_ - 4, sy + sh_ + 2), (sx + 64, sy + sh_ - 2),
               (sx + 76, sy + 40), (sx + 62, sy + 20)], fill=(244, 240, 230), outline=(90, 90, 90))
    d.text((sx + 5, sy + 4), "SECURITY", font=F(10, "b"), fill=(70, 70, 80))
    d.text((sx + 5, sy + 16), "PACT 2022", font=F(10, "b"), fill=(70, 70, 80))
    d.text((sx + 5, sy + 28), "CHINA –", font=F(10, "b"), fill=(70, 70, 80))
    d.text((sx + 5, sy + 40), "SOLOMONS", font=F(10, "b"), fill=(70, 70, 80))
    d.line([(sx + 8, sy + 54), (sx + 50, sy + 54)], fill=(160, 160, 160), width=1)
    d.rectangle([sx + 66, sy + 44, sx + sw_ + 6, sy + 64], fill=RED)
    d.text((sx + 70, sy + 48), "NOT RENEWED", font=F(11, "b"), fill=(255, 255, 255))
    label(x + w - 6, y + h - 14, "SOLOMON ISLANDS", 10, (255, 255, 255), None, "b", "ra")


def art_gaza(x, y, w, h):
    grad(x, y, w, h, (14, 18, 44), (74, 44, 52))
    for i in range(26):  # stars
        sx = x + int(lcg() * w)
        sy = y + int(lcg() * h * 0.4)
        d.point((sx, sy), fill=(210, 210, 230))
    # skyline
    bx = x
    k = 0
    while bx < x + w:
        bw = 22 + (k * 7) % 19
        bh = 20 + (k * 13) % 36
        d.rectangle([bx, y + h - bh, bx + bw - 2, y + h], fill=(30, 30, 38))
        for wy in range(y + h - bh + 4, y + h - 4, 9):
            for wx in range(bx + 3, bx + bw - 6, 7):
                if (wx + wy + k) % 3 == 0:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(240, 200, 90))
        bx += bw
        k += 1
    # strike glow (ground)
    cx, cy = x + 226, y + h - 8
    for r, col in [(46, (120, 40, 20)), (34, (190, 70, 20)), (22, (240, 130, 30)), (11, (255, 230, 150))]:
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=col)
    d.polygon([(cx - 14, cy), (cx - 22, cy - 36), (cx - 6, cy - 54), (cx + 8, cy - 40), (cx + 20, cy - 62),
               (cx + 24, cy - 30), (cx + 14, cy)], fill=(70, 66, 72))
    # drone
    dx, dy = x + 112, y + 22
    d.polygon([(dx - 18, dy), (dx + 18, dy), (dx + 8, dy + 7), (dx - 8, dy + 7)], fill=(190, 192, 200))
    d.line([(dx - 26, dy - 3), (dx + 26, dy - 3)], fill=(190, 192, 200), width=2)
    d.line([(dx, dy + 7), (dx, dy + 12)], fill=(190, 192, 200), width=2)
    # trajectory + crosshair
    d.line([(dx + 4, dy + 12), (cx - 4, cy - 16)], fill=(240, 80, 70), width=1)
    d.ellipse([cx - 16, cy - 30, cx + 16, cy + 2], outline=(240, 70, 60), width=2)
    d.line([(cx - 22, cy - 14), (cx + 22, cy - 14)], fill=(240, 70, 60), width=1)
    d.line([(cx, cy - 36), (cx, cy + 6)], fill=(240, 70, 60), width=1)
    label(x + 6, y + 5, "GAZA · DRONE STRIKE", 11, (255, 255, 255))
    label(x + w - 6, y + 5, "ABU NAHL, 50", 11, (255, 210, 130), None, "b", "ra")


def art_zapor(x, y, w, h):
    grad(x, y, w, h, (96, 120, 150), (190, 170, 150))
    half = 168
    # ground
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(70, 66, 64))
    # apartment block, 5 storeys, partly collapsed
    bx, by, bw, bh = x + 14, y + 14, 112, h - 24
    d.rectangle([bx, by + 14, bx + bw, by + bh], fill=(196, 182, 160), outline=(80, 70, 60))
    rows = 5
    rh = (bh - 14) // rows
    for r in range(rows):
        for c in range(5):
            wx = bx + 8 + c * 21
            wy = by + 14 + r * rh + 4
            lit = (r + c) % 3 == 0
            d.rectangle([wx, wy, wx + 12, wy + rh - 9], fill=(250, 214, 110) if lit else (70, 84, 104))
    # collapsed top-right corner (cut + rubble)
    d.polygon([(bx + bw - 44, by + 14), (bx + bw + 2, by + 14), (bx + bw + 2, by + 44), (bx + bw - 14, by + 36),
               (bx + bw - 24, by + 28)], fill=(150, 140, 150))
    for k in range(9):
        rx = bx + bw - 40 + (k * 11) % 52
        ry = y + h - 14 - (k * 5) % 11
        d.ellipse([rx, ry, rx + 9, ry + 7], fill=(110, 100, 96))
    for (ex, ey, er) in [(bx + bw - 22, by + 10, 16), (bx + bw - 6, by + 2, 12), (bx + bw - 36, by + 4, 10)]:
        d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(150, 150, 158))
    label(bx + 2, y + h - 22, "5-STOREY BLOCK", 10, (255, 255, 255), (40, 40, 48))
    # refinery
    rx = x + 188
    d.rectangle([rx, y + h - 42, rx + 40, y + h - 10], fill=(110, 118, 128), outline=(60, 62, 70))  # tank
    d.rectangle([rx + 48, y + h - 34, rx + 84, y + h - 10], fill=(122, 130, 140), outline=(60, 62, 70))
    d.rectangle([rx + 96, y + 28, rx + 106, y + h - 10], fill=(96, 100, 110), outline=(50, 52, 60))  # tower
    d.rectangle([rx + 112, y + 44, rx + 120, y + h - 10], fill=(96, 100, 110), outline=(50, 52, 60))
    for yy in range(y + 36, y + h - 12, 12):
        d.line([(rx + 96, yy), (rx + 106, yy)], fill=(60, 62, 70))
    fx, fy = rx + 101, y + 26
    d.polygon([(fx - 8, fy), (fx - 10, fy - 14), (fx - 3, fy - 8), (fx, fy - 24), (fx + 4, fy - 10),
               (fx + 10, fy - 16), (fx + 8, fy)], fill=(244, 120, 24))
    d.polygon([(fx - 4, fy), (fx - 3, fy - 8), (fx, fy - 12), (fx + 3, fy - 6), (fx + 4, fy)], fill=(255, 220, 90))
    d.line([(rx + 20, y + h - 42), (rx + 20, y + h - 52), (rx + 60, y + h - 52), (rx + 60, y + h - 34)], fill=(60, 62, 70), width=2)
    label(rx + 4, y + 6, "REFINERY HIT", 10, (255, 255, 255), (40, 40, 48))
    # red retaliation arrow
    ax = x + 140
    d.line([(ax - 6, y + 52), (ax + 34, y + 52)], fill=RED, width=4)
    d.polygon([(ax + 34, y + 44), (ax + 46, y + 52), (ax + 34, y + 60)], fill=RED)
    label(ax - 6, y + 62, "RETALIATION?", 10, (255, 255, 255), RED)


# ----------------------------------------------------------------- SMALL ART (w ~199, h 44)
def art_cup(x, y, w, h):
    for i, c in enumerate([(0, 133, 63), (253, 239, 66), (227, 27, 35)]):  # green/yellow/red bands
        d.rectangle([x + i * (w // 3), y, x + (i + 1) * (w // 3), y + h], fill=c)
    cx = x + w // 2
    d.polygon([(cx - 15, y + 6), (cx + 15, y + 6), (cx + 11, y + 24), (cx - 11, y + 24)], fill=(236, 190, 40), outline=(120, 80, 0))
    d.arc([cx - 24, y + 8, cx - 8, y + 22], 90, 270, fill=(236, 190, 40), width=3)
    d.arc([cx + 8, y + 8, cx + 24, y + 22], 270, 90, fill=(236, 190, 40), width=3)
    d.rectangle([cx - 3, y + 24, cx + 3, y + 33], fill=(236, 190, 40))
    d.rectangle([cx - 12, y + 33, cx + 12, y + 38], fill=(120, 80, 0))
    d.text((cx, y + 15), "1–0", font=F(10, "b"), fill=(90, 50, 0), anchor="mm")


def art_markets(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 40))
    for g in range(1, 4):
        d.line([(x, y + g * 11), (x + w, y + g * 11)], fill=(40, 58, 72))
    vals = [(30, 22), (26, 18), (30, 24), (22, 14), (24, 16), (14, 8), (8, 3)]
    for i, (a, b) in enumerate(vals):
        cx = x + 14 + i * 17
        up = i >= 3
        col = (60, 200, 110) if up else (220, 80, 80)
        top, bot = y + min(a, b) + 4, y + max(a, b) + 14
        d.line([(cx, top - 4), (cx, bot + 4)], fill=col)
        d.rectangle([cx - 4, top, cx + 4, bot], fill=col)
    d.line([(x + 6, y + 36), (x + 128, y + 6)], fill=(250, 220, 80), width=2)
    d.polygon([(x + 128, y + 3), (x + 118, y + 6), (x + 126, y + 14)], fill=(250, 220, 80))
    d.text((x + w - 6, y + 22), "+9.1%", font=F(14, "x"), fill=(90, 230, 130), anchor="rm")


def art_thermo(x, y, w, h):
    grad(x, y, w, h, (250, 170, 60), (240, 90, 40))
    d.ellipse([x + 6, y + 4, x + 38, y + 36], fill=(255, 238, 140))
    for k in range(8):
        a = k * math.pi / 4
        d.line([(x + 22 + 18 * math.cos(a), y + 20 + 18 * math.sin(a)), (x + 22 + 24 * math.cos(a), y + 20 + 24 * math.sin(a))],
               fill=(255, 238, 140), width=2)
    tx = x + 88
    d.rounded_rectangle([tx, y + 3, tx + 14, y + 36], 6, fill=(255, 255, 255), outline=(60, 20, 10))
    d.ellipse([tx - 5, y + 28, tx + 19, y + 46], fill=(255, 255, 255), outline=(60, 20, 10))
    d.rectangle([tx + 4, y + 12, tx + 10, y + 36], fill=(200, 20, 30))
    d.ellipse([tx - 1, y + 31, tx + 15, y + 44], fill=(200, 20, 30))
    for k in range(5):
        d.line([(tx + 16, y + 8 + k * 6), (tx + 21, y + 8 + k * 6)], fill=(60, 20, 10))
    for i, hh in enumerate([10, 16, 22, 32]):  # rising bars
        d.rectangle([x + 130 + i * 15, y + h - hh, x + 141 + i * 15, y + h], fill=(120, 20, 20))


def art_store(x, y, w, h):
    grad(x, y, w, h, (150, 170, 190), (120, 140, 160))
    sx = x + 24
    d.rectangle([sx, y + 3, sx + 150, y + h], fill=(236, 228, 208), outline=(70, 60, 50))
    for i in range(10):  # awning stripes
        d.rectangle([sx + i * 15, y + 3, sx + i * 15 + 14, y + 10], fill=(210, 40, 40) if i % 2 == 0 else (250, 250, 250))
    d.rectangle([sx + 1, y + 11, sx + 149, y + 21], fill=(30, 36, 50))
    d.text((sx + 75, y + 16), "SUPERMARKET", font=F(10, "b"), fill=(255, 255, 255), anchor="mm")
    d.rectangle([sx + 6, y + 24, sx + 92, y + h - 3], fill=(70, 100, 130))  # window
    for i in range(6):  # people held inside (silhouettes)
        px = sx + 12 + i * 13
        d.ellipse([px, y + 27, px + 7, y + 34], fill=(18, 22, 28))
        d.rectangle([px - 1, y + 34, px + 8, y + h - 3], fill=(18, 22, 28))
    d.rectangle([sx + 102, y + 24, sx + 142, y + h - 3], fill=(60, 80, 100))  # door
    for k in range(-1, 8):  # police tape across the front
        d.line([(x + k * 28, y + h - 6), (x + k * 28 + 14, y + h - 12)], fill=(250, 210, 30), width=3)


def art_trial(x, y, w, h):
    for i, c in enumerate([(0, 104, 71), (250, 250, 250), (206, 17, 38)]):  # Mexico tricolour
        d.rectangle([x + i * 22, y, x + (i + 1) * 22, y + h], fill=c)
    d.ellipse([x + 28, y + 15, x + 38, y + 25], fill=(140, 100, 40))
    d.rectangle([x + 66, y, x + w, y + h], fill=(48, 44, 60))
    # gavel
    d.polygon([(x + 90, y + 10), (x + 124, y + 4), (x + 130, y + 18), (x + 96, y + 24)], fill=(160, 100, 40), outline=(70, 40, 10))
    d.line([(x + 108, y + 18), (x + 150, y + 38)], fill=(190, 130, 60), width=5)
    d.rectangle([x + 84, y + 36, x + 170, y + 42], fill=(110, 70, 30))
    # scales of justice
    sx = x + 160
    d.line([(sx, y + 6), (sx, y + h - 4)], fill=(224, 224, 234), width=3)
    d.line([(sx - 22, y + 12), (sx + 22, y + 12)], fill=(224, 224, 234), width=3)
    for px_ in (sx - 22, sx + 22):
        d.line([(px_, y + 12), (px_ - 8, y + 26)], fill=(224, 224, 234))
        d.line([(px_, y + 12), (px_ + 8, y + 26)], fill=(224, 224, 234))
        d.pieslice([px_ - 9, y + 17, px_ + 9, y + 35], 0, 180, fill=(224, 224, 234))
    d.rectangle([sx - 10, y + h - 6, sx + 10, y + h - 3], fill=(224, 224, 234))


def art_factory(x, y, w, h):
    grad(x, y, w, h, (170, 180, 200), (210, 200, 190))
    fx = x + 12
    d.rectangle([fx, y + 18, fx + 120, y + h], fill=(150, 90, 70), outline=(70, 40, 30))
    for i in range(4):  # sawtooth roof
        d.polygon([(fx + i * 30, y + 18), (fx + i * 30 + 30, y + 18), (fx + i * 30 + 30, y + 6)], fill=(110, 70, 60))
    d.rectangle([fx + 128, y + 4, fx + 140, y + h], fill=(120, 110, 110))  # chimney
    for yy in range(y + 10, y + h, 10):
        d.line([(fx + 128, yy), (fx + 140, yy)], fill=(90, 80, 80))
    for i in range(5):
        d.rectangle([fx + 8 + i * 22, y + 24, fx + 20 + i * 22, y + 32], fill=(40, 46, 60))
    # door shuttered
    d.rectangle([fx + 48, y + 34, fx + 82, y + h], fill=(90, 94, 104))
    for yy in range(y + 36, y + h, 4):
        d.line([(fx + 48, yy), (fx + 82, yy)], fill=(60, 64, 74))
    d.arc([fx + 56, y + 24, fx + 74, y + 40], 180, 360, fill=(240, 200, 40), width=3)  # padlock shackle
    d.rectangle([fx + 54, y + 34, fx + 76, y + 44], fill=(240, 200, 40))
    d.text((x + w - 8, y + 22), "481", font=F(14, "x"), fill=(150, 20, 30), anchor="rm")


def art_bunker(x, y, w, h):
    grad(x, y, w, h, (190, 210, 230), (214, 224, 200))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(120, 150, 80))
    d.polygon([(x + 12, y + h - 10), (x + 22, y + h - 24), (x + 96, y + h - 24), (x + 108, y + h - 10)], fill=(110, 110, 100), outline=(60, 60, 54))
    d.rectangle([x + 52, y + h - 20, x + 68, y + h - 10], fill=(40, 40, 36))
    for (cx, cy, r) in [(x + 130, y + 28, 12), (x + 146, y + 20, 14), (x + 162, y + 12, 12), (x + 148, y + 30, 11), (x + 172, y + 24, 12)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(130, 126, 134))
    d.polygon([(x + 120, y + h - 10), (x + 134, y + 34), (x + 160, y + 34), (x + 176, y + h - 10)], fill=(150, 146, 152))
    # hazard diamond
    hx, hy = x + 30, y + 8
    d.polygon([(hx, hy), (hx + 12, hy + 12), (hx, hy + 24), (hx - 12, hy + 12)], fill=(250, 214, 20), outline=(40, 30, 0))
    d.text((hx, hy + 12), "!", font=F(11, "b"), fill=(40, 30, 0), anchor="mm")
    label(x + w - 4, y + h - 14, "LEAD", 10, (255, 255, 255), (60, 60, 66), "b", "ra")


def art_tower(x, y, w, h):
    grad(x, y, w, h, (20, 26, 56), (90, 60, 80))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(24, 24, 32))
    for k, (bx, bh) in enumerate([(10, 18), (36, 26), (150, 24), (176, 16)]):
        d.rectangle([x + bx, y + h - bh, x + bx + 20, y + h], fill=(40, 42, 56))
    tx = x + 84
    d.polygon([(tx, y + h), (tx + 8, y + 8), (tx + 28, y + 8), (tx + 36, y + h)], fill=(52, 58, 80))
    d.rectangle([tx + 6, y + 2, tx + 30, y + 10], fill=(70, 78, 104))
    for r in range(5):
        for c in range(3):
            if (r + c) % 2 == 0:
                d.rectangle([tx + 8 + c * 8, y + 14 + r * 6, tx + 12 + c * 8, y + 17 + r * 6], fill=(250, 214, 110))
    # fire near top
    fx = tx + 30
    d.polygon([(fx - 4, y + 18), (fx - 6, y + 6), (fx, y + 12), (fx + 2, y), (fx + 6, y + 10), (fx + 10, y + 4), (fx + 8, y + 18)], fill=(250, 120, 30))
    # drone with trail
    d.line([(x + 150, y + 6), (tx + 38, y + 14)], fill=(240, 80, 70), width=1)
    d.polygon([(x + 146, y + 4), (x + 162, y + 4), (x + 158, y + 10), (x + 150, y + 10)], fill=(200, 202, 210))
    d.line([(x + 142, y + 3), (x + 166, y + 3)], fill=(200, 202, 210), width=2)


def art_fence(x, y, w, h):
    grad(x, y, w, h, (200, 214, 226), (196, 180, 150))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(170, 150, 110))
    for i in range(6):  # refugees
        px = x + 10 + i * 17
        d.ellipse([px, y + 14, px + 9, y + 23], fill=(70, 50, 40))
        d.polygon([(px - 2, y + h), (px + 4, y + 23), (px + 11, y + h)], fill=(70, 100, 150) if i % 2 == 0 else (150, 80, 70))
    # fence
    for fx in range(x + 112, x + 122):
        pass
    d.line([(x + 118, y + 2), (x + 118, y + h)], fill=(60, 60, 60), width=3)
    for yy in range(y + 6, y + h, 8):
        d.line([(x + 106, yy), (x + 130, yy + 6)], fill=(80, 80, 80))
        d.line([(x + 106, yy + 6), (x + 130, yy)], fill=(80, 80, 80))
    d.line([(x + 98, y + 24), (x + 150, y + 24)], fill=RED, width=3)
    d.polygon([(x + 150, y + 17), (x + 162, y + 24), (x + 150, y + 31)], fill=RED)
    label(x + w - 4, y + 4, "MYANMAR", 10, (255, 255, 255), (50, 50, 60), "b", "ra")


def art_boat(x, y, w, h):
    grad(x, y, w, int(h * 0.55), (186, 214, 230), (150, 190, 210))
    grad(x, y + int(h * 0.55), w, h - int(h * 0.55), (60, 120, 130), (30, 80, 96))
    by = y + 26
    d.polygon([(x + 24, by), (x + 176, by), (x + 160, by + 12), (x + 40, by + 12)], fill=(150, 90, 40), outline=(70, 40, 10))
    for i in range(11):  # overloaded passengers
        px = x + 34 + i * 12
        d.ellipse([px, by - 14, px + 8, by - 6], fill=(60, 44, 36) if i % 2 else (90, 60, 40))
        d.rectangle([px - 1, by - 6, px + 9, by], fill=(200, 80, 70) if i % 3 == 0 else (80, 110, 160))
    for k in range(0, w, 18):
        d.arc([x + k, y + 38, x + k + 14, y + 44], 200, 340, fill=(170, 220, 230))
    d.ellipse([x + 6, y + 6, x + 26, y + 26], outline=(250, 250, 250), width=4)  # life ring
    d.line([(x + 8, y + 8), (x + 24, y + 24)], fill=RED, width=3)  # none worn


# ----------------------------------------------------------------- panels
LEAD_Y, LEAD_H = 104, 202
LEAD_W = 333
LEAD_ART_H = 92
SM_Y0, SM_H = 310, 126
SM_W = 199
SM_ART_H = 44

LEAD_ART = {1: art_solomons, 2: art_gaza, 3: art_zapor}
SMALL_ART = {4: art_cup, 5: art_markets, 6: art_thermo, 7: art_store, 8: art_trial,
             9: art_factory, 10: art_bunker, 11: art_tower, 12: art_fence, 13: art_boat}


def paste_art(fn, x, y, w, h):
    """draw art into a temp image so nothing can bleed outside its box"""
    global d
    tmp = Image.new("RGB", (w, h), PANEL)
    old = d
    d = ImageDraw.Draw(tmp)
    try:
        fn(0, 0, w, h)
    finally:
        d = old
    img.paste(tmp, (x, y))


def lead_panel(i, px, py):
    s = S[i]
    col = REGION_COL[s["region"]]
    d.rectangle([px, py, px + LEAD_W - 1, py + LEAD_H - 1], fill=PANEL, outline=LINE)
    paste_art(LEAD_ART[i], px + 1, py + 1, LEAD_W - 2, LEAD_ART_H)
    d.rectangle([px + 1, py + LEAD_ART_H + 1, px + LEAD_W - 2, py + LEAD_ART_H + 4], fill=col)
    by = py + LEAD_ART_H + 5
    d.rectangle([px + 1, by, px + LEAD_W - 2, by + 36], fill=RED)
    chip(px + 5, by + 7, i, s["region"], 11, F(13, "b"))
    lines = wrap(s["head"], F(15, "x"), LEAD_W - 40)
    if len(lines) > 2:
        warn("lead %d banner %d lines" % (i, len(lines)))
    yy = by + (10 if len(lines) == 1 else 2)
    for ln in lines[:2]:
        d.text((px + 33, yy), ln, font=F(15, "x"), fill=(255, 255, 255))
        yy += 16
    ey = block(px + 6, by + 40, s["body"], F(11, "r"), INK, LEAD_W - 12, 4, 13, "lead%d body" % i)
    d.text((px + 6, py + LEAD_H - 14), s["src"], font=F(10, "b"), fill=col)
    if tw(s["src"], F(10, "b")) > LEAD_W - 12:
        warn("lead %d source too wide" % i)
    if ey > py + LEAD_H - 14:
        warn("lead %d body collides with source line (ey=%d)" % (i, ey))


def small_panel(i, px, py):
    s = S[i]
    col = REGION_COL[s["region"]]
    d.rectangle([px, py, px + SM_W - 1, py + SM_H - 1], fill=PANEL, outline=LINE)
    paste_art(SMALL_ART[i], px + 1, py + 1, SM_W - 2, SM_ART_H)
    chip(px + 3, py + 3, i, s["region"], 9, F(11, "b"))
    d.rectangle([px + 1, py + SM_ART_H + 1, px + SM_W - 2, py + SM_ART_H + 3], fill=col)
    ty = py + SM_ART_H + 5
    ty = block(px + 4, ty, s["head"], F(12, "b"), (150, 12, 24), SM_W - 8, 2, 13, "small%d head" % i)
    ty = block(px + 4, ty + 1, s["body"], F(11, "r"), INK, SM_W - 8, 4, 12, "small%d body" % i)
    if ty > py + SM_H - 12:
        warn("small %d body collides with source (ty=%d, limit %d)" % (i, ty, py + SM_H - 12))
    d.text((px + 4, py + SM_H - 12), s["src"], font=F(10, "b"), fill=col)
    if tw(s["src"], F(10, "b")) > SM_W - 8:
        warn("small %d source too wide" % i)


# ----------------------------------------------------------------- map
def poly(pts):
    return [(p[0], p[1]) for p in pts]


LAND = {
    "namerica": [(-168, 66), (-160, 71), (-140, 70), (-125, 70), (-110, 74), (-95, 72), (-82, 69), (-75, 63), (-65, 60), (-56, 52), (-66, 45),
                 (-70, 42), (-76, 35), (-81, 31), (-80, 26), (-83, 29), (-90, 29), (-97, 26), (-97, 20), (-90, 21), (-87, 21), (-88, 16),
                 (-83, 10), (-79, 9), (-78, 8), (-84, 9), (-87, 13), (-92, 15), (-105, 20), (-110, 24), (-112, 30), (-115, 30), (-110, 23),
                 (-117, 32), (-121, 35), (-124, 40), (-124, 48), (-132, 54), (-140, 59), (-150, 60), (-158, 57), (-165, 60), (-168, 66)],
    "samerica": [(-78, 8), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-35, -6), (-39, -14), (-41, -22), (-48, -26), (-58, -35), (-65, -42),
                 (-68, -52), (-72, -54), (-74, -45), (-73, -37), (-71, -30), (-70, -18), (-76, -14), (-81, -5), (-80, 0), (-78, 8)],
    "greenland": [(-55, 60), (-45, 60), (-30, 68), (-20, 75), (-20, 82), (-50, 83), (-70, 80), (-72, 76), (-55, 68)],
    "eurasia": [(-9, 37), (-9, 43), (-2, 44), (-2, 48), (2, 51), (8, 54), (9, 57), (12, 56), (14, 54), (20, 55), (21, 57), (24, 57), (24, 59.5),
                (30, 60), (30, 65), (28, 70), (40, 68), (60, 70), (80, 73), (100, 77), (115, 74), (140, 72), (160, 70), (180, 69), (180, 65),
                (170, 60), (160, 58), (156, 52), (143, 52), (140, 46), (135, 43), (130, 42), (127, 38), (129, 35), (126, 35), (125, 40),
                (121, 40), (122, 37), (119, 35), (122, 30), (120, 25), (110, 21), (108, 16), (109, 12), (105, 9), (100, 13), (100, 7), (103, 1),
                (98, 8), (98, 16), (94, 17), (91, 22), (87, 21), (80, 15), (78, 8), (73, 16), (72, 21), (67, 24), (61, 25), (57, 26), (56, 27),
                (50, 30), (48, 29), (51, 25), (56, 24), (59, 22), (52, 16), (43, 13), (39, 20), (35, 28), (34, 31), (36, 36), (30, 36), (27, 37),
                (26, 40), (23, 40), (24, 37), (20, 40), (19, 42), (14, 45), (12, 44), (16, 40), (16, 38), (12, 38), (8, 44), (3, 43), (-1, 38),
                (-6, 36), (-9, 37)],
    "scandinavia": [(5, 58), (5, 62), (14, 67), (20, 70), (28, 71), (30, 70), (26, 66), (25, 65), (22, 66), (17, 62), (17, 58), (12, 56), (8, 58)],
    "africa": [(-17, 21), (-13, 28), (-6, 36), (10, 37), (11, 33), (20, 31), (32, 31), (34, 28), (38, 20), (43, 12), (51, 12), (46, 3), (40, -5),
               (40, -15), (35, -24), (32, -29), (27, -34), (20, -35), (17, -30), (12, -17), (14, -8), (9, -1), (9, 4), (5, 6), (-8, 4), (-13, 8),
               (-17, 14), (-17, 21)],
    "madagascar": [(44, -25), (48, -25), (50, -15), (49, -12), (44, -17)],
    "australia": [(114, -22), (122, -18), (130, -12), (137, -12), (142, -11), (146, -19), (153, -26), (151, -34), (146, -39), (138, -35),
                  (131, -31), (115, -34), (114, -22)],
    "nz": [(172, -34), (178, -38), (176, -40), (174, -41), (172, -40)],
    "nz2": [(173, -41), (175, -42), (170, -46), (167, -46), (170, -43)],
    "uk": [(-5, 50), (1, 51), (-2, 57), (-5, 58), (-6, 55), (-3, 54)],
    "ireland": [(-10, 52), (-6, 52), (-6, 55), (-9, 54)],
    "iceland": [(-24, 64), (-14, 64), (-14, 66), (-22, 66)],
    "japan": [(130, 32), (135, 34), (140, 36), (142, 40), (141, 45), (140, 41), (135, 36), (131, 34)],
    "borneo": [(109, 1), (116, 7), (119, 5), (117, -3), (110, -3)],
    "sumatra": [(95, 5), (98, 4), (106, -6), (102, -4)],
    "java": [(106, -6), (114, -7), (114, -8), (106, -7)],
    "png": [(131, -1), (141, -3), (150, -10), (142, -9), (136, -4)],
    "sulawesi": [(119, 1), (125, 1), (122, -5), (120, -4)],
    "philippines": [(120, 18), (122, 18), (126, 8), (124, 7), (121, 14)],
    "solomons": [(155, -6), (159, -8), (162, -10), (160, -10), (156, -7)],
    "sicily": [(12, 38), (15, 38), (15, 37), (13, 37)],
    "cuba": [(-85, 22), (-77, 20), (-74, 20), (-80, 23)],
    "taiwan": [(120, 22), (122, 25), (121, 25.3), (120, 23)],
    "srilanka": [(80, 9.5), (82, 7), (81, 6), (80, 7)],
}
WATER = {
    "black": [(28, 41.5), (28, 44), (30, 46), (33, 46), (35, 45), (38, 47), (41, 42), (36, 41), (31, 41)],
    "caspian": [(47, 45), (50, 47), (53, 45), (54, 40), (53, 37), (49, 38), (49, 41), (47, 43)],
    "baltic": [(10, 54), (14, 54.2), (20, 55), (21, 57), (24, 57), (24, 59.5), (28, 60), (25, 60.4), (21.5, 60.5), (21, 63), (25, 65), (22, 65.8),
               (17.5, 62), (17.5, 58), (13, 56.2), (11, 55.8)],
    "redsea": [(32.3, 29.8), (34.2, 28), (35, 26.5), (37.2, 21.5), (39.5, 16), (42.6, 13), (43.4, 12.6), (42.6, 12.4), (40, 15.2), (38.2, 19.2),
               (35.5, 24.5), (33.7, 27.5), (32.6, 29.6)],
    "persian": [(48, 30), (50, 30), (51.5, 28), (53, 26.8), (56.3, 26.3), (56.3, 25.5), (54, 24.3), (51.5, 24.2), (51, 25.8), (50, 27.5), (48.8, 29.2)],
    "med_hole": [(-1, 36.4), (10, 37.3), (11, 33.2), (20, 32), (32, 31.2), (34, 31.5), (36, 35.5), (30, 36), (26, 35), (20, 38), (16, 38.3), (10, 38.8), (2, 38.7)],
}
SEA = (22, 54, 98)
LANDC = (88, 112, 92)
LANDC2 = (104, 128, 106)


def make_proj(box, lon0, lon1, lat0, lat1):
    bx, by, bw, bh = box
    sx = bw / (lon1 - lon0)
    sy = bh / (lat1 - lat0)  # lat0 = bottom, lat1 = top

    def p(lon, lat):
        return (bx + (lon - lon0) * sx, by + (lat1 - lat) * sy)
    return p


def draw_geo(tile, proj, lw=1):
    """draw land+water polygons onto ImageDraw `tile` using proj"""
    for name, pts in LAND.items():
        tile.polygon([proj(*q) for q in pts], fill=LANDC, outline=LANDC2)
    for name, pts in WATER.items():
        tile.polygon([proj(*q) for q in pts], fill=SEA)


def place_pins(items, rmin):
    """deterministic repulsion; items: list of (id, x, y). returns dict id->(x, y)"""
    pos = {i: [x, y] for i, x, y in items}
    ids = sorted(pos)
    for _ in range(400):
        moved = False
        for a_i in range(len(ids)):
            for b_i in range(a_i + 1, len(ids)):
                a, b = ids[a_i], ids[b_i]
                dx = pos[b][0] - pos[a][0]
                dy = pos[b][1] - pos[a][1]
                dist = math.hypot(dx, dy)
                if dist < rmin:
                    if dist < 0.01:
                        ang = (a * 2.399963 + b) % (2 * math.pi)
                        dx, dy, dist = math.cos(ang), math.sin(ang), 1.0
                    push = (rmin - dist) / 2 + 0.05
                    ux, uy = dx / dist, dy / dist
                    pos[a][0] -= ux * push
                    pos[a][1] -= uy * push
                    pos[b][0] += ux * push
                    pos[b][1] += uy * push
                    moved = True
        if not moved:
            break
    return pos


def draw_map_area(box, lon0, lon1, lat0, lat1, ids, title, tile_name, names=None, title_top_right=False, rects=None):
    bx, by, bw, bh = box
    proj = make_proj((0, 0, bw, bh), lon0, lon1, lat0, lat1)
    tile = Image.new("RGB", (bw, bh), SEA)
    td = ImageDraw.Draw(tile)
    draw_geo(td, proj)
    # graticule
    for lo in range(int(math.ceil(lon0 / 30) * 30), int(lon1) + 1, 30):
        px = proj(lo, 0)[0]
        td.line([(px, 0), (px, bh)], fill=(38, 74, 120))
    for la in range(int(math.ceil(lat0 / 30) * 30), int(lat1) + 1, 30):
        py = proj(0, la)[1]
        td.line([(0, py), (bw, py)], fill=(38, 74, 120))
    for (lo0, lo1, la0, la1, tag) in (rects or []):  # inset markers, under the pins
        x0, y0 = proj(lo0, la1)
        x1, y1 = proj(lo1, la0)
        td.rectangle([x0, y0, x1, y1], outline=(255, 255, 255), width=1)
        ty_ = y1 + 1 if tag == "EU" else y0 - 13
        td.rectangle([x0 - 1, ty_, x0 + 14, ty_ + 12], fill=(255, 255, 255))
        td.text((x0 + 1, ty_ + 1), tag, font=F(10, "b"), fill=(20, 30, 50))
    # pins (true spots -> repulsed)
    true = {}
    for i in ids:
        s = S[i]
        true[i] = proj(s["lon"], s["lat"])
    R = 8
    items = [(i, true[i][0], true[i][1]) for i in ids]
    placed = place_pins(items, 2 * R + 1.5)
    for i in ids:  # clamp
        placed[i][0] = min(max(placed[i][0], R + 3), bw - R - 3)
        placed[i][1] = min(max(placed[i][1], R + 3), bh - R - 3)
    placed = place_pins([(i, placed[i][0], placed[i][1]) for i in ids], 2 * R + 1.5)
    for i in ids:
        placed[i][0] = min(max(placed[i][0], R + 3), bw - R - 3)
        placed[i][1] = min(max(placed[i][1], R + 3), bh - R - 3)
    for i in ids:  # leaders + true-spot dots first
        tx_, ty_ = true[i]
        px, py = placed[i]
        if math.hypot(px - tx_, py - ty_) > 3.5:
            td.line([(tx_, ty_), (px, py)], fill=(255, 255, 255), width=1)
        td.ellipse([tx_ - 2, ty_ - 2, tx_ + 2, ty_ + 2], fill=(255, 255, 255), outline=(20, 20, 20))
    for i in sorted(ids):
        px, py = placed[i]
        col = REGION_COL[S[i]["region"]]
        td.ellipse([px - R, py - R, px + R, py + R], fill=col, outline=(255, 255, 255), width=2)
        td.text((px, py), str(i), font=F(10, "b"), fill=(255, 255, 255), anchor="mm")
    if names:
        for i in sorted(ids):
            if i in names:
                px, py = placed[i]
                nf = F(10, "b")
                nx = px + R + 3
                if nx + tw(names[i], nf) > bw - 2:
                    nx = px - R - 3 - tw(names[i], nf)
                td.rectangle([nx - 1, py - 6, nx + tw(names[i], nf) + 1, py + 6], fill=(14, 28, 52))
                td.text((nx, py), names[i], font=nf, fill=(255, 255, 255), anchor="lm")
    img.paste(tile, (bx, by))
    d.rectangle([bx, by, bx + bw - 1, by + bh - 1], outline=(30, 40, 60))
    # title tag
    f = F(10, "b")
    ty0 = by + bh - 15
    tx0 = bx + 1
    if title_top_right:
        ty0 = by + 2
        tx0 = bx + bw - 8 - int(tw(title, f))
    d.rectangle([tx0, ty0, tx0 + 6 + tw(title, f), ty0 + 13], fill=(255, 255, 255))
    d.text((tx0 + 3, ty0 + 1), title, font=f, fill=(20, 30, 50))
    return placed


# ----------------------------------------------------------------- compose
def main():
    # ---- masthead
    d.rectangle([0, 0, W, 52], fill=(18, 22, 34))
    d.text((8, 0), "TUESDAY 24 NOVEMBER 2026", font=F(29, "x"), fill=(255, 255, 255))
    d.text((W - 8, 6), "THE DAY IN ONE IMAGE", font=F(14, "b"), fill=(255, 214, 90), anchor="ra")
    d.text((W - 8, 23), "%d STORIES · 6 REGIONS · ALL DATED 24 NOV" % TOTAL, font=F(12, "b"), fill=(220, 224, 236), anchor="ra")
    summary = ("Solomon Islands drops China's security pact · Israel kills Hamas security chief · Putin vows retaliation after "
               "Zaporizhzhia strike · Senegal regains Africa Cup")
    f = F(12, "b")
    d.text((10, 37), summary, font=f, fill=(255, 255, 255))
    if tw(summary, f) > W - 20:
        warn("summary too wide")

    # ---- data strip
    cw = (W - 12) // 6
    for k, (num, lab, src) in enumerate(DATA_STRIP):
        cx = 6 + k * cw
        d.rectangle([cx, 55, cx + cw - 3, 100], fill=(255, 244, 214), outline=(214, 170, 60))
        d.text((cx + 5, 54), num, font=F(25, "x"), fill=(160, 20, 30))
        for li, ln in enumerate((lab, "(" + src + ")")):
            if tw(ln, F(10, "b")) > cw - 10:
                warn("data cell %d line too wide: %s" % (k, ln))
            d.text((cx + 5, 82 + li * 10), ln, font=F(10, "b"), fill=INK if li == 0 else GREY)

    # ---- leads
    for k, i in enumerate((1, 2, 3)):
        lead_panel(i, 6 + k * (LEAD_W + 3), LEAD_Y)
    # ---- smalls
    for k, i in enumerate(range(4, 14)):
        r, c = divmod(k, 5)
        small_panel(i, 6 + c * (SM_W + 4), SM_Y0 + r * (SM_H + 3))

    # ---- bottom block
    BY = SM_Y0 + 2 * SM_H + 3 + 4  # 559
    LX, LW = 6, 500
    # ALSO list (left)
    d.rectangle([LX, BY, LX + LW - 1, BY + 14], fill=(18, 22, 34))
    d.text((LX + 5, BY + 1), "ALSO ON 24 NOVEMBER  (number = map pin; colour = region)", font=F(11, "b"), fill=(255, 255, 255))
    ay = BY + 17
    for i in range(14, 33):
        s = S[i]
        d.rounded_rectangle([LX + 1, ay, LX + 21, ay + 12], 5, fill=REGION_COL[s["region"]])
        d.text((LX + 11, ay + 6), str(i), font=F(10, "b"), fill=(255, 255, 255), anchor="mm")
        title = s["head"]
        srcs = " (" + s["src"] + ")"
        ft, fs = F(11, "r"), F(10, "b")
        tx = LX + 25
        maxw = LW - 27
        if tw(title, ft) + tw(srcs, fs) > maxw:
            warn("ALSO %d line too wide (%d px)" % (i, tw(title, ft) + tw(srcs, fs)))
        d.text((tx, ay), title, font=ft, fill=INK)
        d.text((tx + tw(title, ft), ay + 1), srcs, font=fs, fill=REGION_COL[s["region"]])
        ay += 13.5
    also_end = int(ay)
    # UTC strip (left, under ALSO)
    uy = also_end + 3
    d.rectangle([LX, uy, LX + LW - 1, uy + 12], fill=(40, 46, 66))
    d.text((LX + 5, uy), "UTC · 5 BEATS OF THE DAY, IN ORDER (times approximate)", font=F(10, "b"), fill=(255, 255, 255))
    bw5 = LW // 5
    for k, (when, what) in enumerate(BEATS):
        cx = LX + k * bw5
        d.rectangle([cx, uy + 13, cx + bw5 - 1, uy + 13 + 50], fill=(238, 240, 248), outline=(150, 156, 180))
        d.text((cx + 3, uy + 14), "%d · %s" % (k + 1, when), font=F(10, "b"), fill=(30, 40, 120))
        block(cx + 3, uy + 26, what, F(10, "r"), INK, bw5 - 6, 3, 11, "beat%d" % (k + 1))
    left_end = uy + 13 + 50

    # map (right)
    RX, RW = 512, 506
    mp_h = 196
    world_ids = [i for i in S if i not in (3, 6, 14, 15, 16, 2, 11, 17, 18)]
    eu_ids = [3, 6, 14, 15, 16]
    me_ids = [2, 11, 17, 18]
    assert sorted(world_ids + eu_ids + me_ids) == list(range(1, TOTAL + 1)), "every story pinned exactly once"
    d.rectangle([RX, BY, RX + RW - 1, BY + 14], fill=(18, 22, 34))
    d.text((RX + 5, BY + 1), "WORLD MAP — ONE PIN PER STORY (white dot + line = true spot)", font=F(11, "b"), fill=(255, 255, 255))
    draw_map_area((RX, BY + 15, RW, mp_h), -178, 180, -56, 80, world_ids, "WORLD", "world", None, False,
                  [(-12, 42, 36, 61, "EU"), (32, 60, 11.5, 33.5, "ME")])
    iy = BY + 15 + mp_h + 3
    ih = 122
    iw = (RW - 4) // 2
    draw_map_area((RX, iy, iw, ih), -12, 42, 36, 61, eu_ids, "EUROPE inset", "eu",
                  {3: "Zaporizhzhia", 6: "London", 14: "Gulf of Finland", 15: "Copenhagen", 16: "Eskişehir"})
    draw_map_area((RX + iw + 4, iy, iw, ih), 32, 60, 11.5, 33.5, me_ids, "MIDDLE EAST inset (stretched)", "me",
                  {2: "Gaza", 11: "Riyadh", 17: "Sanaa", 18: "RAK"}, True)
    right_end = iy + ih

    # ---- region bar
    ry = max(left_end, right_end) + 3
    x = 6
    totalw = W - 12
    f = F(11, "b")
    for k, r in enumerate(REGIONS):
        segw = int(round(totalw * COUNTS[r] / TOTAL)) if k < len(REGIONS) - 1 else (6 + totalw) - x
        d.rectangle([x, ry, x + segw - 1, ry + 16], fill=REGION_COL[r])
        t = "%s %d" % (r, COUNTS[r])
        if tw(t, f) > segw - 4:
            warn("region label too wide: " + t)
        d.text((x + segw // 2, ry + 8), t, font=f, fill=(255, 255, 255), anchor="mm")
        x += segw
    # ---- date check
    dy = ry + 20
    dh = 58
    d.rectangle([6, dy, W - 7, dy + dh], fill=(255, 232, 230), outline=RED, width=3)
    d.rectangle([6, dy, 126, dy + dh], fill=RED)
    d.text((12, dy + 5), "DATE CHECK", font=F(15, "x"), fill=(255, 255, 255))
    d.text((12, dy + 23), "NOT 24 NOV —", font=F(11, "b"), fill=(255, 255, 255))
    d.text((12, dy + 35), "left out on purpose", font=F(11, "b"), fill=(255, 255, 255))
    cw5 = (W - 14 - 120 - 6) // 5
    for k, (dt, tx_) in enumerate(DATE_CHECK):
        cx = 6 + 123 + k * cw5
        d.text((cx + 4, dy + 4), dt, font=F(13, "x"), fill=RED)
        block(cx + 4, dy + 20, tx_, F(11, "r"), INK, cw5 - 10, 2, 12, "datecheck%d" % k)
    d.text((6 + 123 + 4, dy + dh - 14), "Nothing else on this poster is dated to any other day.", font=F(11, "b"), fill=RED)
    # ---- footer
    fy = dy + dh + 4
    foot1 = ("SOURCES: ABC (AU) · RNZ · Al Jazeera · Kyiv Independent · AP · Reuters · Washington Post · allAfrica · "
             "Gulf News · VnExpress · The Business Standard · Daily Star")
    foot2 = ("CERTAINTY: REPORTED = stated by named press; CLAIM = one side's assertion or counts that differ "
             "(Hamas \"war crime\", hostage numbers, Houthi blame, lead-plume warning).")
    for k, t in enumerate((foot1, foot2)):
        if tw(t, F(10, "r")) > W - 12:
            warn("footer line %d too wide" % (k + 1))
        d.text((6, fy + k * 11), t, font=F(10, "r"), fill=GREY)
    end = fy + 22
    if end > H:
        warn("layout runs %d px past the bottom" % (end - H))
    return dict(also_end=also_end, left_end=left_end, right_end=right_end, region_y=ry, datecheck_y=dy, footer_y=fy, end=end)


if __name__ == "__main__":
    info = main()
    print("layout:", info)
    print("font sizes used:", sorted(SIZES_USED), "floor =", MIN_SIZE)
    assert min(SIZES_USED) >= MIN_SIZE
    img.save(OUT, optimize=False)
    print("saved", OUT, "warnings:", len(WARN))
    sys.exit(1 if WARN else 0)
