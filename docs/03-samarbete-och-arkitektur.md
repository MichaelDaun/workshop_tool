# 3. Samarbete och arkitektur

> Ramverk och teknik är **inte spikade**. Det här dokumentet beskriver de krav och vägval
> som påverkar valet, så att vi kan bestämma när övningarna är tydligare.

## Grundidé: två lager

```
┌─────────────────────────────────────────┐        ┌──────────────────────────────┐
│  WEBBAPPEN (statiska filer)             │        │  RUMSSERVERN (valfri)        │
│  HTML + CSS + JS, moduler, språk,       │◄──────►│  rumskoder, smeknamn,        │
│  soloövningar, framsteg i webbläsaren   │ WebSoc │  livesynk, storskärmsvy,     │
│                                         │  ket   │  ledarkontroller             │
│  Kan ligga på egen server ELLER Pages   │        │  Kräver egen server          │
└─────────────────────────────────────────┘        └──────────────────────────────┘
```

- **Solo fungerar alltid**, helt utan server. Framsteg sparas i webbläsaren (`localStorage`).
- **Rumsläget** läggs till ovanpå. Om servern inte nås (dåligt wifi, brandvägg) faller appen
  tillbaka till solo, och ledaren ser det tydligt.
- Det gör att mockuparna och senare de riktiga modulerna kan förhandsvisas på GitHub Pages
  även om produktionen körs på egen server.

## Vad rummet behöver kunna (från övningsbanken)

| Funktion | Används av | Typ av data |
|---|---|---|
| Gå med med kod + smeknamn | Allt | Närvaro |
| Framsteg per deltagare till ledaren | Översikt | Små händelser ("klarade uppdrag X") |
| Snabbfråga / röstning | Förutsäg → testa | Räknare |
| Kollektiv data | Klassens AI, tärningskurvan | Lista av punkter |
| Ledaren styr läget | Byter vad mobilerna visar | Ett "nuvarande läge" |
| Lagindelning | Lag, pussel | Grupp-id per deltagare |
| Rummet är systemet | Människonätverket, binärt | Tillstånd per deltagare + turordning |
| Delad kontrollpanel | Strömkretsen i lag | Litet gemensamt tillstånd per lag |

**Slutsats:** allt är *små, strukturerade händelser*. Inget kräver samtidig textredigering.
Därför räcker en enkel **händelsebaserad server med ett tillstånd per rum i minnet**.
CRDT-bibliotek (Yjs, Automerge) är onödigt komplexa här, men kan bli aktuella om vi senare
vill ha en gemensam whiteboard.

## Egen server eller GitHub Pages?

| | GitHub Pages | Egen server |
|---|---|---|
| Statiska filer | Ja, gratis, automatisk deploy | Ja |
| Rumsserver / WebSocket | **Nej** | Ja |
| Kontroll över data (GDPR) | Bara statiskt, ingen data | Full kontroll |
| Fungerar offline på plats | Nej | **Ja**, om servern körs lokalt (se nedan) |
| Underhåll | Inget | Uppdateringar, certifikat, övervakning |
| Kostnad | 0 kr | Liten VPS räcker gott (75 användare är en mycket liten last) |

**Rekommendation:** egen server för produktion (ett paket: statiska filer + rumsserver i
**en** container), och GitHub Pages som förhandsvisning av mockupar och moduler under utveckling.

## "Verkstan i en låda": offline på plats

Workshoppar hålls på plats, där wifi ofta är dåligt eller där företagsnät blockerar WebSockets.
Eftersom allt kan ligga i en container kan samma server köras:

1. **I molnet** (vanligt fall): `https://verkstan.<er-domän>`
2. **På en laptop eller Raspberry Pi i rummet** med en egen wifi-router eller mobil hotspot.
   Deltagarna ansluter till det lokala nätet och skannar en QR-kod. Inget internet behövs.

Det är ett starkt argument för egen server och för att **inte** bero på tredjepartstjänster.

## Krav som följer av det

- **Inga externa beroenden i körning.** Typsnitt, ikoner och bibliotek bundlas med appen.
  (Mockuparna hämtar Google Fonts för enkelhetens skull. I produktion ska typsnitten ligga på
  egen server, både för offline och för GDPR, eftersom Google Fonts skickar besökarens IP-adress
  till Google.)
