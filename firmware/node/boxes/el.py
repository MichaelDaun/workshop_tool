# Strömkretsen (nod-01): lysdiod, ratt och strömsensor.
import time
from machine import ADC, I2C, PWM, Pin
from delar import INA219

led = PWM(Pin(15))
led.freq(1000)
pot = ADC(26)
ina = None
s = {"pot": -1.0, "poff": 0, "matt": 0}


def ljus(v):
    # ögat uppfattar inte ljus linjärt, så skärmens värde böjs av
    led.duty_u16(int(65535 * max(0.0, min(1.0, v)) ** 2.2))


def ny_led(d):
    ljus(float(d.get("pwm", 0)))


def poff(_):
    s["poff"] = time.ticks_add(time.ticks_ms(), 1000)


def starta(nod):
    global ina
    nod.har = ["led", "pot", "ina219"]
    try:
        ina = INA219(I2C(0, sda=Pin(4), scl=Pin(5)))
    except OSError:
        nod.har.remove("ina219")
    nod.lyssna("led", ny_led)
    nod.lyssna("poff", poff)
    ljus(0)


def varv(nod):
    nu = time.ticks_ms()
    if s["poff"]:
        if time.ticks_diff(s["poff"], nu) > 0:
            ljus((nu // 60) % 2)
            return
        s["poff"] = 0
        ljus(0)

    v = round(pot.read_u16() / 65535, 2)
    if abs(v - s["pot"]) >= 0.02:
        s["pot"] = v
        nod.skicka("in/pot", {"v": v})

    if ina and time.ticks_diff(nu, s["matt"]) > 500:
        s["matt"] = nu
        # PWM gör att strömmen hoppar, så ta medel av 20 mätningar
        mA = sum(ina.mA() for _ in range(20)) / 20
        nod.skicka("in/strom", {"mA": round(mA, 1)})
