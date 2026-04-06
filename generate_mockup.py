#!/usr/bin/env python3
"""Generate a 小宇宙-style mockup image for the Chinese Clock Alarm app."""

from PIL import Image, ImageDraw, ImageFont
import math

W, H = 420, 780
R = 24  # corner radius


def rounded_rect(draw, box, fill, radius=16, outline=None, outline_width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=outline_width)


def gradient_circle(img, cx, cy, r, color1, color2):
    """Draw a gradient-filled circle."""
    draw = ImageDraw.Draw(img)
    for i in range(r, 0, -1):
        t = (r - i) / r
        c = tuple(int(color1[j] + (color2[j] - color1[j]) * t) for j in range(3))
        draw.ellipse([cx - i, cy - i, cx + i, cy + i], fill=c)


def main():
    img = Image.new("RGB", (W, H), (245, 245, 245))
    draw = ImageDraw.Draw(img)

    # Phone body
    rounded_rect(draw, [0, 0, W, H], fill=(255, 255, 255), radius=32)

    # Try loading font
    try:
        font_b = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        font_m = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
        font_s = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
        font_xs = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 11)
        font_clock = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 38)
        font_clock_s = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except:
        font_b = font_m = font_s = font_xs = font_clock = font_clock_s = font_title = ImageFont.load_default()

    purple1 = (102, 126, 234)
    purple2 = (118, 75, 162)
    gray1 = (26, 26, 26)
    gray2 = (102, 102, 102)
    gray3 = (153, 153, 153)
    gray4 = (240, 240, 245)
    bg_card = (250, 250, 255)

    y = 24

    # ── Header ──
    draw.text((24, y), "Chinese Clock", fill=gray1, font=font_title)
    y += 28
    draw.text((24, y), "Voice Alarm", fill=gray3, font=font_s)
    y += 28

    # ── Clock Circle ──
    cx, cy = W // 2, y + 95
    cr = 90

    # Outer ring
    draw.ellipse([cx - cr - 5, cy - cr - 5, cx + cr + 5, cy + cr + 5],
                 outline=(102, 126, 234, 40), width=2)

    # Gradient circle
    gradient_circle(img, cx, cy, cr, purple1, purple2)
    draw = ImageDraw.Draw(img)  # refresh draw after gradient

    # Clock text
    tw = draw.textlength("15:30:45", font=font_clock)
    draw.text((cx - tw / 2, cy - 22), "15:30:45", fill=(255, 255, 255), font=font_clock)
    tw2 = draw.textlength("2026-04-06  Monday", font=font_clock_s)
    draw.text((cx - tw2 / 2, cy + 22), "2026-04-06  Monday",
              fill=(255, 255, 255, 180), font=font_clock_s)

    y = cy + cr + 20

    # ── Settings Card ──
    card_x, card_w = 16, W - 32
    card_y = y
    card_h = 136
    rounded_rect(draw, [card_x, card_y, card_x + card_w, card_y + card_h],
                 fill=(255, 255, 255), radius=16,
                 outline=(240, 240, 240), outline_width=1)

    # Row: Alarm Time
    ry = card_y + 14
    draw.text((card_x + 18, ry), "Alarm Time", fill=gray2, font=font_m)
    # Pills
    pill_y = ry - 2
    rounded_rect(draw, [card_x + card_w - 120, pill_y, card_x + card_w - 76, pill_y + 28],
                 fill=gray4, radius=14)
    draw.text((card_x + card_w - 110, pill_y + 5), "08", fill=purple1, font=font_m)
    draw.text((card_x + card_w - 72, pill_y + 3), ":", fill=gray3, font=font_m)
    rounded_rect(draw, [card_x + card_w - 64, pill_y, card_x + card_w - 20, pill_y + 28],
                 fill=gray4, radius=14)
    draw.text((card_x + card_w - 54, pill_y + 5), "00", fill=purple1, font=font_m)

    # Divider
    ry += 40
    draw.line([(card_x + 18, ry), (card_x + card_w - 18, ry)], fill=(248, 248, 248), width=1)

    # Row: Gap Between
    ry += 10
    draw.text((card_x + 18, ry), "Gap Between", fill=gray2, font=font_m)
    rounded_rect(draw, [card_x + card_w - 90, ry - 2, card_x + card_w - 50, ry + 26],
                 fill=gray4, radius=14)
    draw.text((card_x + card_w - 80, ry + 3), "1", fill=purple1, font=font_m)
    draw.text((card_x + card_w - 44, ry + 4), "sec", fill=gray3, font=font_s)

    # Divider
    ry += 40
    draw.line([(card_x + 18, ry), (card_x + card_w - 18, ry)], fill=(248, 248, 248), width=1)

    # Row: Voice Speed (slider)
    ry += 10
    draw.text((card_x + 18, ry), "Voice Speed", fill=gray2, font=font_m)
    # Slider track
    sl_x = card_x + card_w - 160
    sl_y = ry + 8
    draw.rounded_rectangle([sl_x, sl_y, sl_x + 140, sl_y + 4], radius=2, fill=(238, 238, 242))
    draw.rounded_rectangle([sl_x, sl_y, sl_x + 84, sl_y + 4], radius=2, fill=purple1)
    # Thumb
    draw.ellipse([sl_x + 78, sl_y - 5, sl_x + 92, sl_y + 9], fill=(255, 255, 255),
                 outline=purple1, width=2)

    y = card_y + card_h + 10

    # ── Voice Card ──
    vc_y = y
    vc_h = 60
    rounded_rect(draw, [card_x, vc_y, card_x + card_w, vc_y + vc_h],
                 fill=bg_card, radius=16, outline=(237, 237, 245), outline_width=1)

    # Voice avatar
    av_x, av_y = card_x + 18, vc_y + 12
    gradient_circle(img, av_x + 18, av_y + 18, 18, purple1, purple2)
    draw = ImageDraw.Draw(img)
    draw.text((av_x + 10, av_y + 6), "V", fill=(255, 255, 255), font=font_m)

    # Voice name & status
    draw.text((av_x + 44, av_y + 2), "Stanley Voice", fill=gray1, font=font_m)
    draw.text((av_x + 44, av_y + 22), "Voice clone active", fill=gray3, font=font_xs)

    # Record button
    rb_x = card_x + card_w - 140
    rounded_rect(draw, [rb_x, vc_y + 16, rb_x + 62, vc_y + 44],
                 fill=purple1, radius=14)
    draw.text((rb_x + 8, vc_y + 22), "Record", fill=(255, 255, 255), font=font_xs)

    # Upload button
    ub_x = rb_x + 68
    rounded_rect(draw, [ub_x, vc_y + 16, ub_x + 62, vc_y + 44],
                 fill=gray4, radius=14)
    draw.text((ub_x + 8, vc_y + 22), "Upload", fill=gray2, font=font_xs)

    y = vc_y + vc_h + 8

    # ── Voice Library ──
    draw.text((card_x + 4, y + 4), "VOICE LIBRARY", fill=gray3, font=font_xs)
    y += 24

    lib_card_h = 80
    rounded_rect(draw, [card_x, y, card_x + card_w, y + lib_card_h],
                 fill=(255, 255, 255), radius=16,
                 outline=(240, 240, 240), outline_width=1)

    # Library item 1 (active)
    ly = y + 8
    rounded_rect(draw, [card_x + 8, ly, card_x + card_w - 8, ly + 30],
                 fill=(240, 240, 255), radius=10)
    draw.ellipse([card_x + 16, ly + 11, card_x + 24, ly + 19], fill=purple1)
    draw.text((card_x + 32, ly + 7), "Stanley Voice", fill=gray1, font=font_s)
    # Active tag
    rounded_rect(draw, [card_x + card_w - 120, ly + 5, card_x + card_w - 76, ly + 24],
                 fill=(238, 238, 255), radius=8)
    draw.text((card_x + card_w - 115, ly + 7), "Active", fill=purple1, font=font_xs)
    # Use button
    rounded_rect(draw, [card_x + card_w - 58, ly + 4, card_x + card_w - 16, ly + 25],
                 fill=(255, 255, 255), radius=10, outline=(230, 230, 230))
    draw.text((card_x + card_w - 50, ly + 7), "Use", fill=gray3, font=font_xs)

    # Library item 2
    ly += 36
    draw.ellipse([card_x + 16, ly + 11, card_x + 24, ly + 19], fill=(220, 220, 220))
    draw.text((card_x + 32, ly + 7), "Recording_01", fill=gray2, font=font_s)
    rounded_rect(draw, [card_x + card_w - 100, ly + 4, card_x + card_w - 58, ly + 25],
                 fill=(255, 255, 255), radius=10, outline=(230, 230, 230))
    draw.text((card_x + card_w - 92, ly + 7), "Use", fill=gray3, font=font_xs)
    rounded_rect(draw, [card_x + card_w - 50, ly + 4, card_x + card_w - 16, ly + 25],
                 fill=(255, 255, 255), radius=10, outline=(230, 230, 230))
    draw.text((card_x + card_w - 44, ly + 7), "Del", fill=gray3, font=font_xs)

    y += lib_card_h + 14

    # ── Action Buttons ──
    btn_w = (card_w - 20) // 3
    # Start
    bx = card_x
    gradient_circle(img, bx + btn_w // 2, y + 22, 1, purple1, purple2)  # just for draw refresh
    draw = ImageDraw.Draw(img)
    rounded_rect(draw, [bx, y, bx + btn_w, y + 44], fill=purple1, radius=14)
    tw = draw.textlength("Start", font=font_m)
    draw.text((bx + btn_w / 2 - tw / 2, y + 12), "Start", fill=(255, 255, 255), font=font_m)
    # Stop
    bx += btn_w + 10
    rounded_rect(draw, [bx, y, bx + btn_w, y + 44], fill=(245, 245, 245), radius=14)
    tw = draw.textlength("Stop", font=font_m)
    draw.text((bx + btn_w / 2 - tw / 2, y + 12), "Stop", fill=gray2, font=font_m)
    # Test
    bx += btn_w + 10
    rounded_rect(draw, [bx, y, bx + btn_w, y + 44], fill=(255, 248, 240), radius=14,
                 outline=(240, 224, 200))
    tw = draw.textlength("Test", font=font_m)
    draw.text((bx + btn_w / 2 - tw / 2, y + 12), "Test", fill=(232, 160, 64), font=font_m)

    y += 56

    # ── Status Bar ──
    rounded_rect(draw, [card_x, y, card_x + card_w, y + 36],
                 fill=bg_card, radius=12)
    draw.ellipse([card_x + 16, y + 14, card_x + 22, y + 20], fill=(82, 216, 128))
    draw.text((card_x + 30, y + 10), "Ready - Set alarm time and press Start",
              fill=gray3, font=font_s)

    # Save
    img.save("/Users/boqian/Desktop/clock/xiaoyuzhou_mockup.png")
    print("Saved xiaoyuzhou_mockup.png")


if __name__ == "__main__":
    main()
