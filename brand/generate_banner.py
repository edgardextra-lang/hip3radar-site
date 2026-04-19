#!/usr/bin/env python3
"""
HIP3Radar Twitter banner — 1500x500, Bloomberg-terminal aesthetic.
Profile-pic safe zone: bottom-left ~220x220 kept clear.
"""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Brand tokens (match site CSS)
BG        = (10, 12, 11)
SURFACE   = (17, 20, 15)
SURFACE_2 = (22, 26, 19)
LINE      = (31, 38, 32)
LINE_2    = (42, 51, 43)
INK       = (232, 236, 228)
INK_2     = (168, 176, 164)
INK_3     = (106, 115, 104)
ACCENT    = (126, 243, 160)   # #7ef3a0
ACCENT_D  = (62, 195, 110)
WARN      = (255, 182, 72)
DANGER    = (255, 107, 107)

TARGET_W, TARGET_H = 1500, 500
SS = 2
W, H = TARGET_W * SS, TARGET_H * SS
OUT = Path(__file__).parent


def font(weight, px):
    px = int(px * SS)
    paths = {
        "mono":    ["/System/Library/Fonts/SFNSMono.ttf", "/System/Library/Fonts/Menlo.ttc"],
        "regular": ["/System/Library/Fonts/Helvetica.ttc"],
        "bold":    ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"],
        "serif":   ["/System/Library/Fonts/Supplemental/Georgia Italic.ttf", "/System/Library/Fonts/Times.ttc"],
    }
    for p in paths[weight]:
        try: return ImageFont.truetype(p, px)
        except Exception: pass
    return ImageFont.load_default()


def background():
    """Dark bg with a subtle green radial glow in the upper-right."""
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    y, x = np.ogrid[:H, :W]
    arr[:, :, 0] = BG[0]; arr[:, :, 1] = BG[1]; arr[:, :, 2] = BG[2]
    glow = np.exp(-((x - W * 0.78) ** 2 + (y - H * 0.30) ** 2) / (2 * (W * 0.28) ** 2))
    arr[:, :, 0] = np.clip(arr[:, :, 0] + ACCENT[0] * glow * 0.10, 0, 255)
    arr[:, :, 1] = np.clip(arr[:, :, 1] + ACCENT[1] * glow * 0.10, 0, 255)
    arr[:, :, 2] = np.clip(arr[:, :, 2] + ACCENT[2] * glow * 0.10, 0, 255)
    return Image.fromarray(arr)


def add_grid(img):
    """Subtle hairline terminal grid."""
    d = ImageDraw.Draw(img, "RGBA")
    step = 40 * SS
    for x in range(0, W, step):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 6), width=1)
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 6), width=1)
    return img


def draw_radar_mark(img, cx, cy, r):
    """HIP3Radar logo glyph — green ring + sweeping arc + center dot."""
    d = ImageDraw.Draw(img, "RGBA")
    # outer ring
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ACCENT, width=int(3 * SS))
    # mid ring
    d.ellipse([cx - r * 0.66, cy - r * 0.66, cx + r * 0.66, cy + r * 0.66],
              outline=(126, 243, 160, 110), width=int(1.5 * SS))
    # sweep wedge
    wedge = Image.new("RGBA", (r * 2 + 20, r * 2 + 20), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wedge)
    wd.pieslice([10, 10, r * 2 + 10, r * 2 + 10], -115, -55,
                fill=(126, 243, 160, 95))
    img.paste(wedge, (cx - r - 10, cy - r - 10), wedge)
    # center dot
    cr = int(r * 0.12)
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=ACCENT)


def grade_pill(img, x, y, grade, rating, color):
    """Letter-grade chip: [AA · 94]"""
    d = ImageDraw.Draw(img, "RGBA")
    fg = color; bg = (*color, 40); border = (*color, 170)
    w, h = 130 * SS, 44 * SS
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(8 * SS), fill=bg, outline=border, width=int(1.5 * SS))
    f_grade  = font("bold", 18)
    f_num    = font("mono", 14)
    d.text((x + 18 * SS, y + 9 * SS), grade, fill=fg, font=f_grade)
    d.text((x + 60 * SS, y + 13 * SS), f"· {rating}", fill=fg, font=f_num)


