#!/usr/bin/env python3
"""Generate HIP3Radar logo PNGs matching the website design system."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

# Brand tokens (matching hip3radar.xyz CSS)
BG = (10, 14, 26)        # --bg: #0a0e1a
PINK = (255, 59, 107)    # --accent: #ff3b6b
DEEP = (176, 21, 74)     # inner gradient stop (darker pink)

# Render at 2x target size, downsample for anti-aliasing
TARGET = 1000
SS = 2  # supersample factor
SIZE = TARGET * SS

OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(parents=True, exist_ok=True)


def render_logo(with_background: bool = True, size: int = SIZE) -> Image.Image:
    """Render the HIP3Radar radar-dot logo.

    with_background=True  -> solid dark square bg (for Twitter profile pic)
    with_background=False -> transparent background (for overlay use)
    """
    if with_background:
        arr = np.full((size, size, 3), BG, dtype=np.uint8)
    else:
        arr = np.zeros((size, size, 4), dtype=np.uint8)

    # Dot geometry
    cx = cy = size / 2
    r_outer = size * 0.42  # outer radius of pink disc
    r_inner = size * 0.16  # inner dark hole (radar pupil)

    # Gradient highlight center (top-left offset for 3D feel)
    hx = size * 0.43
    hy = size * 0.43

    y, x = np.ogrid[:size, :size]
    d_center = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    d_highlight = np.sqrt((x - hx) ** 2 + (y - hy) ** 2)

    # Normalized distance from highlight center (0 center -> 1 edge)
    t = np.clip(d_highlight / r_outer, 0, 1)
    # Power curve for smoother falloff toward the edge
    t_smooth = t ** 1.4

    # Interpolate color: PINK -> DEEP
    r_ch = (PINK[0] * (1 - t_smooth) + DEEP[0] * t_smooth).astype(np.uint8)
    g_ch = (PINK[1] * (1 - t_smooth) + DEEP[1] * t_smooth).astype(np.uint8)
    b_ch = (PINK[2] * (1 - t_smooth) + DEEP[2] * t_smooth).astype(np.uint8)

    # Soft edge: blend disc into background over a 3-pixel ring at target res (6 at SS)
    edge_soft = 6
    alpha_outer = np.clip((r_outer - d_center) / edge_soft, 0, 1)
    alpha_inner_cut = np.clip((d_center - r_inner) / edge_soft, 0, 1)
    alpha_disc = alpha_outer * alpha_inner_cut  # 1 where full pink, 0 where hole or outside

    if with_background:
        bg_r = np.full((size, size), BG[0], dtype=np.float32)
        bg_g = np.full((size, size), BG[1], dtype=np.float32)
        bg_b = np.full((size, size), BG[2], dtype=np.float32)
        arr[:, :, 0] = (r_ch * alpha_disc + bg_r * (1 - alpha_disc)).astype(np.uint8)
        arr[:, :, 1] = (g_ch * alpha_disc + bg_g * (1 - alpha_disc)).astype(np.uint8)
        arr[:, :, 2] = (b_ch * alpha_disc + bg_b * (1 - alpha_disc)).astype(np.uint8)
        img = Image.fromarray(arr, mode="RGB")
    else:
        arr[:, :, 0] = r_ch
        arr[:, :, 1] = g_ch
        arr[:, :, 2] = b_ch
        arr[:, :, 3] = (alpha_disc * 255).astype(np.uint8)
        img = Image.fromarray(arr, mode="RGBA")

    # Add a subtle outer glow (only meaningful when background is present)
    if with_background:
        glow_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        glow_arr = np.zeros((size, size, 4), dtype=np.uint8)
        # Glow = pink where just outside the disc, fading outward
        glow_falloff = np.clip((d_center - r_outer) / (r_outer * 0.4), 0, 1)
        glow_alpha = (1 - glow_falloff) ** 2
        glow_mask = (d_center > r_outer * 0.95) & (d_center < r_outer * 1.45)
        glow_arr[glow_mask, 0] = PINK[0]
        glow_arr[glow_mask, 1] = PINK[1]
        glow_arr[glow_mask, 2] = PINK[2]
        glow_arr[glow_mask, 3] = (glow_alpha[glow_mask] * 100).astype(np.uint8)
        glow_layer = Image.fromarray(glow_arr, mode="RGBA")
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(size * 0.02))

        base = img.convert("RGBA")
        composed = Image.alpha_composite(base, glow_layer)
        # Recomposite disc on top so glow doesn't bleed into the pink body
        disc_only = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        disc_arr = np.zeros((size, size, 4), dtype=np.uint8)
        disc_arr[:, :, 0] = r_ch
        disc_arr[:, :, 1] = g_ch
        disc_arr[:, :, 2] = b_ch
        disc_arr[:, :, 3] = (alpha_disc * 255).astype(np.uint8)
        disc_only = Image.fromarray(disc_arr, mode="RGBA")
        composed = Image.alpha_composite(composed, disc_only)
        img = composed.convert("RGB")

    return img


def main():
    # Twitter profile pic (square, dark background, 1000x1000)
    full = render_logo(with_background=True, size=SIZE)
    full.thumbnail((TARGET, TARGET), Image.Resampling.LANCZOS)
    full.save(OUT_DIR / "hip3radar-logo-1000.png", "PNG", optimize=True)

    # Smaller variants for different use cases
    for sz in (800, 512, 400, 200):
        img = render_logo(with_background=True, size=sz * SS)
        img.thumbnail((sz, sz), Image.Resampling.LANCZOS)
        img.save(OUT_DIR / f"hip3radar-logo-{sz}.png", "PNG", optimize=True)

    # Transparent version (for overlay use)
    trans = render_logo(with_background=False, size=SIZE)
    trans.thumbnail((TARGET, TARGET), Image.Resampling.LANCZOS)
    trans.save(OUT_DIR / "hip3radar-logo-transparent-1000.png", "PNG", optimize=True)

    print("Generated:")
    for f in sorted(OUT_DIR.glob("hip3radar-logo*.png")):
        print(f"  {f.name:40s} {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
