# 7. Modulplaner

Mål, steg och låda för varje verkstad. Mockuparna ligger i `mockups/moduler/`, firmware i
`firmware/`. Priserna är ungefärliga styckpriser hösten 2026.

## Gemensamt

**Standardnoden** (ca 200 kr): Raspberry Pi Pico W, powerbank 5 V, låda med numret på locket,
statuslampa med 220 Ω. Alla lådor kör `firmware/verkstan_nod/` och skiljer sig bara i filen under
`lador/`. Ljudlådan är undantaget och kör C++.

**Nät:** en egen reserouter med 2,4 GHz. Rumsservern kör Mosquitto och översätter till
WebSocket för webbläsarna, så att ingen deltagare kan styra en låda direkt.

```text
verkstan/<rum>/<nod>/hej       {"har": [...], "fw": "0.2"}   (retain)
verkstan/<rum>/<nod>/status    "uppe" / "borta"              (LWT)
verkstan/<rum>/<nod>/in/<sak>  från lådan
verkstan/<rum>/<nod>/ut/<sak>  till lådan, ut/hitta blinkar statuslampan
```

**Regler:** högst 5 V. Varje verkstad fungerar utan låda. Det som går sönder på skärmen går inte
sönder på riktigt. Lådan ska tåla 75 personer.

---

## Ellära

### Strömkretsen (`nod-01`, `lador/el.py`)

Mål: ström behöver en hel slinga, fler batterier trycker på mer, motstånd bromsar.

| Steg | Klart när |
|---|---|
| Tänd lampan | Brytaren sluten och ström över noll |
| Gör lampan stark | Visaren i det markerade fältet |
| Lagom ljus med 4 batterier | Fyra batterier och visaren i fältet |
| Se kretsen som vatten | Vattenvyn på |
| Ge lampan för mycket ström | Lampan går sönder på skärmen |

Lådan (ca 100 kr): lysdiod 10 mm, potentiometer 10 kΩ, INA219.

| Koppling | Stift |
|---|---|
| Lysdiod via INA219 och 100 Ω | GP15 |
| Potentiometer | GP26 |
| INA219 SDA / SCL | GP4 / GP5 |

`ut/led {"pwm": 0.61}`, `ut/poff {}`, `in/pot {"v": 0.42}`, `in/strom {"mA": 12.3}`.
INA219 mäter ett hoppande medel med PWM, så firmware tar medel av 20 mätningar.

### Ficklampan (ingen låda)

Mål: batterier i rad ger mer spänning, bredvid varandra räcker de längre. Lampor i rad delar på
spänningen.

| Steg | Klart när |
|---|---|
| Tänd båda lamporna | Båda lyser |
| Gör dem så starka det går | Båda får 3 W |
| Skruva ur en så att den andra slocknar | Lampor i rad, en skruvas ur |
| Minst 8 timmar | Båda lyser och batterierna räcker 8 h |

Riktiga batterihållare och lamphållare på bordet fungerar lika bra som en låda.

### Vad drar mest? (ingen låda)

Mål: watt är hur mycket just nu, räkningen är watt gånger timmar.

| Steg | Klart när |
|---|---|
| Mät vattenkokaren | Vattenkokaren inkopplad |
| Hitta det som drar minst | Mobilladdaren inkopplad |
| Jämför lamporna | Båda lamporna mätta |
| Något som drar lite men kostar mer än vattenkokaren | Till exempel kylskåpet |

En färdig energimätare för vägguttag (ca 150 kr) och några apparater. Inget eget bygge på 230 V.

## Digital logik

### Logikgrindar (`nod-02`, `lador/logik.py`)

Mål: en dator fattar beslut med OCH, ELLER och INTE.

| Steg | Klart när |
|---|---|
| Tänd lampan | Utgången har varit 1 |
| Fyll sanningstabellen | Fyra lägen med samma grind |
| Gåtan om kassaskåpet | OCH |
| Gåtan om trappljuset | XOR |

Lådan (ca 70 kr): två arkadknappar, tre lysdioder.

| Koppling | Stift |
|---|---|
| Knapp A, B | GP14, GP13 |
| Lampa ut, A, B | GP16, GP17, GP18 |

`in/knapp {"a": true, "b": false}`, `ut/grind {"typ": "xor"}`. Lådan räknar själv ut lampan.

### Åtta lampor (`nod-08`, `lador/binart.py`)

Mål: åtta bitar räcker till 0–255, och bokstäver är tal.

| Steg | Klart när |
|---|---|
| Visa 5 | 00000101 |
| Visa 100 | 01100100 |
| Visa det största talet | 255 |
| Skriv H | 72 |

I rummet håller åtta personer upp mobilen som var sin bit. Lådan (ca 60 kr): åtta lysdioder och
åtta tryckknappar.

