# 6. Design manual

Covers screens, copy and boxes. The visual version is
[`mockups/design.html`](../mockups/design.html). Part C is the checklist.

## A. What we removed

The first mockups carried the usual marks of AI-generated design:

- capitalised mono labels with letter spacing
- cards in cards with shadows, pill buttons
- decorative pastel circles and confetti
- all seven area colours at once
- green meaning both software and right
- bold lead-ins, exclamation marks, praise and machines speaking in the first person
- triads and slogans
- hints under every task, legends next to pictures that already say it, leads and commentary
- tasks so small that one person could click through them alone

## B. The manual

### The workbench

Verkstan looks like a tidy workbench: a cutting mat with a grid, circuit diagrams, meters and
warning tape. The scene is the bench. Colour shows what is active, everything else is graphite and
paper.

### Workshops and tasks

A workshop is one problem, stated as the h2: ”Exakt en ampere”, ”En ficklampa för natten”. It has
three tasks for a team of 2–4.

1. The core idea on screen.
2. The same idea under a constraint, with a prediction first, or with information only one person
   has.
3. The box does something concrete.

”Vad hände?” is two or three sentences and at most one formula, folded away.

### Colour

| Token | Light | Dark | Use |
|---|---|---|---|
| `--paper` | `#f3f4f1` | `#121514` | Background |
| `--sheet` | `#ffffff` | `#1a1e1d` | Scene, panels |
| `--grid` | `#e4e7e3` | `#242a28` | Grid, dividers |
| `--line` | `#cdd2cd` | `#343b38` | Borders |
| `--pencil` | `#5b6360` | `#9aa39f` | Secondary text |
| `--graphite` | `#1c2120` | `#e8ece9` | Text, lines, primary button |

| Area | Token | Light | Dark |
|---|---|---|---|
| Electricity | `--power` | `#d99a00` | `#f2b630` |
| Digital logic | `--logic` | `#16899b` | `#3cc0d0` |
| Signals | `--signal` | `#6a4fd8` | `#9b86ff` |
| AI | `--ai` | `#c8417a` | `#f06aa2` |
| Networks | `--net` | `#2d6bd2` | `#6a9cff` |
| Software | `--code` | `#3f8a3a` | `#6cc466` |
| Mathematics | `--math` | `#d9631c` | `#ff8f4a` |

- Inside a module, only its area colour (`--active`) and the neutrals, on at most a tenth of the area.
- Colour never carries information alone.
- Done is a drawn tick. Danger is warning tape in graphite and `#f2c200`. No red and green.

### Type

Atkinson Hyperlegible Next for text, Atkinson Hyperlegible Mono for values and code.

| Token | Size | Weight |
|---|---|---|
| `--fs-h1` | 32–44 px | 800 |
| `--fs-h2` | 28 px | 800 |
| `--fs-h3` | 20 px | 700 |
| `--fs-body` | 17 px | 400 |
| `--fs-small` | 14 px | 400 |
| `--font-num` | 22–32 px | 600 |

Sentence case headings. No capitals. Mono only for numbers with units and code.

### Shape

The stage has a 10 px radius and a 1 px border. Buttons and fields 6 px. No shadows. No cards in
cards. Buttons are rectangles.

### Components

| Component | Class |
|---|---|
| Primary button, one per view | `.btn` |
| Secondary button | `.btn.ghost` |
| Choice | `.chip[aria-pressed]` |
| Slider with value | `.control` |
| Stepper | `.stepper` |
| Readout, only for numbers the scene cannot show | `.readout` |
| Tasks | `.tasks`, made by `K.tasks()` |
| Status line | `.status`, `.status.danger` |
| Vad hände? | `details.why` |
| Box | `.box`, made by `K.box()` |

### Show, don't tell

- Values sit in the scene next to the part they belong to: 6 V on the battery, 0,46 A at the bulb.
- No legend where the picture carries it. A glow shows brightness; no ”mörkt, lagom, för mycket”.
- No hints or sub-lines under tasks.
- No status message that repeats what the scene already shows.

### Icons, images and motion

24 px grid, 2 px strokes with round caps. Scenes are drawn as circuit diagrams. No gradients except
light that glows. No emoji. Motion shows cause and effect; the interface moves in 150–220 ms. The
reward happens in the scene. `prefers-reduced-motion` turns off the decorative.

### Layout

The scene takes at least 60 % of the width with the panel beside it. On a phone the panel goes
below.

### Language

The UI is Swedish, with English in `data-en`. Short and concrete. Assume capable adults.

1. Describe the world, not the person: ”Lampan gick sönder.”
2. Verb first in a task. One sentence, two at most.
3. Everyday words first, the technical term once.
4. No exclamation marks.
5. Machines do not speak in the first person.
6. No slogans, triads, em-dash asides or ”inte X, utan Y”.
7. ”Workshop” in Swedish too. No ”verkstad” or ”verkstäder”. No ”på bordet”; the box is its node id.

| Text | At most |
|---|---|
| Workshop name | 3 words |
| Problem | 6 words |
| Task | 2 sentences |
| Vad hände? | 3 sentences and a formula |

Avoid: magisk, resa, utforska, upptäck, dyk ner, låt oss, kraftfull, sömlös, superenkelt. In
English: magic, journey, explore, dive in, powerful, seamless, unlock, amazing.

Swedish typography: ”citat”, decimal comma, 3,0 V, 10–15 min, − for minus, 75 000. English copy is
British and written on its own terms, not translated word for word.

| Not this | This |
|---|---|
| Gör lampan stark. Till det markerade fältet. | Få exakt 1 A genom lampan. |
| Ge lampan för mycket ström. Bara på skärmen. | Nothing. The bulb breaks when it gets too much. |
| Jag tror: citron (67 %) | Citron, 67 % |
| Rätt! Det var ett äpple. | Uppgift 1 av 3 klar. |
| Verkstäder | Workshops |

### The boxes

Each box has its area colour and the node id on the lid. Lights: the area colour means active, a
fast white blink means found, alternating yellow and black means danger. Labels on the box use the
same words as the app.

## C. Checklist

- [ ] One problem and three tasks; the last one runs on the box.
- [ ] Tasks 1 and 2 need the team to decide something together.
- [ ] Only the area colour and neutrals.
- [ ] No capitals, pills or shadowed cards.
- [ ] The primary button is graphite.
- [ ] No hints, sub-lines, leads or legends the scene could carry.
- [ ] No exclamation marks, no first person, no praise.
- [ ] ”Citat”, decimal comma, a space before units.
- [ ] English written on its own terms.
- [ ] 400 px, light and dark, keyboard, reduced motion.
