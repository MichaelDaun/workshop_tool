# 6. Designmanual

Gäller skärmar, texter och lådor. Visuell version i
[`mockups/designmanual.html`](../mockups/designmanual.html). Del C är checklistan.

## A. Det vi tog bort

De första mockuparna bar typiska drag från AI-genererad design:

- versala etiketter i mono med spärrning
- kort i kort med skugga, pillerformade knappar
- dekorativa pastellcirklar och konfetti
- alla sju ämnesfärger samtidigt
- grönt som betyder både mjukvara och rätt
- ett extra rubriktypsnitt
- fetstilta inledningar, utropstecken, beröm och maskiner i jag-form
- triader och slogans, som ”Prova. Se. Förstå.”
- för mycket text och metakommentarer

Det som behölls: scenen först, en färg per ämne, riktiga enheter, metaforer som går att slå av
och båda språken.

## B. Manualen

### Arbetsbänken

Verkstan ser ut som en välordnad arbetsbänk: skärmatta med rutnät, kopplingsscheman,
mätinstrument och varningstejp. Scenen är bänken. Kontroller ser ut som instrument. Färg visar
det som är aktivt, resten är grafit och papper.

### Färg

| Token | Ljust | Mörkt | Till |
|---|---|---|---|
| `--papper` | `#f3f4f1` | `#121514` | Bakgrund |
| `--ark` | `#ffffff` | `#1a1e1d` | Scen, paneler |
| `--rutnat` | `#e4e7e3` | `#242a28` | Rutnät, avdelare |
| `--linje` | `#cdd2cd` | `#343b38` | Kanter |
| `--blyerts` | `#5b6360` | `#9aa39f` | Sekundär text |
| `--grafit` | `#1c2120` | `#e8ece9` | Text, linjer, primärknapp |

| Område | Token | Ljust | Mörkt |
|---|---|---|---|
| Ellära | `--el` | `#d99a00` | `#f2b630` |
| Digital logik | `--logik` | `#16899b` | `#3cc0d0` |
| Signalteknik | `--signal` | `#6a4fd8` | `#9b86ff` |
| AI | `--ai` | `#c8417a` | `#f06aa2` |
| Nätverk | `--nat` | `#2d6bd2` | `#6a9cff` |
| Mjukvara | `--kod` | `#3f8a3a` | `#6cc466` |
| Matematik | `--matte` | `#d9631c` | `#ff8f4a` |

- I en modul bara modulens färg plus neutraler, på högst en tiondel av ytan.
- Färg bär aldrig information ensam.
- Klart är en ritad bock. Fara är varningstejp i grafit och `#f2c200`. Inget rött och grönt.

### Typografi

Atkinson Hyperlegible Next för text, Atkinson Hyperlegible Mono för värden och kod.

| Steg | Storlek | Vikt |
|---|---|---|
| Rubrik 1 | 40–48 px | 800 |
| Rubrik 2 | 28 px | 800 |
| Rubrik 3 | 20 px | 700 |
| Brödtext | 17 px | 400 |
| Liten | 14 px | 400 |
| Värde | 22–32 px | Mono 600 |

Rubriker i meningsform. Inga versaler. Mono bara för siffror med enhet och kod. Högst 60 tecken
per rad.

### Form

Scenen 10 px rundning och 1 px kant. Knappar och fält 6 px. Inga skuggor utom på det som svävar.
Inga kort i kort. Knappar är rektanglar.

### Komponenter

| Komponent | Utseende |
|---|---|
| Primärknapp | Grafit, 48 px hög, en per vy |
| Sekundärknapp | 1 px grafitkant |
| Fader | Spår med värde och enhet till höger |
| Vippbrytare | Ritad vippa med 0 och 1 |
| Stegare | − och + med värdet mellan |
| Mätare | Mono-siffra med namn under |
| Protokoll | Numrerade steg, nästa markerat i kanten, bock ritas när klart |
| Vad hände? | Två korta stycken |

### Ikoner, bilder och rörelse

24 px rutnät, 2 px linjer med runda ändar. Scener ritas som kopplingsscheman. Inga gradienter
utom ljus som lyser. Inga emoji. Rörelse visar orsak och verkan, gränssnittet rör sig 150–220 ms.
Belöningen sker i scenen. `prefers-reduced-motion` stänger av det dekorativa.

### Layout

Scenen tar minst 60 % av bredden, protokollet ligger bredvid. På mobil hamnar protokollet under.

### Språk

Kort, konkret och vänligt. Vuxna behandlas som vuxna. Mindre text är oftast tydligare.

1. Beskriv världen, inte personen: ”Lampan lyser.”
2. Verb först i instruktioner.
3. Vardagsord först, fackord en gång.
4. Inga utropstecken utom ljudord i scenen.
5. Maskiner talar inte i jag-form.
6. Inga slogans, triader, inskjutna tankstreck eller ”inte X, utan Y”.
7. Fetstil bara på ett nytt begrepp.
8. Fel är information: ”Roboten körde in i ett träd vid steg 3.”
9. Inga metakommentarer om vad sidan ska göra eller vad man ska lära sig.

| Text | Högst |
|---|---|
| Namn | 3 ord |
| Lead | 1 mening |
| Steg | 8 ord |
| Vad hände? | 2 stycken à 2 meningar |

Undvik: magisk, resa, utforska, dyk ner, kraftfull, sömlös, superenkelt, hemligheten bakom, värt
att notera, fantastiskt. På engelska: magic, journey, explore, dive in, powerful, seamless,
unlock, amazing.

Svensk typografi: ”citat”, decimalkomma, 3,0 V, 10–15 min, − för minus, 75 000. Engelska med
brittisk stavning och egen formulering.

| Före | Efter |
|---|---|
| Jag tror: Citron (67 %) | Maskinens gissning: citron, 67 % |
| Rätt! Det var ett äpple. | Det var ett äpple. Gissningen stämde. |
| Aj! Där var en bugg. | Roboten körde in i ett träd. |
| Du tänker redan som en datorkonstruktör. | Alla gåtor lösta. |

### Lådorna

Lådan har modulens färg och numret på locket. Lampor: modulens färg är aktivt, kort vitt blink
är klart, gul och svart växling är fara. Etiketter använder samma ord som appen.

## C. Checklista

- [ ] Bara modulens färg och neutraler.
- [ ] Inga versaler, piller eller skuggade kort.
- [ ] Primärknappen är grafit.
- [ ] Varje steg ger en reaktion i scenen.
- [ ] Lead är en mening som börjar med ett verb.
- [ ] Inga utropstecken, ingen jag-form, inget beröm.
- [ ] ”Citat”, decimalkomma, mellanslag före enhet.
- [ ] Egen engelsk formulering.
- [ ] 400 px, ljust och mörkt, tangentbord, reducerad rörelse.
