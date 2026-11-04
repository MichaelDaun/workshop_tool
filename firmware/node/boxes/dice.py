# node-10, Dice. A shaker with an accelerometer and a display. A shake rolls the dice.
import os
import time
from machine import I2C, Pin
from parts import MPU6050, TM1637

display = TM1637(2, 3)
acc = None
SHAKE = 0.6                      # g beyond gravity
s = {"dice": 1, "shaking": 0, "quiet": 0, "spun": 0}


def roll():
    return 1 + os.urandom(1)[0] % 6


def set_dice(d):
    s["dice"] = max(1, min(3, int(d.get("n", 1))))


def setup(node):
    global acc
    node.parts = ["acc", "display"]
    acc = MPU6050(I2C(0, sda=Pin(4), scl=Pin(5)))
    node.on("dice", set_dice)
    display.number(None)


def loop(node):
    x, y, z = acc.acc()
    now = time.ticks_ms()
    if abs((x * x + y * y + z * z) ** 0.5 - 1) > SHAKE:
        s["shaking"] += 1
        s["quiet"] = now
    elif time.ticks_diff(now, s["quiet"]) > 300:
        if s["shaking"] >= 3:
            r = [roll() for _ in range(s["dice"])]
            display.number(sum(r))
            node.send("roll", {"v": r, "sum": sum(r)})
        s["shaking"] = 0
        return
    if s["shaking"] >= 3 and time.ticks_diff(now, s["spun"]) > 80:
        s["spun"] = now                                # the digits spin while the shaker moves
        display.number(sum(roll() for _ in range(s["dice"])))
