# Firmware

Ingenting här har körts på en riktig Pico W. Lådfilerna är provkörda mot låtsade stift på en
dator och ljudlådan kompilerar mot stubbar. Räkna med att rätta saker vid första provet.

```text
verkstan_nod/          MicroPython, alla lådor utom nod-03
  main.py              startar noden
  nod.py               wifi, MQTT, statuslampa, "Hitta"
  delar.py             knapp, servo, vred, stegmotor, TM1637, HX711, INA219, TCS34725, MPU6050
  config_exempel.py    kopiera till config.py
  lador/               en fil per låda: el, logik, ai, natverk, robot, matte, binart, pixlar, tarning
nod03_ljud/            C++ för Arduino-Pico, ljudlådan
```

## MicroPython

1. Flasha MicroPython för Pico W.
2. `mpremote mip install umqtt.simple`
3. Kopiera `config_exempel.py` till `config.py` och fyll i.
4. `mpremote cp -r verkstan_nod/* :`
5. Lyssna på datorn: `mosquitto_sub -v -t 'verkstan/#'`

En ny låda är en fil i `lador/` med `starta(nod)` och `varv(nod)`. `nod.lyssna("sak", f)` tar emot
`ut/sak`, `nod.skicka("in/sak", {...})` skickar.

## Ljudlådan

Arduino IDE med kortet Raspberry Pi Pico W (earlephilhower) och biblioteken PubSubClient,
ArduinoJson 7 och Adafruit NeoPixel. Kopiera `config_exempel.h` till `config.h`.

Stift och meddelanden för varje låda står i `docs/07-modulplaner.md`.
