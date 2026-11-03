# 1. Vision, målgrupp och pedagogik

## Visionen i en mening

**Verkstan** är en webbapp där människor utan teknisk bakgrund får *göra* saker med teknik
(el, logik, signaler, AI, nätverk, mjukvara och matematik) och förstå den genom det de ser hända,
ensamma eller tillsammans i ett rum.

## Målgrupp

| | |
|---|---|
| **Vilka** | Icke-teknisk publik som introduceras till STEM, t.ex. allmänhet, nyanställda, beslutsfattare och skolelever |
| **Förkunskap** | Ingen. Vi utgår från att ord som "spänning", "algoritm" och "paket" är okända |
| **Format** | Workshops på plats, 5–75 deltagare, lagstorlek varierar |
| **Tempo** | Egen takt. Ledaren kan ha gemensamma moment men ingen ska behöva vänta på någon annan |
| **Enheter** | Blandat. Mobil ska fungera för de flesta moduler. Några få får vara "bäst på dator" |
| **Språk** | Svenska och engelska, med växling när som helst |
| **Identitet** | Anonyma smeknamn. Inga konton |

## Pedagogiska principer

### 1. Gör → Se → Förstå
Varje modul följer samma rytm:

1. **Gör:** första skärmen är något att trycka, dra eller slå på. Ingen text att läsa först.
2. **Se:** systemet reagerar direkt och synligt med en animation, ett ljud eller en färg.
3. **Förstå:** först *efter* att man gjort något finns en kort förklaring ("Vad hände?"),
   med de riktiga begreppen (Ohms lag, sanningstabell, bias...).

Detta är en variant av *concreteness fading*: konkret först, abstrakt sist.

### 2. Låg tröskel, högt tak, breda väggar
(Efter Seymour Papert och Mitchel Resnick.)
- **Låg tröskel:** det första uppdraget klarar alla på under 30 sekunder ("Tänd lampan").
- **Högt tak:** det sista uppdraget kräver eftertanke ("Lagom ljus med exakt 4 batterier").
- **Breda väggar:** man kan leka fritt utan att följa uppdragen.

### 3. Metaforer som går att växla bort
Varje abstrakt begrepp får en vardaglig bild: el som vatten, nätverk som hus och vägar,
funktion som maskin, AI som en som frågar sina grannar. Metaforen ska gå att **slå av och på**
(se vattenvyn i Strömkretsen), så att man ser att det är samma sak.

### 4. Fel är en del av upplägget
- Att spräcka lampan, krocka med roboten eller lura AI:n är **uppdrag**, inte misslyckanden.
- Feedback är aldrig skämmande: "Aj! Där var en bugg" i stället för "Fel!".

### 5. Kopplingen till verkligheten
Varje "Vad hände?" slutar med en koppling till vardagen: brusreducerande hörlurar,
ansiktsigenkänning med bias, internet som inte stannar när en kabel går av.

### 6. Allt hänger ihop
Startsidans karta visar hur områdena bygger på varandra:
ström → 1 och 0 → program → AI. Målet är att deltagaren går därifrån med en *helhetsbild*,
inte sju lösryckta fakta.

## Designriktlinjer

| Princip | I praktiken |
|---|---|
| **Bild före text** | Max ~2 korta meningar innan man får göra något. Instruktioner är verb: "Tryck", "Dra", "Klipp" |
| **En sak i fokus** | En stor scen per modul. Reglage under, uppdrag vid sidan |
| **Ämnesfärger** | Varje område har en egen färg som följer med överallt (kort, kablar, glöd) |
| **Mjuka animationer** | 0,3–0,8 s, mjuk easing. Rörelse visar *orsak och verkan*, aldrig bara dekoration |
| **Stora tryckytor** | Minst 44 px. Allt ska fungera med finger |
| **Läsbart typsnitt** | Atkinson Hyperlegible för brödtext (designat för läsbarhet), Bricolage Grotesque för rubriker, JetBrains Mono för värden och enheter |
| **Riktiga enheter** | V, A, Ω, Hz, ms visas som de är. Det gör det äkta |
| **Ljust och mörkt** | Båda teman från start. Ljust fungerar bäst på projektor |
| **Respektera rörelsekänslighet** | `prefers-reduced-motion` stänger av animationer |
| **Tillgänglighet** | Tangentbordsstyrning, aria-etiketter, färg är aldrig enda bäraren av information |

## Modulens anatomi

Alla mockupar följer samma mall, så att deltagaren bara behöver lära sig gränssnittet en gång:

```
┌──────────────────────────────────────────────┬───────────────────┐
│  ← Titel                     EN  ◐  Smeknamn │                   │
├──────────────────────────────────────────────┼───────────────────┤
│                                              │  UPPDRAG          │
│              SCENEN                          │  ○ Tänd lampan    │
│     (det man trycker på och ser hända)       │  ○ ...            │
│                                              │  ▓▓▓░░░ framsteg  │
│  [mätare]  [mätare]  [mätare]                ├───────────────────┤
│  ───●─── reglage    ───●─── reglage          │  ? Vad hände?     │
│                                              ├───────────────────┤
│                                              │  Lagidé / not     │
└──────────────────────────────────────────────┴───────────────────┘
```

På mobil staplas panelen under scenen.

## Hur en workshop kan se ut (exempel, 60 min)

| Tid | Moment | Läge |
|---|---|---|
| 0–5 | Alla går med via rumskod och väljer smeknamn | Rum |
| 5–10 | Snabbfråga på storskärmen: "Vad händer om en internetkabel går sönder?" | Hela rummet |
| 10–40 | Egen takt: välj valfria verkstäder. Ledaren ser översikten och går runt | Solo/par |
| 40–50 | Gemensamt experiment: "Klassens AI" där alla lägger till frukt från mobilen | Hela rummet |
| 50–60 | Ledaren visar kartan "Allt hänger ihop" och knyter ihop | Hela rummet |
