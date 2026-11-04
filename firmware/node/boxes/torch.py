# node-11, The torch. A build board with two AA holders, two bulbs and an INA219 in the supply line.
# The team wires it with leads. The display shows how many hours the batteries last with that wiring.
import time
from machine import I2C, Pin
from parts import INA219, TM1637

CELL_MAH = 2000                  # one AA cell
display = TM1637(2, 3)
ina = None
s = {"measured": 0}


def hours(volts, mA):
    if mA < 5:
        return None
    # two cells in series give about 3 V, in parallel 1.5 V with twice the capacity
    cap = CELL_MAH if volts > 2.2 else 2 * CELL_MAH
    return cap / mA


def setup(node):
    global ina
    node.parts = ["ina219", "display"]
    ina = INA219(I2C(0, sda=Pin(4), scl=Pin(5)))
    display.number(None)


def loop(node):
    now = time.ticks_ms()
    if time.ticks_diff(now, s["measured"]) < 500:
        return
    s["measured"] = now
    v, mA = ina.volts(), ina.mA()
    h = hours(v, mA)
    display.number(None if h is None else min(999, round(h)))
    node.send("power", {"V": round(v, 2), "mA": round(mA), "h": None if h is None else round(h, 1)})
