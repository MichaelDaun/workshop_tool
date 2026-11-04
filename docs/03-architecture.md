# 3. Architecture

No framework has been chosen.

## Two layers

```text
Web app (static files)  ⇄ WebSocket ⇄  Room server (optional)  ⇄ MQTT ⇄  Boxes
modules, languages, solo               room codes, sync, big screen      Pico W nodes
```

Solo always works and stores progress in the browser. Room mode sits on top. If the server cannot
be reached, the app falls back to solo. The box task needs the room server.

## What the room needs

Joining, progress to the leader, teams, polls, shared data, the leader switching modes, and
pairing boxes with workshops. These are all small events, so one in-memory state per room is
enough. No CRDT.

## Own server or GitHub Pages

| | GitHub Pages | Own server |
|---|---|---|
| Static files | Yes | Yes |
| WebSocket | No | Yes |
| Offline on site | No | Yes |
| Maintenance | None | Certificates, updates |

Own server for production, with the static files and the room server in one container. GitHub
Pages for previews.

## Verkstan in a box

The same container runs on a Raspberry Pi with its own router in the room. Participants join the
local network and scan a QR code. No internet is needed. The boxes connect to the same Pi.

This needs:

- Fonts and libraries served locally. The mockups load Google Fonts; production must not.
- Local HTTPS, which the microphone needs. Open question.
- Reconnecting to the same nickname with an anonymous token.

## Privacy

Only nicknames and progress. Rooms are deleted after 12 hours. No tracking. Statistics only in
aggregate. Nicknames are treated as personal data.

## Moderation

No free text in room activities. Suggested nicknames by default. The leader can rename, remove
and freeze.

## Protocol

```jsonc
// participant → server
{ "t": "join",     "room": "VERK-42", "nick": "Snabba Uttern", "token": "…" }
{ "t": "progress", "module": "circuit", "task": "one-amp" }
{ "t": "submit",   "activity": "class-ai", "data": { "x": 0.12, "y": 0.7, "c": "apple" } }
{ "t": "vote",     "activity": "poll-1", "choice": "B" }
{ "t": "box",      "node": "node-01", "topic": "out/…", "data": { … } }

// leader → server
{ "t": "mode",   "activity": "class-ai" }
{ "t": "teams",  "size": 4 }
{ "t": "pair",   "node": "node-01", "module": "circuit" }
{ "t": "reveal", "activity": "poll-1" }

// server → everyone
{ "t": "state", "mode": "class-ai", "people": 23, "activity": { … } }
{ "t": "event", "kind": "submit", "by": "Snabba Uttern", "data": { … } }
{ "t": "box",   "node": "node-01", "topic": "in/current", "data": { "mA": 19.6 } }
```

The server only forwards `out/` messages from a team to the box paired with its workshop.

## Candidates

| Layer | Options |
|---|---|
| Modules | Plain JS, Svelte, Lit |
| Room server | Node with `ws` and `mqtt`, Bun, Python |
| Hosting | Docker and Caddy |

## Open questions

1. Where does the production server run?
2. Is Verkstan in a box needed from the start?
3. Should results be kept after the session?
4. Is one secret leader link per room enough?
