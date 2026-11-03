# Verkstan

En webbapp med workshopövningar som introducerar teknik för en **icke-teknisk publik**:
ellära, digital logik, signalteknik, AI/ML, nätverk, mjukvara och matematik.
Man gör saker först och förstår sedan. Det fungerar ensam i egen takt eller tillsammans i ett rum.

> **Status:** idéspåning och klickbara mockupar. Ramverk och teknik är inte valda än.

## Prova mockuparna

Öppna `mockups/index.html` direkt i webbläsaren, eller kör en lokal server:

```bash
cd mockups && python3 -m http.server 8000
```

och gå till <http://localhost:8000>.

| Mockup | Område | Vad man gör |
|---|---|---|
| [Startsidan](mockups/index.html) | – | Smeknamn, rumskod, kartan "Allt hänger ihop", alla verkstäder |
| [Strömkretsen](mockups/moduler/el-krets.html) | Ellära | Batterier, motstånd, lampa. Växla till vattenvy |
| [Logikgrindar](mockups/moduler/logik-grindar.html) | Digital logik | Brytare, grindar, sanningstabell, gåtor |
| [Ljudvågor](mockups/moduler/signal-vagor.html) | Signalteknik | Riktigt ljud, blanda vågor, släck ljud med motvåg |
| [Fruktsorteraren](mockups/moduler/ai-sortera.html) | AI/ML | Lär upp en AI, upptäck bias, lura den |
| [Paketresan](mockups/moduler/natverk-paket.html) | Nätverk | Skicka paket, klipp kablar, se omvägar |
| [Robotens väg](mockups/moduler/robot-kod.html) | Mjukvara | Blockprogrammering, buggar, upprepning |
| [Funktionsmaskinen](mockups/moduler/matte-maskin.html) | Matematik | Hitta den hemliga regeln, se linjen i grafen |
| [Rumsläge](mockups/rum.html) | – | Storskärm för ledaren + deltagarmobil (simulerad) |
| [Designmanual](mockups/designmanual.html) | – | Den nya visuella riktningen med levande komponenter (utkast) |

Alla mockupar är ren HTML/CSS/JS utan byggsteg. De delar `mockups/shared/theme.css`
(färger, typsnitt, komponenter) och `mockups/shared/kit.js` (språk, smeknamn, uppdrag, firande).

## Dokument

1. [Vision och pedagogik](docs/01-vision-och-pedagogik.md): målgrupp, principer, designriktlinjer, exempel på workshop
2. [Övningsbank](docs/02-ovningsbank.md): ~45 övningsidéer per område och samarbetsmönster för 5–75 personer
3. [Samarbete och arkitektur](docs/03-samarbete-och-arkitektur.md): egen server eller GitHub Pages, offline på plats, GDPR, protokoll
4. [Moduler skrivna av AI](docs/04-ai-forfattade-moduler.md): byggsats, modulformat, kvalitetskontroller, arbetsflöde
5. [Fysiska enheter](docs/05-fysiska-enheter.md): mikrokontroller per modul, Verkstan-noden, hur den pratar med appen
6. [Designmanual](docs/06-designmanual.md): granskning av AI-drag i mockuparna, färg, typografi, komponenter och språk

## GitHub Pages

`.github/workflows/pages.yml` publicerar mappen `mockups/` vid push till `main`.
Slå på det en gång under **Settings → Pages → Source: GitHub Actions**.
