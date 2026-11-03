# Små drivrutiner för delarna i lådorna.
import time
from machine import Pin, PWM, disable_irq, enable_irq


def s16(hog, lag):
    v = hog << 8 | lag
    return v - 0x10000 if v & 0x8000 else v


class Knapp:
    """Knapp till GND med intern pull-up."""

    def __init__(self, stift):
        self.p = Pin(stift, Pin.IN, Pin.PULL_UP)
        self.nere = False
        self.t = 0

    def tryckt(self):
        """Sant en gång per nedtryckning."""
        nu, v = time.ticks_ms(), not self.p.value()
        if v != self.nere and time.ticks_diff(nu, self.t) > 20:
            self.nere, self.t = v, nu
            return v
        return False


class Servo:
    def __init__(self, stift):
        self.pwm = PWM(Pin(stift))
        self.pwm.freq(50)

    def vinkel(self, grader):
        self.pwm.duty_u16(int((0.5 + 2 * grader / 180) / 20 * 65535))

    def slapp(self):
        self.pwm.duty_u16(0)


class Vred:
    """KY-040. Läses med avbrott så att inga steg tappas."""

    def __init__(self, clk, dt, knapp):
        self.clk = Pin(clk, Pin.IN, Pin.PULL_UP)
        self.dt = Pin(dt, Pin.IN, Pin.PULL_UP)
        self.knapp = Knapp(knapp)
        self.steg = 0
        self.clk.irq(self._irq, Pin.IRQ_FALLING)

    def _irq(self, _):
        self.steg += 1 if self.dt.value() else -1

    def ta(self):
        s, self.steg = self.steg, 0
        return s


class Stegmotor:
    """28BYJ-48 via ULN2003, halvsteg. 4096 steg per varv."""
    SEKV = ((1, 0, 0, 0), (1, 1, 0, 0), (0, 1, 0, 0), (0, 1, 1, 0),
            (0, 0, 1, 0), (0, 0, 1, 1), (0, 0, 0, 1), (1, 0, 0, 1))

    def __init__(self, stift):
        self.p = [Pin(x, Pin.OUT, value=0) for x in stift]
        self.i = 0

    def steg(self, riktning):
        self.i = (self.i + riktning) % 8
        for p, v in zip(self.p, self.SEKV[self.i]):
            p.value(v)

    def av(self):
        for p in self.p:
            p.value(0)


class TM1637:
    """Fyrsiffrig display."""
    SIFFROR = b"\x3f\x06\x5b\x4f\x66\x6d\x7d\x07\x7f\x6f"
    MINUS = 0x40

    def __init__(self, clk, dio, ljus=3):
        self.clk = Pin(clk, Pin.OUT, value=1)
        self.dio = Pin(dio, Pin.OUT, value=1)
        self.ljus = ljus

    def _byte(self, b):
        for i in range(8):
            self.dio((b >> i) & 1)
            time.sleep_us(5)
            self.clk(1); time.sleep_us(5); self.clk(0); time.sleep_us(5)
        self.clk(1); time.sleep_us(5); self.clk(0); time.sleep_us(5)

    def _start(self):
        self.dio(0); time.sleep_us(5); self.clk(0); time.sleep_us(5)

    def _stopp(self):
        self.dio(0); time.sleep_us(5); self.clk(1); time.sleep_us(5); self.dio(1)

    def segment(self, seg):
        self._start(); self._byte(0x40); self._stopp()
        self._start(); self._byte(0xC0)
        for s in seg:
            self._byte(s)
        self._stopp()
        self._start(); self._byte(0x88 | self.ljus); self._stopp()

    def tal(self, n):
        if n is None:
            return self.segment(bytes([self.MINUS] * 4))
        t = "%4d" % max(-999, min(9999, int(n)))
        self.segment(bytes(0 if c == " " else self.MINUS if c == "-" else self.SIFFROR[int(c)] for c in t))


class HX711:
    """Förstärkare för lastcell. Kanal A, förstärkning 128."""

    def __init__(self, dt, sck, skala=420.0):
        self.dt = Pin(dt, Pin.IN)
        self.sck = Pin(sck, Pin.OUT, value=0)
        self.skala = skala            # råvärde per gram, mät med en känd vikt
        self.noll = 0

    def ra(self):
        t = time.ticks_ms()
        while self.dt():
            if time.ticks_diff(time.ticks_ms(), t) > 200:
                raise OSError("hx711 svarar inte")
        v = 0
        irq = disable_irq()           # klockan får inte vara hög i mer än 60 µs
        for _ in range(24):
            self.sck(1); self.sck(0)
            v = v << 1 | self.dt()
        self.sck(1); self.sck(0)
        enable_irq(irq)
        return v - (1 << 24) if v & 0x800000 else v

    def tarera(self, n=10):
        self.noll = sum(self.ra() for _ in range(n)) / n

    def gram(self):
        return (self.ra() - self.noll) / self.skala


class INA219:
    """Strömsensor. Läser spänningen över shuntmotståndet direkt."""

    def __init__(self, i2c, adr=0x40, shunt=0.1):
        self.i2c, self.adr, self.shunt = i2c, adr, shunt
        i2c.writeto_mem(adr, 0x00, b"\x39\x9f")

    def mA(self):
        d = self.i2c.readfrom_mem(self.adr, 0x01, 2)
        return s16(d[0], d[1]) * 0.01 / self.shunt     # 10 µV per steg


class TCS34725:
    """Färgsensor."""

    def __init__(self, i2c, adr=0x29):
        self.i2c, self.adr = i2c, adr
        self._w(0x01, 0xD5)           # integrationstid 101 ms
        self._w(0x0F, 0x01)           # förstärkning 4x
        self._w(0x00, 0x01)
        time.sleep_ms(3)
        self._w(0x00, 0x03)

    def _w(self, reg, v):
        self.i2c.writeto_mem(self.adr, 0x80 | reg, bytes([v]))

    def rgbc(self):
        d = self.i2c.readfrom_mem(self.adr, 0xB4, 8)
        c, r, g, b = (d[i] | d[i + 1] << 8 for i in (0, 2, 4, 6))
        return r, g, b, c


class MPU6050:
    """Accelerometer. Ger g längs x, y, z."""

    def __init__(self, i2c, adr=0x68):
        self.i2c, self.adr = i2c, adr
        i2c.writeto_mem(adr, 0x6B, b"\x00")

    def acc(self):
        d = self.i2c.readfrom_mem(self.adr, 0x3B, 6)
        return tuple(s16(d[i], d[i + 1]) / 16384 for i in (0, 2, 4))
