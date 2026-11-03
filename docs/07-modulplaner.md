# 7. Modulplaner

En plan per verkstad: vad deltagaren ska förstå, vad som händer på skärmen, stegen i protokollet,
hur det fungerar i lag och vad lådan på bordet innehåller. Mockuparna i `mockups/moduler/` följer
planerna. Hårdvaran bygger på dokument 5 och utgår från Raspberry Pi Pico W med wifi.

Priserna är ungefärliga styckpriser i kronor från svenska hobbybutiker hösten 2026. Kontrollera
mot leverantören innan ni beställer. Mycket finns troligen redan i lådorna.

## Gemensamt för alla lådor

### Standardnoden

| Del | Antal | Ca pris | Kommentar |
|---|---|---|---|
| Raspberry Pi Pico W (eller Pico 2 W) | 1 | 90–110 kr | Wifi på 2,4 GHz. Stifthuvuden fastlödda |
| Kopplingsdäck, halvstort | 1 | 40 kr | Bara för prototyp. Lödda kort i lådorna som används ofta |
| Powerbank 5 V, minst 5 000 mAh | 1 | 100–150 kr | Räcker en heldag för allt utom roboten |
| Låda (plast eller kartong) med nummer på locket | 1 | 0–60 kr | Nodens id står stort på locket, till exempel `nod-04` |
| Lysdiod för status + 220 Ω | 1 | 2 kr | Blinkar vid ”Hitta” och när wifi tappas |

Alla lådor kör samma grundprogram (se `firmware/`) och skiljer sig bara i vilka delar som sitter i
och en liten fil med lådans beteende.

### Nät

- **Egen router.** Pico W kan bara 2,4 GHz och klarar inte inloggning som eduroam eller
  gästnät med webbsida. En reserouter (ca 300–500 kr) med ett eget nät, till exempel `verkstan`,
  löser det och fungerar likadant i varje lokal.
- **Rumsservern** kör en MQTT-förmedlare (Mosquitto). Lådorna pratar MQTT med den. Webbläsarna
  pratar inte MQTT direkt, de går via rumsservern som översätter till samma WebSocket-meddelanden
  som resten av rummet använder (dokument 3). Då kan ingen deltagare skicka egna kommandon till
  en låda.
- **Ämnen** (topics) följer ett mönster:
  `verkstan/<rum>/<nod>/<riktning>/<sak>`, där riktning är `in` (från lådan) eller `ut` (till lådan).
  Bara ASCII i ämnena, alltså `strom` och inte `ström`.

```text
verkstan/VERK-42/nod-01/hej        {"har": ["led", "pot", "ina219"], "fw": "0.1"}   (sparas, retain)
verkstan/VERK-42/nod-01/status     "uppe" / "borta"                                 (sista vilja, LWT)
verkstan/VERK-42/nod-01/in/pot     {"v": 0.42}
verkstan/VERK-42/nod-01/ut/led     {"pwm": 0.61}
verkstan/VERK-42/nod-01/ut/hitta   {}
```

### Ihopparning

Ledaren ser alla lådor under fliken **Lådor** i rumsvyn (`mockups/rum.html`) och väljer vilken
verkstad eller vilket lag varje låda hör till. ”Hitta” får lådans statuslampa att blinka i tre
sekunder. En ny låda dyker upp när man håller in dess knapp vid start. Om en låda tappar kontakten
visas varningstejp i listan, och verkstaden fortsätter att fungera på skärmen.

### Regler för alla lådor

- Bara 5 V och lägre. Inga nätanslutna lampor eller motorer.
- Varje verkstad fungerar fullt ut utan låda. Lådan är ett tillägg.
- Det som går sönder på skärmen går aldrig sönder på riktigt. Lampan som ”spricker” i Strömkretsen
  blinkar och släcks.
- Lådan ska tåla att 75 personer har tryckt på den. Arkadknappar, skruvade kontakter och
  dragavlastade sladdar.

---

## 1. Strömkretsen (ellära, `nod-01`)

**Mål:** förstå att ström behöver en hel slinga, att fler batterier trycker på mer och att
motstånd bromsar. Ohms lag kommer sist, som en sammanfattning av det man redan sett.

