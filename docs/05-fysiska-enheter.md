# 5. Fysiska enheter

Idéspåning om hur modulerna kan styra och påverkas av riktiga saker på bordet.
Utgångspunkt: vi har tillgång till många mikrokontroller och komponenter.

## Varför

En lampa som lyser på skärmen är en bild. En lampa som lyser på bordet när man drar i ett
reglage i mobilen gör kopplingen mellan kod och verklighet uppenbar. Det fysiska gör också
workshopen social: folk samlas runt en sak, pekar och provar.

Tre sätt att koppla ihop skärm och sak:

| Riktning | Exempel | Vad deltagaren lär sig |
|---|---|---|
| Skärm → sak | Reglaget i appen ändrar ljusstyrkan på en riktig lampa | Programvara styr hårdvara |
| Sak → skärm | En sensor mäter riktig ström och appen ritar den | Mätvärden blir data |
| Tvilling | Sak och skärm visar samma tillstånd, ändras det ena ändras det andra | Den digitala modellen beskriver verkligheten |

Tvillingen är den starkaste formen pedagogiskt: man kan peka på skärmen och säga ”det här är
vad som händer inuti lådan”.

## Idéer per modul

### Strömkretsen (ellära)
- **Kretsbrädan.** En riktig krets med lysdiod, potentiometer och strömsensor (INA219).
  Skärmen ritar exakt det som mäts. Vrid på potentiometern så rör sig elektronerna i appen.
- **Lampan som går sönder.** Appen styr en LED-slinga. När ”lampan spricker” på skärmen blinkar
  slingan och släcks. Ingen riktig överbelastning, bara låg spänning.
- **Ledare eller isolator.** Två kontaktspetsar på bordet. Deltagarna håller dit gem, sudd eller
  en citron och appen visar resistansen.

### Logikgrindar (digital logik)
- **Stora knappar.** Två arkadknappar (A och B) och en lampa. Grinden väljs i appen.
  Fungerar som stationsövning för ett lag.
- **Grindlådor.** Små lådor med två ingångar och en utgång, där appen bestämmer vilken grind
  lådan är. Deltagarna kopplar ihop lådorna med sladdar och bygger en adderare på bordet.
- **Binära rummet.** Åtta lampor i rad på väggen. Varje lampa styrs av en deltagares mobil.
  Rummet visar talet tillsammans.

### Ljudvågor (signalteknik)
- **Visslingsskopet.** Mikrofon (INMP441) på en mikrokontroller skickar riktiga ljudvågor
  till appen. Vissla, sjung eller klappa och se vågen.
- **Riktig högtalare.** Appens toner spelas i en högtalare på bordet, så alla i rummet hör
  när någon släcker ljudet med en motvåg.
- **Handtermin.** En avståndssensor styr tonhöjden. Handen blir ett reglage.

### Fruktsorteraren (AI)
- **Färgsensorn.** En färgsensor (TCS34725) läser av riktiga frukter eller färgade klossar.
  Punkten hamnar på AI-kartan med den uppmätta färgen. Sedan får AI:n gissa nästa sak man
  håller fram.
- **Trollstaven.** En pinne med accelerometer. Deltagarna spelar in rörelser (cirkel, sicksack)
  och tränar en modell som känner igen dem. Bra för att visa att AI lär sig av exempel, och
  att den blir sämre om bara en person har spelat in allt.

### Paketresan (nätverk)
- **Nätverket på bordet.** Sju små noder (hus) med en LED-ring var, ihopkopplade med LED-slingor
  som kablar. Paketen syns som ljuspunkter som vandrar mellan husen, samtidigt som på skärmen.
  Dra ur en kabel (magnetkontakt) så tar ljuset en omväg.
- **Människonätverket med lampor.** Varje deltagare får en nod i handen. Ett paket kommer fram
  som ljus i ens egen nod, och man skickar det vidare genom att trycka.

### Robotens väg (mjukvara)
- **Robot på golvmatta.** En liten robot på hjul kör programmet på en tryckt rutmatta, samtidigt
  som roboten på skärmen. Krocka med ett riktigt träd (kartongbit).
- **Programkort.** Instruktionerna är fysiska kort med NFC-tagg. Lägg korten i rad framför en läsare
  så byggs programmet i appen. Fungerar för personer som tycker att skärmar är krångliga.

### Funktionsmaskinen (matematik)
- **Lådan med vred.** En låda med vridratt (in), sifferdisplay (ut) och en servomotor som snurrar
  kugghjul medan maskinen räknar. Den hemliga regeln ställs in från ledarens skärm.
- **Tärningsburkar.** Burkar med accelerometer som deltagarna skakar. Varje skak blir ett
  tärningskast i appen, och 75 personers kast bildar en kurva på storskärmen.

### För hela rummet
- **Rumslampan.** En stor LED-lampa eller ljusslinga i rummet som visar läget:
  röstningsresultat som färger, en våg av ljus när någon klarar en modul, eller nedräkning.
- **Stationsskylt.** En liten display vid varje station som visar vilken modul som körs och
  hur många som är där.

## Gemensam plattform: Verkstan-noden

I stället för en ny konstruktion per modul föreslår vi **en standardnod** som alla moduler
kan använda, med olika sensorer inkopplade.