| Koppling | Stift |
|---|---|
| Lysdioder 128 … 1 | GP2–GP9 |
| Knappar 128 … 1 | GP10–GP17 |

`in/bitar {"v": 72}`, `ut/bitar {"v": 72}`.

## Signalteknik

### Ljudvågor (`nod-03`, `firmware/nod03_ljud/`)

Mål: tonhöjd är hur ofta, styrka är hur långt. Två vågor läggs ihop, en motvåg släcker.

| Steg | Klart när |
|---|---|
| Spela ett ljud | Ljudet på |
| Gör tonen ljus | Över 600 Hz |
| Lägg linjen på målvågen | Summan nära målet |
| Släck ljudet med en motvåg | Samma ton och styrka, ett halvt varv förskjuten |

Bäst på dator. Lådan (ca 210 kr): PAM8302, högtalare 8 Ω, MAX9814, stapel med 8 WS2812.

| Koppling | Stift |
|---|---|
| Ljud ut till förstärkaren | GP18 |
| Mikrofon | GP26 |
| Stapel | GP22 |

`ut/vagor {"fa": 220, "aa": 0.7, "fb": 330, "ab": 0.5, "fas": 180, "spelar": true}`,
`in/mik {"hz": 8000, "prov": [256 värden]}` fem gånger per sekund. Skriven i C++ för Arduino-Pico
eftersom MicroPython inte hinner räkna fram ljud.

### Pixlar (`nod-09`, `lador/pixlar.py`)

Mål: en bild är ett rutnät av tal.

| Steg | Klart när |
|---|---|
| Zooma tills du ser rutorna | Rutnätet syns |
| Zooma tills du ser siffrorna | RGB-talen syns |
| Gör en pixel helt vit | 255, 255, 255 |
| Visa bilden med 8 × 8 pixlar | Upplösning 8 |

Lådan (ca 80 kr): matris med 8 × 8 WS2812 på GP22, som alltid visar bilden i 8 × 8.
`ut/bild {"px": "rrggbb…"}` med 64 färger. Styrkan begränsas till 15 %.

## AI

### Fruktsorteraren (`nod-04`, `lador/ai.py`)

Mål: en maskin lär sig av exempel, och skeva exempel ger skeva svar.

| Steg | Klart när |
|---|---|
| Lägg till fyra exempel | Fyra nya märken |
| Visa tre mystiska frukter | Tre gissningar |
| Känn igen ett grönt äpple | Grönt äpple gissas rätt |
| Lura maskinen | Ett äpple där den var säker på citron |

Lådan (ca 230 kr): TCS34725, lastcell 1 kg med HX711, servo SG90, knapp.

| Koppling | Stift |
|---|---|
| TCS34725 SDA / SCL | GP4 / GP5 |
| HX711 DT / SCK | GP16 / GP17 |
| Servo | GP15 |
| Knapp | GP14 |

`in/frukt {"farg": 0.82, "storlek": 0.64}` när vågen stått still en halv sekund, med
`"exempel": true` när knappen trycks. `ut/lucka {"mot": "apple"}`. Färgsensorn behöver en kåpa.

### Nästa ord (ingen låda)

Mål: en språkmodell räknar ut vilket ord som brukar komma härnäst.

| Steg | Klart när |
|---|---|
| Bygg en mening med fem ord | Fem ord |
| Välj ett ord maskinen tror lite på | Under 20 % |
| Låt maskinen skriva en mening | Fram till punkt |
| Lär den en ny mening | En egen mening inläst |

I rummet kan alla rösta på nästa ord från mobilen, och storskärmen visar rösterna som staplar.

## Nätverk

### Paketresan (`nod-05`, `lador/natverk.py`)

Mål: meddelanden delas i paket som hittar nya vägar när en kabel går sönder.

| Steg | Klart när |
|---|---|
| Skicka ett meddelande | Alla paket framme |
| Klipp en kabel och skicka igen | Framme via längre väg |
| Klipp medan paketen reser | Framme ändå |
| Gör så att inget kommer fram | Mottagaren avskuren |

Lådan (ca 250 kr): sju hus på en skiva, tio bitar LED-slinga med sex lysdioder var, en bygel på
varje kabel, nätagg 5 V 2 A.

| Koppling | Stift |
|---|---|
| LED-slinga | GP22 |
| Byglar | GP2–GP11 |

`in/kablar {"klippta": [9]}`, `ut/paket {"kabel": 3, "fran": "D", "till": "F", "t": 0.4}`.
Styrkan begränsas till 20 %.

### Hemliga färger (ingen låda)

Mål: två kan dela en hemlighet över en öppen linje, eftersom blandning inte går att ta isär.

| Steg | Klart när |
|---|---|
| Blanda och skicka | Blandningen syns på nätet |
| Få samma färg som vännen | Båda har blandat i sin hemlighet |
| Låt tjuvlyssnaren försöka | Tjuvlyssnarens blandning blir fel |
| Gör det igen med en annan färg | Ny hemlighet |

