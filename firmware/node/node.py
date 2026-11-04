# What every box shares: wifi, MQTT, the status LED and "find".
#
# Topics are verkstan/<room>/<node>/...
#   hello      retained, the parts this box has and the firmware version
#   status     retained, "up" or "gone" (last will)
#   in/<x>     box to room server
#   out/<x>    room server to box; out/find blinks the status LED for 3 s
import json
import time
import network
from machine import Pin, unique_id
from umqtt.simple import MQTTClient

FIRMWARE = "0.3"


class Node:
    def __init__(self, config):
        self.c = config
        self.base = "verkstan/%s/%s/" % (config.ROOM, config.NODE)
        self.led = Pin(config.STATUS_LED, Pin.OUT)
        self.handlers = {}
        self.parts = []
        self.find_until = 0
        self.mqtt = None

    def blink(self, times=1, ms=120):
        for _ in range(times):
            self.led.on(); time.sleep_ms(ms)
            self.led.off(); time.sleep_ms(ms)

    def _paint_led(self):
        now = time.ticks_ms()
        if time.ticks_diff(self.find_until, now) > 0:
            self.led.value((now // 250) % 2)
        else:
            self.led.on()

    def _wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            wlan.connect(self.c.WIFI_SSID, self.c.WIFI_PASSWORD)
            for _ in range(40):
                if wlan.isconnected():
                    break
                self.blink(1, 60)
                time.sleep_ms(250)
        if not wlan.isconnected():
            raise OSError("no wifi")

    def _connect(self):
        client = self.c.NODE + "-" + "".join("%02x" % b for b in unique_id()[-3:])
        m = MQTTClient(client, self.c.SERVER, keepalive=30)
        m.set_last_will(self.base + "status", "gone", retain=True)
        m.set_callback(self._receive)
        m.connect()
        m.publish(self.base + "status", "up", retain=True)
        m.publish(self.base + "hello", json.dumps({"parts": self.parts, "fw": FIRMWARE}), retain=True)
        m.subscribe(self.base + "out/#")
        self.mqtt = m

    def _receive(self, topic, data):
        key = topic.decode()[len(self.base):]
        try:
            payload = json.loads(data) if data else {}
        except ValueError:
            return
        if key == "out/find":
            self.find_until = time.ticks_add(time.ticks_ms(), 3000)
        elif key in self.handlers:
            self.handlers[key](payload)

    def on(self, name, fn):
        """Call fn(payload) when the room server publishes to out/<name>."""
        self.handlers["out/" + name] = fn

    def send(self, name, payload):
        """Publish payload as JSON to in/<name>."""
        if self.mqtt:
            self.mqtt.publish(self.base + "in/" + name, json.dumps(payload))

    def run(self, box):
        box.setup(self)
        while True:
            try:
                self._wifi()
                self._connect()
                while True:
                    self.mqtt.check_msg()
                    box.loop(self)
                    self._paint_led()
                    time.sleep_ms(10)
            except OSError:
                self.mqtt = None
                self.blink(3)
                time.sleep(2)
