# node-05, Packet tour. Seven houses joined by ten LED strip cables. Each cable has a jumper;
# pulling it cuts the cable. The app routes packets and sends where each one is.
import time
from machine import Pin
from neopixel import NeoPixel

# the same order as in the app
CABLES = (("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"),
          ("D", "F"), ("D", "E"), ("E", "G"), ("F", "G"), ("B", "F"))
PER_CABLE = 6
BRIGHTNESS = 0.2                 # 60 LEDs at full brightness draw more than 3 A
IDLE, PACKET = (6, 6, 6), (40, 90, 255)

strip = NeoPixel(Pin(22), len(CABLES) * PER_CABLE)
jumpers = [Pin(2 + i, Pin.IN, Pin.PULL_UP) for i in range(len(CABLES))]
s = {"cut": None, "packets": {}, "drawn": 0}


def dim(c):
    return tuple(int(v * BRIGHTNESS) for v in c)


def packet(d):
    k = d.get("cable")
    if k is None or not 0 <= k < len(CABLES):
        return
    t = float(d.get("t", 0))
    if d.get("from") == CABLES[k][1]:
        t = 1 - t
    s["packets"][k] = (min(PER_CABLE - 1, int(t * PER_CABLE)), time.ticks_ms())


def setup(node):
    node.parts = ["strip", "jumpers"]
    node.on("packet", packet)


def loop(node):
    cut = [i for i, j in enumerate(jumpers) if j.value()]      # a pulled jumper reads high
    if cut != s["cut"]:
        s["cut"] = cut
        node.send("cables", {"cut": cut})

    now = time.ticks_ms()
    if time.ticks_diff(now, s["drawn"]) < 40:
        return
    s["drawn"] = now
    for k in range(len(CABLES)):
        for i in range(PER_CABLE):
            strip[k * PER_CABLE + i] = (0, 0, 0) if k in cut else dim(IDLE)
        p = s["packets"].get(k)
        if p and time.ticks_diff(now, p[1]) < 300:
            strip[k * PER_CABLE + p[0]] = dim(PACKET)
    strip.write()
