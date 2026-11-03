# Firmware för Verkstan-noden (utkast)

> **Otestat utkast.** Koden är skriven utan att ha körts på en Pico W. Den visar upplägget,
> inte en färdig lösning. Räkna med att behöva rätta saker vid första provkörningen.

Varje låda kör samma grundprogram och en liten fil med lådans beteende.

```
verkstan_nod/
  main.py              startar allt, ändras inte per låda
  nod.py               wifi, MQTT, statuslampa, "Hitta", återanslutning
  config_exempel.py    kopiera till config.py och fyll i nät, server och lådans id
  lador/
    logik.py           Logikgrindar (nod-02): två knappar och en lampa
```

## Kom igång

1. Installera MicroPython för Pico W (UF2-fil från micropython.org).
2. Installera MQTT-klienten på Picon, till exempel med `mpremote mip install umqtt.simple`.
3. Kopiera `config_exempel.py` till `config.py` och fyll i värdena.
4. Kopiera hela `verkstan_nod/` till Picon: `mpremote cp -r verkstan_nod/* :`
5. Starta en MQTT-förmedlare på datorn (`mosquitto -v`) och lyssna:
   `mosquitto_sub -v -t 'verkstan/#'`

Ämnen och meddelanden beskrivs i `docs/05-fysiska-enheter.md`, och delar och kopplingar per låda
i `docs/07-modulplaner.md`.

## En ny låda

Skriv en ny fil i `lador/` med två funktioner:

- `starta(nod)` körs en gång. Ställ in stift och prenumerera på `ut/`-ämnen med `nod.lyssna(...)`.
- `varv(nod)` körs om och om igen, ungefär 100 gånger per sekund. Läs knappar och sensorer och
  skicka med `nod.skicka("in/...", {...})`.

Sätt `LADA = "namnet"` i `config.py`.
