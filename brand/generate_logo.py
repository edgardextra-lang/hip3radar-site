#!/usr/bin/env python3
"""Generate HIP3Radar logo PNGs matching the new Bloomberg-terminal green design system."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

# Brand tokens — RADAR (green) design system
BG = (10, 12, 11)         # #0a0c0b (terminal near-black)
GREEN = (126, 243, 160)   # oklch(0.82 0.18 145) ≈ #7ef3a0 (radar accent)
GREEN_DEEP = (62, 195, 110)  # darker green for gradient
INK_DARK = (11, 21, 16)   # #0b1510 (accent-ink, the "pupil" color)

TARGET = 1000
SS = 2
SIZE = TARGET * SS

OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(parents=True, exist_ok=True)


def render_logo(with_background: bool = True, size: int = SIZE) -> Image.Image:
    """Radar dot: green disc with darker pupil, soft green glow."""
    if with_background:
        arr = np.full((size, size, 3), BG, dtype=np.uint8)
    else:
        arr = np.zeros((size, size, 4), dtype=np.uint8)

    cx = cy = size / 2
    r_outer = size * 0.42
    r_inner = size * 0.16

    # Highlight center for radial gradient (top-left offset)
    hx = size * 0.43
    hy = size * 0.43

    y, x = np.ogrid[:size, :size]
    d_center = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    d_highlight = np.sqrt((x - hx) ** 2 + (y - hy) ** 2)

    t = np.clip(d_highlight / r_outer, 0, 1)
    t_smooth = t ** 1.4

    r_ch = (GREEN[0] * (1 - t_smooth) + GREEN_DEEP[0] * t_smooth).astype(np.uint8)
    g_ch = (GREEN[1] * (1 - t_smooth) + GREEN_DEEP[1] * t_smooth).astype(np.uint8)
    b_ch = (GREEN[2] * (1 - t_smooth) + GREEN_DEEP[2] * t_smooth).astype(np.uint8)

    edge_soft = 6
    alpha_outer = np.clip((r_outer - d_center) / edge_soft, 0, 1)
    alpha_inner_cut = np.clip((d_center - r_inner) / edge_soft, 0, 1)
    alpha_disc = alpha_outer * alpha_inner_cut

    if with_background:
        bg_r = np.full((size, size), BG[0], dtype=np.float32)
        bg_g = np.full((size, size), BG[1], dtype=np.float32)
        bg_b = np.full((size, size), BG[2], dtype=np.float32)
        arr[:, :, 0] = (r_ch * alpha_disc + bg_r * (1 - alpha_disc)).astype(np.uint8)
        arr[:, :, 1] = (g_ch * alpha_disc + bg_g * (1 - alpha_disc)).astype(np.uint8)
        arr[:, :, 2] = (b_ch * alpha_disc + bg_b * (1 - alpha_disc)).astype(np.uint8)
        # Paint inner pupil with INK_DARK
        inner_mask = d_center <= r_inner
        arr[inner_mask, 0] = INK_DARK[0]
        arr[inner_mask, 1] = INK_DARK[1]
        arr[inner_mask, 2] = INK_DARK[2]
        img = Image.fromarray(arr, mode="RGB")
    else:
        arr[:, :, 0] = r_ch
        arr[:, :, 1] = g_ch
        arr[:, :, 2] = b_ch
        arr[:, :, 3] = (alpha_disc * 255).astype(np.uint8)
        img = Image.fromarray(arr, mode="RGBA")

    if with_background:
        # Add soft outer glow in green
        glow_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        glow_arr = np.zeros((size, size, 4), dtype=np.uint8)
        glow_falloff = np.clip((d_center - r_outer) / (r_outer * 0.4), 0, 1)
        glow_alpha = (1 - glow_falloff) ** 2
        glow_mask = (d_center > r_outer * 0.95) & (d_center < r_outer * 1.45)
        glow_arr[glow_mask, 0] = GREEN[0]
        glow_arr[glow_mask, 1] = GREEN[1]
        glow_arr[glow_mask, 2] = GREEN[2]
        glow_arr[glow_mask, 3] = (glow_alpha[glow_mask] * 90).astype(np.uint8)
        glow_layer = Image.fromarray(glow_arr, mode="RGBA")
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(size * 0.02))

        base = img.convert("RGBA")
        composed = Image.alpha_composite(base, glow_layer)
        # Recomposite disc on top
        disc_arr = np.zeros((size, size, 4), dtype=np.uint8)
        disc_arr[:, :, 0] = r_ch
        disc_arr[:, :, 1] = g_ch
        disc_arr[:, :, 2] = b_ch
        disc_arr[:, :, 3] = (alpha_disc * 255).astype(np.uint8)
        # Add inner pupil to the disc layer
        disc_arr[d_center <= r_inner, 0] = INK_DARK[0]
        disc_arr[d_center <= r_inner, 1] = INK_DARK[1]
        disc_arr[d_center <= r_inner, 2] = INK_DARK[2]
        disc_arr[d_center <= r_inner, 3] = 255
        disc_only = Image.fromarray(disc_arr, mode="RGBA")
        composed = Image.alpha_composite(composed, disc_only)
        img = composed.convert("RGB")

    return img


def main():
    full = render_logo(with_background=True, size=SIZE)
    full.thumbnail((TARGET, TARGET), Image.Resampling.LANCZOS)
    full.save(OUT_DIR / "hip3radar-logo-1000.png", "PNG", optimize=True)

    for sz in (800, 512, 400, 200):
        img = render_logo(with_background=True, size=sz * SS)
        img.thumbnail((sz, sz), Image.Resampling.LANCZOS)
        img.save(OUT_DIR / f"hip3radar-logo-{sz}.png", "PNG", optimize=True)

    trans = render_logo(with_background=False, size=SIZE)
    trans.thumbnail((TARGET, TARGET), Image.Resampling.LANCZOS)
    trans.save(OUT_DIR / "hip3radar-logo-transparent-1000.png", "PNG", optimize=True)

    print("Generated:")
    for f in sorted(OUT_DIR.glob("hip3radar-logo*.png")):
        print(f"  {f.name:40s} {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
