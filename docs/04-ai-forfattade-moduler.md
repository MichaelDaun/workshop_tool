# 4. Moduler skrivna av AI

Modulerna ska skrivas av en AI (Claude, Codex eller liknande) tillsammans med dig.
Det fungerar bra, men bara om AI:n får **tydliga ramar**. Annars blir varje modul en egen
liten app med egen stil, egna buggar och egen tillgänglighetsnivå.

## Problemet att lösa

| Utan ramar | Med ramar |
|---|---|
| Varje modul har egna knappar, färger och animationer | Alla moduler ser ut och beter sig likadant |
| AI:n skriver 500 rader per modul, mest upprepning | AI:n skriver innehåll + en scen, resten finns redan |
| Svårt för dig att granska | Du granskar pedagogik och innehåll, inte layout |
| Svenska och engelska glider isär | Båda språken krävs och kontrolleras automatiskt |

## Lösningen: en byggsats + ett modulformat

### 1. Byggsatsen (komponenter)

När de sex mockuparna byggdes återkom samma delar i alla. Det är dessa som ska bli
återanvändbara komponenter:

| Komponent | Finns i mockupen som | Används av |
|---|---|---|
| Toppfält (tillbaka, titel, språk, tema, smeknamn) | `K.topbar()` | Alla |
| Scen + panel-layout | `.module`, `.stage`, `.panel` | Alla |
| Uppdragslista med framsteg och firande | `K.tasks()` | Alla |
| "Vad hände?"-kort | `details.why` | Alla |
| Mätare / avläsning | `.readout` | El, nätverk, AI |
| Reglage med värde och enhet | `.control` + `input[type=range]` | El, signal, AI |
| Växlare (på/av) | brytare i logik, våg B i signal | Logik, signal |
| Val bland kort | grindväljaren, fruktval | Logik, AI |
| Toast + konfetti | `K.toast()`, `K.confetti()` | Alla |
| Språksträngar | `data-en`, `K.t()` | Alla |

Nästa steg är "scenkomponenter" som är specifika men återanvändbara: ett **kopplingsschema**,
ett **rutnät med figur**, en **graf/oscilloskop**, ett **nodnät** och en **2D-karta med punkter**.

### 2. Modulformatet (manifest)

Varje modul beskrivs med en fil som AI:n fyller i. Förslag:

```yaml
id: el-krets
domain: el               # bestämmer färg och plats på kartan
title: { sv: Strömkretsen, en: The circuit }
minutes: 10
devices: all             # all | desktop
formats: [solo, lag]

intro:                   # max 2 korta meningar
  sv: Tryck på strömbrytaren, lägg till batterier och ändra motståndet.
  en: Tap the switch, add batteries and change the resistance.

scene: circuit           # vilken scenkomponent som används
state:                   # det scenen exponerar och uppdragen kan läsa
  batteries: { min: 1, max: 6, start: 2 }
  resistance: { min: 0.5, max: 20, step: 0.5, start: 10, unit: Ω }
  switch: { start: off }

tasks:
  - id: tand
    text: { sv: Tänd lampan, en: Turn on the bulb }
    done_when: power > 0.05
  - id: lagom
    text: { sv: Lagom ljus med exakt 4 batterier, en: Just right with exactly 4 batteries }
    done_when: batteries == 4 and power >= 2.5 and power <= 4.5

why:
  - sv: "**Batterier knuffar.** Fler batterier betyder mer knuff (spänning)."
    en: "**Batteries push.** More batteries means more push (voltage)."
  - formula: { sv: "I = U ÷ R", en: "I = V ÷ R" }

real_world: { sv: Laddaren till mobilen…, en: Your phone charger… }

team:                    # valfri lag- eller rumsversion
  pattern: delad-kontrollpanel
  roles: [batteries, resistance, switch]
```

Om en modul behöver något nytt (en ny sorts scen) bygger AI:n en ny scenkomponent, som sedan
blir en del av byggsatsen.

### 3. Instruktionsfil för AI-agenter

En fil i repot (`AGENTS.md`, och `CLAUDE.md` som pekar på den) som alla AI-verktyg läser.
Den ska innehålla:

- Målgruppen: icke-teknisk, ingen förkunskap.
- Rytmen *Gör → Se → Förstå* och de andra principerna i `01-vision-och-pedagogik.md`.
- Hårda regler: båda språken, högst 2 meningar före första interaktionen, bara färger från
  temat, inga externa beroenden, minst 44 px tryckytor, tangentbordsstöd.
- Ordlista med vardagliga ord som ska användas ("knuff" före "spänning" första gången).
- Exempel på en bra modul och en dålig.

## Kvalitetskontroller (automatiska)

Varje ny eller ändrad modul ska passera, i GitHub Actions:

| Kontroll | Fångar |
|---|---|
| Manifestet följer schemat | Saknade fält, fel typer |
| Alla texter finns på sv **och** en | Glömda översättningar |
| Introtext ≤ 2 meningar, uppdrag ≤ 60 tecken | För mycket text |
| Skärmdumpar: mobil + dator, ljust + mörkt | Trasig layout, text som klipps |
| Tillgänglighetstest (axe) | Kontrast, etiketter, fokus |
| "Kan man klara alla uppdrag?" (scriptat test) | Omöjliga eller buggiga uppdrag |
| Inga konsolfel | Krascher |

Skärmdumparna läggs som kommentar på pull requesten så att du kan granska utan att köra något.

## Arbetsflöde för en ny modul

```
1. Idé            Välj ur övningsbanken (02-ovningsbank.md)
      │
2. Brief          AI:n skriver en kort brief: aha-ögonblick, metafor,
      │           3–5 uppdrag, koppling till verkligheten, lagversion
      │           → du godkänner eller justerar (5 min)
      │
3. Bygg           AI:n skriver manifest + ev. ny scenkomponent på en egen branch
      │
4. Kontroller     Automatiska tester + skärmdumpar på pull requesten
      │
5. Provkör        Testa med 1–2 personer ur målgruppen. Tittar de på skärmen
      │           eller på texten? Hittar de första uppdraget själva?
      │
6. Merge          Modulen dyker upp på kartan
```

### Mall för en modul-brief (att ge till AI:n)

```text
Skriv en modul-brief för Verkstan (se docs/01–04).
Område: <t.ex. Nätverk>
Idé: <rad ur övningsbanken>
Leverera:
- Aha-ögonblicket i en mening
- Metaforen, och hur den kan slås av/på
- Scenen: vad syns, vad kan man trycka/dra på
- 3–5 uppdrag från lätt till klurigt, med villkor för "klart"
- "Vad hände?" i 3 korta stycken + koppling till vardagen
- Lag- eller rumsversion enligt ett av samarbetsmönstren
- Vilka befintliga komponenter som används, och vad som är nytt
Båda språken (sv/en). Ingen förkunskap hos målgruppen.
```

## Risker och hur vi hanterar dem

| Risk | Åtgärd |
|---|---|
| Faktafel i förklaringar | Du granskar alltid "Vad hände?". Håll förklaringarna korta, de är lättare att kontrollera |
| Förenklingar som blir fel ("el är vatten") | Säg uttryckligen var metaforen tar slut, t.ex. i en "Men…"-rad |
| Stilen glider över tid | Byggsatsen + automatiska skärmdumpar |
| Modulerna blir för lika och tråkiga | Variera scenkomponenterna, inte grundlayouten |
| Beroende av ett visst AI-verktyg | Allt ligger som vanliga filer i repot. Vilket verktyg som helst kan läsa instruktionerna |
