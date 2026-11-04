# Fruktsorteraren (nod-04): våg, färgsensor, lucka och en knapp.
import time
from machine import I2C, Pin
from delar import HX711, TCS34725, Knapp, Servo

vag = HX711(16, 17)
lucka = Servo(15)
knapp = Knapp(14)
farg = None
MINST, STORST = 20, 300          # gram
s = {"g": 0.0, "stilla": 0, "skickad": False, "senast": None}


def las():
    r, g, _, _ = farg.rgbc()
    rod = r / (r + g) if r + g else 0.5
    return {
        "farg": round(max(0.0, min(1.0, (rod - 0.4) / 0.45)), 2),
        "storlek": round(max(0.0, min(1.0, s["g"] / STORST)), 2),
    }


def ny_lucka(d):
    lucka.vinkel(45 if d.get("mot") == "apple" else 135)


def starta(nod):
    global farg
    nod.har = ["vag", "farg", "lucka", "knapp"]
    farg = TCS34725(I2C(0, sda=Pin(4), scl=Pin(5)))
    vag.tarera()
    lucka.vinkel(90)
    nod.lyssna("lucka", ny_lucka)


def varv(nod):
    try:
        g = vag.gram()
    except OSError:
        return
    nu = time.ticks_ms()
    if abs(g - s["g"]) > 3:
        s.update(g=g, stilla=nu)
    if g < MINST:
        if s["skickad"]:
            lucka.vinkel(90)
        s.update(skickad=False, senast=None)
        return
    if not s["skickad"] and time.ticks_diff(nu, s["stilla"]) > 500:
        s["senast"] = las()
        s["skickad"] = True
        nod.skicka("in/frukt", s["senast"])
    if knapp.tryckt() and s["senast"]:
        nod.skicka("in/frukt", dict(s["senast"], exempel=True))
