# Instruktioner för AI i det här repot

Läs först `docs/06-designmanual.md` (del C är checklistan), `docs/07-modulplaner.md` och
`docs/04-ai-forfattade-moduler.md`.

## Teknik

- En HTML-fil per modul i `mockups/moduler/`, utan byggsteg.
- `mockups/shared/theme.css` och `mockups/shared/kit.js` (global `K`). Använd befintliga klasser:
  `.stage`, `.scen`, `.status`, `.mission`, `.why`, `.readout`, `.control`, `.btn`, `.chip`, `.rad`, `.lada`.
- Svenska i elementet, engelska i `data-en`, eller `K.t(sv, en)`.
- `K.tasks(...)` för stegen, `K.status(text, "info" | "klar" | "fara")`, `K.lada(...)` för lådan.
- `data-domain` på `body` ger `--aktiv`.
- Firmware: en fil i `firmware/verkstan_nod/lador/` med `starta(nod)` och `varv(nod)`.

## Regler

- Modulens färg plus neutraler. Inga versaler, piller, skuggor, kort i kort eller konfetti.
- Primärknappen är grafit. Fara är varningstejp. Inget rött och grönt för rätt och fel.
- Mono bara för värden och kod.
- Kort text. En mening räcker oftast. Inga metakommentarer.
- Inga utropstecken, ingen jag-form för maskiner, inget beröm, inga inskjutna tankstreck, inga
  triader, inga ”inte X, utan Y”, inga fetstilta inledningar.
- ”Svenska citattecken”, decimalkomma, mellanslag före enhet (0,46 A). Brittisk engelska.
- Varje verkstad fungerar utan låda.

## Kontrollera

400 px bredd, mörkt läge, alla steg i protokollet, tom konsol. Inga modellnamn i commits eller filer.
