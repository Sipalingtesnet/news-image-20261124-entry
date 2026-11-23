import os
import hashlib
from PIL import Image, ImageDraw, ImageFont

def draw_newspaper():
    width, height = 1024, 1024
    bg_color = (247, 243, 235)
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    font_path_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_path_reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    font_masthead = ImageFont.truetype(font_path_bold, 40)
    font_dateline = ImageFont.truetype(font_path_reg, 16)
    font_sec_label = ImageFont.truetype(font_path_bold, 14)
    font_headline = ImageFont.truetype(font_path_bold, 20)
    font_summary = ImageFont.truetype(font_path_reg, 14)
    font_ticker_title = ImageFont.truetype(font_path_bold, 12)
    font_ticker_text = ImageFont.truetype(font_path_reg, 13)

    c_red = (180, 40, 30)
    c_darkblue = (25, 45, 85)
    c_black = (20, 20, 20)
    c_gray = (100, 100, 100)
    c_white = (255, 255, 255)
    c_panel_bg = (255, 253, 248)
    c_border = (210, 200, 185)

    margin = 24
    content_width = width - (2 * margin)

    y = margin
    draw.text((width // 2, y), "THE WORLD IN ONE PICTURE", fill=c_black, font=font_masthead, anchor="mm")
    y += 44
    draw.text((width // 2, y), "TUESDAY, 24 NOVEMBER 2026", fill=c_gray, font=font_dateline, anchor="mm")
    y += 20

    draw.line([(margin, y), (width - margin, y)], fill=c_red, width=3)
    y += 5
    draw.line([(margin, y), (width - margin, y)], fill=c_black, width=1)
    y += 12

    ticker_height = 68
    bottom_limit = height - margin - ticker_height
    grid_height = bottom_limit - y - 8

    cols = 2
    rows = 2
    gap = 14
    panel_w = (content_width - gap) // cols
    panel_h = (grid_height - gap) // rows

    stories = [
        {
            "label": "INDIA & NEPAL",
            "headline": "Modi & Shah Flag Off Saryu-Kamala Express.",
            "summary": "PM Modi and Nepal PM Balendra Shah virtually launched the new train linking Ayodhya and Janakpur Dham, signing 8 bilateral agreements with a Rs 15,000 crore package.",
            "art": "train"
        },
        {
            "label": "INDONESIA",
            "headline": "Banten Factory Fire Leaves 24 Dead.",
            "summary": "At least 24 people died and 30 are missing after a severe fire tore through a confectionery factory in Banten province. Rescuers continue searching the wreckage.",
            "art": "factory"
        },
        {
            "label": "CLIMATE / COP31",
            "headline": "COP31 Climate Summit Ends in Deadlock.",
            "summary": "The Antalya summit concluded with no deal after the EU and other blocs rejected a draft text that dropped language on phasing out fossil fuels.",
            "art": "climate"
        },
        {
            "label": "UKRAINE",
            "headline": "Kyiv Drone Strike Hits Residential Block.",
            "summary": "A Russian drone strike hit a Kyiv residential building, leaving 14 missing. President Zelenskiy noted rescuers and residents are searching the rubble.",
            "art": "drone"
        }
    ]

    for i, s in enumerate(stories):
        col = i % cols
        row = i // cols
        px = margin + col * (panel_w + gap)
        py = y + row * (panel_h + gap)

        draw.rectangle([px, py, px + panel_w, py + panel_h], fill=c_panel_bg, outline=c_border, width=1)
        draw.rectangle([px, py, px + panel_w, py + 24], fill=c_darkblue)
        draw.text((px + 10, py + 12), s["label"], fill=c_white, font=font_sec_label, anchor="lm")

        content_py = py + 30
        art_box_h = 120
        art_box = [px + 12, content_py, px + panel_w - 12, content_py + art_box_h]
        draw.rectangle(art_box, fill=(240, 237, 228), outline=c_border, width=1)

        draw_art(draw, s["art"], art_box)

        text_y = content_py + art_box_h + 10
        h_lines = wrap_text(s["headline"], font_headline, panel_w - 24, draw)
        for hl in h_lines[:2]:
            draw.text((px + 12, text_y), hl, fill=c_black, font=font_headline)
            text_y += 24

        text_y += 2
        s_lines = wrap_text(s["summary"], font_summary, panel_w - 24, draw)
        for sl in s_lines[:3]:
            draw.text((px + 12, text_y), sl, fill=(60, 60, 60), font=font_summary)
            text_y += 18

    ticker_y = bottom_limit + 6
    draw.rectangle([margin, ticker_y, width - margin, height - margin], fill=(238, 234, 224), outline=c_darkblue, width=1)
    draw.rectangle([margin, ticker_y, margin + 54, height - margin], fill=c_red)
    draw.text((margin + 27, ticker_y + (ticker_height // 2)), "ALSO", fill=c_white, font=font_ticker_title, anchor="mm")

    also_text = (
        "Russian cargo ship on fire off Finland after attack in Gulf of Finland. "
        "Lisbon trade union CGTP plans rally outside Assembly ahead of 2027 budget vote. "
        "India vs NZ 1st Test ends in draw (Rishabh Pant 128). "
        "Max Verstappen wins Las Vegas GP. "
        "Bangladesh vows to arrest Sheikh Hasina if she returns. "
        "China announces 2030 elderly care and childcare targets. "
        "South Korea nominates new Foreign Minister and intelligence chief. "
        "Armenia proposes new constitution for peace talks. "
        "India Sensex falls 1,484 points."
    )

    ticker_box_w = content_width - 64
    t_lines = wrap_text(also_text, font_ticker_text, ticker_box_w, draw)
    ty = ticker_y + 8
    for tl in t_lines[:2]:
        draw.text((margin + 64, ty), tl, fill=c_black, font=font_ticker_text)
        ty += 18

    return img

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_art(draw, art_type, box):
    x1, y1, x2, y2 = box
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

    if art_type == "train":
        draw.arc([x1 + 20, y1 + 45, x2 - 20, y2 - 10], 180, 360, fill=(120, 110, 100), width=5)
        draw.line([x1 + 20, y2 - 18, x2 - 20, y2 - 18], fill=(100, 90, 80), width=3)
        train_y = y2 - 38
        draw.rectangle([cx - 36, train_y, cx + 36, train_y + 20], fill=(40, 40, 40), outline=(20, 20, 20))
        draw.rectangle([cx - 26, train_y - 10, cx - 4, train_y], fill=(70, 70, 70))
        draw.ellipse([cx - 26, train_y + 16, cx - 16, train_y + 26], fill=(20, 20, 20))
        draw.ellipse([cx + 10, train_y + 16, cx + 20, train_y + 26], fill=(20, 20, 20))
        draw.ellipse([cx - 30, train_y - 18, cx - 20, train_y - 8], fill=(200, 200, 200))
        draw.line([x1 + 25, y1 + 65, x1 + 25, y1 + 25], fill=(80, 80, 80), width=2)
        draw.rectangle([x1 + 25, y1 + 25, x1 + 50, y1 + 40], fill=(240, 130, 40))
        draw.line([x2 - 25, y1 + 65, x2 - 25, y1 + 20], fill=(80, 80, 80), width=2)
        draw.polygon([(x2 - 25, y1 + 20), (x2 - 5, y1 + 30), (x2 - 25, y1 + 40)], fill=(200, 30, 30))

    elif art_type == "factory":
        fx1, fy1 = cx - 55, y1 + 30
        fx2, fy2 = cx + 55, y2 - 10
        draw.rectangle([fx1, fy1, fx2, fy2], fill=(160, 150, 140), outline=(100, 90, 80), width=2)
        draw.rectangle([fx1 + 12, fy1 - 22, fx1 + 26, fy1], fill=(130, 120, 110))
        draw.rectangle([fx2 - 26, fy1 - 30, fx2 - 12, fy1], fill=(130, 120, 110))
        draw.polygon([(cx - 18, fy1 + 10), (cx - 10, fy1 - 14), (cx, fy1 + 10)], fill=(230, 80, 20))
        draw.polygon([(cx + 4, fy1 + 12), (cx + 16, fy1 - 10), (cx + 22, fy1 + 12)], fill=(240, 130, 20))
        for wy in range(fy1 + 16, fy2 - 8, 18):
            draw.rectangle([fx1 + 12, wy, fx1 + 30, wy + 10], fill=(50, 50, 50))
            draw.rectangle([fx2 - 30, wy, fx2 - 12, wy + 10], fill=(50, 50, 50))
        hx, hy = cx, y2 - 20
        draw.arc([hx - 16, hy - 8, hx + 16, hy + 10], 180, 360, fill=(240, 180, 20), width=5)
        draw.rectangle([hx - 10, hy + 3, hx + 10, hy + 7], fill=(200, 140, 10))

    elif art_type == "climate":
        gx, gy, gr = cx - 30, cy, 34
        draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(180, 205, 225), outline=(100, 130, 160), width=2)
        draw.rectangle([gx - 7, gy - gr - 10, gx - 2, gy - gr], fill=(100, 100, 100))
        draw.rectangle([gx + 2, gy - gr - 15, gx + 7, gy - gr], fill=(100, 100, 100))
        draw.ellipse([gx - 12, gy - gr - 22, gx - 2, gy - gr - 14], fill=(210, 210, 210))
        dx, dy = cx + 12, cy - 20
        dw, dh = 50, 58
        draw.rectangle([dx, dy, dx + dw, dy + dh], fill=(255, 255, 255), outline=(120, 120, 120), width=1)
        draw.line([dx + 6, dy + 6, dx + dw - 6, dy + dh - 6], fill=(200, 40, 30), width=3)
        draw.line([dx + dw - 6, dy + 6, dx + 6, dy + dh - 6], fill=(200, 40, 30), width=3)
        draw.text((dx + dw // 2, dy + dh // 2), "NO DEAL", fill=(180, 30, 30), font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10), anchor="mm")

    elif art_type == "drone":
        ax1, ay1 = cx - 40, y1 + 30
        ax2, ay2 = cx + 40, y2 - 8
        draw.rectangle([ax1, ay1, ax2, ay2], fill=(150, 150, 160), outline=(90, 90, 100), width=2)
        for wx in range(ax1 + 8, ax2 - 8, 16):
            for wy in range(ay1 + 10, ay2 - 8, 14):
                draw.rectangle([wx, wy, wx + 8, wy + 8], fill=(230, 220, 150))
        draw.polygon([(ax1, ay2 - 20), (ax1 + 15, ay2 - 10), (ax1, ay2)], fill=(80, 80, 90))
        dx, dy = cx, y1 + 16
        draw.line([dx - 18, dy, dx + 18, dy], fill=(30, 30, 30), width=3)
        draw.line([dx - 10, dy - 5, dx + 10, dy - 5], fill=(30, 30, 30), width=2)
        draw.ellipse([dx - 4, dy - 3, dx + 4, dy + 3], fill=(200, 30, 30))
        draw.polygon([(dx, dy + 3), (ax1 - 8, ay2), (ax2 + 8, ay2)], fill=(255, 255, 200))

if __name__ == "__main__":
    img = draw_newspaper()
    img.save("entry.png")
    print("entry.png generated.")
