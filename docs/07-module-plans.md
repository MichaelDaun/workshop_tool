# 7. Module plans

Problem, tasks and box for each workshop. Mockups are in `mockups/modules/`, firmware in
`firmware/`. Task texts are quoted in English; the Swedish originals are in the mockups. Prices are
rough unit prices, autumn 2026.

## Common

**Standard node** (about 200 kr): Raspberry Pi Pico W, 5 V power bank, an enclosure with the node
id on the lid, the Pico's own LED as the status light. Every box runs `firmware/node/` and differs
only in its file under `boxes/`. The sound box is the exception and runs C++.

**Network:** a 2.4 GHz travel router. The room server runs Mosquitto and bridges to WebSocket for
the browsers, so no participant can drive a box directly.

```text
verkstan/<room>/<node>/hello      {"parts": [...], "fw": "0.3"}   retained
verkstan/<room>/<node>/status     "up" / "gone"                   retained, last will
verkstan/<room>/<node>/in/<x>     from the box
verkstan/<room>/<node>/out/<x>    to the box; out/find blinks the status light for 3 s
```

**Rules:** 5 V at most. Every on-screen task works without a box. What breaks on screen does not
break for real. A box must survive 75 people.

**Task shape:** three tasks. Tasks 1 and 2 are on screen and need the team to decide something.
Task 3 runs on the box.

---

## Electricity

### The circuit, ”Exakt en ampere” (`node-01`, `boxes/circuit.py`)

| Task | Done when |
|---|---|
| Get exactly 1 A through the bulb. | Switch closed, 0.95–1.05 A |
| Do the same with 6 batteries. | 6 batteries, 0.95–1.05 A |
| With 4 batteries: work out the resistance for 1 A before you flip the switch. | 1 A at the moment the switch closes |
| The LED on the box takes 20 mA. Make it as bright as it can be. | Box reads 19–20 mA |

The bulb has 3 Ω and breaks above 8 W. The team has to calculate in task 3, since trying values
with the switch closed does not count.

Box (about 75 kr): 5 V from VBUS through the INA219, a 100 Ω resistor, a 500 Ω potentiometer wired
as a variable resistor and a red LED. The Pico only measures: I = (5 V − 2 V) ÷ (100 Ω + R), so the
knob covers 5–30 mA. Over 20 mA the display blinks.

| Part | Pins |
|---|---|
| INA219 SDA / SCL | GP4 / GP5 |
| TM1637 CLK / DIO | GP2 / GP3 |

`in/current {"mA": 19.6}`

### The torch, ”En ficklampa för natten” (`node-11`, `boxes/torch.py`)

| Task | Done when |
|---|---|
| Make both bulbs shine as brightly as they can. | Batteries in series, bulbs in parallel |
| Build a torch that lasts at least 8 hours with both bulbs. | Both lit and at least 8 h |
| Wire the same torch on the box. | The box wiring matches the screen and lasts at least 8 h |

Box (about 155 kr): a build board with two AA holders, two 2.5 V bulbs in holders, leads with
crocodile clips and an INA219 in the supply line. The firmware reads volts and current, works out
series or parallel from the voltage and shows hours on the display.

| Part | Pins |
|---|---|
| INA219 SDA / SCL | GP4 / GP5 |
| TM1637 CLK / DIO | GP2 / GP3 |

`in/power {"V": 1.48, "mA": 310, "h": 12.9}`

### What uses most?, ”Vad kostar en kopp te?” (`plug-01`, no firmware)

| Task | Done when |
|---|---|
| Find something that draws little but costs more per year than the kettle. | The fridge, the router or the TV on standby |
| Boil half a litre of water on the box using less than 60 Wh. | A boil under 60 Wh (lid on) |
| What does a cup of tea a day cost over a year? A cup is 250 ml. | Answer within 25 % of the measured cost |

Box (about 500 kr): a Shelly Plus Plug S and a kettle. No home-built 230 V. Set the plug's MQTT
prefix to `verkstan/<room>/plug-01`; it publishes `status/switch:0` with `apower` (W) and
`aenergy.total` (Wh). The room server translates these to `in/power {"W": …, "Wh": …}`.

## Digital logic

### Logic gates, ”Tre lampor, tre regler” (`node-02`, `boxes/gates.py`)

| Task | Done when |
|---|---|
| The safe should open only when both guards turn their key. | AND, all four combinations tried |
| The stair light should switch on and off from either switch. | XOR, all four combinations tried |
| The lamp on the box should stay on until someone presses a button. | NOR on the box, all four combinations tried |

Gates to choose from: AND, OR, XOR, NOR, NOT. The box applies the gate itself, so it keeps working
if the network drops.

Box (about 70 kr): two arcade buttons and one LED.

| Part | Pins |
|---|---|
| Button A / B | GP14 / GP13 |
| LED with 220 Ω | GP16 |

`out/gate {"type": "nor"}`, `in/buttons {"a": true, "b": false}`

### Eight lamps, ”Rummet räknar binärt” (`node-08`, `boxes/binary.py`)

