#!/usr/bin/env python3
"""
HIP3Radar Open Graph image generator.
1200x630 — standard OG/Twitter card spec.

Used in <meta property="og:image"> for link previews on
Twitter, iMessage, Telegram, Slack, Discord, LinkedIn, etc.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Brand tokens
BG = (10, 12, 11)            # terminal near-black
BG_2 = (17, 20, 15)          # elevated surface
TEXT = (232, 236, 228)       # ink
TEXT_MUTED = (168, 176, 164) # ink-2
PINK = (126, 243, 160)    # radar-green accent
PINK_DEEP = (62, 195, 110)    # deeper green
AMBER = (255, 176, 32)
BORDER = (31, 38, 32)        # line

TARGET_W, TARGET_H = 1200, 630
SS = 2
W, H = TARGET_W * SS, TARGET_H * SS

OUT_DIR = Path(__file__).parent


def load_font(weight: str, px_target: int):
    px = int(px_target * SS)
    candidates = {
        "black": [
            "/System/Library/Fonts/Supplemental/Arial Black.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ],
        "bold": [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ],
        "regular": [
            "/System/Library/Fonts/Helvetica.ttc",
        ],
        "mono": [
            "/System/Library/Fonts/SFNSMono.ttf",
            "/System/Library/Fonts/Menlo.ttc",
            "/System/Library/Fonts/Monaco.ttf",
        ],
    }
    for path in candidates[weight]:
        try:
            return ImageFont.truetype(path, px)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def draw_background():
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    y, x = np.ogrid[:H, :W]
    # Dark gradient with subtle pink glow upper-right
    dist = np.sqrt((x - W * 0.75) ** 2 + (y - H * 0.2) ** 2) / (W * 0.9)
    t = np.clip(dist, 0, 1)
    r = BG_2[0] * (1 - t) + BG[0] * t
    g = BG_2[1] * (1 - t) + BG[1] * t
    b = BG_2[2] * (1 - t) + BG[2] * t
    pink_glow = np.exp(-((x - W * 0.82) ** 2 + (y - H * 0.3) ** 2) / (2 * (W * 0.25) ** 2))
    r += PINK[0] * pink_glow * 0.1
    g += PINK[1] * pink_glow * 0.1
    b += PINK[2] * pink_glow * 0.1
    arr[:, :, 0] = np.clip(r, 0, 255)
    arr[:, :, 1] = np.clip(g, 0, 255)
    arr[:, :, 2] = np.clip(b, 0, 255)
    return Image.fromarray(arr, mode="RGB")


def draw_radar_dot(img, cx, cy, radius):
    draw = ImageDraw.Draw(img, "RGBA")
    # Glow
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    glow_r = int(radius * 1.7)
    gd.ellipse([cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r], fill=PINK + (70,))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius * 0.5))
    img.paste(glow_layer, (0, 0), glow_layer)
    # Outer disc with radial gradient
    size = radius * 2 + 10
    disc = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    disc_arr = np.zeros((size, size, 4), dtype=np.uint8)
    yy, xx = np.ogrid[:size, :size]
    disc_cx = disc_cy = size / 2
    hx = size * 0.42
    hy = size * 0.42
    d_c = np.sqrt((xx - disc_cx) ** 2 + (yy - disc_cy) ** 2)
    d_h = np.sqrt((xx - hx) ** 2 + (yy - hy) ** 2)
    t = np.clip(d_h / radius, 0, 1) ** 1.4
    r_ch = PINK[0] * (1 - t) + PINK_DEEP[0] * t
    g_ch = PINK[1] * (1 - t) + PINK_DEEP[1] * t
    b_ch = PINK[2] * (1 - t) + PINK_DEEP[2] * t
    mask = d_c <= radius
    disc_arr[mask, 0] = r_ch[mask]
    disc_arr[mask, 1] = g_ch[mask]
    disc_arr[mask, 2] = b_ch[mask]
    disc_arr[mask, 3] = 255
    inner_r = radius * 0.38
    inner_mask = d_c <= inner_r
    disc_arr[inner_mask, 0] = BG[0]
    disc_arr[inner_mask, 1] = BG[1]
    disc_arr[inner_mask, 2] = BG[2]
    disc_arr[inner_mask, 3] = 255
    disc = Image.fromarray(disc_arr, mode="RGBA")
    img.paste(disc, (int(cx - size / 2), int(cy - size / 2)), disc)


def generate_jelly_curve(width_px, height_px):
    jelly_scores = [4.1, 11.8, 28.5, 36.2, 42.8, 51.4, 56.9, 62.3, 67.5,
                    73.1, 78.9, 82.4, 85.7, 87.4, 86.9, 82.1, 74.3, 68.9, 58.2, 48.7, 0]
    n = len(jelly_scores)
    points = []
    for i, s in enumerate(jelly_scores):
        x = (i / (n - 1)) * width_px
        y = height_px - (s / 100) * height_px
        points.append((x, y))
    return points


def draw_risk_curve(img):
    draw = ImageDraw.Draw(img, "RGBA")
    chart_x0 = int(W * 0.56)
    chart_x1 = int(W * 0.94)
    chart_y0 = int(H * 0.30)
    chart_y1 = int(H * 0.74)
    chart_w = chart_x1 - chart_x0
    chart_h = chart_y1 - chart_y0

    # Threshold lines
    for frac, color in [(0.40, AMBER), (0.60, PINK)]:
        y = int(chart_y0 + chart_h * (1 - frac))
        dash_len = int(12 * SS)
        gap_len = int(10 * SS)
        x_cur = chart_x0
        while x_cur < chart_x1:
            draw.line([(x_cur, y), (min(x_cur + dash_len, chart_x1), y)],
                      fill=color + (160,), width=int(2 * SS))
            x_cur += dash_len + gap_len

    # Curve
    curve = generate_jelly_curve(chart_w, chart_h)
    curve_abs = [(chart_x0 + x, chart_y0 + y) for x, y in curve]

    # Filled area
    fill_polygon = [(chart_x0, chart_y1)] + curve_abs + [(chart_x1, chart_y1)]
    fill_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(fill_layer).polygon(fill_polygon, fill=PINK + (70,))
    fill_layer = fill_layer.filter(ImageFilter.GaussianBlur(SS * 2))
    img.paste(fill_layer, (0, 0), fill_layer)
    fill2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(fill2).polygon(fill_polygon, fill=PINK + (45,))
    img.paste(fill2, (0, 0), fill2)

    # Curve line
    draw.line(curve_abs, fill=PINK, width=int(6 * SS), joint="curve")

    # Peak dot
    peak = max(curve_abs, key=lambda p: -p[1])
    for rr in range(int(24 * SS), int(6 * SS), -2):
        a = int(50 * (1 - (rr - 6 * SS) / (18 * SS)))
        draw.ellipse([peak[0] - rr, peak[1] - rr, peak[0] + rr, peak[1] + rr], fill=PINK + (a,))
    dot_r = int(10 * SS)
    draw.ellipse([peak[0] - dot_r, peak[1] - dot_r, peak[0] + dot_r, peak[1] + dot_r], fill=PINK)
    inner_r = int(4 * SS)
    draw.ellipse([peak[0] - inner_r, peak[1] - inner_r, peak[0] + inner_r, peak[1] + inner_r], fill=TEXT)

    # Peak label pill
    label_font = load_font("black", 26)
    label = "87.4"
    bbox = draw.textbbox((0, 0), label, font=label_font)
    lw = bbox[2] - bbox[0]
    lh = bbox[3] - bbox[1]
    px = peak[0] - lw - int(24 * SS)
    py = peak[1] - lh // 2 - int(6 * SS)
    pad_x = int(14 * SS)
    pad_y = int(8 * SS)
    draw.rounded_rectangle(
        [px - pad_x, py - pad_y, px + lw + pad_x, py + lh + pad_y],
        radius=int(10 * SS), fill=PINK + (240,))
    draw.text((px, py - int(2 * SS)), label, font=label_font, fill=TEXT)

    # Chart caption
    cap_font = load_font("bold", 13)
    draw.text((chart_x0, chart_y0 - int(32 * SS)),
              "JELLY · MAR 26 2025 · $12M HLP LOSS",
              font=cap_font, fill=TEXT_MUTED)


def draw_text_zone(img):
    draw = ImageDraw.Draw(img, "RGBA")
    x0 = int(W * 0.06)

    # "PUBLIC BETA" pill
    badge_font = load_font("bold", 16)
    badge_text = "● PUBLIC BETA"
    bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    pad_x = int(16 * SS)
    pad_y = int(9 * SS)
    badge_y = int(H * 0.23)
    draw.rounded_rectangle(
        [x0, badge_y - bh - pad_y,
         x0 + bw + 2 * pad_x, badge_y + pad_y],
        radius=int(12 * SS), fill=(255, 59, 107, 35),
        outline=PINK + (140,), width=int(2 * SS))
    draw.text((x0 + pad_x, badge_y - bh - int(2 * SS)), badge_text, font=badge_font, fill=PINK)

    # Radar dot + "HIP3Radar" wordmark
    dot_r = int(34 * SS)
    dot_x = x0 + dot_r
    dot_y = badge_y + int(70 * SS)
    draw_radar_dot(img, dot_x, dot_y, dot_r)

    wordmark_font = load_font("black", 64)
    wm_x = dot_x + dot_r + int(26 * SS)
    wm_bbox = draw.textbbox((0, 0), "HIP3Radar", font=wordmark_font)
    wm_h = wm_bbox[3] - wm_bbox[1]
    wm_y = dot_y - wm_h // 2 - int(8 * SS)
    draw.text((wm_x, wm_y), "HIP3Radar", font=wordmark_font, fill=TEXT)

    # Headline (two lines)
    head_font = load_font("black", 48)
    head_start = dot_y + dot_r + int(40 * SS)
    line1 = "Early warning for every"
    line2 = "Hyperliquid perp."
    bbox1 = draw.textbbox((0, 0), line1, font=head_font)
    line_h = bbox1[3] - bbox1[1]
    draw.text((x0, head_start), line1, font=head_font, fill=TEXT)
    draw.text((x0, head_start + line_h + int(12 * SS)), line2, font=head_font, fill=PINK)

    # Subtag
    sub_font = load_font("bold", 20)
    sub_y = head_start + 2 * (line_h + int(12 * SS)) + int(22 * SS)
    draw.text((x0, sub_y), "324 markets · 9 dexes · scored every 60 seconds",
              font=sub_font, fill=TEXT_MUTED)

    # URL at bottom-left
    url_font = load_font("mono", 22)
    url_y = int(H * 0.87)
    bar_w = int(5 * SS)
    bar_h = int(26 * SS)
    draw.rectangle([x0, url_y + int(4 * SS),
                    x0 + bar_w, url_y + int(4 * SS) + bar_h], fill=PINK)
    draw.text((x0 + int(16 * SS), url_y), "hip3radar.xyz", font=url_font, fill=TEXT)


def draw_top_accent(img):
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, int(6 * SS)], fill=PINK)


def main():
    img = draw_background()
    draw_risk_curve(img)
    draw_text_zone(img)
    draw_top_accent(img)
    img = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
    out_png = OUT_DIR / "hip3radar-og.png"
    img.save(out_png, "PNG", optimize=True)
    print(f"Saved: {out_png.name} ({out_png.stat().st_size // 1024} KB)")
    jpg = OUT_DIR / "hip3radar-og.jpg"
    img.convert("RGB").save(jpg, "JPEG", quality=92, optimize=True)
    print(f"Saved: {jpg.name} ({jpg.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
