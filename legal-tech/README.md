# legal-tech

Ten katalog zawiera skill **Szukaj Orzeczeń v2.0** — narzędzie do przeszukiwania polskich orzeczeń sądowych przez SAOS API z generacją raportów DOCX.

## Zawartość

| Plik | Opis |
|------|------|
| `szukaj-orzeczen.skill` | Skill gotowy do instalacji w Claude.ai lub Claude Code |
| `szukaj-orzeczen-v2.zip` | Archiwum z kodem źródłowym i pełną dokumentacją skilla |
| `szukaj-orzeczen.md` | Dokumentacja skilla: opis, instalacja, przykłady użycia |

## Co robi skill?

Skill łączy się z bazą **SAOS** (System Analizy Orzeczeń Sądowych — [saos.org.pl](https://www.saos.org.pl)) i pozwala:

1. **Wyszukać orzeczenia** po frazach, sygnaturach, sądzie lub zakresie dat — wyniki zapisywane do JSON i DOCX
2. **Wygenerować raport tematyczny** — grupowanie orzeczeń w klastry, statystyki, wnioski w formacie DOCX

## Szybki start

### Instalacja w Claude.ai

1. Przejdź do **Ustawienia projektu → Skills → Dodaj umiejętność z pliku**
2. Wgraj plik `szukaj-orzeczen.skill`
3. W ustawieniach projektu dodaj `saos.org.pl` do dozwolonych domen (Network settings)

### Instalacja w Claude Code

1. Skopiuj folder ze skill'em do katalogu projektu:
   ```bash
   unzip szukaj-orzeczen-v2.zip -d .claude/skills/
   ```
2. Claude Code ma bezpośredni dostęp do sieci — nie wymaga dodatkowej konfiguracji

### Wymagania

- Python 3.8+
- `python-docx` — instalowany automatycznie przy pierwszym użyciu
- Dostęp sieciowy do `saos.org.pl`

## Przykładowe komendy

```
/szukaj-orzeczen "odszkodowanie za wypadek komunikacyjny" sąd:"Sąd Najwyższy" rok:2023-2024

/orzeczenia "klauzula abuzywna" limit:50

/raport-tematyczny --plik wyniki.json --klastry 5
```

## Powiązanie z pluginem AI Polish Text Expert

Skill ten jest niezależnym modułem legal-tech, który można używać samodzielnie lub w połączeniu z pluginem **ai-polish-text-expert** — np. do analizy treści pobranych orzeczeń (`/analiza-tresci`) lub porównania wersji dokumentów (`/porownanie-tresci`).

## Wersja i licencja

- Wersja: 2.0
- Licencja: MIT (szczegóły w [ai-polish-text-expert-plugin/LICENSE](../ai-polish-text-expert-plugin/LICENSE))
- Autor: GSkuza
