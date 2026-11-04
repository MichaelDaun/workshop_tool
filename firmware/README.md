# Firmware

None of this has run on a real Pico W yet. The box files have been run against fake pins on a
computer, and the sound box compiles against stubs. Expect fixes at the first real test.

```text
node/                 MicroPython, every box except node-03
  main.py             starts the node with the box named in config.py
  node.py             wifi, MQTT, status light, find
  parts.py            Button, Servo, Knob, Stepper, TM1637, MAX7219, HX711, INA219, TCS34725, MPU6050
  config_example.py   copy to config.py
  boxes/              one file per box
node03_sound/         C++ for Arduino-Pico, the sound box
```

| Box | File |
|---|---|
| node-01 | `circuit` |
| node-02 | `gates` |
| node-04 | `fruit` |
| node-05 | `packets` |
| node-06 | `robot` |
| node-07 | `function` |
| node-08 | `binary` |
| node-09 | `pixels` (also Sorting) |
| node-10 | `dice` |
| node-11 | `torch` |
| node-12 | `nextword` |
| node-13 | `secret` |

plug-01 is a Shelly Plus Plug S with its own firmware; see `docs/07-module-plans.md`.

## MicroPython

1. Flash MicroPython for the Pico W.
2. `mpremote mip install umqtt.simple` (and `ssd1306` for node-08).
3. Copy `config_example.py` to `config.py` and fill it in.
4. `mpremote cp -r node/* :`
5. Listen on a computer: `mosquitto_sub -v -t 'verkstan/#'`

A new box is a file in `boxes/` with `setup(node)` and `loop(node)`. `node.on("x", fn)` receives
`out/x`, `node.send("x", {...})` publishes to `in/x`.

## The sound box

Arduino IDE with the Raspberry Pi Pico W board (earlephilhower) and the libraries PubSubClient,
ArduinoJson 7 and Adafruit NeoPixel. Copy `config_example.h` to `config.h`.

Pins and messages for every box are in `docs/07-module-plans.md`.
