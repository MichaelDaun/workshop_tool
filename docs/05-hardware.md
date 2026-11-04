# 5. Hardware

A lamp on a screen is a picture. An LED on the box that the team drives to exactly its limit shows
that the numbers are real. A team also gathers around an object and argues about it.

| Direction | Example |
|---|---|
| Screen → box | The team's program drives the robot |
| Box → screen | The box measures the current and the app shows it |
| Twin | Box and screen show the same state |

## The Verkstan node

One standard node per box: a Raspberry Pi Pico W with the workshop's parts, a power bank and the
node id on the lid. At start it announces its parts, for example `{"parts": ["ina219", "display"]}`.
The leader pairs a node with a workshop under Lådor in the room view.

## How the node talks to the app

| Route | Works with | Drawback |
|---|---|---|
| Wifi and MQTT to the room server | Everything, iPhone too | Needs a server and its own network |
| Web Serial | Chrome and Edge on a computer | Not iPhone or Firefox |
| Web Bluetooth | Chrome on a computer and Android | Not iPhone |

Chosen: wifi and MQTT (Mosquitto) on the room server, which bridges to WebSocket. Browsers never
reach a node directly. Topics and messages are in [document 7](07-module-plans.md).

The firmware is MicroPython, so the code can be shown to participants. The sound box runs C++.

## Formats

| Format | Boxes | Suits |
|---|---|---|
| Station | 1 per workshop | Teams rotate, 20–40 people |
| Team kit | 1 per team | Most boxes, every team finishes on hardware |

## Constraints

- iPhone has neither Web Serial nor Web Bluetooth, so everything goes through the server.
- The Pico W only does 2.4 GHz and not eduroam. A travel router solves it.
- 5 V at most. Power banks, never loose lithium cells.
- 75 people press hard. Arcade buttons and screw terminals.
- With 20 boxes, over-the-air updates are needed.
- Every on-screen task works without a box.

## More ideas

- Conductor or insulator: two probes, try paper clips, rubbers or a lemon.
- Gate boxes wired together into an adder.
- A theremin: a distance sensor sets the pitch.
- A wand with an accelerometer that learns gestures.
- Program cards with NFC tags laid out in front of a reader.
