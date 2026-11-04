# Small drivers for the parts in the boxes.
# The OLED in node-08 uses the standard ssd1306 module (mpremote mip install ssd1306).
import time
import framebuf
from machine import Pin, PWM, disable_irq, enable_irq


def s16(high, low):
    v = high << 8 | low
    return v - 0x10000 if v & 0x8000 else v


class Button:
    """Button to GND with the internal pull-up."""

    def __init__(self, pin):
        self.p = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.down = False
        self.t = 0

    def pressed(self):
        """True once per press, debounced."""
        now, v = time.ticks_ms(), not self.p.value()
        if v != self.down and time.ticks_diff(now, self.t) > 20:
            self.down, self.t = v, now
            return v
        return False


class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)

    def angle(self, degrees):
        self.pwm.duty_u16(int((0.5 + 2 * degrees / 180) / 20 * 65535))

    def release(self):
        self.pwm.duty_u16(0)


class Knob:
    """KY-040 rotary encoder with a push button. Read on interrupts so no steps are lost."""

    def __init__(self, clk, dt, button):
        self.clk = Pin(clk, Pin.IN, Pin.PULL_UP)
        self.dt = Pin(dt, Pin.IN, Pin.PULL_UP)
        self.button = Button(button)
        self.steps = 0
        self.clk.irq(self._irq, Pin.IRQ_FALLING)

    def _irq(self, _):
        self.steps += 1 if self.dt.value() else -1

    def take(self):
        s, self.steps = self.steps, 0
        return s


class Stepper:
    """28BYJ-48 on a ULN2003, half steps. 4096 steps per turn."""
    SEQ = ((1, 0, 0, 0), (1, 1, 0, 0), (0, 1, 0, 0), (0, 1, 1, 0),
           (0, 0, 1, 0), (0, 0, 1, 1), (0, 0, 0, 1), (1, 0, 0, 1))

    def __init__(self, pins):
        self.p = [Pin(x, Pin.OUT, value=0) for x in pins]
        self.i = 0

    def step(self, direction):
        self.i = (self.i + direction) % 8
        for p, v in zip(self.p, self.SEQ[self.i]):
            p.value(v)

    def off(self):
        for p in self.p:
            p.value(0)


class TM1637:
    """Four-digit seven-segment display."""
    DIGITS = b"\x3f\x06\x5b\x4f\x66\x6d\x7d\x07\x7f\x6f"
    MINUS = 0x40

    def __init__(self, clk, dio, brightness=3):
        self.clk = Pin(clk, Pin.OUT, value=1)
        self.dio = Pin(dio, Pin.OUT, value=1)
        self.brightness = brightness

    def _byte(self, b):
        for i in range(8):
            self.dio((b >> i) & 1)
            time.sleep_us(5)
            self.clk(1); time.sleep_us(5); self.clk(0); time.sleep_us(5)
        self.clk(1); time.sleep_us(5); self.clk(0); time.sleep_us(5)

    def _start(self):
        self.dio(0); time.sleep_us(5); self.clk(0); time.sleep_us(5)

    def _stop(self):
        self.dio(0); time.sleep_us(5); self.clk(1); time.sleep_us(5); self.dio(1)

    def segments(self, seg):
        self._start(); self._byte(0x40); self._stop()
        self._start(); self._byte(0xC0)
        for s in seg:
            self._byte(s)
        self._stop()
        self._start(); self._byte(0x88 | self.brightness); self._stop()

    def number(self, n):
        """Show an integer, or four dashes for None."""
        if n is None:
            return self.segments(bytes([self.MINUS] * 4))
        t = "%4d" % max(-999, min(9999, int(n)))
        self.segments(bytes(0 if c == " " else self.MINUS if c == "-" else self.DIGITS[int(c)] for c in t))


class MAX7219:
    """A chain of 8 × 8 LED matrices, drawn through framebuf."""

    def __init__(self, spi, cs, modules=4, brightness=2):
        self.spi, self.cs, self.n = spi, Pin(cs, Pin.OUT, value=1), modules
        self.buf = bytearray(8 * modules)
        self.fb = framebuf.FrameBuffer(self.buf, 8 * modules, 8, framebuf.MONO_HLSB)
        for reg, v in ((0x0C, 0), (0x0F, 0), (0x09, 0), (0x0B, 7), (0x0A, brightness), (0x0C, 1)):
            self._all(reg, v)

    def _all(self, reg, v):
        self.cs(0)
        for _ in range(self.n):
            self.spi.write(bytes([reg, v]))
        self.cs(1)

    def show(self):
        for y in range(8):
            self.cs(0)
            for m in range(self.n):
                self.spi.write(bytes([1 + y, self.buf[y * self.n + m]]))
            self.cs(1)


class HX711:
    """Load cell amplifier. Channel A, gain 128."""

    def __init__(self, dt, sck, scale=420.0):
        self.dt = Pin(dt, Pin.IN)
        self.sck = Pin(sck, Pin.OUT, value=0)
        self.scale = scale            # raw counts per gram, measure with a known weight
        self.zero = 0

    def raw(self):
        t = time.ticks_ms()
        while self.dt():
            if time.ticks_diff(time.ticks_ms(), t) > 200:
                raise OSError("hx711 not answering")
        v = 0
        irq = disable_irq()           # the clock must not stay high for more than 60 µs
        for _ in range(24):
            self.sck(1); self.sck(0)
            v = v << 1 | self.dt()
        self.sck(1); self.sck(0)
        enable_irq(irq)
        return v - (1 << 24) if v & 0x800000 else v

    def tare(self, n=10):
        self.zero = sum(self.raw() for _ in range(n)) / n

    def grams(self):
        return (self.raw() - self.zero) / self.scale


class INA219:
    """Current and voltage sensor. Reads the shunt voltage directly, so no calibration register is needed."""

    def __init__(self, i2c, addr=0x40, shunt=0.1):
        self.i2c, self.addr, self.shunt = i2c, addr, shunt
        i2c.writeto_mem(addr, 0x00, b"\x39\x9f")       # 32 V range, ±320 mV shunt, 12 bit

    def mA(self):
        d = self.i2c.readfrom_mem(self.addr, 0x01, 2)
        return s16(d[0], d[1]) * 0.01 / self.shunt     # 10 µV per count

    def volts(self):
        d = self.i2c.readfrom_mem(self.addr, 0x02, 2)
        return ((d[0] << 8 | d[1]) >> 3) * 0.004       # 4 mV per count


class TCS34725:
    """Colour sensor."""

    def __init__(self, i2c, addr=0x29):
        self.i2c, self.addr = i2c, addr
        self._w(0x01, 0xD5)           # integration time 101 ms
        self._w(0x0F, 0x01)           # gain 4x
        self._w(0x00, 0x01)
        time.sleep_ms(3)
        self._w(0x00, 0x03)

    def _w(self, reg, v):
        self.i2c.writeto_mem(self.addr, 0x80 | reg, bytes([v]))

    def rgbc(self):
        d = self.i2c.readfrom_mem(self.addr, 0xB4, 8)
        c, r, g, b = (d[i] | d[i + 1] << 8 for i in (0, 2, 4, 6))
        return r, g, b, c


class MPU6050:
    """Accelerometer. Returns g along x, y and z."""

    def __init__(self, i2c, addr=0x68):
        self.i2c, self.addr = i2c, addr
        i2c.writeto_mem(addr, 0x6B, b"\x00")

    def acc(self):
        d = self.i2c.readfrom_mem(self.addr, 0x3B, 6)
        return tuple(s16(d[i], d[i + 1]) / 16384 for i in (0, 2, 4))
