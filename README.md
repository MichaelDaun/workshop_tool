# Verkstan

Workshopövningar om teknik för en publik utan teknisk bakgrund. Femton verkstäder i sju ämnen:
ellära, digital logik, signalteknik, AI, nätverk, mjukvara och matematik. Ensam eller i ett rum.

Status: klickbara mockupar och firmware-utkast.

## Prova

Öppna `mockups/index.html`, eller:

```bash
cd mockups && python3 -m http.server 8000
```

| Ämne | Verkstäder |
|---|---|
| Ellära | [Strömkretsen](mockups/moduler/el-krets.html), [Ficklampan](mockups/moduler/el-ficklampa.html), [Vad drar mest?](mockups/moduler/el-energi.html) |
| Digital logik | [Logikgrindar](mockups/moduler/logik-grindar.html), [Åtta lampor](mockups/moduler/logik-binart.html) |
| Signalteknik | [Ljudvågor](mockups/moduler/signal-vagor.html), [Pixlar](mockups/moduler/signal-pixlar.html) |
| AI | [Fruktsorteraren](mockups/moduler/ai-sortera.html), [Nästa ord](mockups/moduler/ai-sprakmodell.html) |
| Nätverk | [Paketresan](mockups/moduler/natverk-paket.html), [Hemliga färger](mockups/moduler/nat-hemligt.html) |
| Mjukvara | [Robotens väg](mockups/moduler/robot-kod.html), [Sortera](mockups/moduler/kod-sortera.html) |
| Matematik | [Funktionsmaskinen](mockups/moduler/matte-maskin.html), [Tärningar](mockups/moduler/matte-tarning.html) |

Dessutom [rumsvyn](mockups/rum.html) för ledaren och [designmanualen](mockups/designmanual.html).
Ren HTML, CSS och JS utan byggsteg. Lådorna är simulerade, firmware finns i [`firmware/`](firmware/).

## Dokument

1. [Vision och pedagogik](docs/01-vision-och-pedagogik.md)
2. [Övningsbank](docs/02-ovningsbank.md)
3. [Samarbete och arkitektur](docs/03-samarbete-och-arkitektur.md)
4. [Moduler skrivna av AI](docs/04-ai-forfattade-moduler.md)
5. [Fysiska enheter](docs/05-fysiska-enheter.md)
6. [Designmanual](docs/06-designmanual.md)
7. [Modulplaner](docs/07-modulplaner.md): steg, delar, stift och meddelanden per verkstad

En AI som skriver moduler läser [AGENTS.md](AGENTS.md).

## GitHub Pages

`.github/workflows/pages.yml` publicerar `mockups/` vid push till `main`. Slå på under
Settings → Pages → Source: GitHub Actions.
