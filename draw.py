"""Draw the 23 November 2026 world-news front page (1024x1024 PNG).

Stories are as reported on 23 November 2026 (weekend reports carried
that day): COP31 in Antalya ends with no deal; Iran strikes Bahrain;
Ukraine hits Russian ships in Libya; Russian strikes kill in Kyiv
region; Asian chip stocks tumble; Mexico captures a cartel chief.
Layout is a newspaper front page: masthead with the date, one lead
story, four stories in a grid, and a short 'also' strip.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
BLACK = (20, 20, 20)
RED = (176, 0, 0)
BLUE = (24, 78, 140)
LIGHT = (238, 240, 244)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit width in pixels, word by word."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, width, fill, spacing=4):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def panel(draw, box, label, headline, body, icon, accent):
    """One story panel: coloured label, headline, body, small icon."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=BLACK, width=2)
    draw.rectangle([x0, y0, x1, y0 + 26], fill=accent)
    draw.text((x0 + 10, y0 + 4), label, font=font(SANS_B, 15), fill=WHITE)
    icon(draw, x1 - 118, y0 + 36, 104, 78)
    y = draw_wrapped(draw, (x0 + 12, y0 + 36), headline,
                     font(SANS_B, 24), x1 - x0 - 142, BLACK, spacing=2)
    draw_wrapped(draw, (x0 + 12, y + 4), body,
                 font(SANS, 17), x1 - x0 - 142, BLACK, spacing=3)


