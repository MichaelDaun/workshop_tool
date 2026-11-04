# Instructions for AI tools in this repository

Read `docs/06-design-manual.md` (part C is the checklist), `docs/07-module-plans.md` and
`docs/04-ai-authored-modules.md` first.

## Language

- Code, comments, identifiers, file names, MQTT topics, firmware, docs and commit messages are English.
- Only UI strings are Swedish, with the English version in `data-en` or `K.t(sv, en)`.
- English is British.

## Technology

- One HTML file per workshop in `mockups/modules/`, no build step.
- `mockups/shared/theme.css` and `mockups/shared/kit.js` (global `K`). Use the existing classes:
  `.stage`, `.scene`, `.panel`, `.mission`, `.tasks`, `.why`, `.status`, `.readout`, `.control`, `.btn`,
  `.chip`, `.stepper`, `.row`, `.box`, and the `hw-*` classes for box drawings.
- `K.tasks(el, id, list)` for tasks, `K.status(text, "info" | "done" | "danger")`, `K.box(el, {...})` for the box.
- `data-domain` on `body` sets `--active`. Domains: power, logic, signal, ai, net, code, math.
- Firmware: one file in `firmware/node/boxes/` with `setup(node)` and `loop(node)`.

## Workshops

- One problem, three tasks, for teams of 2–4. Tasks 1 and 2 are solved on screen and need discussion:
  a prediction, a limit or information only one person has. Task 3 makes the box do something concrete.
- Every task except the box task works without a box.

## Rules

- Domain colour plus neutrals. No capitals, pills, shadows, cards in cards or confetti.
- The primary button is graphite. Danger is warning tape. No red and green for right and wrong.
- Mono only for values and code.
- Show rather than tell. No hints, sub-lines, leads, legends or labels where the scene can carry it.
- No exclamation marks, no first person for machines, no praise, no em-dash asides, no triads,
  no ”inte X, utan Y”, no bold lead-ins.
- Write ”workshop” in Swedish, not ”verkstad” or ”verkstäder”. The name Verkstan stays. No ”på bordet”.
- Swedish typography: ”citat”, decimal comma, a space before units (0,46 A).

## Check

400 px width, dark mode, every task completable, empty console. No model names in commits or files.