- **HTTPS** behövs för WebSocket över `wss://` och för vissa webbläsar-API:er (mikrofon m.m.).
  Lokalt läge behöver därför en lösning för certifikat, eller så körs det över `http://` med
  begränsningar. Det här är en öppen fråga.
- **Återanslutning:** mobiler somnar och tappar uppkopplingen. Deltagaren ska komma tillbaka
  till samma smeknamn och framsteg (spara en anonym rums-token i webbläsaren).
- **Reservläge** om WebSocket blockeras: long-polling (t.ex. Socket.IO har det inbyggt).

## Integritet och GDPR

| Princip | Så gör vi |
|---|---|
| Minimal data | Bara smeknamn och framsteg. Inga konton, e-post eller namn krävs |
| Kortlivat | Rum raderas automatiskt efter t.ex. 12 timmar. Inget sparas på disk som standard |
| Ingen spårning | Inga analysverktyg från tredje part, inga spårningscookies |
| Smeknamn kan vara riktiga namn | Behandla dem som personuppgifter: radera med rummet |
| Statistik | Om vi vill mäta (t.ex. vilka uppdrag folk fastnar på): bara aggregerat, utan smeknamn |

## Moderering

Med upp till 75 anonyma deltagare kommer någon att skriva något olämpligt.

- **Undvik fritext** i rumsövningar. Använd strukturerade val: röstknappar, punkter på en karta, färger.
- **Föreslagna smeknamn** (som i mockupen, "Snabba Uttern") som standard, fritt namn som tillval.
- **Ledaren kan** byta namn på och ta bort deltagare, och "frysa" rummet.

## Skiss på meddelandeprotokoll

Ett förslag på hur få och enkla meddelanden som behövs:

```jsonc
// deltagare → server
{ "t": "join",     "room": "VERK-42", "nick": "Snabba Uttern", "token": "…" }
{ "t": "progress", "module": "el-krets", "task": "lagom" }
{ "t": "submit",   "activity": "klassens-ai", "data": { "x": 0.12, "y": 0.7, "c": "apple" } }
{ "t": "vote",     "activity": "snabbfraga-1", "choice": "B" }

// ledare → server (kräver ledartoken)
{ "t": "mode",  "activity": "klassens-ai" }      // byt vad alla mobiler visar
{ "t": "teams", "size": 4 }
{ "t": "reveal","activity": "snabbfraga-1" }

// server → alla
{ "t": "state", "mode": "klassens-ai", "people": 23, "activity": { … } }
{ "t": "event", "kind": "submit", "by": "Snabba Uttern", "data": { … } }
```

Varje gemensam aktivitet blir en liten **aktivitetstyp** på servern (röstning, punktinsamling,
turordning), som många moduler kan återanvända.

## Kandidater att välja mellan senare

Inga beslut, bara en karta över alternativen:

| Lager | Alternativ | Kommentar |
|---|---|---|
| Moduler | Ren HTML/JS (som mockuparna) · Svelte · React · Lit (webbkomponenter) | Webbkomponenter passar bra för en komponentbank som AI ska använda (se dok 4) |
| Sidor och innehåll | Vite · Astro | Astro passar innehållstunga sajter med interaktiva "öar" |
| Rumsserver | Node + `ws`/Socket.IO · Bun · Deno · Python (FastAPI) | En process klarar 75 personer med marginal |
| Drift | Docker + Caddy (automatisk HTTPS) | En container, ett kommando |
| Förhandsvisning | GitHub Pages via GitHub Actions | Mockupar och moduler syns för alla i teamet |

## Öppna frågor

1. Var ska produktionsservern stå (egen hårdvara, VPS, organisationens moln)?
2. Behövs offline-läget ("Verkstan i en låda") från start, eller senare?
3. Ska ledaren kunna spara ett rum (t.ex. resultaten från "Klassens AI") efter workshopen?
4. Behöver ledare logga in, eller räcker en hemlig ledarlänk per rum?
5. Vilka nätverk brukar ni ha på plats? (Gästnät hos kund, skolans nät, eget.)
