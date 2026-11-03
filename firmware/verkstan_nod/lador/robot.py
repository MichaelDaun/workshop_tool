# Robotens väg (nod-06): två stegmotorer och en stötfångare.
from machine import Pin, Timer
from delar import Knapp, Stegmotor

RUTA = 3260                      # halvsteg för 15 cm med 60 mm hjul
SVANG = 1700                     # halvsteg för 90 grader, justera på mattan
# riktning för vänster och höger motor; motorerna sitter spegelvända
RORELSE = {"F": (1, -1, RUTA), "V": (-1, -1, SVANG), "H": (1, 1, SVANG)}

vanster = Stegmotor((2, 3, 4, 5))
hoger = Stegmotor((6, 7, 8, 9))
krock = Knapp(14)
s = {"kvar": [], "i": 0, "jobb": None, "steg": 0, "klar": False}
timer = None


def tick(_):
    j = s["jobb"]
    if not j:
        return
    vanster.steg(j[0])
    hoger.steg(j[1])
    s["steg"] -= 1
    if s["steg"] <= 0:
        s["jobb"] = None
        s["klar"] = True


def nytt_program(d):
    s.update(kvar=[x for x in d.get("steg", []) if x in RORELSE], i=0, jobb=None, klar=False)


def starta(nod):
    global timer
    nod.har = ["motorer", "krock"]
    nod.lyssna("program", nytt_program)
    timer = Timer(mode=Timer.PERIODIC, freq=900, callback=tick)


def varv(nod):
    if krock.tryckt() and (s["jobb"] or s["kvar"]):
        s.update(kvar=[], jobb=None, klar=False)
        nod.skicka("in/krock", {})
    if s["klar"]:
        s["klar"] = False
        nod.skicka("in/steg", {"i": s["i"], "klar": True})
        s["i"] += 1
    if not s["jobb"]:
        if s["kvar"]:
            r = RORELSE[s["kvar"].pop(0)]
            s["steg"] = r[2]
            s["jobb"] = r
        else:
            vanster.av()         # spolarna drar ström även när roboten står still
            hoger.av()
