# 5. Fysiska enheter

En lampa på skärmen är en bild. En lampa på bordet som tänds när man drar i ett reglage i mobilen
visar att kod styr saker. Folk samlas också runt en sak och provar.

| Riktning | Exempel |
|---|---|
| Skärm → sak | Reglaget i appen tänder en riktig lampa |
| Sak → skärm | En sensor mäter ström och appen ritar den |
| Tvilling | Sak och skärm visar samma läge |

Tvillingen är starkast: man kan peka på skärmen och säga ”det här händer i lådan”.

## Fler idéer

- Ledare eller isolator: två kontaktspetsar, håll dit gem, sudd eller en citron.
- Grindlådor som kopplas ihop med sladdar till en adderare.
- Handtermin: en avståndssensor styr tonhöjden.
- Trollstav med accelerometer som lär sig känna igen rörelser.
- Programkort med NFC-tagg som läggs i rad framför en läsare.
- Rumslampa som visar röster eller blinkar när någon blir klar.

## Verkstan-noden

En standardnod per låda: Raspberry Pi Pico W med modulens delar, powerbank och numret på locket.
Den berättar vid start vad den har, till exempel `{"har": ["led", "pot", "ina219"]}`. Ledaren
kopplar noden till en verkstad under Lådor i rumsvyn.

## Hur noden pratar med appen

| Väg | Fungerar med | Nackdel |
|---|---|---|
| Wifi och MQTT till rumsservern | Alla, även iPhone | Kräver server och eget nät |
| Web Serial | Chrome och Edge på dator | Inte iPhone eller Firefox |
| Web Bluetooth | Chrome på dator och Android | Inte iPhone |

Valt: wifi och MQTT (Mosquitto) på rumsservern, som översätter till WebSocket. Webbläsarna når
aldrig en nod direkt. Ämnen och meddelanden står i [dokument 7](07-modulplaner.md).

Firmware är MicroPython, så att koden går att visa för deltagarna. Ljudlådan kör C++.
En knapp ”Visa koden i lådan” i varje verkstad vore ett bra tillägg.

## Format

| Format | Enheter | Passar |
|---|---|---|
| Demo | 1 per modul | Ledaren visar, deltagarna styr från mobilen |
| Station | 1 per modul | Grupper roterar, 20–40 personer |
| Lagkit | 1 per lag | Flest enheter |

## Hinder

- iPhone saknar Web Serial och Web Bluetooth, så allt går via servern.
- Pico W klarar bara 2,4 GHz och inte eduroam. En egen reserouter löser det.
- Bara 5 V. Powerbanks i stället för lösa litiumbatterier.
- 75 personer trycker hårt. Arkadknappar och skruvade kontakter.
- Med 20 lådor behövs trådlös uppdatering.
- Varje modul fungerar utan nod.
