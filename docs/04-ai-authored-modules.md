# 4. Moduler skrivna av AI

En AI skriver modulerna tillsammans med den som underhåller projektet. Utan ramar blir varje
modul en egen app med egen stil. Med en byggsats skriver AI:n innehåll och en scen, och den som
granskar tittar på pedagogiken.

## Byggsatsen

| Del | I mockuparna |
|---|---|
| Toppfält | `K.topbar()` |
| Scen och panel | `.module`, `.stage`, `.panel` |
| Steg med bockar | `K.tasks()` |
| Statusrad | `K.status()` |
| Vad hände? | `details.why` |
| Avläsning | `.readout` |
| Reglage | `.control` |
| Val | `.chip[aria-pressed]` |
| Lådan på bordet | `K.lada()` |
| Språk | `data-en`, `K.t()` |

Återkommande scener som kan bli egna komponenter: kopplingsschema, rutnät med figur, graf,
nodnät, karta med punkter, stapeldiagram.

## Modulformat

```yaml
id: el-krets
domain: el
title: { sv: Strömkretsen, en: The circuit }
minutes: 10
scene: circuit
state:
  batteries: { min: 1, max: 6, start: 2 }
  resistance: { min: 0.5, max: 20, step: 0.5, start: 10, unit: Ω }
tasks:
  - id: lagom
    text: { sv: Lagom ljus med 4 batterier, en: Just right with 4 batteries }
    done_when: batteries == 4 and power >= 2.5 and power <= 4.5
why:
  - { sv: Fler batterier trycker på mer., en: More batteries push harder. }
box: nod-01
```

## Automatiska kontroller

| Kontroll | Fångar |
|---|---|
| Schema | Saknade fält |
| Båda språken | Glömda översättningar |
| Längd: lead en mening, steg högst 60 tecken | För mycket text |
| Skärmdumpar i 400 och 1280 px, ljust och mörkt | Trasig layout |
| axe | Kontrast, etiketter, fokus |
| Skriptat genomspel av alla steg | Omöjliga steg |
| Tom konsol | Krascher |

## Arbetsgång

1. Välj en idé ur övningsbanken.
2. AI:n skriver en brief: aha, metafor, 4 steg, vardagskoppling, rumsversion. Godkänn.
3. AI:n bygger på en egen gren.
4. Kontroller och skärmdumpar på pull requesten.
5. Provkör med en eller två personer ur målgruppen.

## Risker

| Risk | Åtgärd |
|---|---|
| Faktafel | Granska alltid ”Vad hände?” |
| Metaforen blir fel | Säg var den tar slut |
| Stilen glider | Byggsatsen och skärmdumparna |
| För mycket text | Längdkontrollen |