**Scenen:** en krets med batterier, motstånd, lampa och brytare. Elektroner rör sig längs tråden
i en takt som följer strömmen. En ljusmätare visar ”lagom” som ett markerat fält och för mycket
som varningstejp. Vattenvyn byter batteriet mot en pump och motståndet mot ett smalt rör.

| Steg | Deltagaren gör | Klart när |
|---|---|---|
| 1 | Tänd lampan | Brytaren är sluten och strömmen är över noll |
| 2 | Gör lampan stark | Visaren når det markerade fältet |
| 3 | Lagom ljus med exakt 4 batterier | Fyra batterier och visaren i fältet, alltså har motståndet ändrats |
| 4 | Se kretsen som vatten | Vattenvyn är påslagen |
| 5 | Ge lampan för mycket ström | Lampan går sönder på skärmen |

**I lag:** tre personer delar en krets. En styr batterierna, en motståndet och en brytaren, var
och en från sin mobil. De måste prata för att hitta lagom ljus.

**Lådan:** en riktig lysdiod lyser lika starkt som lampan på skärmen. Vrider man på lådans ratt
ändras motståndet i appen. En strömsensor mäter den verkliga strömmen genom lysdioden, och appen
visar den bredvid den beräknade.

| Del | Ca pris |
|---|---|
| Standardnod | se ovan |
| Lysdiod 10 mm, varmvit, + 100 Ω | 5 kr |
| Potentiometer 10 kΩ med ratt | 20 kr |
| Strömsensor INA219 (I²C) | 60–90 kr |
| **Summa utöver nod** | **ca 100 kr** |

| Koppling | Stift på Pico W |
|---|---|
| Lysdiod via INA219 och 100 Ω | GP15 (PWM) |
| Potentiometer, mittben | GP26 (ADC0), ytterben till 3V3 och GND |
| INA219 SDA / SCL | GP4 / GP5 (I2C0) |

**Beteende**

| Riktning | Vad |
|---|---|
| Skärm → låda | `ut/led {"pwm": 0..1}` beräknas ur strömmen i appen. `ut/poff {}` får lysdioden att blinka snabbt i en sekund och släckas |
| Låda → skärm | `in/pot {"v": 0..1}` blir motståndet i appen. `in/strom {"mA": 12.3}` visas som uppmätt ström |

**Att bygga:** koppla på kopplingsdäck, prova med `firmware/`-skelettet, löd sedan på ett
experimentkort och skruva fast i lådan. Ratten ska sitta på locket.

**Risker:** PWM gör att INA219 mäter ett medelvärde som hoppar. Läs av 20 gånger och ta medel.
Lysdiodens ljus ökar inte linjärt med strömmen, så ljusstyrkan behöver en korrigeringskurva för
att se ut som skärmen.

---

## 2. Logikgrindar (digital logik, `nod-02`)

**Mål:** förstå att en dator fattar beslut med enkla regler som OCH, ELLER och INTE, och att
några få sådana regler räcker för att räkna.

**Scenen:** två vippbrytare A och B, en grind i mitten och en lampa. Ledningarna fylls i ämnesfärg
när de bär en etta. Sanningstabellen fylls i medan man provar. Gåtor om ett kassaskåp (OCH) och
trappljus (XOR) knyter grindarna till vardagen.

| Steg | Deltagaren gör | Klart när |
|---|---|---|
| 1 | Tänd lampan | Utgången har varit 1 |
| 2 | Fyll hela sanningstabellen | Alla fyra lägen provade med samma grind |
| 3 | Lös gåtan om kassaskåpet | Rätt grind vald i gåtan |
| 4 | Lös gåtan om trappljuset | Rätt grind vald i gåtan |

**Med hela rummet:** varje deltagare är en grind i sin mobil. Storskärmen ritar sladdarna mellan
dem, och tillsammans bygger rummet en halvadderare som räknar 1 + 1.

**Lådan:** två stora arkadknappar och en lampa. Vilken grind lådan är väljs i appen. Knapparna i
ritningen på skärmen går att trycka på, och de riktiga knapparna ändrar A och B i appen.

