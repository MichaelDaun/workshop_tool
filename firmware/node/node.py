# Det alla lådor delar: wifi, MQTT, statuslampa och "Hitta".
import json
import time
import network
from machine import Pin, unique_id
from umqtt.simple import MQTTClient


class Nod:
    def __init__(self, config):
        self.c = config
        self.bas = "verkstan/%s/%s/" % (config.RUM, config.NOD)
        self.lampa = Pin(config.STATUSLAMPA, Pin.OUT)
        self.lyssnare = {}
        self.har = []
        self.hitta_till = 0
        self.mqtt = None

    def blinka(self, ggr=1, ms=120):
        for _ in range(ggr):
            self.lampa.on(); time.sleep_ms(ms)
            self.lampa.off(); time.sleep_ms(ms)

    def _lampa_varv(self):
        nu = time.ticks_ms()
        if time.ticks_diff(self.hitta_till, nu) > 0:
            self.lampa.value((nu // 250) % 2)
        else:
            self.lampa.on()

    def _wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            wlan.connect(self.c.WIFI_NAMN, self.c.WIFI_LOSEN)
            for _ in range(40):
                if wlan.isconnected():
                    break
                self.blinka(1, 60)
                time.sleep_ms(250)
        if not wlan.isconnected():
            raise OSError("ingen wifi")

    def _mqtt(self):
        klient = self.c.NOD + "-" + "".join("%02x" % b for b in unique_id()[-3:])
        m = MQTTClient(klient, self.c.SERVER, keepalive=30)
        m.set_last_will(self.bas + "status", "borta", retain=True)
        m.set_callback(self._ta_emot)
        m.connect()
        m.publish(self.bas + "status", "uppe", retain=True)
        m.publish(self.bas + "hej", json.dumps({"har": self.har, "fw": "0.2"}), retain=True)
        m.subscribe(self.bas + "ut/#")
        self.mqtt = m

    def _ta_emot(self, amne, data):
        sak = amne.decode()[len(self.bas):]
        try:
            innehall = json.loads(data) if data else {}
        except ValueError:
            return
        if sak == "ut/hitta":
            self.hitta_till = time.ticks_add(time.ticks_ms(), 3000)
        elif sak in self.lyssnare:
            self.lyssnare[sak](innehall)

    def lyssna(self, sak, funktion):
        """funktion(innehall) körs när rumsservern skickar till ut/<sak>."""
        self.lyssnare["ut/" + sak] = funktion

    def skicka(self, sak, innehall):
        if self.mqtt:
            self.mqtt.publish(self.bas + sak, json.dumps(innehall))

    def kor(self, lada):
        lada.starta(self)
        while True:
            try:
                self._wifi()
                self._mqtt()
                while True:
                    self.mqtt.check_msg()
                    lada.varv(self)
                    self._lampa_varv()
                    time.sleep_ms(10)
            except OSError:
                self.mqtt = None
                self.blinka(3)
                time.sleep(2)
