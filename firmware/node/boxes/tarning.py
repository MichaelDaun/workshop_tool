# Tärningar (nod-10): en skakburk med accelerometer och en display.
import os
import time
from machine import I2C, Pin
from delar import MPU6050, TM1637

visa = TM1637(2, 3)
acc = None
SKAK = 0.6                       # g utöver tyngdkraften
s = {"antal": 1, "skakar": 0, "tyst": 0, "rullar": 0}


def slag():
    return 1 + os.urandom(1)[0] % 6


def nytt_antal(d):
    s["antal"] = max(1, min(3, int(d.get("antal", 1))))


def starta(nod):
    global acc
    nod.har = ["acc", "display"]
    acc = MPU6050(I2C(0, sda=Pin(4), scl=Pin(5)))
    nod.lyssna("tarningar", nytt_antal)
    visa.tal(None)


def varv(nod):
    x, y, z = acc.acc()
    nu = time.ticks_ms()
    if abs((x * x + y * y + z * z) ** 0.5 - 1) > SKAK:
        s["skakar"] += 1
        s["tyst"] = nu
    elif time.ticks_diff(nu, s["tyst"]) > 300:
        if s["skakar"] >= 3:
            kast = [slag() for _ in range(s["antal"])]
            visa.tal(sum(kast))
            nod.skicka("in/kast", {"v": kast, "sum": sum(kast)})
        s["skakar"] = 0
        return
    if s["skakar"] >= 3 and time.ticks_diff(nu, s["rullar"]) > 80:
        s["rullar"] = nu                               # siffrorna snurrar medan burken skakas
        visa.tal(sum(slag() for _ in range(s["antal"])))
