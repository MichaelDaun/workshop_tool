# node-04, The fruit sorter. A scale, a colour sensor, a servo flap and a button.
# A fruit that lies still for half a second is measured and sent. The app answers with the flap side.
import time
from machine import I2C, Pin
from parts import HX711, TCS34725, Button, Servo

scale = HX711(16, 17)
flap = Servo(15)
button = Button(14)
colour = None
MIN_G, MAX_G = 20, 300
s = {"g": 0.0, "still": 0, "sent": False, "last": None}


def measure():
    r, g, _, _ = colour.rgbc()
    red = r / (r + g) if r + g else 0.5
    # the same 0 to 1 axes as the plot in the app: x is colour, y is size
    return {
        "x": round(max(0.0, min(1.0, (red - 0.4) / 0.45)), 2),
        "y": round(max(0.0, min(1.0, s["g"] / MAX_G)), 2),
    }


def set_flap(d):
    flap.angle(45 if d.get("to") == "apple" else 135)


def setup(node):
    global colour
    node.parts = ["scale", "colour", "flap", "button"]
    colour = TCS34725(I2C(0, sda=Pin(4), scl=Pin(5)))
    scale.tare()
    flap.angle(90)
    node.on("flap", set_flap)


def loop(node):
    try:
        g = scale.grams()
    except OSError:
        return
    now = time.ticks_ms()
    if abs(g - s["g"]) > 3:
        s.update(g=g, still=now)
    if g < MIN_G:
        if s["sent"]:
            flap.angle(90)
        s.update(sent=False, last=None)
        return
    if not s["sent"] and time.ticks_diff(now, s["still"]) > 500:
        s["last"] = measure()
        s["sent"] = True
        node.send("fruit", s["last"])
    # the button marks the fruit on the scale as a teaching example
    if button.pressed() and s["last"]:
        node.send("fruit", dict(s["last"], example=True))
