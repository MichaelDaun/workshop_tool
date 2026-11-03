# Instruktioner för AI som arbetar i det här repot

Verkstan är en webbapp med workshopövningar för en publik utan teknisk bakgrund.
Modulerna skrivs av en AI tillsammans med den som underhåller projektet. Läs det här först.

## Läs innan du skriver något

- `docs/06-designmanual.md`: färg, typografi, komponenter och språk. Del C är en checklista
  som ska vara uppfylld innan du lämnar över.
- `docs/07-modulplaner.md`: plan, steg och låda för varje verkstad.
- `docs/04-ai-forfattade-moduler.md`: hur en modul är uppbyggd och hur den granskas.

## Teknik i mockuparna

- Ren HTML, CSS och JavaScript utan byggsteg. En fil per modul i `mockups/moduler/`.
- Gemensam stil i `mockups/shared/theme.css` och gemensamma funktioner i `mockups/shared/kit.js`
  (global `K`). Använd klasserna som finns: `.stage`, `.scen`, `.status`, `.mission`, `.why`,
  `.readout`, `.control`, `.btn`, `.chip`, `.stegare`, `.lada`.
- Text på två språk: svenska i elementet och engelska i `data-en`, eller `K.t(sv, en)` i kod.
- Protokollet byggs med `K.tasks(...)`, återkoppling med `K.status(text, "info" | "klar" | "fara")`
  och lådan på bordet med `K.lada(...)`.
- Sätt `data-domain` på `body` så att `--aktiv` blir modulens färg.

## Regler som är lätta att missa

- Bara modulens egen färg plus neutraler. Färgen sitter på det som är aktivt i scenen.
- Inga versala etiketter, inga piller, inga skuggor, inga kort inuti kort, ingen konfetti.
- Primärknappen är grafit. Fara visas med varningstejp, aldrig med rött. Inget rött och grönt för rätt och fel.
- Mono bara för värden med enhet och för kod.
- Beskriv vad som hände i världen, inte personen. Verb först i instruktioner.
- Inga utropstecken, ingen jag-form för maskiner, inget beröm.
- Inga inskjutna tankstreck, inga triader, inga ”inte X, utan Y”, inga fetstilta inledningar.
- Svenska citattecken (”så här”), decimalkomma och mellanslag före enhet (0,46 A). Brittisk engelska.
- Varje verkstad fungerar fullt ut utan låda.

## Kontrollera

Öppna sidan i 400 px bredd och i mörkt läge. Gå igenom alla steg i protokollet och se att varje
steg ger en reaktion i scenen. Kontrollera att konsolen är tom.

## Git

Inga modellnamn i commit-meddelanden eller filer.
