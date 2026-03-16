# Shared Configuration — Jedno Źródło Prawdy

Ten katalog zawiera wspólną konfigurację dla wszystkich skills, agentów i raportów DOCX.

## Pliki

| Plik | Opis |
|------|------|
| `badges.json` | Odznaki statusu: kolory, teksty, opisy — używane w raportach DOCX i w czacie |
| `theme.json` | Paleta kolorów, fonty, rozmiary czcionek, konfiguracja strony A4, format raportów |

## Zasada

**Każda zmiana wizualna (kolory, fonty, odznaki) powinna być wprowadzana TUTAJ** — pliki skills i agentów referencjonują te definicje. Dzięki temu zmiana palety kolorów wymaga edycji w 1 miejscu zamiast w ~8.

## Referencjonowanie

W plikach skills i agentów odwołuj się do tej konfiguracji:
- Odznaki: patrz `shared/badges.json`
- Kolory i fonty: patrz `shared/theme.json`

Pliki `.skill` (ZIP) i `.md` powinny zawierać komentarz:
```
# Konfiguracja wizualna: patrz shared/badges.json i shared/theme.json
```
