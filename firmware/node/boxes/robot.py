# node-06, The robot's path. Two steppers and a bumper. Runs on a mat printed with level 3.
from machine import Timer
from parts import Button, Stepper

SQUARE = 3260                    # half steps for 15 cm with 60 mm wheels
TURN = 1700                      # half steps for 90 degrees, tune on the mat
# direction of the left and right motor; the motors are mirrored
MOVES = {"fwd": (1, -1, SQUARE), "left": (-1, -1, TURN), "right": (1, 1, TURN)}

left = Stepper((2, 3, 4, 5))
right = Stepper((6, 7, 8, 9))
bumper = Button(14)
s = {"queue": [], "i": 0, "job": None, "steps": 0, "done": False}
timer = None


def tick(_):
    j = s["job"]
    if not j:
        return
    left.step(j[0])
    right.step(j[1])
    s["steps"] -= 1
    if s["steps"] <= 0:
        s["job"] = None
        s["done"] = True


def program(d):
    s.update(queue=[x for x in d.get("steps", []) if x in MOVES], i=0, job=None, done=False)


def setup(node):
    global timer
    node.parts = ["motors", "bumper"]
    node.on("program", program)
    timer = Timer(mode=Timer.PERIODIC, freq=900, callback=tick)


def loop(node):
    if bumper.pressed() and (s["job"] or s["queue"]):
        s.update(queue=[], job=None, done=False)
        node.send("bump", {"i": s["i"]})
    if s["done"]:
        s["done"] = False
        node.send("step", {"i": s["i"]})
        s["i"] += 1
    if not s["job"]:
        if s["queue"]:
            m = MOVES[s["queue"].pop(0)]
            s["steps"] = m[2]
            s["job"] = m
        else:
            left.off()           # the coils draw current even when the robot stands still
            right.off()
