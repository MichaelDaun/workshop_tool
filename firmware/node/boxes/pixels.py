# node-09, an 8 × 8 WS2812 matrix. Used by Pixels (a picture) and by Sorting (eight bars).
from machine import Pin
from neopixel import NeoPixel

BRIGHTNESS = 0.15
SERPENTINE = False               # true if every other row runs backwards on the matrix
BAR, ACTIVE = (40, 160, 60), (240, 240, 230)
matrix = NeoPixel(Pin(22), 64)


def put(x, y, c):
    if SERPENTINE and y % 2:
        x = 7 - x
    matrix[y * 8 + x] = tuple(int(v * BRIGHTNESS) for v in c)


def image(d):
    # px is 64 colours as hex, "rrggbb" one after the other, row by row from the top
    px = d.get("px", "")
    if len(px) != 64 * 6:
        return
    for i in range(64):
        y, x = divmod(i, 8)
        c = px[i * 6:i * 6 + 6]
        put(x, y, tuple(int(c[k:k + 2], 16) for k in (0, 2, 4)))
    matrix.write()


def bars(d):
    # v is eight heights from 1 to 8; the two being compared are lit white
    v, hot = d.get("v", [])[:8], d.get("compare", [])
    for x in range(8):
        h = int(v[x]) if x < len(v) else 0
        for y in range(8):
            put(x, y, (ACTIVE if x in hot else BAR) if 7 - y < h else (0, 0, 0))
    matrix.write()


def setup(node):
    node.parts = ["matrix"]
    node.on("image", image)
    node.on("bars", bars)
    matrix.fill((0, 0, 0))
    matrix.write()


def loop(node):
    pass
