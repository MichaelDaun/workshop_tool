# node-08, Eight lamps. Eight LEDs, eight buttons (one per bit), a send button and an OLED.
# Send shows the byte as a letter (65 = A) on the OLED, so the team can write its initials.
import framebuf
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from parts import Button

VALUES = (128, 64, 32, 16, 8, 4, 2, 1)
leds = [Pin(2 + i, Pin.OUT, value=0) for i in range(8)]
buttons = [Button(10 + i) for i in range(8)]
send = Button(18)
oled = None
glyph = framebuf.FrameBuffer(bytearray(8), 8, 8, framebuf.MONO_HLSB)
s = {"v": 0, "text": ""}


def paint():
    for led, v in zip(leds, VALUES):
        led.value(bool(s["v"] & v))
    oled.fill(0)
    oled.text("%3d" % s["v"], 0, 0)
    # framebuf text is 8 px, so each letter is drawn at twice the size by hand
    for i, ch in enumerate(s["text"]):
        glyph.fill(0)
        glyph.text(ch, 0, 0)
        for y in range(8):
            for x in range(8):
                if glyph.pixel(x, y):
                    oled.fill_rect(i * 16 + x * 2, 24 + y * 2, 2, 2, 1)
    oled.show()


def bits(d):
    s["v"] = int(d.get("v", 0)) & 0xFF
    paint()


def setup(node):
    global oled
    node.parts = ["leds", "buttons", "send", "oled"]
    oled = SSD1306_I2C(128, 64, I2C(0, sda=Pin(20), scl=Pin(21)))
    node.on("bits", bits)
    paint()


def loop(node):
    for b, v in zip(buttons, VALUES):
        if b.pressed():
            s["v"] ^= v
            paint()
            node.send("bits", {"v": s["v"]})
    if send.pressed():
        if 65 <= s["v"] <= 90:
            s["text"] = (s["text"] + chr(s["v"]))[-8:]
        paint()
        node.send("sent", {"v": s["v"], "text": s["text"]})