| Del | Ca pris |
|---|---|
| Arkadknapp 30 mm | 2 × 30 kr |
| Lysdiod 10 mm + 100 Ω (eller arkadknapp med inbyggd lampa) | 5 kr |
| Två små lysdioder som visar A och B | 2 kr |
| **Summa utöver nod** | **ca 70 kr** |

| Koppling | Stift |
|---|---|
| Knapp A, knapp B (till GND, intern pull-up) | GP14, GP13 |
| Utgångslampa | GP16 |
| Lampa för A, för B | GP17, GP18 |

**Beteende:** `in/knapp {"a": true, "b": false}` vid varje ändring. `ut/grind {"typ": "xor"}`
när grinden byts. Lådan räknar själv ut lampan, så den fungerar även om nätet hackar.

**Risker:** knappar studsar. 20 ms avstudsning i firmware.

**Nästa steg:** ”grindlådor” med två ingångar och en utgång som kopplas ihop med sladdar på
bordet, så att ett lag bygger en adderare med fyra lådor.

---

## 3. Ljudvågor (signalteknik, `nod-03`)

**Mål:** se att ljud är en rörelse fram och tillbaka, att tonhöjd är hur ofta och styrka är hur
långt. Två vågor läggs ihop, och en motvåg kan släcka ljud.

**Scenen:** ett oscilloskop med högtalaren ritad som schema till vänster. Våg A är heldragen,
våg B streckad och summan tjock i ämnesfärg. En målvåg visas som ett brett, ljust band. Riktigt
ljud spelas via Web Audio.

| Steg | Deltagaren gör | Klart när |
|---|---|---|
| 1 | Spela ett ljud | Ljudet är på |
| 2 | Gör tonen riktigt ljus | Över 600 Hz |
| 3 | Lägg linjen på målvågen | Summan ligger nära målvågen |
| 4 | Släck ljudet med en motvåg | Samma ton och styrka, förskjuten ett halvt varv |

Reglagen ”fastnar” nära samma värde som våg A, annars blir motvågen nästan omöjlig att träffa.
Modulen är märkt ”bäst på dator” eftersom mobilhögtalare inte återger låga toner.

**I lag:** varje person styr en våg från sin mobil. Tillsammans bygger de ett ackord, eller
släcker ett brummande ljud som spelas i högtalaren på bordet.

**Lådan:** en högtalare som spelar samma ljud som appen så att hela bordet hör, och en stapel med
åtta lysdioder som visar styrkan. En mikrofon gör det möjligt att vissla och se sin egen våg.

| Del | Ca pris |
|---|---|
| Förstärkare PAM8302 (mono, 2,5 W) | 60 kr |
| Högtalare 8 Ω, 0,5–1 W, ca 50 mm | 30 kr |
| Mikrofon med förstärkning MAX9814 | 70 kr |
| Stapel med 8 adresserbara lysdioder (WS2812) | 50 kr |
| **Summa utöver nod** | **ca 210 kr** |

| Koppling | Stift |
|---|---|
| Ljud ut (PWM) till förstärkaren | GP18 |
| Mikrofon ut | GP26 (ADC0) |
| Lysdiodsstapel, data | GP22 |

**Beteende:** appen skickar inte ljudet, bara inställningarna:
`ut/vagor {"fa": 220, "aa": 0.7, "fb": 330, "ab": 0.5, "fas": 180, "spelar": true}`.
Lådan räknar fram ljudet själv. Mikrofonen skickar korta block:
`in/mik {"hz": 8000, "prov": [ ... 256 värden ... ]}` fem gånger per sekund.

**Risker:** det här är den enda lådan där MicroPython inte räcker för att räkna fram ljud i
realtid. Förslag: en färdigräknad vågtabell som spelas med DMA, eller C (Arduino-Pico) för just
den här lådan. Motvågen släcker sällan helt i ett rum, eftersom ljudet studsar. Det är värt att
säga högt, det förklarar varför brusreducerande hörlurar sitter nära örat.

---

## 4. Fruktsorteraren (AI och maskininlärning, `nod-04`)

**Mål:** förstå att en maskin lär sig av exempel, att den bara kan det den har sett och att
skeva exempel ger skeva svar.

