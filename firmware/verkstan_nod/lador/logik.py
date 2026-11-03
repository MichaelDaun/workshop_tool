# Logikgrindar (nod-02): två arkadknappar och en lampa.
# Grinden väljs i appen. Lådan räknar själv ut lampan, så den fungerar även om nätet hackar.
# OTESTAT UTKAST. Stift enligt docs/07-modulplaner.md.
import time
from machine import Pin

GRINDAR = {
    "and": lambda a, b: a and b,
    "or": lambda a, b: a or b,
    "xor": lambda a, b: a != b,
    "nand": lambda a, b: not (a and b),
    "not": lambda a, b: not a,
}

knapp_a = Pin(14, Pin.IN, Pin.PULL_UP)
knapp_b = Pin(13, Pin.IN, Pin.PULL_UP)
lampa_ut = Pin(16, Pin.OUT)
lampa_a = Pin(17, Pin.OUT)
lampa_b = Pin(18, Pin.OUT)

lage = {"grind": "and", "a": False, "b": False, "senast": 0}


def byt_grind(innehall):
    if innehall.get("typ") in GRINDAR:
        lage["grind"] = innehall["typ"]
        visa()


def visa():
    lampa_a.value(lage["a"])
    lampa_b.value(lage["b"])
    lampa_ut.value(GRINDAR[lage["grind"]](lage["a"], lage["b"]))


def starta(nod):
    nod.har = ["knapp_a", "knapp_b", "lampa"]
    nod.lyssna("grind", byt_grind)
    visa()


def varv(nod):
    # knapparna drar stiftet till jord när de trycks ner
    a, b = not knapp_a.value(), not knapp_b.value()
    if (a, b) == (lage["a"], lage["b"]):
        return
    nu = time.ticks_ms()
    if time.ticks_diff(nu, lage["senast"]) < 20:   # avstudsning
        return
    lage.update(a=a, b=b, senast=nu)
    visa()
    nod.skicka("in/knapp", {"a": a, "b": b})
