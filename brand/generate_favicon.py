#!/usr/bin/env python3
"""Generate animated GIF favicon — radar dot with sweeping arc."""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT_DIR = Path(__file__).parent
SIZE = 128       # render at 128, will downsample for favicon
TARGET = 64      # favicon target
FRAMES = 32      # one full sweep
DURATION_MS = 80 # per frame

# Brand tokens
BG = (10, 12, 11)
GREEN = (126, 243, 160)
GREEN_DEEP = (62, 195, 110)
INK_DARK = (11, 21, 16)


def render_frame(angle_deg: float, size: int = SIZE) -> Image.Image:
    """One frame: green dot + radial sweep arc rotated to `angle_deg`."""
    img = Image.new("RGB", (size, size), BG)
    draw = ImageDraw.Draw(img, "RGBA")

    cx = cy = size / 2
    r_outer = size * 0.42
    r_inner = size * 0.16

    # Outer disc (green)
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=GREEN)

    # Inner pupil (dark)
    draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=INK_DARK)

    # Sweep arc — a wedge (pieslice) clipped to the outer disc
    sweep_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sweep_draw = ImageDraw.Draw(sweep_layer)
    # Wedge from angle_deg to angle_deg + 60° (the "sweep beam")
    bbox = [cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer]
    start = angle_deg
    end = angle_deg + 60
    # Light green wedge with gradient via multiple overlapping wedges of decreasing alpha
    for i in range(5):
        alpha = int(120 * (1 - i / 5))
        sweep_draw.pieslice(bbox, start + i * 2, end - i * 2,
                            fill=(255, 255, 255, alpha))
    # Mask: only keep inside the outer disc
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=255)
    sweep_layer.putalpha(Image.eval(mask, lambda x: x))
    img_rgba = img.convert("RGBA")
    composed = Image.alpha_composite(img_rgba, sweep_layer)

    # Re-draw inner pupil on top so the sweep doesn't cover it
    pupil_draw = ImageDraw.Draw(composed)
    pupil_draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=INK_DARK)

    return composed.convert("RGB")


def main():
    frames = []
    for i in range(FRAMES):
        angle = (i / FRAMES) * 360 - 90  # start pointing up
        f = render_frame(angle, SIZE)
        f = f.resize((TARGET, TARGET), Image.Resampling.LANCZOS)
        frames.append(f)

    # Save as animated GIF (favicon-sized 64x64)
    out = OUT_DIR / "hip3radar-favicon.gif"
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"Saved: {out.name} ({out.stat().st_size // 1024} KB, {len(frames)} frames @ {DURATION_MS}ms)")

    # Also save a 32x32 version for tighter inline embed
    frames32 = [f.resize((32, 32), Image.Resampling.LANCZOS) for f in frames]
    out32 = OUT_DIR / "hip3radar-favicon-32.gif"
    frames32[0].save(
        out32, save_all=True, append_images=frames32[1:],
        duration=DURATION_MS, loop=0, optimize=True, disposal=2,
    )
    print(f"Saved: {out32.name} ({out32.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