**Scenen:** en karta där åt höger betyder rödare och uppåt betyder större. Varje exempel är en
citron (oval) eller ett äpple (rund med skaft). Ytan där maskinen skulle svara äpple är tonad.
En mystisk frukt får streckade linjer till sina närmaste grannar, och maskinens gissning visas som
”Äpple, 67 %”. Maskinen pratar aldrig i jag-form.

| Steg | Deltagaren gör | Klart när |
|---|---|---|
| 1 | Lägg till fyra egna exempel | Fyra nya märken på kartan |
| 2 | Visa maskinen tre mystiska frukter | Tre gissningar |
| 3 | Få den att känna igen ett grönt äpple | Ett grönt äpple gissas som äpple |
| 4 | Lura den med ett felaktigt exempel | Ett äpple läggs där maskinen var säker på citron |

Den andra mystiska frukten är alltid ett grönt äpple, så att alla möter skevheten.

**Med hela rummet:** alla lägger till frukt från mobilen på en gemensam karta (fliken Klassens AI
i rumsvyn). Variant: halva rummet får bara röda äpplen, sedan byter halvorna maskin och jämför.

**Lådan:** en köksvåg med färgsensor och en lucka över två lådor. Lägg en riktig frukt (eller en
färgad boll) på vågen. Vikten blir storlek och färgsensorn blir färg, märket hamnar på kartan och
servot vinklar luckan mot den låda maskinen väljer.

| Del | Ca pris |
|---|---|
| Färgsensor TCS34725 med egen lysdiod | 90–120 kr |
| Lastcell 1 kg + förstärkare HX711 | 60–90 kr |
| Servo SG90 | 40 kr |
| Två plastlådor, en lucka i kartong eller 3D-utskrift | 0–40 kr |
| **Summa utöver nod** | **ca 230 kr** |

| Koppling | Stift |
|---|---|
| TCS34725 SDA / SCL | GP4 / GP5 |
| HX711 DT / SCK | GP16 / GP17 |
| Servo, signal (ström från VBUS 5 V) | GP15 |
| Knapp ”lägg in som exempel” | GP14 |

**Beteende:** `in/frukt {"farg": 0.82, "storlek": 0.64}` när vågen har stått still i en halv
sekund. `ut/lucka {"mot": "apple"}` när appen har gissat.

**Risker:** färgsensorn påverkas av rummets ljus. Sensorn ska sitta i en liten kåpa och mäta på
2 cm avstånd. Vågen måste nollställas vid start. Riktiga gröna äpplen och citroner är lika i vikt,
vilket är bra: då syns det att färg ensam inte räcker.

---

## 5. Paketresan (nätverk, `nod-05`)

**Mål:** förstå att meddelanden delas upp i paket, att varje router skickar paketet ett steg
närmare och att många kablar gör nätet tåligt.

**Scenen:** sju hus (Ali till Gus) och tio kablar. Kortaste vägen just nu ritas tjock i ämnesfärg.
Paketen är små rutor med en bokstav var. En klippt kabel ritas prickad. Ett paket som är på väg
över en kabel som klipps vänder tillbaka och letar en ny väg.

| Steg | Deltagaren gör | Klart när |
|---|---|---|
| 1 | Skicka ett meddelande | Alla paket framme |
| 2 | Klipp en kabel på vägen och skicka igen | Alla paket framme via en längre väg |
| 3 | Klipp en kabel medan paketen reser | En kabel klipps under resan och alla kommer fram ändå |
| 4 | Gör så att inget kommer fram | Mottagaren är avskuren |

**Med hela rummet:** varje deltagare är en router i mobilen och skickar paket vidare med ett tryck.
Ledaren klipper kablar på storskärmen och rummet får hitta nya vägar.

**Lådan:** ”nätverksbordet”. Sju små hus i kartong på en skiva, och tio bitar LED-slinga som
kablar. Paketen syns som ljuspunkter som vandrar mellan husen samtidigt som på skärmen. Varje
kabel har en bygelkontakt mitt på. Dra ur den så är kabeln klippt, både på bordet och i appen.

