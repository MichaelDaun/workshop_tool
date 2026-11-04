# 3. Samarbete och arkitektur

Ramverk och teknik är inte valda.

## Två lager

```text
Webbappen (statiska filer)  ⇄ WebSocket ⇄  Rumsservern (valfri)
moduler, språk, solo                       rumskoder, synk, storskärm, lådor
```

Solo fungerar alltid och sparar framsteg i webbläsaren. Rumsläget läggs ovanpå. Nås inte servern
faller appen tillbaka till solo.

## Vad rummet behöver

Gå med, framsteg till ledaren, röstning, gemensam data, ledaren byter läge, lagindelning, tillstånd
per deltagare. Allt är små händelser, så ett tillstånd per rum i minnet räcker. Ingen CRDT.

## Egen server eller GitHub Pages

| | GitHub Pages | Egen server |
|---|---|---|
| Statiska filer | Ja | Ja |
| WebSocket | Nej | Ja |
| Offline på plats | Nej | Ja |
| Underhåll | Inget | Certifikat, uppdateringar |

Egen server för produktion, statiska filer och rumsserver i en container. GitHub Pages för
förhandsvisning.

## Verkstan i en låda

Samma container kan köras på en Raspberry Pi med egen router i rummet. Deltagarna ansluter till
det lokala nätet och skannar en QR-kod. Inget internet behövs. Lådorna (dokument 5) ansluter
till samma Pi.

Det kräver:

- Typsnitt och bibliotek lokalt. Mockuparna hämtar Google Fonts, produktion ska inte göra det.
- En lösning för HTTPS lokalt, som mikrofonen behöver. Öppen fråga.
- Återanslutning till samma smeknamn med en anonym token.

## Integritet

Bara smeknamn och framsteg. Rum raderas efter 12 timmar. Ingen spårning. Statistik bara
aggregerad. Smeknamn behandlas som personuppgifter.

## Moderering

Ingen fritext i rumsövningar. Föreslagna smeknamn som standard. Ledaren kan byta namn, ta bort
och frysa rummet.

## Protokoll

```jsonc
// deltagare → server
{ "t": "join",     "room": "VERK-42", "nick": "Snabba Uttern", "token": "…" }
{ "t": "progress", "module": "el-krets", "task": "lagom" }
{ "t": "submit",   "activity": "klassens-ai", "data": { "x": 0.12, "y": 0.7, "c": "apple" } }
{ "t": "vote",     "activity": "snabbfraga-1", "choice": "B" }

// ledare → server
{ "t": "mode",   "activity": "klassens-ai" }
{ "t": "teams",  "size": 4 }
{ "t": "reveal", "activity": "snabbfraga-1" }

// server → alla
{ "t": "state", "mode": "klassens-ai", "people": 23, "activity": { … } }
{ "t": "event", "kind": "submit", "by": "Snabba Uttern", "data": { … } }
```

## Kandidater

| Lager | Alternativ |
|---|---|
| Moduler | Ren JS, Svelte, Lit |
| Rumsserver | Node med `ws`, Bun, Python |
| Drift | Docker och Caddy |

## Öppna frågor

1. Var står produktionsservern?
2. Behövs Verkstan i en låda från start?
3. Ska resultat kunna sparas efter workshopen?
4. Räcker en hemlig ledarlänk per rum?
