# Verkstan

Technology workshops for people with no technical background. Fifteen workshops in seven areas:
electricity, digital logic, signals, AI, networks, software and mathematics. Teams of 2–4 solve one
problem per workshop, first on screen and then on a physical box.

Status: clickable mockups and draft firmware. The UI is Swedish with English as a second language.
Everything else in the repository is English.

## Try it

Open `mockups/index.html`, or:

```bash
cd mockups && python3 -m http.server 8000
```

| Area | Workshops |
|---|---|
| Electricity | [The circuit](mockups/modules/circuit.html), [The torch](mockups/modules/torch.html), [What uses most?](mockups/modules/energy.html) |
| Digital logic | [Logic gates](mockups/modules/gates.html), [Eight lamps](mockups/modules/binary.html) |
| Signals | [Sound waves](mockups/modules/waves.html), [Pixels](mockups/modules/pixels.html) |
| AI | [The fruit sorter](mockups/modules/fruit.html), [Next word](mockups/modules/nextword.html) |
| Networks | [Packet tour](mockups/modules/packets.html), [Secret colours](mockups/modules/secret.html) |
| Software | [The robot's path](mockups/modules/robot.html), [Sorting](mockups/modules/sorting.html) |
| Mathematics | [The function machine](mockups/modules/function.html), [Dice](mockups/modules/dice.html) |

Also the [room view](mockups/room.html) for the workshop leader and the
[design manual](mockups/design.html). Plain HTML, CSS and JS with no build step. The boxes are
simulated in the mockups; their firmware is in [`firmware/`](firmware/).

## Documents

1. [Vision](docs/01-vision.md)
2. [Exercise bank](docs/02-exercise-bank.md)
3. [Architecture](docs/03-architecture.md)
4. [AI-authored modules](docs/04-ai-authored-modules.md)
5. [Hardware](docs/05-hardware.md)
6. [Design manual](docs/06-design-manual.md)
7. [Module plans](docs/07-module-plans.md): tasks, parts, pins and messages per workshop

An AI writing modules reads [AGENTS.md](AGENTS.md) first.

## GitHub Pages

`.github/workflows/pages.yml` publishes `mockups/` on every push to `main`. Turn it on under
Settings → Pages → Source: GitHub Actions.
