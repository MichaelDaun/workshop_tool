# node-02, Logic gates. Buttons A and B and one LED.
# The box applies the gate itself, so it keeps working if the network drops.
from machine import Pin
from parts import Button

GATES = {
    "and": lambda a, b: a and b,
    "or": lambda a, b: a or b,
    "xor": lambda a, b: a != b,
    "nor": lambda a, b: not (a or b),
    "not": lambda a, b: not a,
}

button_a, button_b = Button(14), Button(13)
led = Pin(16, Pin.OUT)
s = {"gate": "and", "a": False, "b": False}


def paint():
    led.value(GATES[s["gate"]](s["a"], s["b"]))


def set_gate(d):
    if d.get("type") in GATES:
        s["gate"] = d["type"]
        paint()


def setup(node):
    node.parts = ["button_a", "button_b", "led"]
    node.on("gate", set_gate)
    paint()


def loop(node):
    changed = False
    for name, b in (("a", button_a), ("b", button_b)):
        b.pressed()
        if b.down != s[name]:
            s[name] = b.down
            changed = True
    if changed:
        paint()
        node.send("buttons", {"a": s["a"], "b": s["b"]})