| Task | Done when |
|---|---|
| Show 100. | 64 + 32 + 4 |
| Count from 0 to 15 without skipping a number. | Each number from 0 to 15 in order |
| Write the team's initials on the box screen. | At least two different letters sent |

In a room, eight people each hold up a phone as one bit. The team splits the bits between them.

Box (about 110 kr): eight LEDs, eight buttons, a send button and a 128 × 64 OLED. Send shows the
byte as a letter (65 = A).

| Part | Pins |
|---|---|
| LEDs, 128 to 1 | GP2–GP9 |
| Buttons, 128 to 1 | GP10–GP17 |
| Send | GP18 |
| SSD1306 SDA / SCL | GP20 / GP21 |

`out/bits {"v": 72}`, `in/bits {"v": 72}`, `in/sent {"v": 65, "text": "MA"}`

## Signals

### Sound waves, ”Härma ett ljud” (`node-03`, `firmware/node03_sound/`)

| Task | Done when |
|---|---|
| Lay wave A exactly on the grey wave. | 330 Hz and amplitude 0.6 |
| Make it completely silent without turning off wave A. | Wave B equal and 180° out of phase |
| Whistle into the box microphone. Play the same note back through the box. | Within 3 % of the whistle |

Best on a computer. Box (about 210 kr): PAM8302 amplifier, 8 Ω speaker, MAX9814 microphone, a bar of
8 WS2812. The app finds the pitch from the samples.

| Part | Pins |
|---|---|
| Speaker (PWM audio) | GP18 |
| Microphone | GP26 |
| LED bar | GP22 |

`out/waves {"fa": 330, "aa": 0.6, "fb": 330, "ab": 0.6, "phase": 180, "playing": true}`,
`in/mic {"hz": 8000, "samples": [...]}`

### Pixels, ”En bild är tal” (`node-09`, `boxes/pixels.py`)

| Task | Done when |
|---|---|
| Turn the sun green by changing the numbers. | Every sun pixel green |
| The box accepts 200 numbers at most. Make the picture as sharp as you can. | 8 × 8 (192 numbers) |
| Draw the team's symbol on the box lamps. | At least 8 pixels changed at 8 × 8 |

Box (about 80 kr): an 8 × 8 WS2812 matrix. The same box serves Sorting.

| Part | Pins |
|---|---|
| Matrix | GP22 |

`out/image {"px": "rrggbb" × 64}`

## AI

### The fruit sorter, ”Lär en maskin att sortera” (`node-04`, `boxes/fruit.py`)

| Task | Done when |
|---|---|
| Get the machine to guess right five times in a row. | Five right in a row |
| Fool it into calling a red apple a lemon. | Examples placed so a red apple is classed as lemon |
| Sort real fruit with the box, five right in a row. | Five right in a row on the scale |

The mystery fruit is a third each green apples, lemons and red apples, so colour alone does not
work.

Box (about 230 kr): TCS34725 colour sensor, 1 kg load cell with an HX711, SG90 servo flap, a button
that marks a fruit as a teaching example.

| Part | Pins |
|---|---|
| HX711 DT / SCK | GP16 / GP17 |
| TCS34725 SDA / SCL | GP4 / GP5 |
| Servo | GP15 |
| Button | GP14 |

`in/fruit {"x": 0.82, "y": 0.4, "example": true}`, `out/flap {"to": "apple"}`

### Next word, ”Gissa nästa ord” (`node-12`, `boxes/nextword.py`)

| Task | Done when |
|---|---|
| Build a sentence that is not in the machine's text. | A finished sentence of at least 3 words not in the text |
| Teach the machine so that Most likely writes ”katten sover i solen”. | Most likely produces the sentence with no ties |
| Show that sentence on the box. | Sent after task 2 |

Box (about 70 kr): four MAX7219 8 × 8 matrices in a row. The built-in font is ASCII, so å, ä and ö
show as a, a and o.

| Part | Pins |
|---|---|
| SPI0 SCK / MOSI / CS | GP18 / GP19 / GP17 |

`out/text {"text": "katten sover i solen"}`, `in/shown {"text": …}`

## Networks

### Packet tour, ”Ett nät som håller” (`node-05`, `boxes/packets.py`)

| Task | Done when |
|---|---|
| Cut Gus off from everyone else with as few cuts as possible. | G unreachable after exactly 2 cuts |
| Cut 4 cables so that everyone can still reach everyone. | 4 cuts and the network still connected |
| Unplug 4 cables on the box and still send a message from Ali to Gus. | 4 jumpers out and every packet arrives |

Box (about 250 kr): seven houses on a board, ten cables of LED strip with six LEDs each, a jumper on
each cable. At 20 % brightness, since 60 LEDs at full draw more than 3 A.

| Part | Pins |
|---|---|
| LED strip | GP22 |
| Jumpers, cable 0–9 | GP2–GP11 |

`in/cables {"cut": [3, 7]}`, `out/packet {"cable": 3, "from": "D", "t": 0.4}`

### Secret colours, ”En hemlighet i det öppna” (`node-13`, `boxes/secret.py`)

