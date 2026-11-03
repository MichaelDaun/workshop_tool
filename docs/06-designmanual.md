# 6. Designmanual

Den här manualen gäller allt som byggs i Verkstan: skärmar, texter och fysiska enheter.
Den är skriven så att både människor och AI-agenter kan följa den.
En visuell version finns i [`mockups/designmanual.html`](../mockups/designmanual.html).

Del A granskar de första mockuparna. Del B är själva manualen. Del C är en checklista.

---

## A. Granskning av mockuparna

De första mockuparna byggdes snabbt av en AI (Claude). De fungerar, men de bär tydliga spår av
hur språkmodeller brukar designa och skriva. Det här är de spåren, med exempel ur vår egen kod.

### Visuella drag

| Drag | Hos oss | Varför det är ett problem |
|---|---|---|
| Versala etiketter i monospace med extra spärrning ovanför varje rubrik | 26 ställen, t.ex. ”ALLT HÄNGER IHOP · TRYCK PÅ EN BUBBLA” | Ser tekniskt ut utan att säga något. Svårläst för ovana läsare |
| Kort i kort, alla med samma rundning och skugga | 8 skuggade ytor, kort inuti scenen i logik och matte | Allt blir lika viktigt. Hierarkin försvinner |
| Dekorativa pastellcirklar | Bilderna på modulkorten på startsidan | Fyller ut men betyder ingenting |
| Pillerformade knappar och etiketter överallt | `999px` på 9 ställen, ”10 min”, ”Solo · Lag” | Ett vanligt mallutseende |
| Tre ord, tre färger, tre punkter | ”Prova. Se. Förstå.” | Den vanligaste sloganformen i genererade sidor |
| Konfetti och notis vid varje avklarat uppdrag | Alla moduler | Belöningen är generisk. Notisen täcker innehållet på mobil |
| Alla sju ämnesfärger samtidigt, starkt mättade | Startsidan, kartan, rumsvyn | Det ser ut som en barnapp och färgen slutar betyda något |
| Färger som krockar med betydelser | Mjukvarans grönt ≈ ”rätt”-grönt, AI:s korall ≈ ”fel”-rött, ellärans bärnsten ≈ varning | Deltagaren kan inte veta om grönt betyder ”mjukvara” eller ”rätt” |
| Ett ”personligt” rubriktypsnitt ovanpå läsbarhetstypsnittet | Bricolage Grotesque för rubriker | Ett typiskt val för att se ”distinkt” ut. Tre familjer är en för mycket |
| Streckade rutor för ”kommer snart” och anteckningar | Idékort, mockup-noter | Ser oavslutat ut |
| Frågetecken som blir utropstecken | ”Vad hände?” | Gulligt men generiskt |

### Språkliga drag

| Drag | Hos oss | Bättre |
|---|---|---|
| Fetstilt inledning på varje stycke | 44 gånger, t.ex. ”**Batterier knuffar.** Fler batterier …” | Vanliga meningar. Fetstil bara på det enda ord som är nytt |
| Beröm av personen | ”Du tänker redan som en datorkonstruktör.” | Beskriv vad som hände: ”Alla gåtor lösta. Båda grindarna fungerar.” |
| Utropstecken | ”Rätt!”, ”Var snabb!”, ”Du är med!” | Punkt. Utropstecken bara i ljudord i scenen (”Poff”) |
| Maskinen talar i jag-form | ”Jag tror: Citron (67 %)” | ”Maskinens gissning: citron, 67 %”. Särskilt viktigt i AI-modulen, där vi vill motverka bilden av att AI ”tänker” |
| Engelska citattecken i svensk text | Dokumenten använder "så här" | Svenska citattecken: ”så här” |
| Allt i tabeller, alla avsnitt lika långa | Dokumenten 1–4 | Tabell när det finns rader att jämföra. Annars text |

Det som fungerar och ska behållas: scenen först, en färg per ämne för att hitta rätt,
riktiga enheter, metaforer som går att slå av, båda språken, respekt för rörelsekänslighet,
och ordvitsar som är genuint svenska (”Paketresan”).

---

## B. Manualen

### Grundidé: arbetsbänken

Verkstan ska se ut som en välordnad arbetsbänk. Det är världen där tekniken faktiskt byggs:
skärmatta med rutnät, kopplingsscheman, mätinstrument, etiketter på komponenter och
varningstejp. Vi lånar därifrån, men utan att göra det kitschigt. Inga skruvhuvuden eller
falska trästrukturer.

