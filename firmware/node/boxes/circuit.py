# node-01, The circuit. 5 V through a 100 Ω resistor, a 500 Ω knob and an LED.
# The knob sets the current directly; the Pico only measures it: I = (5 V - 2 V) / (100 Ω + R).
# At R = 0 the LED gets 30 mA, above its 20 mA rating, so the display blinks over 20 mA.
import time
from machine import I2C, Pin
from parts import INA219, TM1637

LIMIT_MA = 20
display = TM1637(2, 3)
ina = None
s = {"measured": 0, "mA": 0.0}


def setup(node):
    global ina
    node.parts = ["ina219", "display"]
    ina = INA219(I2C(0, sda=Pin(4), scl=Pin(5)))
    display.number(None)


def loop(node):
    now = time.ticks_ms()
    if time.ticks_diff(now, s["measured"]) < 250:
        return
    s["measured"] = now
    mA = sum(ina.mA() for _ in range(8)) / 8
    if abs(mA - s["mA"]) >= 0.1:
        node.send("current", {"mA": round(mA, 1)})
    s["mA"] = mA
    if mA > LIMIT_MA and (now // 250) % 2:
        display.segments(bytes(4))
    else:
        display.number(round(mA))
