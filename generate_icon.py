#!/usr/bin/env python3
"""Generate a Blue Sound Wave Circle icon for 报时宝 (BaoShiBao)."""

from PIL import Image, ImageDraw, ImageFont
import math


def gradient_circle(img, cx, cy, r, color1, color2):
    """Draw a gradient-filled circle."""
    draw = ImageDraw.Draw(img)
    for i in range(r, 0, -1):
        t = (r - i) / r
        c = tuple(int(color1[j] + (color2[j] - color1[j]) * t) for j in range(3))
        draw.ellipse([cx - i, cy - i, cx + i, cy + i], fill=c)


def create_icon(size=1024):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size / 2, size / 2

    # Soft circular background
    pad = size * 0.02
    draw.ellipse(
        [pad, pad, size - pad, size - pad],
        fill=(240, 246, 255, 255),  # very light blue bg
        outline=(208, 228, 245, 255),
        width=int(size * 0.012),
    )

    # Main blue circle
    main_r = int(size * 0.36)
    blue1 = (91, 155, 213)   # #5B9BD5
    blue2 = (74, 138, 196)   # #4A8AC4
    gradient_circle(img, int(cx), int(cy), main_r, blue1, blue2)
    draw = ImageDraw.Draw(img)

    # Subtle inner ring
    inner_r = main_r - int(size * 0.015)
    draw.ellipse(
        [cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
        outline=(255, 255, 255, 50), width=int(size * 0.008),
    )

    # Clock face markers (12 positions)
    for i in range(12):
        angle = math.radians(-90 + i * 30)
        inner = main_r * 0.75
        outer = main_r * 0.88
        x1 = cx + math.cos(angle) * inner
        y1 = cy + math.sin(angle) * inner
        x2 = cx + math.cos(angle) * outer
        y2 = cy + math.sin(angle) * outer
        w = int(size * 0.014) if i % 3 == 0 else int(size * 0.008)
        draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 200), width=w)

    # Hour hand (10 o'clock)
    hour_angle = math.radians(-90 + 300)
    hx = cx + math.cos(hour_angle) * main_r * 0.45
    hy = cy + math.sin(hour_angle) * main_r * 0.45
    draw.line([(cx, cy), (hx, hy)], fill=(255, 255, 255, 240), width=int(size * 0.024))

    # Minute hand (2 o'clock)
    min_angle = math.radians(-90 + 60)
    mx = cx + math.cos(min_angle) * main_r * 0.65
    my = cy + math.sin(min_angle) * main_r * 0.65
    draw.line([(cx, cy), (mx, my)], fill=(255, 255, 255, 220), width=int(size * 0.018))

    # Center dot
    dot_r = size * 0.02
    draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r],
                 fill=(255, 255, 255, 250))

    # Sound wave arcs (right side)
    wave_cx = cx + main_r + size * 0.06
    wave_cy = cy
    wave_colors = [
        (91, 155, 213, 180),   # strong
        (91, 155, 213, 130),   # medium
        (91, 155, 213, 80),    # light
    ]
    for i, wr in enumerate([size * 0.06, size * 0.10, size * 0.14]):
        bbox = [wave_cx - wr, wave_cy - wr, wave_cx + wr, wave_cy + wr]
        draw.arc(bbox, start=-40, end=40, fill=wave_colors[i],
                 width=int(size * 0.018))

    # Sound wave arcs (left side, smaller, subtle)
    wave_lx = cx - main_r - size * 0.06
    for i, wr in enumerate([size * 0.05, size * 0.08, size * 0.11]):
        bbox = [wave_lx - wr, wave_cy - wr, wave_lx + wr, wave_cy + wr]
        draw.arc(bbox, start=140, end=220, fill=wave_colors[i],
                 width=int(size * 0.014))

    return img


if __name__ == "__main__":
    icon = create_icon(1024)
    icon.save("/Users/boqian/Desktop/clock/icon_1024.png")
    print("Saved icon_1024.png")

    for s in [512, 256, 128, 64, 32, 16]:
        resized = icon.resize((s, s), Image.LANCZOS)
        resized.save(f"/Users/boqian/Desktop/clock/icon_{s}.png")
        print(f"Saved icon_{s}.png")