def icon_globe(draw, x, y, w, h):
    draw.ellipse([x, y, x + w, y + h], fill=(52, 130, 200), outline=BLUE, width=2)
    draw.ellipse([x + 18, y + 16, x + 48, y + 40], fill=(74, 160, 90))
    draw.ellipse([x + 52, y + 44, x + 88, y + 66], fill=(74, 160, 90))
    draw.line([x, y + h // 2, x + w, y + h // 2], fill=WHITE, width=2)


def icon_burst(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    for dx, dy in [(0, -30), (26, -15), (26, 15), (0, 30), (-26, 15), (-26, -15)]:
        draw.line([cx, cy, cx + dx, cy + dy], fill=RED, width=5)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 180, 0))


def icon_ship(draw, x, y, w, h):
    draw.rectangle([x, y + 58, x + w, y + 78], fill=BLUE)
    draw.polygon([(x + 8, y + 52), (x + 96, y + 52), (x + 84, y + 76), (x + 20, y + 76)], fill=(60, 60, 60))
    draw.rectangle([x + 46, y + 18, x + 52, y + 52], fill=(60, 60, 60))
    draw.polygon([(x + 52, y + 18), (x + 78, y + 30), (x + 52, y + 34)], fill=RED)


def icon_building(draw, x, y, w, h):
    draw.rectangle([x + 10, y + 20, x + 44, y + 78], fill=(120, 120, 120))
    draw.rectangle([x + 56, y + 34, x + 90, y + 78], fill=(90, 90, 90))
    for bx in (10, 56):
        for by in (30, 48, 64):
            draw.rectangle([x + bx + 6, y + by, x + bx + 14, y + by + 8], fill=(255, 220, 120))
    draw.line([x + 24, y + 18, x + 34, y + 2], fill=GREY, width=3)
    draw.ellipse([x + 28, y - 6, x + 44, y + 10], fill=(200, 200, 200))


def icon_chart(draw, x, y, w, h):
    draw.line([x, y + 66, x + w, y + 66], fill=BLACK, width=2)
    draw.line([x, y + 10, x + 14, y + 22, x + 34, y + 18, x + 56, y + 38, x + 78, y + 44, x + 96, y + 62], fill=RED, width=4)
    draw.polygon([(x + 96, y + 62), (x + 86, y + 56), (x + 88, y + 68)], fill=RED)


def icon_shield(draw, x, y, w, h):
    draw.polygon([(x + 52, y + 4), (x + 96, y + 18), (x + 96, y + 48), (x + 52, y + 76), (x + 8, y + 48), (x + 8, y + 18)], fill=BLUE, outline=BLACK, width=2)
    draw.text((x + 38, y + 26), "★", font=font(SANS_B, 30), fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([MARGIN - 6, MARGIN - 6, W - MARGIN + 6, H - MARGIN + 6], outline=BLACK, width=4)
    # Masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 34), title, font=tf, fill=BLACK)
    d.line([MARGIN + 10, 118, W - MARGIN - 10, 118], fill=BLACK, width=3)
    dateline = "MONDAY, 23 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE"
    df = font(SANS_B, 22)
    d.text(((W - d.textlength(dateline, font=df)) / 2, 128), dateline, font=df, fill=RED)
    d.line([MARGIN + 10, 162, W - MARGIN - 10, 162], fill=BLACK, width=2)

    # Lead story: COP31
    x0, y0, x1, y1 = MARGIN + 10, 176, W - MARGIN - 10, 400
    d.rectangle([x0, y0, x1, y1], outline=BLACK, width=2)
    d.rectangle([x0, y0, x1, y0 + 28], fill=RED)
    d.text((x0 + 12, y0 + 5), "CLIMATE  •  TURKEY", font=font(SANS_B, 16), fill=WHITE)
    icon_globe(d, x1 - 230, y0 + 42, 170, 170)
    y = draw_wrapped(d, (x0 + 14, y0 + 42), "COP31 ENDS\nWITH NO DEAL",
                     font(SANS_B, 46), 620, BLACK, spacing=2)
    draw_wrapped(d, (x0 + 14, y + 8),
                 "UN climate talks in Antalya close two days late — the longest ever — split over fossil fuels and money, with no new agreement.",
                 font(SANS, 20), 620, BLACK, spacing=4)

    # Four stories in a 2x2 grid
    gx0, gy0 = MARGIN + 10, 416
    gw, gh, gap = (W - 2 * MARGIN - 20 - 16) // 2, 208, 14
    stories = [
        ("MIDDLE EAST", "IRAN HITS BAHRAIN", "Iranian missiles and drones strike US positions and a civilian site; two hurt, defences intercept most.", icon_burst, RED),
        ("WAR AT SEA", "UKRAINE SINKS SHIP IN LIBYA", "Sea drones hit two Russian ships at the port of Benghazi, Kyiv says; the war at sea spreads far from Ukraine.", icon_ship, BLUE),
        ("UKRAINE", "RUSSIAN STRIKES KILL IN KYIV REGION", "Overnight attacks kill at least 15, damage homes, a hospital and schools; 14 missing in Dymer.", icon_building, (90, 90, 90)),
        ("MARKETS  •  ASIA", "ASIAN CHIP STOCKS TUMBLE", "Kospi falls 3.3% as doubts over AI spending rout Wall Street; Samsung -3.1%, SK Hynix -2.5%.", icon_chart, (0, 120, 60)),
    ]
    for i, (label, head, body, icon, accent) in enumerate(stories):
        x = gx0 + (i % 2) * (gw + gap)
        yy = gy0 + (i // 2) * (gh + gap)
        panel(d, (x, yy, x + gw, yy + gh), label, head, body, icon, accent)

    # Also strip
    ax0, ay0 = MARGIN + 10, gy0 + 2 * gh + gap + 8
    d.rectangle([ax0, ay0, W - MARGIN - 10, ay0 + 88], outline=BLACK, width=2)
    d.text((ax0 + 12, ay0 + 8), "ALSO ON 23 NOVEMBER", font=font(SANS_B, 16), fill=RED)
    draw_wrapped(d, (ax0 + 12, ay0 + 34),
                 "Mexico captures cartel chief “Chapo Isidro” after a firefight kills 11  •  Peru quake, magnitude 6.7, shakes the Andes  •  Indonesia factory fire kills 24, dozens missing",
                 font(SANS, 18), W - 2 * MARGIN - 44, BLACK, spacing=4)
    d.text((MARGIN + 10, H - MARGIN - 14), "Stories as reported on 23 November 2026.",
           font=font(SANS, 14), fill=GREY)
    d.text((W - MARGIN - 10 - d.textlength("THE WORLD TODAY", font=font(SANS_B, 14)), H - MARGIN - 14),
           "THE WORLD TODAY", font=font(SANS_B, 14), fill=GREY)
    img.save("/home/hatch/workspace/makefun-news-image/entry/entry.png", "PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