Tre följder av det:

1. **Scenen är bänken.** Det man arbetar med ligger på en yta med svagt rutnät. Resten av
   gränssnittet är verktyg runt omkring och ska vara tyst.
2. **Kontroller ser ut som instrument.** Reglage har skala och enhet som en mixerpult.
   Brytare ser ut som vippbrytare. Värden visas som på en multimeter.
3. **Färg är signal.** Färg används för det som är aktivt: strömmen som flyter, paketet som
   rör sig, brytaren som är på. Allt annat är grafit och papper.

### Färg

**Neutraler (bas för allt):**

| Token | Ljust | Mörkt | Används till |
|---|---|---|---|
| `--papper` | `#f3f4f1` | `#121514` | Sidans bakgrund |
| `--ark` | `#ffffff` | `#1a1e1d` | Scenen, paneler |
| `--rutnat` | `#e4e7e3` | `#242a28` | Rutnät på scenen, avdelare |
| `--linje` | `#cdd2cd` | `#343b38` | Kanter, inaktiva sladdar |
| `--blyerts` | `#5b6360` | `#9aa39f` | Sekundär text, etiketter |
| `--grafit` | `#1c2120` | `#e8ece9` | Text, linjer i illustrationer, primärknappar |

Neutralerna har en svag grön ton, som en skärmatta. Inte krämvit, inte blågrå.

**Ämnesfärger:** en per område. De är till för att *hitta* (kartan, kortet, modulens prick i
toppfältet) och för att visa *vad som är aktivt* i scenen.

| Område | Token | Ljust | Mörkt |
|---|---|---|---|
| Ellära | `--el` | `#d99a00` | `#f2b630` |
| Digital logik | `--logik` | `#16899b` | `#3cc0d0` |
| Signalteknik | `--signal` | `#6a4fd8` | `#9b86ff` |
| AI & ML | `--ai` | `#c8417a` | `#f06aa2` |
| Nätverk | `--nat` | `#2d6bd2` | `#6a9cff` |
| Mjukvara | `--kod` | `#3f8a3a` | `#6cc466` |
| Matematik | `--matte` | `#d9631c` | `#ff8f4a` |

Regler:

- Inne i en modul används **bara modulens egen färg** plus neutraler. Inga andra ämnesfärger.
- Ämnesfärgen täcker högst ungefär en tiondel av skärmen. Inga tonade bakgrundsytor,
  utom svagt för det valda alternativet i en grupp.
- Ämnesfärgen är aldrig ensam bärare av information. Den följs alltid av ikon eller namn.

**Lägen (betydelser):** vi använder *inte* rött och grönt för rätt och fel, eftersom det krockar
med ämnesfärgerna och är svårt för färgblinda.

| Läge | Utseende |
|---|---|
| Klart, lyckat | Bock (ritad, inte tecken) i modulens färg + en reaktion i scenen |
| Fara, för mycket | **Varningstejp:** diagonala ränder i grafit och gult `#f2c200` |
| Information | Grafit text, ingen färg |
| Inaktivt | `--linje`, inga ränder |

### Typografi

En enda familj, byggd för läsbarhet:
**Atkinson Hyperlegible Next** för all text och **Atkinson Hyperlegible Mono** för värden och enheter.
Familjen är framtagen av Braille Institute för personer med nedsatt syn. Det passar en publik
som ofta är ovan att läsa tekniska texter. Personligheten kommer från illustrationerna och
layouten, inte från ett speciellt rubriktypsnitt.

| Steg | Storlek | Vikt | Används till |
|---|---|---|---|
| Rubrik 1 | 40–48 px | 800 | Startsidans rubrik |
| Rubrik 2 | 28 px | 800 | Modulens namn |
| Rubrik 3 | 20 px | 700 | Avsnitt i panelen |
| Brödtext | 17 px | 400 | Allt löpande |
| Liten | 14 px | 400 | Etiketter, hjälptext |
| Värde | 22–32 px | Mono 600 | Mätvärden: 3,0 V, 0,46 A |

- Rubriker i meningsform (”Lagom ljus”, inte ”Lagom Ljus”).
- Inga versaler med spärrning. Etiketter skrivs i vanlig text i `--blyerts`.
- Mono används **bara** för siffror med enhet och för kod. Aldrig som dekoration.
- Radlängd för brödtext högst ca 60 tecken.

### Form

