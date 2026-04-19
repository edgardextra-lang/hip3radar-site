#!/usr/bin/env python3
"""
HIP3Radar OG image — 1200x630, Bloomberg-terminal aesthetic.
Used for iMessage / Telegram / Slack / Discord / Twitter link previews.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BG, SURFACE, LINE, INK, INK_2, INK_3 = (10,12,11), (17,20,15), (31,38,32), (232,236,228), (168,176,164), (106,115,104)
ACCENT, WARN, DANGER = (126,243,160), (255,182,72), (255,107,107)

T_W, T_H = 1200, 630
SS = 2
W, H = T_W * SS, T_H * SS
OUT = Path(__file__).parent

def font(weight, px):
    px = int(px * SS)
    paths = {
        "mono":  ["/System/Library/Fonts/SFNSMono.ttf", "/System/Library/Fonts/Menlo.ttc"],
        "bold":  ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"],
        "serif": ["/System/Library/Fonts/Supplemental/Georgia Italic.ttf", "/System/Library/Fonts/Times.ttc"],
    }
    for p in paths[weight]:
        try: return ImageFont.truetype(p, px)
        except Exception: pass
    return ImageFont.load_default()

def background():
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    arr[:,:,0]=BG[0]; arr[:,:,1]=BG[1]; arr[:,:,2]=BG[2]
    y, x = np.ogrid[:H, :W]
    glow = np.exp(-((x - W*0.5)**2 + (y - H*0.85)**2) / (2*(W*0.45)**2))
    for i,c in enumerate(ACCENT):
        arr[:,:,i] = np.clip(arr[:,:,i] + c * glow * 0.10, 0, 255)
    return Image.fromarray(arr)

def add_grid(img):
    d = ImageDraw.Draw(img, "RGBA")
    step = 48 * SS
    for x in range(0, W, step): d.line([(x,0),(x,H)], fill=(255,255,255,5))
    for y in range(0, H, step): d.line([(0,y),(W,y)], fill=(255,255,255,5))
    return img

def radar_mark(img, cx, cy, r):
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=ACCENT, width=int(3*SS))
    d.ellipse([cx-int(r*0.66), cy-int(r*0.66), cx+int(r*0.66), cy+int(r*0.66)],
              outline=(126,243,160,110), width=int(1.5*SS))
    wedge = Image.new("RGBA", (r*2+20, r*2+20), (0,0,0,0))
    wd = ImageDraw.Draw(wedge)
    wd.pieslice([10,10,r*2+10,r*2+10], -115, -55, fill=(126,243,160,110))
    img.paste(wedge, (cx-r-10, cy-r-10), wedge)
    cr = int(r*0.12)
    d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=ACCENT)

def grade_pill(img, x, y, grade, rating, color):
    d = ImageDraw.Draw(img, "RGBA")
    w, h = 140*SS, 50*SS
    d.rounded_rectangle([x, y, x+w, y+h], radius=int(8*SS),
                        fill=(*color, 38), outline=(*color, 170), width=int(1.5*SS))
    d.text((x + 20*SS, y + 11*SS), grade, fill=color, font=font("bold", 20))
    d.text((x + 70*SS, y + 17*SS), f"· {rating}", fill=color, font=font("mono", 15))

def main():
    img = background()
    img = add_grid(img)
    d = ImageDraw.Draw(img, "RGBA")

    d.rectangle([0, 0, W, 70*SS], fill=(17,20,15,220))
    d.line([(0, 70*SS), (W, 70*SS)], fill=LINE, width=1)
    d.text((48*SS, 28*SS), "● LIVE   ·   325 MARKETS   ·   9 DEPLOYERS   ·   60-SECOND REFRESH",
           fill=ACCENT, font=font("mono", 13))
    d.text((W - 200*SS, 28*SS), "hip3radar.xyz", fill=INK_2, font=font("mono", 13))

    radar_mark(img, 110*SS, 165*SS, 50*SS)
    d.text((180*SS, 137*SS), "HIP3Radar", fill=INK, font=font("bold", 48))
    d.text((180*SS, 200*SS), "// independent risk surveillance for HIP-3",
           fill=INK_3, font=font("mono", 16))

    d.text((48*SS, 270*SS), "Know the risk.", fill=INK, font=font("bold", 86))
    d.text((48*SS, 360*SS), "Before you route the order.", fill=INK_2, font=font("serif", 64))

    gy = 480*SS
    d.text((48*SS, gy - 30*SS), "// SAFETY GRADES · from a 5-signal composite",
           fill=INK_3, font=font("mono", 12))
    pills = [("AA", 94, ACCENT), ("A", 87, ACCENT), ("B+", 74, WARN),
             ("C", 58, WARN), ("D", 38, DANGER), ("F", 18, DANGER)]
    px = 48*SS
    for g, r, c in pills:
        grade_pill(img, px, gy, g, r, c)
        px += 170*SS

    d.text((48*SS, 580*SS),
           "oracle drift  ·  mark-oracle spread  ·  OI velocity  ·  OI/volume  ·  funding extremity",
           fill=INK_3, font=font("mono", 12))

    img = img.resize((T_W, T_H), Image.LANCZOS)
    png = OUT / "hip3radar-og.png"
    jpg = OUT / "hip3radar-og.jpg"
    img.save(png, "PNG", optimize=True)
    img.convert("RGB").save(jpg, "JPEG", quality=92, optimize=True)
    print(f"→ {png} ({png.stat().st_size // 1024}KB)")
    print(f"→ {jpg} ({jpg.stat().st_size // 1024}KB)")

if __name__ == "__main__":
    main()
