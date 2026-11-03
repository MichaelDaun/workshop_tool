# Funktionsmaskinen (nod-07): vred, två displayer och ett lock.
from delar import TM1637, Servo, Vred

vred = Vred(10, 11, 12)
visa_in = TM1637(2, 3)
visa_ut = TM1637(4, 5)
lock = Servo(15)
s = {"x": 0}


def visa(d):
    if "in" in d:
        s["x"] = int(d["in"])
        visa_in.tal(s["x"])
    visa_ut.tal(d.get("ut"))


def ny_lock(d):
    lock.vinkel(100 if d.get("oppen") else 0)


def starta(nod):
    nod.har = ["vred", "display_in", "display_ut", "lock"]
    nod.lyssna("visa", visa)
    nod.lyssna("lock", ny_lock)
    visa_in.tal(0)
    visa_ut.tal(None)
    lock.vinkel(0)


def varv(nod):
    steg = vred.ta()
    if steg:
        s["x"] = max(-99, min(999, s["x"] + steg))
        visa_in.tal(s["x"])
        visa_ut.tal(None)
    if vred.knapp.tryckt():
        nod.skicka("in/tal", {"x": s["x"]})