| Task | Done when |
|---|---|
| Agree on a colour with your friend without the eavesdropper working it out. | Both mixed, the eavesdropper fails |
| Pick a secret colour that lets the eavesdropper succeed. | A secret equal to the public colour |
| Open the chest on the box with your shared colour. | The chest opens |

Colours mix as paint: the geometric mean per channel. The chest is the friend. It picks the public
colour and its own secret, sends its mix, and computes the shared colour from the team's mix:
shared = (team mix² · secret)^⅓.

Box (about 135 kr): a small chest with an SG90 servo lock and a common-cathode RGB LED.

| Part | Pins |
|---|---|
| Servo | GP15 |
| RGB LED R / G / B, 220 Ω each | GP10 / GP11 / GP12 |

`in/public {"colour": "blue", "mix": [99, 150, 224]}`, `out/mix {"rgb": [...]}`,
`out/open {"rgb": [...]}`, `in/chest {"open": true}`, `out/start {}`

## Software

### The robot's path, ”Programmera roboten” (`node-06`, `boxes/robot.py`)

| Task | Done when |
|---|---|
| Reach the star on level 3 with five blocks at most. | Star reached with ≤ 5 blocks |
| Level 4: one person sees the course and describes it. The others build the program without looking. | Star reached with the course hidden |
| Run level 3 on the real robot so that it stops on the star. | Star reached on the box |

Box (about 230 kr): two 28BYJ-48 steppers with ULN2003 drivers, 60 mm wheels, a bumper, a floor mat
of 7 × 5 squares of 15 cm printed with level 3.

| Part | Pins |
|---|---|
| Left motor | GP2–GP5 |
| Right motor | GP6–GP9 |
| Bumper | GP14 |

`out/program {"steps": ["fwd", "fwd", "left", …]}`, `in/step {"i": 3}`, `in/bump {"i": 4}`

### Sorting, ”Sortera som en dator” (`node-09`, `boxes/pixels.py`)

| Task | Done when |
|---|---|
| Sort 8 cards by hand with 20 comparisons at most. | Sorted with ≤ 20 comparisons |
| Show that merge sort wins by more the more cards there are. | Both methods run at 8 and 64 cards |
| Run the fastest method on the box lamps. | Bubble then merge on the box, merge faster |

The same matrix as Pixels, drawn as eight bars.

`out/bars {"v": [3, 1, 8, 2, 7, 5, 4, 6], "compare": [2, 3]}`

## Mathematics

### The function machine, ”Vad gör maskinen?” (`node-07`, `boxes/function.py`)

| Task | Done when |
|---|---|
| Crack machines 1 and 2 with three tests each at most. | Both cracked within three tests |
| Crack machine 4. | a = 3, b = −2 |
| Set a secret rule in the box for another team. | Any rule other than x |

Box (about 160 kr): KY-040 knob for x, two TM1637 displays for in and out, a lid on a servo. With a
rule set, the box computes a·x + b itself and works as a machine for the next team.

| Part | Pins |
|---|---|
| Knob CLK / DT / SW | GP10 / GP11 / GP12 |
| Display in CLK / DIO | GP2 / GP3 |
| Display out CLK / DIO | GP4 / GP5 |
| Servo | GP15 |

`out/rule {"a": 3, "b": -2}`, `out/lid {"open": true}`, `in/test {"x": 4, "y": 10}`

### Dice, ”Slumpen blir en kurva” (`node-10`, `boxes/dice.py`)

| Task | Done when |
|---|---|
| Guess which total comes up most with two dice. Then roll 100 times. | Guess made before rolling, 100 rolls |
| Roll one die until the bars are nearly level. | At least 60 rolls, lowest bar over 75 % of the highest |
| Shake the box die 20 times. | 20 shakes on the box |

”The whole room rolls” adds 75 rolls. Box (about 80 kr): a shaker with an MPU6050 and a TM1637.

| Part | Pins |
|---|---|
| MPU6050 SDA / SCL | GP4 / GP5 |
| TM1637 CLK / DIO | GP2 / GP3 |

`out/dice {"n": 2}`, `in/roll {"v": [3, 4], "sum": 7}`

## Budget

| Box | Cost |
|---|---|
| node-01 The circuit | 275 kr |
| node-11 The torch | 355 kr |
| plug-01 What uses most? | 500 kr |
| node-02 Logic gates | 270 kr |
| node-08 Eight lamps | 310 kr |
| node-03 Sound waves | 410 kr |
| node-09 Pixels and Sorting | 280 kr |
| node-04 The fruit sorter | 430 kr |
| node-12 Next word | 270 kr |
| node-05 Packet tour | 450 kr |
| node-13 Secret colours | 335 kr |
| node-06 The robot's path | 430 kr |
| node-07 The function machine | 360 kr |
| node-10 Dice | 280 kr |
| Travel router | 400 kr |
| One set | about 5 400 kr |

## Build order

1. node-02 and node-01: the simplest, and they test the node, MQTT and the room server.
2. node-09: one box for two workshops.
3. node-05 and node-06: the most visible in a room.
4. The rest.

## Open questions

1. Who builds the boxes, and how are they repaired on site?
2. Over-the-air updates: `mpremote` over wifi or a home-built loader?
3. Can the room server run on the travel router itself?
