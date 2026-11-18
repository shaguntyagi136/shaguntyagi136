
import math
import os

W, H = 420, 500
STEP, R = 4.6, 1.15

def pip(x, y, poly):
    inside = False
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]

        if (y1 > y) != (y2 > y) and x < (
            (x2 - x1) * (y - y1) / (y2 - y1) + x1
        ):
            inside = not inside
    return inside


def in_ellipse(x, y, cx, cy, rx, ry):
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def dist_to_seg(px, py, a, b):
    ax, ay = a
    bx, by = b

    dx, dy = bx - ax, by - ay
    t = max(0, min(1, (
        (px - ax) * dx + (py - ay) * dy
    ) / (dx * dx + dy * dy)))

    return math.hypot(
        px - (ax + t * dx),
        py - (ay + t * dy)
    )


# Cat silhouette
body = [
    (140, 85), (160, 110), (182, 160),
    (200, 182), (232, 182), (255, 150),
    (272, 85), (292, 110), (312, 150),
    (322, 200), (320, 290), (300, 320),
    (262, 335), (258, 360), (275, 400),
    (298, 485), (96, 485), (122, 400),
    (140, 360), (138, 335), (100, 320),
    (92, 290), (92, 200), (100, 150),
    (118, 110)
]

eyes = [
    (155, 248, 29, 23),
    (264, 248, 29, 23)
]

pupils = [
    (168, 244, 8, 15),
    (251, 246, 8, 15)
]

whiskers = [
    ((100, 288), (55, 290)),
    ((100, 300), (58, 312)),
    ((106, 312), (70, 337)),
    ((314, 285), (366, 285)),
    ((314, 297), (362, 307)),
    ((310, 310), (346, 337))
]


# Generate halftone dots
dots = []
y = 80
row = 0

while y < 490:
    x = 50 + (STEP / 2 if row % 2 else 0)

    while x < 370:
        keep = False

        if pip(x, y, body):
            keep = True

            for cx, cy, rx, ry in eyes:
                if in_ellipse(x, y, cx, cy, rx, ry):
                    keep = False

            for cx, cy, rx, ry in pupils:
                if in_ellipse(x, y, cx, cy, rx, ry):
                    keep = True

        if any(
            dist_to_seg(x, y, a, b) < 1.6
            for a, b in whiskers
        ):
            keep = True

        if keep:
            dots.append((x, y))

        x += STEP

    y += STEP * 0.9
    row += 1


# Build SVG
svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'viewBox="0 0 {W} {H}" width="100%">',

    '<rect width="100%" height="100%" fill="#141418"/>',
    '<g fill="#ffffff">'
]

svg += [
    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R}"/>'
    for x, y in dots
]

svg.append('</g>')

svg.append(
    '<text x="380" y="262" fill="#ffffff" '
    'font-family="Menlo,Consolas,monospace" '
    'font-size="13" text-anchor="end">-mao</text>'
)

svg.append('</svg>')


# Save inside assets folder
os.makedirs("assets", exist_ok=True)

with open("assets/header.svg", "w") as f:
    f.write('\n'.join(svg))

print(len(dots), "dots generated")
print("SVG saved to assets/header.svg")
