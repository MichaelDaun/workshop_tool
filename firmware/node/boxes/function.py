# node-07, The function machine. A knob for x, an input and an output display, and a lid on a servo.
# The team sends a rule a·x + b. The box then works as a machine for another team to crack.
from parts import TM1637, Servo, Knob

knob = Knob(10, 11, 12)
show_in = TM1637(2, 3)
show_out = TM1637(4, 5)
lid = Servo(15)
s = {"x": 0, "a": None, "b": None}


def rule(d):
    s["a"], s["b"] = int(d.get("a", 1)), int(d.get("b", 0))
    lid.angle(0)
    show_out.number(None)


def set_lid(d):
    lid.angle(100 if d.get("open") else 0)


def setup(node):
    node.parts = ["knob", "display_in", "display_out", "lid"]
    node.on("rule", rule)
    node.on("lid", set_lid)
    show_in.number(0)
    show_out.number(None)
    lid.angle(0)


def loop(node):
    steps = knob.take()
    if steps:
        s["x"] = max(-99, min(999, s["x"] + steps))
        show_in.number(s["x"])
        show_out.number(None)
    if knob.button.pressed():
        y = None if s["a"] is None else s["a"] * s["x"] + s["b"]
        show_out.number(y)
        node.send("test", {"x": s["x"], "y": y})