| Element | Rundning | Kant | Skugga |
|---|---|---|---|
| Scenen | 10 px | 1 px `--linje` | Ingen |
| Knappar, fält, reglage | 6 px | – | Ingen |
| Bilder på kort | 6 px | – | Ingen |
| Notis, dialog (svävar) | 10 px | – | En, mjuk |

- Ytor skiljs åt med luft och tunna linjer, inte med skuggade kort.
- Inga kort inuti kort.
- Knappar är rektanglar med liten rundning, inte piller.

### Komponenter

| Komponent | Utseende | Beteende |
|---|---|---|
| **Primärknapp** | Grafit platta, vit text, 48 px hög | En per vy. Ämnesfärgen är reserverad för scenen |
| **Sekundärknapp** | 1 px kant i grafit, ingen fyllning | – |
| **Fader** (reglage) | Spår med skalstreck, värde och enhet till höger | Värdet ändras medan man drar |
| **Vippbrytare** | Ritad vippa med ”0” och ”1” | Klick med kort ljud (valfritt) |
| **Stegare** | − och + med värdet mellan | Håll inne för att stega snabbt |
| **Mätare** | Mono-siffra med enhet och namn under, som en multimeter | Uppdateras live |
| **Protokoll** (uppdragen) | Numrerad lista. Nästa steg markerat med en linje i kanten | Bocken ritas när steget klaras |
| **Förklaring** | Fälls ut under scenen efter första avklarade steget | Högst tre korta stycken |

Uppdragen numreras eftersom de faktiskt är en ordning. Andra listor numreras inte.

### Ikoner och illustrationer

- Ett rutnät på 24 px, linjer 2 px med runda ändar. En stil för allt.
- Illustrationer i scenen ritas som **kopplingsscheman eller ritningar**: grafitlinjer,
  platta ytor i `--ark`, och modulens färg på det som är aktivt.
- Inga dekorativa former, inga gradienter. Undantag: ljus som lyser (lampans sken) får ha ett
  mjukt sken, eftersom det är det som faktiskt händer.
- Inga emoji. Bockar, kryss och pilar ritas som ikoner.

### Rörelse

- Rörelse i scenen ska visa orsak och verkan, och hastigheten ska betyda något
  (elektronerna går fortare när strömmen är större).
- Gränssnittet rör sig kort och lugnt: 150–220 ms, mjuk inbromsning.
- **Belöningen sker i scenen**: lampan blinkar till, roboten snurrar ett varv, maskinen
  öppnar locket. Ingen konfetti. Ingen notis som täcker innehållet.