```
┌──────────────────────────────┐
│  VERKSTAN-NOD                │
│                              │
│   ( LED-ring, 12 lysdioder ) │      Mikrokontroller med wifi och Bluetooth
│                              │      (t.ex. ESP32-S3)
│   [ A ]            [ B ]     │      2 knappar
│                              │      USB-C för ström och programmering
│  ◦ sensoruttag (I²C)         │      Standardiserat uttag (Qwiic/STEMMA QT)
│  ◦ utgång (PWM / servo)      │      för färg, ljud, ström, rörelse ...
│                              │
│  Låda i modulens färg        │
└──────────────────────────────┘
```

Noden berättar själv vad den kan när den startar, till exempel
`{ "id": "nod-07", "har": ["led_ring", "knapp_a", "knapp_b", "fargsensor"] }`.
Modulen säger vad den behöver, och ledaren kopplar en nod till en modul eller ett lag i rumsvyn.

Med samma låda, samma firmware och samma kontakter blir det enklare att bygga, laga och byta ut.

## Hur noden pratar med appen

| Väg | Fungerar med | Bra till | Nackdel |
|---|---|---|---|
| **Wifi till rumsservern** (WebSocket eller MQTT) | Alla deltagarenheter, även iPhone | Standardvalet. Alla mobiler i rummet når alla noder via servern | Kräver rumsserver och att noderna når nätet |
| Web Serial (USB-kabel) | Chrome och Edge på dator | Ledarens dator styr en enda demo-enhet utan server | Fungerar inte på iPhone, iPad eller i Firefox |
| Web Bluetooth | Chrome på dator och Android | En nod per deltagare utan nät | Fungerar inte på iPhone |
| ESP-NOW (radio mellan noder) | Noderna själva | Nätverket på bordet, noder pratar direkt | Bara mellan noder, inte med mobiler |

**Förslag:** noderna ansluter till rumsservern via wifi. Då fungerar det på alla deltagares
mobiler, och det passar ihop med ”Verkstan i en låda” (dokument 3), där en Raspberry Pi
är både wifi, rumsserver och meddelandeförmedlare. Web Serial blir ett reservläge för ledarens
egen demo när det inte finns någon server.

Utkast till meddelanden, i samma stil som rumsprotokollet:

```jsonc
// nod → server
{ "t": "hello", "id": "nod-07", "har": ["led_ring", "fargsensor"] }
{ "t": "sensor", "id": "nod-07", "fargsensor": { "r": 212, "g": 48, "b": 40 } }
{ "t": "knapp", "id": "nod-07", "knapp": "a", "nere": true }

// server → nod
{ "t": "led", "id": "nod-07", "ring": "fyll", "farg": "modul", "styrka": 0.6 }
{ "t": "ut",  "id": "nod-07", "pwm": 0.42 }
```

## Firmware

| Alternativ | För | Emot |
|---|---|---|
| MicroPython eller CircuitPython | Koden är lätt att läsa och kan visas för deltagarna (”så här ser programmet i lådan ut”) | Något långsammare, mindre bra för ljud i realtid |
| Arduino (C++) | Snabbt, stort utbud av bibliotek | Svårare att visa för nybörjare |
| ESPHome | Mycket lite kod, konfiguration i YAML | Mindre flexibelt för egna beteenden |

En idé som passar målgruppen: **öppna lådan**. Varje modul har en knapp ”Visa koden i lådan”
som visar det korta program som körs på noden, med kommentarer på vardagssvenska.

## Format för workshoppen

| Format | Antal enheter | Passar när |
|---|---|---|
| **Demo** | 1 per modul | Ledaren visar för hela rummet, deltagarna styr från mobilen |
| **Station** | 1 per modul | Grupper roterar mellan bord. Bra för 20–40 personer |
| **Lagkit** | 1 per lag | Varje lag har en egen nod. Kräver flest enheter |
| **Personlig** | 1 per person | Bara för små grupper, eller med billiga noder |

## Hinder att planera för

- **iPhone saknar Web Serial och Web Bluetooth.** Allt som deltagare ska styra måste gå via server.
- **Nätverk.** Noder och mobiler måste vara på samma nät. Gästnät isolerar ofta enheter från
  varandra. Egen router löser det.
- **Säkerhet.** Bara låg spänning (5 V från USB). Inga nätanslutna lampor. Litiumbatterier
  laddas under uppsikt eller ersätts med powerbanks.
- **Tålighet.** 75 personer trycker hårt. Arkadknappar och skruvade kontakter håller bättre än
  kopplingsdäck.
- **Uppdateringar.** Med 20+ noder behöver firmware kunna uppdateras trådlöst.
- **Ihopparning.** Det måste vara enkelt att veta vilken låda som hör till vilken modul.
  Färgen på lådan, ett nummer på locket och att LED-ringen blinkar när man trycker ”Hitta” i appen.
- **Reservläge.** Varje modul ska fungera fullt ut utan nod. Det fysiska är ett tillägg.

## Förslag på första steg

1. **Inventering.** Vilka mikrokontroller finns (ESP32, Raspberry Pi Pico W, Arduino Uno, micro:bit)?
   Det avgör om wifi-vägen fungerar direkt.
2. **En prototypnod** med LED-ring och två knappar, kopplad till **Logikgrindar** via Web Serial.
   Liten insats, och den visar hela idén.
3. **Nätverket på bordet** som första större bygge. Det är den mest visuella idén och den kan
   visas för hela rummet.
