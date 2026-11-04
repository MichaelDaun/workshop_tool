# node-12, Next word. Four MAX7219 matrices in a row scroll the sentence the team sends.
# The built-in 8 px font is ASCII only, so å, ä and ö are shown as a, a and o.
import time
from machine import SPI, Pin
from parts import MAX7219

display = None
PLAIN = {"å": "a", "ä": "a", "ö": "o", "Å": "A", "Ä": "A", "Ö": "O"}
s = {"text": "", "x": 32, "moved": 0}


def text(d):
    t = "".join(PLAIN.get(c, c) for c in str(d.get("text", "")))
    s.update(text=t[:120], x=32)


def setup(node):
    global display
    node.parts = ["matrix_32x8"]
    display = MAX7219(SPI(0, baudrate=10_000_000, sck=Pin(18), mosi=Pin(19)), cs=17)
    node.on("text", text)


def loop(node):
    now = time.ticks_ms()
    if not s["text"] or time.ticks_diff(now, s["moved"]) < 45:
        return
    s["moved"] = now
    display.fb.fill(0)
    display.fb.text(s["text"], s["x"], 0, 1)
    display.show()
    s["x"] -= 1
    if s["x"] < -8 * len(s["text"]):
        s["x"] = 32
        node.send("shown", {"text": s["text"]})
