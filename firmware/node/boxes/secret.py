# node-13, Secret colours. A chest with a servo lock and an RGB LED. The chest plays the friend:
# it picks the public colour and its own secret, and opens for the shared colour.
# Colours mix as paint does in the app: the geometric mean per channel.
import os
from machine import Pin, PWM
from parts import Servo

COLOURS = {
    "yellow": (250, 214, 60), "red": (214, 52, 52), "blue": (40, 92, 210), "pink": (240, 140, 190),
    "teal": (40, 190, 180), "purple": (130, 60, 170), "white": (245, 245, 240),
}
NAMES = sorted(COLOURS)
lock = Servo(15)
rgb = [PWM(Pin(p)) for p in (10, 11, 12)]
s = {"public": None, "secret": None, "shared": None, "told": False}


def pick(names):
    return names[os.urandom(1)[0] % len(names)]


def mix(*cs):
    out = []
    for ch in range(3):
        p = 1.0
        for c in cs:
            p *= c[ch]
        out.append(round(p ** (1 / len(cs))))
    return out


def show(c):
    for pwm, v in zip(rgb, c):
        pwm.freq(1000)
        pwm.duty_u16(int((v / 255) ** 2.2 * 65535))


def start(_=None):
    s["public"] = pick(NAMES)
    s["secret"] = pick([n for n in NAMES if n != s["public"]])
    s.update(shared=None, told=False)
    lock.angle(0)
    show(COLOURS[s["public"]])


def their_mix(d):
    # the team's mix is public·theirs; the shared colour is public·theirs·secret, so
    # shared = (their_mix² · secret)^(1/3) per channel
    m, sec = d.get("rgb", [0, 0, 0]), COLOURS[s["secret"]]
    s["shared"] = [round((m[i] * m[i] * sec[i]) ** (1 / 3)) for i in range(3)]


def try_open(d):
    c = d.get("rgb", [0, 0, 0])
    ok = s["shared"] is not None and all(abs(c[i] - s["shared"][i]) < 4 for i in range(3))
    if ok:
        lock.angle(100)
        show(s["shared"])
    return ok


def setup(node):
    node.parts = ["lock", "rgb"]
    node.on("start", start)
    node.on("mix", their_mix)
    node.on("open", lambda d: node.send("chest", {"open": try_open(d)}))
    start()


def loop(node):
    # announce once there is a connection: the public colour and the chest's own mix
    if not s["told"] and node.mqtt:
        node.send("public", {"colour": s["public"], "mix": mix(COLOURS[s["public"]], COLOURS[s["secret"]])})
        s["told"] = True
