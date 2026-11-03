# Åtta lampor (nod-08): åtta lysdioder och åtta knappar, en per bit.
from machine import Pin
from delar import Knapp

VARDEN = (128, 64, 32, 16, 8, 4, 2, 1)
lampor = [Pin(2 + i, Pin.OUT, value=0) for i in range(8)]
knappar = [Knapp(10 + i) for i in range(8)]
s = {"v": 0}


def visa():
    for lampa, v in zip(lampor, VARDEN):
        lampa.value(bool(s["v"] & v))


def nya_bitar(d):
    s["v"] = int(d.get("v", 0)) & 0xFF
    visa()


def starta(nod):
    nod.har = ["lampor", "knappar"]
    nod.lyssna("bitar", nya_bitar)
    visa()


def varv(nod):
    for k, v in zip(knappar, VARDEN):
        if k.tryckt():
            s["v"] ^= v
            visa()
            nod.skicka("in/bitar", {"v": s["v"]})