Fungerar också med riktig färg i muggar: alla ser de blandade muggarna men ingen kan ta isär dem.

## Mjukvara

### Robotens väg (`nod-06`, `lador/robot.py`)

Mål: ett program är instruktioner i ordning, och en bugg är när det gör något annat än man menade.

| Steg | Klart när |
|---|---|
| Nivå 1 | Framme |
| Kör in i ett träd | En krock |
| Nivå 2 | Framme |
| Nivå 3 med högst fem block | Framme |

Lådan (ca 230 kr): två 28BYJ-48 med ULN2003, hjul 60 mm, golvmatta 7 × 5 rutor à 15 cm.

| Koppling | Stift |
|---|---|
| Vänster motor IN1–IN4 | GP2–GP5 |
| Höger motor IN1–IN4 | GP6–GP9 |
| Stötfångare | GP14 |

`ut/program {"steg": ["F", "F", "V", "H"]}`, `in/steg {"i": 2, "klar": true}`, `in/krock {}`.
`RUTA` och `SVANG` i firmware justeras på mattan.

### Sortera (ingen låda)

Mål: olika metoder tar olika lång tid, och skillnaden växer med antalet.

| Steg | Klart när |
|---|---|
| Sortera 8 kort för hand | Sorterat |
| Kör bubbelsortering | Klar |
| Kör samsortering på samma kort | Klar |
| Jämför båda med 64 kort | Båda körda på 64 |

I rummet sorterar lag riktiga kort med olika metoder och tar tid.

## Matematik

### Funktionsmaskinen (`nod-07`, `lador/matte.py`)

Mål: en funktion är en regel, och ”gånger något plus något” blir en rak linje.

| Steg | Klart när |
|---|---|
| Mata maskinen med tre tal | Tre tal |
| Maskin 1 | in + 3 |
| Maskin 2 | in × 2 |
| Alla fyra | även in × 2 + 1 och in × 3 − 2 |

Lådan (ca 160 kr): vred KY-040, två TM1637, servo med lock.

| Koppling | Stift |
|---|---|
| Vred CLK / DT / knapp | GP10 / GP11 / GP12 |
| Display in CLK / DIO | GP2 / GP3 |
| Display ut CLK / DIO | GP4 / GP5 |
| Servo | GP15 |

`in/tal {"x": 4}`, `ut/visa {"in": 4, "ut": 11}`, `ut/lock {"oppen": true}`. Regeln finns bara
i rumsservern.

### Tärningar (`nod-10`, `lador/tarning.py`)

Mål: ett kast går inte att förutsäga, många kast går.

| Steg | Klart när |
|---|---|
| Kasta en tärning 10 gånger | 10 kast |
| Kasta tills staplarna är jämna | Minst 60 kast, lägsta stapeln över 75 % av den högsta |
| Vanligaste summan med två tärningar | 7, efter minst 100 kast |
| Klockan med tre tärningar | 300 kast |

”Hela rummet kastar” lägger till 75 kast. Lådan (ca 80 kr): en burk med MPU6050 och en TM1637.

| Koppling | Stift |
|---|---|
| MPU6050 SDA / SCL | GP4 / GP5 |
| Display CLK / DIO | GP2 / GP3 |

`in/kast {"v": [3, 5], "sum": 8}` när burken slutat skaka. `ut/tarningar {"antal": 2}`.

---

## Budget

| Låda | Med nod |
|---|---|
| nod-01 Strömkretsen | 300 kr |
| nod-02 Logikgrindar | 270 kr |
| nod-03 Ljudvågor | 410 kr |
| nod-04 Fruktsorteraren | 430 kr |
| nod-05 Paketresan | 450 kr |
| nod-06 Robotens väg | 430 kr |
| nod-07 Funktionsmaskinen | 360 kr |
| nod-08 Åtta lampor | 260 kr |
| nod-09 Pixlar | 280 kr |
| nod-10 Tärningar | 280 kr |
| Energimätare och router | 550 kr |
| **Ett set** | **ca 4 200 kr** |

## Byggordning

1. Logikgrindar. Visar hela kedjan från knapp till skärm.
2. Åtta lampor och Tärningar. Samma enkla delar.
3. Strömkretsen. Första sensorn.
4. Paketresan och Pixlar. Adresserbara lysdioder.
5. Funktionsmaskinen och Fruktsorteraren. Servo och fler sensorer.
6. Robotens väg. Mest mekanik.
7. Ljudvågor. Ljud i realtid.

## Öppna frågor

- Vilka delar finns redan?
- Var står rumsservern: ledarens dator eller en Raspberry Pi i lådan?
- Hur uppdateras firmware i tjugo lådor?