| Del | Ca pris |
|---|---|
| LED-slinga WS2812, 60 per meter, 1 m | 100–150 kr |
| Tio bygelkontakter (stifthuvud + bygel) | 20 kr |
| Nätagg 5 V 2 A i stället för powerbank | 80 kr |
| Skiva ca 60 × 40 cm, kartong till husen | 0–50 kr |
| **Summa utöver nod** | **ca 250 kr** |

| Koppling | Stift |
|---|---|
| LED-slinga, data (alla bitar i serie) | GP22 |
| Tio bygelkontakter (till GND, intern pull-up) | GP2–GP11 |

**Beteende:** `in/kablar {"klippta": [9]}` vid varje ändring.
`ut/paket {"kabel": 3, "fran": "D", "till": "F", "t": 0.4}` skickas tio gånger per sekund medan
paketen reser. Lådan tänder punkten på rätt ställe på slingan.

**Risker:** 60 lysdioder på full styrka drar över 3 A. Begränsa styrkan i firmware till 20 %.
3,3 V datasignal fungerar oftast till WS2812 på korta avstånd, annars behövs en nivåomvandlare
(74AHCT125, ca 15 kr). Kablarna ska kunna lossas från skivan för transport.

---

## 6. Robotens väg (mjukvara, `nod-06`)

**Mål:** förstå att ett program är en lista instruktioner som körs i ordning, att en bugg är när
programmet gör något annat än man menade och att en loop sparar arbete.

**Scenen:** ett rutnät 7 × 5 med träd och en stjärna. Programmet byggs av block (Framåt, Sväng
vänster, Sväng höger). Ett Framåt-block kan upprepas ×2 till ×5. Under körningen markeras blocket
som körs. Vid krock markeras blocket där det gick fel med varningstejp, och statusraden säger vilket
nummer det har.

| Steg | Deltagaren gör | Klart när |
|---|---|---|
| 1 | Nivå 1: nå stjärnan | Roboten står på stjärnan |
| 2 | Kör in i ett träd med flit | En krock |
| 3 | Nivå 2: sväng åt rätt håll | Roboten står på stjärnan |
| 4 | Nivå 3: högst fem block | Framme med fem block eller färre |

**I par:** en person ser kartan, den andra skriver programmet utan att se den. Sedan kör roboten
på golvet det de har kommit överens om.

**Lådan:** en liten robot på en golvmatta med samma rutnät. Stegmotorer gör att roboten kör exakt
en ruta och svänger exakt 90 grader utan extra sensorer. Den är långsam, ungefär tre sekunder per
ruta, vilket gör det lätt att följa med.

| Del | Ca pris |
|---|---|
| Stegmotor 28BYJ-48 med drivkort ULN2003 | 2 × 40 kr |
| Två hjul ca 60 mm och ett kulhjul | 50 kr |
| Chassi (3D-utskrift, plywood eller en matlåda) | 0–50 kr |
| Golvmatta: presenning eller vaxduk med 7 × 5 rutor à 15 cm | 50–100 kr |
| **Summa utöver nod** | **ca 230 kr** |

| Koppling | Stift |
|---|---|
| Vänster motor IN1–IN4 | GP2–GP5 |
| Höger motor IN1–IN4 | GP6–GP9 |
| Stötfångare (mikrobrytare, valfri) | GP14 |

**Beteende:** appen skickar hela programmet på en gång: `ut/program {"steg": ["F","F","V","F"]}`.
Lådan svarar `in/steg {"i": 2, "klar": true}` efter varje steg, och appen väntar in roboten i
stället för att köra i sin egen takt. `in/krock {}` om stötfångaren slår till.

**Risker:** stegmotorerna drar ström även när de står still. Stäng av spolarna mellan körningar.
En powerbank som stänger av sig vid låg ström behöver en ”håll vaken”-funktion eller bytas.
Hjulen slirar på blankt golv, så mattan ska ha friktion.

---

## 7. Funktionsmaskinen (matematik, `nod-07`)

**Mål:** förstå att en funktion är en regel som gör om ett tal till ett annat, och att regler av
typen ”gånger något plus något” blir raka linjer.

**Scenen:** en maskin med ränna in, kugghjul och ränna ut. Ett tal rullar in, kugghjulen snurrar
och ett nytt tal rullar ut. Varje test blir en prick i grafen och en rad i loggen, där deltagarens
gissning jämförs med svaret (`9 ≠ 11`). När gissningen stämmer lyfts locket och regeln syns.

