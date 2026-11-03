# 5. Fysiska enheter

Idéspåning om hur modulerna kan styra och påverkas av riktiga saker på bordet.
Utgångspunkt: vi har tillgång till Raspberry Pi Pico W, kopplingsdäck, lysdioder, enklare sensorer
och motorer.

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

I stället för en ny konstruktion per modul använder vi **en standardnod** med olika delar
inkopplade. Valet är **Raspberry Pi Pico W** (eller Pico 2 W), eftersom den finns i lådorna,
har wifi och kör MicroPython.

```
┌──────────────────────────────┐
│  nod-04                      │      Nodens id står stort på locket
│                              │
│   ( statuslampa )            │      Blinkar vid ”Hitta” och när wifi tappas
│                              │
│   Pico W                     │      Wifi 2,4 GHz, MicroPython
│   + modulens delar           │      Sensorer på I²C (GP4/GP5), servo och lysdioder på PWM
│                              │
│   USB från powerbank         │      5 V, inget annat
└──────────────────────────────┘
```

Noden berättar själv vad den kan när den startar, till exempel
`{"har": ["led", "pot", "ina219"], "fw": "0.1"}`.
Ledaren kopplar en nod till en verkstad eller ett lag under fliken **Lådor** i rumsvyn.

Delar, kopplingar och meddelanden för varje låda finns i [dokument 7](07-modulplaner.md).

## Hur noden pratar med appen

| Väg | Fungerar med | Bra till | Nackdel |
|---|---|---|---|
| **Wifi och MQTT till rumsservern** | Alla deltagarenheter, även iPhone | Standardvalet. Alla mobiler i rummet når alla noder via servern | Kräver rumsserver och ett nät där noderna når den |
| Web Serial (USB-kabel) | Chrome och Edge på dator | Ledarens dator styr en enda demo-enhet utan server | Fungerar inte på iPhone, iPad eller i Firefox |
| Web Bluetooth | Chrome på dator och Android | En nod per deltagare utan nät | Fungerar inte på iPhone. Bluetooth på Pico W är nyare och mindre beprövat |

**Valt:** noderna ansluter via wifi till en MQTT-förmedlare (Mosquitto) på rumsservern.
MicroPython har en färdig MQTT-klient (`umqtt.simple`, installeras med `mip`). Rumsservern
översätter mellan MQTT och de WebSocket-meddelanden som webbläsarna redan använder (dokument 3).
Webbläsarna pratar alltså aldrig direkt med en nod, så en deltagare kan inte skicka egna kommandon
till lådorna.

Det passar ihop med ”Verkstan i en låda” (dokument 3), där en Raspberry Pi är router, rumsserver
och MQTT-förmedlare på en gång. Web Serial blir ett reservläge för ledarens egen demo.

Ämnen och meddelanden, i samma stil som rumsprotokollet:

```text
verkstan/<rum>/<nod>/hej        {"har": [...], "fw": "0.1"}   lådan startar (sparas, retain)
verkstan/<rum>/<nod>/status     "uppe" eller "borta"          "borta" skickas av förmedlaren om lådan tystnar (LWT)
verkstan/<rum>/<nod>/in/<sak>   från lådan, t.ex. in/pot {"v": 0.42}
verkstan/<rum>/<nod>/ut/<sak>   till lådan, t.ex. ut/led {"pwm": 0.61}
verkstan/<rum>/<nod>/ut/hitta   {}                            statuslampan blinkar i tre sekunder
```

Bara ASCII i ämnena (`strom`, inte `ström`).

## Firmware

**Valt:** MicroPython. Koden är lätt att läsa och kan visas för deltagarna. Varje låda kör samma
grundprogram (wifi, MQTT, ”Hitta”, återanslutning) och en liten fil med lådans beteende.
Ett första skelett finns i [`firmware/`](../firmware/). Det är otestat.

Undantaget är Ljudvågor, där ljud i realtid kan kräva C (Arduino-Pico) eller en DMA-lösning.

En idé som passar målgruppen: **öppna lådan**. Varje verkstad kan ha en knapp ”Visa koden i lådan”
som visar beteendefilen, med kommentarer på vardagssvenska.

## Format för workshoppen

| Format | Antal enheter | Passar när |
|---|---|---|
| **Demo** | 1 per modul | Ledaren visar för hela rummet, deltagarna styr från mobilen |
| **Station** | 1 per modul | Grupper roterar mellan bord. Bra för 20–40 personer |
| **Lagkit** | 1 per lag | Varje lag har en egen nod. Kräver flest enheter |
| **Personlig** | 1 per person | Bara för små grupper, eller med billiga noder |

## Hinder att planera för

- **iPhone saknar Web Serial och Web Bluetooth.** Allt som deltagare ska styra måste gå via server.
- **Nätverk.** Noder och mobiler måste nå rumsservern. Pico W kan bara 2,4 GHz och klarar inte
  eduroam eller gästnät med inloggningssida, och gästnät isolerar ofta enheter från varandra.
  En egen reserouter löser allt detta.
- **Säkerhet.** Bara låg spänning (5 V från USB). Inga nätanslutna lampor. Litiumbatterier
  laddas under uppsikt eller ersätts med powerbanks.
- **Tålighet.** 75 personer trycker hårt. Arkadknappar och skruvade kontakter håller bättre än
  kopplingsdäck.
- **Uppdateringar.** Med 20+ noder behöver firmware kunna uppdateras trådlöst.
- **Ihopparning.** Det måste vara enkelt att veta vilken låda som hör till vilken modul.
  Ett nummer på locket och att statuslampan blinkar när man trycker ”Hitta” i rumsvyn.
- **Reservläge.** Varje modul ska fungera fullt ut utan nod. Det fysiska är ett tillägg.

## Förslag på första steg

1. **Inventering.** Hur många Pico W finns, och vilka sensorer, servon och lysdiodsslingor?
2. **Logikgrindar** som första låda: två knappar och en lampa, kopplade via MQTT till en
   Mosquitto på en bärbar dator. Den visar hela kedjan med minst hårdvara.
3. **Paketresan** som första större bygge. Den syns för hela rummet.

Byggordning och budget för alla sju lådor finns i [dokument 7](07-modulplaner.md).