def main():
    img = background()
    img = add_grid(img)

    # ── scan-line ticker strip at top ──
    d = ImageDraw.Draw(img, "RGBA")
    ticker_y = 28 * SS
    d.rectangle([0, 0, W, ticker_y + 46 * SS], fill=(17, 20, 15, 200))
    d.line([(0, ticker_y + 46 * SS), (W, ticker_y + 46 * SS)], fill=LINE, width=1)
    f_mono_sm = font("mono", 12)
    tickers = [
        ("●", ACCENT, "LIVE"),
        ("", INK_3, "HL:BTC"),  ("", INK, " $72,481 "), ("", ACCENT, "+0.22%  "),
        ("", INK_3, "XYZ:TSLA"),("", INK, " $428.04 "), ("", ACCENT, "+2.38%  "),
        ("", INK_3, "VT:OPENAI"),("", INK, " $341.70 "),("", ACCENT, "+4.81%  "),
        ("", INK_3, "hY:ETH"),  ("", INK, " $3,914 "),  ("", ACCENT, "+1.02%  "),
        ("", INK_3, "AU:10Y"),  ("", INK, " 4.31% "),   ("", ACCENT, "+6bps  "),
        ("", INK_3, "DC:F1"),   ("", INK, " $1.28 "),   ("", DANGER, "-1.92%  "),
        ("", INK_3, "MK:KAITO"),("", INK, " $1.07 "),   ("", ACCENT, "+9.2%  "),
    ]
    tx = 36 * SS
    for _, color, txt in tickers:
        d.text((tx, ticker_y + 14 * SS), txt, fill=color, font=f_mono_sm)
        tw = d.textbbox((0, 0), txt, font=f_mono_sm)[2]
        tx += tw + 2 * SS

    # ── logo + brand ──
    logo_x, logo_y = 60 * SS, 140 * SS
    draw_radar_mark(img, logo_x + 40 * SS, logo_y + 40 * SS, 36 * SS)
    f_brand = font("bold", 36)
    d.text((logo_x + 100 * SS, logo_y + 18 * SS), "HIP3Radar", fill=INK, font=f_brand)
    f_url = font("mono", 13)
    d.text((logo_x + 100 * SS, logo_y + 65 * SS), "hip3radar.xyz", fill=INK_3, font=f_url)

    # ── primary headline (right side) ──
    hx = 600 * SS
    hy = 140 * SS
    f_eye = font("mono", 11)
    d.text((hx, hy), "// INDEPENDENT · NOT AFFILIATED", fill=ACCENT, font=f_eye)
    f_h1 = font("bold", 40)
    d.text((hx, hy + 28 * SS), "Risk surveillance", fill=INK, font=f_h1)
    f_h1_em = font("serif", 40)
    d.text((hx, hy + 76 * SS), "for every HIP-3 perp.", fill=INK_2, font=f_h1_em)

    f_sub = font("mono", 13)
    d.text((hx, hy + 138 * SS),
           "325 markets  ·  9 deployers  ·  scored every 60s  ·  public API",
           fill=INK_2, font=f_sub)

    # ── letter-grade ribbon (bottom-right) ──
    gy = 380 * SS
    gx = 600 * SS
    d.text((gx, gy - 24 * SS), "// SAFETY GRADES", fill=INK_3, font=f_eye)
    grade_pill(img, gx,                gy, "AA", 94, ACCENT)
    grade_pill(img, gx + 150 * SS,     gy, "A",  87, ACCENT)
    grade_pill(img, gx + 300 * SS,     gy, "B+", 74, WARN)
    grade_pill(img, gx + 450 * SS,     gy, "C",  58, WARN)
    grade_pill(img, gx + 600 * SS,     gy, "D",  38, DANGER)
    grade_pill(img, gx + 750 * SS,     gy, "F",  18, DANGER)

    # ── right-edge stamp ──
    stamp_x, stamp_y = W - 280 * SS, 150 * SS
    f_stamp_lbl = font("mono", 11)
    f_stamp_val = font("bold", 52)
    d.text((stamp_x, stamp_y), "TRUST LAYER FOR HIP-3", fill=ACCENT, font=f_stamp_lbl)
    d.text((stamp_x, stamp_y + 26 * SS), "HL + 8 dexes", fill=INK, font=font("bold", 28))
    d.text((stamp_x, stamp_y + 80 * SS), "324", fill=ACCENT, font=f_stamp_val)
    d.text((stamp_x + 125 * SS, stamp_y + 108 * SS), "markets live", fill=INK_2, font=f_mono_sm)

    # downsample for AA
    img = img.resize((TARGET_W, TARGET_H), Image.LANCZOS)

    # ── clear the profile-pic safe zone (bottom-left ~220x220) with a subtle tint ──
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, TARGET_H - 220, 220, TARGET_H], fill=(10, 12, 11, 210))

    png_path = OUT / "hip3radar-banner-twitter.png"
    jpg_path = OUT / "hip3radar-banner-twitter.jpg"
    img.save(png_path, "PNG", optimize=True)
    img.convert("RGB").save(jpg_path, "JPEG", quality=92, optimize=True)
    print(f"→ {png_path} ({png_path.stat().st_size // 1024}KB)")
    print(f"→ {jpg_path} ({jpg_path.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
