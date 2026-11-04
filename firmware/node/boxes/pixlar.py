# Pixlar (nod-09): en matris med 8 × 8 adresserbara lysdioder.
from machine import Pin
from neopixel import NeoPixel

STYRKA = 0.15
ORM = False                      # sant om varannan rad går baklänges på matrisen
matris = NeoPixel(Pin(22), 64)


def ny_bild(d):
    # px är 64 färger som hex, "rrggbb" efter varandra
    px = d.get("px", "")
    if len(px) != 64 * 6:
        return
    for i in range(64):
        y, x = divmod(i, 8)
        if ORM and y % 2:
            x = 7 - x
        c = px[i * 6:i * 6 + 6]
        matris[y * 8 + x] = tuple(int(int(c[k:k + 2], 16) * STYRKA) for k in (0, 2, 4))
    matris.write()


def starta(nod):
    nod.har = ["matris"]
    nod.lyssna("bild", ny_bild)
    matris.fill((0, 0, 0))
    matris.write()


def varv(nod):
    pass