- Med `prefers-reduced-motion` stängs all dekorativ rörelse av. Scenens rörelse ersätts av
  stillbilder med värden.

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ ←  ● Strömkretsen                               SV/EN   ◐   SU  │  toppfält, tyst
├───────────────────────────────────────────┬─────────────────────┤
│                                           │ Protokoll           │
│   SCENEN (bänken, rutnät)                 │ 1 ✓ Tänd lampan     │
│   minst 60 % av bredden                   │ 2 ▌ Gör den stark   │  ← nästa steg
│                                           │ 3   Lagom med 4 …   │
│   3,0 V      0,46 A      10 Ω             │                     │
│   ├──┼──┼──●──┼──┤  Motstånd     10 Ω     │ Förklaring          │
│                                           │ (fälls ut senare)   │
└───────────────────────────────────────────┴─────────────────────┘
```

- På mobil kommer protokollet under scenen, hopfällt till nästa steg.
- Startsidan visar kartan och listan över verkstäder. Ingen stor slogan.

---

### Språk: verkstadsrösten

Vi skriver som en bra slöjdlärare pratar: kort, konkret och vänligt, utan att överdriva.
Deltagarna är vuxna eller nästan vuxna och ska inte behandlas som barn.

**Regler**

1. **Beskriv världen, inte personen.** ”Lampan lyser. 0,9 A går genom tråden.” i stället för ”Snyggt jobbat!”
2. **Verb först i instruktioner.** ”Tryck på brytaren.” ”Dra reglaget åt höger.”
3. **Vardagsord först, fackord sedan, en gång.** ”Knuffen (spänningen) ökar.” Därefter räcker ”spänning”.
4. **Inga utropstecken** i gränssnittet. Undantag: ljudord i scenen.
5. **Maskiner talar inte i jag-form.** Varken AI:n, roboten eller appen.
6. **Inga slogans och inga triader.** Inga ”Prova. Se. Förstå.”, inga ”snabbt, enkelt och roligt”.
7. **Inga inskjutna tankstreck.** Skriv två meningar i stället.
8. **Inga ”inte X, utan Y”** och inga rubriker med kolon och avslöjande (”Elektricitet: mer än du tror”).
9. **Fetstil sparsamt**, bara på ett nytt begrepp första gången det dyker upp.
10. **Fel är information.** ”Roboten körde in i ett träd vid steg 3.” i stället för ”Fel!” eller ”Hoppsan!”.

**Längder**

| Text | Högst |
|---|---|
| Modulens namn | 3 ord |
| Introtext | 2 meningar |
| Ett steg i protokollet | 8 ord |
| Förklaring | 3 stycken, 2 meningar var |

**Ord vi undviker**

| Svenska | Engelska |
|---|---|
| magisk, magi | magic, magical |
| resa (om lärande) | journey |
| utforska, upptäck (som utfyllnad) | explore, discover (as filler) |
| dyk ner, låt oss | dive in, let's |
| kraftfull, sömlös, smidig | powerful, seamless, effortless |
| superenkelt, supercoolt | super easy, awesome |
| hemligheten bakom | the secret behind, unlock |
| värt att notera | worth noting, it's important to note |
| fantastiskt, grymt (som beröm) | amazing, great job |

Ordvitsar som bara fungerar på svenska är välkomna (”Paketresan”). De översätts inte
ord för ord. Den engelska versionen får en egen titel (”The packet journey” var för platt,
nu heter den ”Packet tour”).

**Svensk typografi**

- Citattecken: ”så här”. Apostrof: ’.
- Decimalkomma och mellanslag före enhet: 3,0 V, 0,46 A, 440 Hz.
- Tankstreck utan mellanslag i intervall: 10–15 min. Minus som −, inte bindestreck.
- Tusental med mellanslag: 75 000.

**Engelska:** brittisk stavning (colour, recognise), meningsform i rubriker,
samma ton som på svenska.

**Före och efter, ur mockuparna**

| Före | Efter |
|---|---|
| Prova. Se. Förstå. | Sju verkstäder om tekniken omkring dig |
| Jag tror: Citron (67 %) | Maskinens gissning: citron, 67 % |
| Rätt! Det var ett äpple. | Det var ett äpple. Gissningen stämde. |
| Fel! Det var ett äpple. Jag har inte sett nog med sådana. | Det var ett äpple. Maskinen har inga gröna äpplen bland sina exempel. |
| Aj! Där var en bugg. Ändra programmet och prova igen. | Roboten körde in i ett träd. Ändra programmet och kör igen. |
| Du tänker redan som en datorkonstruktör. | Alla gåtor lösta. |
| Poff! För mycket ström. Byt lampa och prova igen. | Poff. Lampan tålde inte strömmen. Byt lampa. |
| **Batterier knuffar.** Fler batterier betyder mer knuff (spänning). | Batterierna knuffar strömmen runt. Fler batterier ger mer knuff, det som kallas **spänning**. |

---

### Fysiska enheter

Samma manual gäller lådorna på bordet (se dokument 5):

- Lådan har modulens ämnesfärg. Locket är grafit med etikett i Atkinson Hyperlegible.
- Lamporna på lådan följer samma betydelser som skärmen: modulens färg betyder aktivt,
  ett kort vitt blink betyder klart, gul–svart växling betyder fara.
- Etiketter på knappar och uttag använder samma ord som appen (”A”, ”B”, ”Sensor”).
- Nummer på locket (”07”) matchar numret i appens rumsvy.

---

## C. Checklista för en ny modul

Ska kontrolleras av den som bygger, människa eller AI, före granskning:

- [ ] Bara modulens egen färg och neutraler används.
- [ ] Inga versala etiketter, inga piller, inga skuggade kort i scenen.
- [ ] Primärknappen är grafit. Färgen sitter på det aktiva i scenen.
- [ ] Varje steg i protokollet ger en synlig reaktion i scenen.
- [ ] Introtexten är högst två meningar och börjar med ett verb.
- [ ] Inga utropstecken, ingen jag-form, inget beröm av personen.
- [ ] Fackord introduceras med ett vardagsord först.
- [ ] Svenska citattecken, decimalkomma och mellanslag före enhet.
- [ ] Engelska texten har egen formulering, inte ordagrann översättning.
- [ ] Fungerar på 400 px bredd, i ljust och mörkt, med tangentbord och med reducerad rörelse.
