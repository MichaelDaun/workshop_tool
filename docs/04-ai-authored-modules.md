# 4. AI-authored modules

An AI writes the modules together with the maintainer. Without a frame, each module becomes its
own app with its own style. With a kit, the AI writes the problem, the scene and the box task, and
the reviewer checks the teaching.

## The kit

| Part | In the mockups |
|---|---|
| Top bar | `header.topbar` with `data-title-sv` and `data-title-en` |
| Scene and panel | `.module`, `.stage`, `.scene`, `.panel` |
| Problem and tasks | `.mission` with an h2, `K.tasks()` |
| Status line | `K.status()` |
| Vad hände? | `details.why` |
| Box | `K.box()` with a drawing in `hw-*` classes |
| Controls | `.control`, `.chip[aria-pressed]`, `.stepper`, `.btn` |
| Language | `data-en`, `K.t()` |

Recurring scenes that could become components: circuit diagram, grid with a figure, graph, node
network, plot of points, bar chart.

## Module format

```yaml
id: circuit
domain: power
title: { sv: Strömkretsen, en: The circuit }
problem: { sv: Exakt en ampere, en: Exactly one ampere }
minutes: 20
scene: circuit
state:
  batteries: { min: 1, max: 6, start: 2 }
  resistance: { min: 0.5, max: 20, step: 0.5, start: 10, unit: Ω }
tasks:
  - id: one-amp
    text: { sv: Få exakt 1 A genom lampan., en: Get exactly 1 A through the bulb. }
    done_when: closed and abs(current - 1) <= 0.05
  - id: predict
    text: { sv: "Med 4 batterier: räkna ut motståndet för 1 A innan ni slår på brytaren.", en: "…" }
    done_when: on_close(batteries == 4 and abs(current - 1) <= 0.05)
  - id: led
    box: true
    done_when: box.mA >= 19 and box.mA <= 20
why:
  - { sv: Mer motstånd ger mindre ström., en: More resistance gives less current. }
box: node-01
```

## Automatic checks

| Check | Catches |
|---|---|
| Schema | Missing fields |
| Both languages | Forgotten translations |
| Length: task at most 2 sentences, no lead | Too much text |
| Exactly one task needs the box, and it is last | A workshop with no hardware ending |
| Screenshots at 400 and 1280 px, light and dark | Broken layout |
| axe | Contrast, labels, focus |
| A scripted run through every task | Impossible tasks |
| Empty console | Crashes |

## Workflow

1. Pick an idea from the exercise bank.
2. The AI writes a brief: the problem, three tasks, what the team must discuss, what the box does.
   Approve it.
3. The AI builds it on its own branch.
4. Checks and screenshots on the pull request.
5. Try it with one team from the audience.

## Risks

| Risk | Mitigation |
|---|---|
| Factual errors | Always review ”Vad hände?” |
| The task is too easy | Each task needs a decision the team argues about |
| Style drift | The kit and the screenshots |
| Too much text | The length check |