| Steg | Deltagaren gör | Klart när |
|---|---|---|
| 1 | Mata maskinen med tre tal | Tre tal inmatade |
| 2 | Knäck maskin 1 (ut = in + 3) | Rätt regel |
| 3 | Knäck maskin 2 (ut = in × 2) | Rätt regel |
| 4 | Knäck alla fyra | Även in × 2 + 1 och in × 3 − 2 |

**Lag mot lag:** ett lag ställer in en hemlig regel i lådan, det andra knäcker den med så få test
som möjligt. Sedan byter de.

**Lådan:** en låda med ett vred (in), två sifferdisplayer (in och ut) och ett lock som ett servo
lyfter när regeln är knäckt. Ledaren ställer in den hemliga regeln från sin vy.

| Del | Ca pris |
|---|---|
| Vridomkopplare KY-040 med ratt | 30 kr |
| 4-siffrig display TM1637 | 2 × 40 kr |
| Servo SG90 och ett lätt lock med gångjärn | 50 kr |
| **Summa utöver nod** | **ca 160 kr** |

| Koppling | Stift |
|---|---|
| KY-040 CLK / DT / knapp | GP10 / GP11 / GP12 |
| Display in, CLK / DIO | GP2 / GP3 |
| Display ut, CLK / DIO | GP4 / GP5 |
| Servo | GP15 |

**Beteende:** vrid till ett tal och tryck på ratten: `in/tal {"x": 4}`. Appen svarar med
`ut/visa {"in": 4, "ut": 11}` och `ut/lock {"oppen": true}` när regeln är knäckt. Regeln finns
bara i rumsservern, så lådan kan inte avslöja den.

**Risker:** billiga vridomkopplare hoppar över steg. Läs dem med avbrott, inte i en slinga.
Servot rycker till vid start, så locket ska vara lätt och inte kunna klämma fingrar.

---

## Budget

| Låda | Delar utöver nod | Med nod (ca 200 kr) |
|---|---|---|
| nod-01 Strömkretsen | 100 kr | 300 kr |
| nod-02 Logikgrindar | 70 kr | 270 kr |
| nod-03 Ljudvågor | 210 kr | 410 kr |
| nod-04 Fruktsorteraren | 230 kr | 430 kr |
| nod-05 Paketresan | 250 kr | 450 kr |
| nod-06 Robotens väg | 230 kr | 430 kr |
| nod-07 Funktionsmaskinen | 160 kr | 360 kr |
| Router för eget nät | – | 400 kr |
| **Ett set, en låda per verkstad** | | **ca 3 000 kr** |

För stationsformat räcker ett set. För lagformat med tio lag blir det tio av de billigaste lådorna
(Logikgrindar eller Funktionsmaskinen), ungefär 3 000 kr till.

## Byggordning

1. **Logikgrindar.** Enklast hårdvara, och den visar hela kedjan: knapp på bordet, MQTT,
   rumsservern, appen och tillbaka till lampan. Bygg firmware-skelettet klart här.
2. **Strömkretsen.** Samma enkla delar plus en sensor. Visar riktningen låda → skärm med mätvärden.
3. **Paketresan.** Mest synlig för hela rummet och bra att visa upp tidigt.
4. **Funktionsmaskinen** och **Fruktsorteraren**. Servo, displayer och sensorer.
5. **Robotens väg.** Mest mekanik och mest att justera.
6. **Ljudvågor.** Kräver ljud i realtid, se riskerna.

## Öppna frågor

- Vilka mikrokontroller och delar finns redan? Inventeringen kan ändra budgeten mycket.
- Ska lådorna ha egna lysdiodsringar som standard (dokument 5), eller räcker en statuslampa?
- Var ska rumsservern stå: på ledarens dator, på en Raspberry Pi i ”Verkstan i en låda” eller på
  en server på nätet? Lådorna behöver bara veta adressen, så valet kan vänta.
- Vem uppdaterar firmware när det finns tjugo lådor? Trådlös uppdatering (OTA) med MicroPython
  är möjlig men behöver testas.
