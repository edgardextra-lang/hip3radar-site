#!/usr/bin/env python3
"""
HIP3Radar Twitter banner generator.

Output: 1500x500 PNG matching Twitter's header spec.
Profile-pic safe zone respected (bottom-left ~220x220 area stays clear).
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# --- brand tokens ---
BG = (10, 14, 26)          # #0a0e1a
BG_2 = (15, 21, 36)        # #0f1524
PANEL = (20, 28, 48)       # #141c30
BORDER = (31, 42, 68)      # #1f2a44
TEXT = (230, 237, 247)     # #e6edf7
TEXT_MUTED = (136, 146, 168)  # #8892a8
PINK = (255, 59, 107)      # #ff3b6b
PINK_DEEP = (176, 21, 74)  # #b0154a
AMBER = (255, 176, 32)     # #ffb020
OK = (32, 217, 123)        # #20d97b

# --- output sizing (supersampled for AA, then downsampled) ---
TARGET_W, TARGET_H = 1500, 500
SS = 2
W, H = TARGET_W * SS, TARGET_H * SS

OUT_DIR = Path(__file__).parent


def load_font(weight: str, px_target: int):
    """Return a PIL ImageFont scaled for supersample factor."""
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
            "/System/Library/Fonts/Supplemental/Arial.ttf",
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
    """Dark gradient background: slightly lighter top-right, darker bottom-left."""
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    y, x = np.ogrid[:H, :W]
    # Radial fade from top-right (more pink tint) to bottom-left (darker)
    dist = np.sqrt((x - W * 0.75) ** 2 + (y - H * 0.25) ** 2) / (W * 0.9)
    t = np.clip(dist, 0, 1)
    # Base colors
    r = (BG_2[0] * (1 - t) + BG[0] * t)
    g = (BG_2[1] * (1 - t) + BG[1] * t)
    b = (BG_2[2] * (1 - t) + BG[2] * t)
    # Add very subtle pink glow in the upper-right area
    pink_glow = np.exp(-((x - W * 0.78) ** 2 + (y - H * 0.35) ** 2) / (2 * (W * 0.22) ** 2))
    r += PINK[0] * pink_glow * 0.08
    g += PINK[1] * pink_glow * 0.08
    b += PINK[2] * pink_glow * 0.08
    arr[:, :, 0] = np.clip(r, 0, 255)
    arr[:, :, 1] = np.clip(g, 0, 255)
    arr[:, :, 2] = np.clip(b, 0, 255)
    return Image.fromarray(arr, mode="RGB")


def generate_jelly_curve(width_px: int, height_px: int) -> list[tuple[float, float]]:
    """Generate a JELLY-shaped risk curve: slow rise, spike, slow decline.
    Returns list of (x, y) points where y=0 is top (high risk) and y=height_px is bottom.
    Uses the real JELLY replay shape from the incident archive.
    """
    # Risk score timeline from the real JELLY replay (0-100 scale)
    jelly_scores = [4.1, 11.8, 28.5, 36.2, 42.8, 51.4, 56.9, 62.3, 67.5, 73.1,
                    78.9, 82.4, 85.7, 87.4, 86.9, 82.1, 74.3, 68.9, 58.2, 48.7, 0]
    n = len(jelly_scores)
    points = []
    for i, score in enumerate(jelly_scores):
        x = (i / (n - 1)) * width_px
        # Invert: 100 risk at top (y=0), 0 risk at bottom
        y = height_px - (score / 100) * height_px
        points.append((x, y))
    return points


def draw_risk_curve(img: Image.Image):
    """Draw the stylized JELLY risk curve on the right half of the banner."""
    draw = ImageDraw.Draw(img, "RGBA")

    # Chart area (right half, with margins, avoiding the text zone)
    chart_x0 = int(W * 0.52)
    chart_x1 = int(W * 0.96)
    chart_y0 = int(H * 0.22)
    chart_y1 = int(H * 0.78)
    chart_w = chart_x1 - chart_x0
    chart_h = chart_y1 - chart_y0

    # Faint grid lines (horizontal at 25, 50, 75, 100)
    for frac in (0.25, 0.5, 0.75):
        y = int(chart_y0 + chart_h * frac)
        draw.line([(chart_x0, y), (chart_x1, y)],
                  fill=BORDER + (120,), width=int(1 * SS))

    # Threshold lines: warning (40) and critical (60)
    y_warn = int(chart_y0 + chart_h * (1 - 0.40))
    y_crit = int(chart_y0 + chart_h * (1 - 0.60))
    # Warning line (amber, dashed)
    dash_len = int(10 * SS)
    gap_len = int(8 * SS)
    x_cur = chart_x0
    while x_cur < chart_x1:
        draw.line([(x_cur, y_warn), (min(x_cur + dash_len, chart_x1), y_warn)],
                  fill=AMBER + (140,), width=int(2 * SS))
        x_cur += dash_len + gap_len
    # Critical line (pink, dashed, slightly bolder)
    x_cur = chart_x0
    while x_cur < chart_x1:
        draw.line([(x_cur, y_crit), (min(x_cur + dash_len, chart_x1), y_crit)],
                  fill=PINK + (180,), width=int(2 * SS))
        x_cur += dash_len + gap_len

    # Build the risk curve points
    curve = generate_jelly_curve(chart_w, chart_h)
    curve_abs = [(chart_x0 + x, chart_y0 + y) for x, y in curve]

    # Filled area under curve (gradient effect via overlay)
    fill_polygon = [(chart_x0, chart_y1)] + curve_abs + [(chart_x1, chart_y1)]
    # Create a separate fill layer to control alpha
    fill_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fill_draw = ImageDraw.Draw(fill_layer)
    fill_draw.polygon(fill_polygon, fill=PINK + (80,))
    # Blur the fill slightly for a glow effect
    fill_layer = fill_layer.filter(ImageFilter.GaussianBlur(SS * 1.5))
    img.paste(fill_layer, (0, 0), fill_layer)

    # Redraw the area with a sharper gradient fill on top
    fill_layer2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fill_draw2 = ImageDraw.Draw(fill_layer2)
    fill_draw2.polygon(fill_polygon, fill=PINK + (50,))
    img.paste(fill_layer2, (0, 0), fill_layer2)

    # Curve line itself — sharp, pink
    draw.line(curve_abs, fill=PINK, width=int(5 * SS), joint="curve")

    # Highlight peak point
    peak_idx = max(range(len(curve_abs)), key=lambda i: -curve_abs[i][1])
    peak_x, peak_y = curve_abs[peak_idx]
    # Outer glow
    for radius in range(int(20 * SS), int(6 * SS), -2):
        alpha = int(60 * (1 - (radius - 6 * SS) / (14 * SS)))
        draw.ellipse([peak_x - radius, peak_y - radius,
                      peak_x + radius, peak_y + radius],
                     fill=PINK + (alpha,))
    # Solid dot
    dot_r = int(8 * SS)
    draw.ellipse([peak_x - dot_r, peak_y - dot_r, peak_x + dot_r, peak_y + dot_r],
                 fill=PINK)
    # Inner dot (contrast)
    inner_r = int(3 * SS)
    draw.ellipse([peak_x - inner_r, peak_y - inner_r, peak_x + inner_r, peak_y + inner_r],
                 fill=TEXT)

    # Label: "87.4" near peak
    label_font = load_font("black", 22)
    label_text = "87.4"
    label_bbox = draw.textbbox((0, 0), label_text, font=label_font)
    label_w = label_bbox[2] - label_bbox[0]
    label_h = label_bbox[3] - label_bbox[1]
    label_x = peak_x - label_w - int(16 * SS)
    label_y = peak_y - label_h // 2 - int(4 * SS)
    # Background pill
    pill_pad_x = int(10 * SS)
    pill_pad_y = int(6 * SS)
    pill_r = int(8 * SS)
    draw.rounded_rectangle(
        [label_x - pill_pad_x, label_y - pill_pad_y,
         label_x + label_w + pill_pad_x, label_y + label_h + pill_pad_y],
        radius=pill_r, fill=PINK + (230,))
    draw.text((label_x, label_y - int(2 * SS)), label_text, font=label_font, fill=TEXT)

    # Small "PEAK RISK" subtitle under the label
    sub_font = load_font("bold", 9)
    sub_text = "PEAK RISK"
    sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text((label_x - pill_pad_x + (label_w + 2 * pill_pad_x - sub_w) // 2,
               label_y + label_h + pill_pad_y + int(6 * SS)),
              sub_text, font=sub_font, fill=TEXT_MUTED)

    # Axis labels: y-axis threshold markers (tiny)
    tiny_font = load_font("bold", 9)
    draw.text((chart_x1 + int(8 * SS), y_crit - int(6 * SS)),
              "CRIT 60", font=tiny_font, fill=PINK + (200,))
    draw.text((chart_x1 + int(8 * SS), y_warn - int(6 * SS)),
              "WARN 40", font=tiny_font, fill=AMBER + (200,))

    # X-axis labels: start / peak / end
    x_label_y = chart_y1 + int(12 * SS)
    draw.text((chart_x0, x_label_y), "13:00", font=tiny_font, fill=TEXT_MUTED)
    draw.text((peak_x - int(16 * SS), x_label_y), "14:25", font=tiny_font, fill=TEXT_MUTED)
    draw.text((chart_x1 - int(40 * SS), x_label_y), "17:30 ✕", font=tiny_font, fill=TEXT_MUTED)

    # Chart title tag above the chart (small, uppercase)
    title_font = load_font("bold", 11)
    draw.text((chart_x0, chart_y0 - int(28 * SS)),
              "WE BUILT THIS AFTER JELLY · $12M HLP LOSS · MARCH 2025",
              font=title_font, fill=TEXT_MUTED)


def draw_radar_dot(img: Image.Image, cx: int, cy: int, radius: int):
    """Small radar-dot logo glyph (matching the site favicon)."""
    draw = ImageDraw.Draw(img, "RGBA")
    # Outer disc
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=PINK)
    # Inner dark pupil
    inner_r = int(radius * 0.38)
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=BG)
    # Outer glow
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_r = int(radius * 1.6)
    glow_draw.ellipse([cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r],
                      fill=PINK + (50,))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius * 0.5))
    img.paste(glow_layer, (0, 0), glow_layer)
    # Redraw dot on top so glow doesn't cover it
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=PINK)
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=BG)


def draw_text_zone(img: Image.Image):
    """Big wordmark + tagline + URL on the left side."""
    draw = ImageDraw.Draw(img, "RGBA")

    # Layout zone for text (avoiding profile-pic safe area bottom-left)
    x0 = int(W * 0.04)
    headline_y = int(H * 0.22)

    # Small eyebrow badge
    badge_font = load_font("bold", 13)
    badge_text = "● INDEPENDENT · NEUTRAL · PUBLIC"
    badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    bw = badge_bbox[2] - badge_bbox[0]
    bh = badge_bbox[3] - badge_bbox[1]
    pad_x = int(14 * SS)
    pad_y = int(7 * SS)
    draw.rounded_rectangle(
        [x0, headline_y - bh - 2 * pad_y,
         x0 + bw + 2 * pad_x, headline_y - int(8 * SS)],
        radius=int(10 * SS), fill=(255, 59, 107, 30),
        outline=PINK + (120,), width=int(1 * SS))
    draw.text((x0 + pad_x, headline_y - bh - pad_y - int(4 * SS)),
              badge_text, font=badge_font, fill=PINK)

    # Radar dot + wordmark row
    dot_radius = int(24 * SS)
    dot_x = x0 + dot_radius
    dot_y = headline_y + dot_radius + int(6 * SS)
    draw_radar_dot(img, dot_x, dot_y, dot_radius)

    # Wordmark "HIP3Radar"
    wordmark_font = load_font("black", 54)
    wordmark_text = "HIP3Radar"
    wm_x = dot_x + dot_radius + int(20 * SS)
    wm_bbox = draw.textbbox((0, 0), wordmark_text, font=wordmark_font)
    wm_h = wm_bbox[3] - wm_bbox[1]
    wm_y = dot_y - wm_h // 2 - int(6 * SS)
    draw.text((wm_x, wm_y), wordmark_text, font=wordmark_font, fill=TEXT)

    # Headline below: two lines
    headline_font = load_font("black", 40)
    line1 = "Every Hyperliquid perp,"
    line2 = "graded."
    headline_start_y = dot_y + dot_radius + int(28 * SS)
    draw.text((x0, headline_start_y), line1, font=headline_font, fill=TEXT)
    line1_bbox = draw.textbbox((0, 0), line1, font=headline_font)
    line1_h = line1_bbox[3] - line1_bbox[1]
    line2_y = headline_start_y + line1_h + int(8 * SS)
    # "Hyperliquid." with gradient-ish tint (pink accent for emphasis)
    draw.text((x0, line2_y), line2, font=headline_font, fill=PINK)

    # Tagline below headline
    tagline_font = load_font("bold", 18)
    tagline_y = line2_y + line1_h + int(24 * SS)
    tagline = "324 markets · 9 perp dexes · scored every 60 seconds"
    draw.text((x0, tagline_y), tagline, font=tagline_font, fill=TEXT_MUTED)

    # URL (mono, bottom-right of text zone, avoiding profile-pic safe area)
    url_font = load_font("mono", 16)
    url_text = "hip3radar.xyz"
    url_y = int(H * 0.86)
    url_x = int(W * 0.28)  # Away from bottom-left profile zone
    # Pink accent bar to the left of the URL
    bar_w = int(4 * SS)
    bar_h = int(18 * SS)
    draw.rectangle([url_x - int(14 * SS), url_y + int(4 * SS),
                    url_x - int(14 * SS) + bar_w, url_y + int(4 * SS) + bar_h],
                   fill=PINK)
    draw.text((url_x, url_y), url_text, font=url_font, fill=TEXT)


def draw_top_accent(img: Image.Image):
    """Thin pink bar at the very top of the banner."""
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, int(4 * SS)], fill=PINK)


def main():
    img = draw_background()

    # Layer 1: risk curve on right
    draw_risk_curve(img)

    # Layer 2: text + logo on left
    draw_text_zone(img)

    # Layer 3: top accent bar
    draw_top_accent(img)

    # Downsample to target resolution with LANCZOS for crisp edges
    img = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
    out_path = OUT_DIR / "hip3radar-banner-twitter.png"
    img.save(out_path, "PNG", optimize=True)
    print(f"Saved: {out_path.name} ({out_path.stat().st_size // 1024} KB)")

    # Also save a JPG for smaller file size (Twitter accepts both)
    jpg_path = OUT_DIR / "hip3radar-banner-twitter.jpg"
    img.convert("RGB").save(jpg_path, "JPEG", quality=92, optimize=True)
    print(f"Saved: {jpg_path.name} ({jpg_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
