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

| Mockup | Område | Vad man gör | Låda på bordet |
|---|---|---|---|
| [Startsidan](mockups/index.html) | – | Smeknamn, rumskod, karta över hur ämnena hänger ihop, alla verkstäder | – |
| [Strömkretsen](mockups/moduler/el-krets.html) | Ellära | Batterier, motstånd och lampa. Växla till vattenvy | Lysdiod, ratt och strömsensor |
| [Logikgrindar](mockups/moduler/logik-grindar.html) | Digital logik | Brytare, grindar, sanningstabell, gåtor | Två arkadknappar och en lampa |
| [Ljudvågor](mockups/moduler/signal-vagor.html) | Signalteknik | Riktigt ljud, blanda vågor, släck en ton med motvåg | Högtalare, mikrofon, lysdiodsstapel |
| [Fruktsorteraren](mockups/moduler/ai-sortera.html) | AI och ML | Lär en maskin att sortera, se skevheten, lura den | Våg, färgsensor och en lucka |
| [Paketresan](mockups/moduler/natverk-paket.html) | Nätverk | Skicka paket, klipp kablar, se omvägar | Ljusslingor som kablar mellan sju hus |
| [Robotens väg](mockups/moduler/robot-kod.html) | Mjukvara | Blockprogram, buggar, upprepning | Robot med stegmotorer på golvmatta |
| [Funktionsmaskinen](mockups/moduler/matte-maskin.html) | Matematik | Hitta den hemliga regeln, se linjen i grafen | Vred, två displayer och ett lock |
| [Rumsvyn](mockups/rum.html) | – | Storskärm för ledaren, deltagarmobil, ihopparning av lådor (simulerat) | Alla |
| [Designmanual](mockups/designmanual.html) | – | Färger, typografi och komponenter med levande exempel | – |

Alla mockupar är ren HTML/CSS/JS utan byggsteg och följer designmanualen (dokument 6).
De delar `mockups/shared/theme.css` (färger, typsnitt, komponenter) och `mockups/shared/kit.js`
(språk, smeknamn, protokoll, statusrad och lådpanelen ”På bordet”). Lådorna är simulerade i
mockuparna. Firmware-utkastet finns i [`firmware/`](firmware/).

## Dokument

1. [Vision och pedagogik](docs/01-vision-och-pedagogik.md): målgrupp, principer, designriktlinjer, exempel på workshop
2. [Övningsbank](docs/02-ovningsbank.md): ~45 övningsidéer per område och samarbetsmönster för 5–75 personer
3. [Samarbete och arkitektur](docs/03-samarbete-och-arkitektur.md): egen server eller GitHub Pages, offline på plats, GDPR, protokoll
4. [Moduler skrivna av AI](docs/04-ai-forfattade-moduler.md): byggsats, modulformat, kvalitetskontroller, arbetsflöde
5. [Fysiska enheter](docs/05-fysiska-enheter.md): idéer per modul, Verkstan-noden med Pico W, MQTT över wifi
6. [Designmanual](docs/06-designmanual.md): granskning av AI-drag i mockuparna, färg, typografi, komponenter och språk
7. [Modulplaner](docs/07-modulplaner.md): mål, steg och låda för alla sju verkstäder, med delar, kopplingar, meddelanden och budget

Den som låter en AI skriva eller ändra moduler ska peka den till [AGENTS.md](AGENTS.md).

## GitHub Pages

`.github/workflows/pages.yml` publicerar mappen `mockups/` vid push till `main`.
Slå på det en gång under **Settings → Pages → Source: GitHub Actions**.
