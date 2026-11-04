# Logikgrindar (nod-02): två knappar och tre lampor.
# Lådan räknar själv ut lampan, så den fungerar även om nätet hackar.
from machine import Pin
from delar import Knapp

GRINDAR = {
    "and": lambda a, b: a and b,
    "or": lambda a, b: a or b,
    "xor": lambda a, b: a != b,
    "nand": lambda a, b: not (a and b),
    "not": lambda a, b: not a,
}

knapp_a, knapp_b = Knapp(14), Knapp(13)
lampa_ut, lampa_a, lampa_b = Pin(16, Pin.OUT), Pin(17, Pin.OUT), Pin(18, Pin.OUT)
s = {"grind": "and", "a": False, "b": False}


def visa():
    lampa_a.value(s["a"])
    lampa_b.value(s["b"])
    lampa_ut.value(GRINDAR[s["grind"]](s["a"], s["b"]))


def byt_grind(d):
    if d.get("typ") in GRINDAR:
        s["grind"] = d["typ"]
        visa()


def starta(nod):
    nod.har = ["knapp_a", "knapp_b", "lampa"]
    nod.lyssna("grind", byt_grind)
    visa()


def varv(nod):
    andrad = False
    for namn, k in (("a", knapp_a), ("b", knapp_b)):
        k.tryckt()
        if k.nere != s[namn]:
            s[namn] = k.nere
            andrad = True
    if andrad:
        visa()
        nod.skicka("in/knapp", {"a": s["a"], "b": s["b"]})
