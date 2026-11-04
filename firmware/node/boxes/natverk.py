# Paketresan (nod-05): tio kablar av LED-slinga och en bygel på varje.
import time
from machine import Pin
from neopixel import NeoPixel

# samma ordning som i appen
KABLAR = (("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"),
          ("D", "F"), ("D", "E"), ("E", "G"), ("F", "G"), ("B", "F"))
PER_KABEL = 6
STYRKA = 0.2                     # 60 lysdioder på full styrka drar över 3 A
HEL, PAKET = (6, 6, 6), (40, 90, 255)

slinga = NeoPixel(Pin(22), len(KABLAR) * PER_KABEL)
byglar = [Pin(2 + i, Pin.IN, Pin.PULL_UP) for i in range(len(KABLAR))]
s = {"klippta": None, "paket": {}, "ritad": 0}


def dampa(c):
    return tuple(int(v * STYRKA) for v in c)


def nytt_paket(d):
    k = d.get("kabel")
    if k is None or not 0 <= k < len(KABLAR):
        return
    t = float(d.get("t", 0))
    if d.get("fran") == KABLAR[k][1]:
        t = 1 - t
    s["paket"][k] = (min(PER_KABEL - 1, int(t * PER_KABEL)), time.ticks_ms())


def starta(nod):
    nod.har = ["slinga", "byglar"]
    nod.lyssna("paket", nytt_paket)


def varv(nod):
    klippta = [i for i, b in enumerate(byglar) if b.value()]   # urdragen bygel ger hög nivå
    if klippta != s["klippta"]:
        s["klippta"] = klippta
        nod.skicka("in/kablar", {"klippta": klippta})

    nu = time.ticks_ms()
    if time.ticks_diff(nu, s["ritad"]) < 40:
        return
    s["ritad"] = nu
    for k in range(len(KABLAR)):
        for i in range(PER_KABEL):
            slinga[k * PER_KABEL + i] = (0, 0, 0) if k in klippta else dampa(HEL)
        p = s["paket"].get(k)
        if p and time.ticks_diff(nu, p[1]) < 300:
            slinga[k * PER_KABEL + p[0]] = dampa(PAKET)
    slinga.write()
