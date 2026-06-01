# SAOS Search Skill
## Ważne

Przed uruchomieniem wejdż w: https://claude.ai/settings/capabilities i w "additional allowed domains" dodaj koniecznie:

a) saos.org.pl

b) www.saos.org.pl

## Overview
 
Przeszukuje polskie orzeczenia sądowe przez **SAOS API** (System Analizy Orzeczeń Sądowych — https://www.saos.org.pl) i zapisuje wyniki w JSON + DOCX. Opcjonalnie generuje **raport tematyczny** — automatyczne grupowanie orzeczeń w klastry tematyczne z analizą wzorców.
 
SAOS agreguje orzeczenia ze wszystkich polskich sądów: powszechnych (rejonowe, okręgowe, apelacyjne), Sądu Najwyższego, sądów administracyjnych, Trybunału Konstytucyjnego i Krajowej Izby Odwoławczej. API jest publiczne, nie wymaga klucza ani autoryzacji.
 
## Trigger
 
### Wyszukiwanie orzeczeń
 
Komendy: `/saos-search "fraza"`, `/saos "fraza"`, `/orzeczenia "fraza"`
 
```
/saos-search "dobro dziecka"
/saos "odszkodowanie za błąd medyczny"
/orzeczenia "naruszenie dóbr osobistych"
/saos-search "emerytura, swobodna ocena dowodów" --mode keywords
```
 
### Raport tematyczny
 
Trigger na dwa sposoby:
 
**A) Jako flaga przy wyszukiwaniu:**
```
/saos-search "dobro dziecka" --raport-tematyczny
```
Wyszukuje orzeczenia, pobiera treści, a następnie automatycznie generuje raport tematyczny.
 
**B) Jako komenda follow-up po wcześniejszym wyszukiwaniu:**
```
pogrupuj tematycznie te orzeczenia
zrób raport tematyczny z tych wyników
jakie wzorce widać w tych orzeczeniach?
pogrupuj orzeczenia z pliku saos_judgments_*.json
```
Działa na pliku `saos_judgments_*.json` z bieżącej sesji lub przesłanym przez użytkownika.
 
---
 
## Rozpoznanie środowiska
 
Skill działa w dwóch środowiskach. Rozpoznaj, w którym jesteś, i stosuj odpowiednią ścieżkę dostarczenia wyników.
 
### Claude.ai (czat webowy / mobilny / desktop)
 
**Dostępne narzędzia:**
 
| Narzędzie | Zastosowanie w tym skillu |
|-----------|--------------------------|
| `bash_tool` | Uruchamianie skryptu Python/Node, instalacja zależności, testowanie API |
| `view` | Podgląd struktury plików wyjściowych, odczyt logów, odczyt references/ |
| `create_file` | Tworzenie skryptów JS do generacji raportów DOCX |
| `present_files` | **KRYTYCZNE** — jedyny sposób dostarczenia plików użytkownikowi |
 
**Ograniczenia sieciowe:**
- Kontener ma listę dozwolonych domen (`allowed_domains`). Domena `saos.org.pl` **NIE** jest domyślnie na tej liście.
- Jeśli API SAOS jest niedostępne, poinformuj użytkownika: *„Domena saos.org.pl nie jest na liście dozwolonych. Zaktualizuj ustawienia sieciowe (Network settings) w ustawieniach projektu, dodając `saos.org.pl` do allowed domains."*
**Ścieżki plików:**
- Katalog roboczy: `/home/claude/`
- Pliki wyjściowe **MUSZĄ** trafić do: `/mnt/user-data/outputs/`
- Pliki użytkownika: `/mnt/user-data/uploads/`
### Claude Code (terminal / GitHub)
 
**Dostępne narzędzia:**
 
| Narzędzie | Zastosowanie w tym skillu |
|-----------|--------------------------|
| Terminal (bezpośredni) | Uruchamianie Python, pip, curl, node — bez wrappera `bash_tool` |
| System plików | Bezpośredni dostęp do plików |
| `curl` | Testowanie API SAOS: `curl -s "https://www.saos.org.pl/api/search/judgments?all=test&pageSize=1"` |
| `git` | Opcjonalnie: wersjonowanie wyników, commit do repozytorium |
 
**Brak ograniczeń sieciowych** — bezpośredni dostęp do `saos.org.pl`.
 
**Ścieżki plików:** bieżący katalog projektu lub `./saos-output/`
 
---
 
## Chain of Thought (zoptymalizowana sekwencja)
 
Workflow składa się z **6 faz**. Fazy 1–5 obsługują wyszukiwanie i pobieranie. Faza 6 obsługuje raport tematyczny (opcjonalna — tylko na życzenie użytkownika lub z flagą `--raport-tematyczny`).
 
### Faza 1: PARSE — parsuj komendę (natychmiast, 0 API calls)
 
Wyciągnij z komendy użytkownika:
1. **Frazę wyszukiwania** — tekst w cudzysłowie po `/saos-search`
2. **Tryb** — `all` (domyślny) lub `keywords`
3. **Limit** — jeśli user podał `--max-results N`
4. **Flaga raportu tematycznego** — `--raport-tematyczny` lub prośba o grupowanie
**Walidacja:**
- Fraza nie może być pusta
- Jeśli fraza zawiera przecinki i tryb to `keywords` → osobne hasła z logiką AND
### Faza 2: PROBE — sprawdź API i zbadaj skalę (1 call, ~2s)
 
Lekkie zapytanie do Search API z `pageSize=10` — sprawdź `totalResults` i pokaż 3 pierwsze wyniki.
 
**Jeśli ERROR** — domena niedostępna → poinformuj o allowed domains.
 
### Faza 3: PLAN — zdecyduj o strategii (0 API calls)
 
| Wynik | Strategia | Szacowany czas |
|-------|-----------|----------------|
| 0 | Brak wyników → zaproponuj inną frazę lub tryb | — |
| 1–50 | Pełne pobieranie | ~30s–1min |
| 51–200 | Pełne pobieranie, poinformuj o czasie | ~1–4min |
| 201–500 | Zapytaj: wszystkie czy `--max-results`? | ~4–10min |
| 500+ | Rekomenduj `--max-results 100` | 10min+ |
 
### Faza 4: EXECUTE — uruchom skrypt (główne pobieranie)
 
**4a: Zależności:**
```bash
python3 -c "import docx" 2>/dev/null || pip install python-docx --break-system-packages -q
```
 
**4b: Uruchom skrypt** (Claude.ai → output do `/home/claude/saos-output`, Claude Code → `./saos-output/`)
 
**Parametry:** `"<FRAZA>"`, `--mode all|keywords`, `--max-results N`, `--skip-details`, `--output-dir PATH`
 
### Faza 5: DELIVER — dostarcz wyniki
 
Claude.ai: skopiuj do `/mnt/user-data/outputs/`, użyj `present_files`.
Claude Code: podaj ścieżki, zaproponuj git commit.
 
**Po Fazie 5:** Jeśli `--raport-tematyczny` lub pobranych ≥15 orzeczeń → zaproponuj Fazę 6.
 
### Faza 6: THEMATIC — raport tematyczny (opcjonalna)
 
**Kiedy się uruchamia:**
- Flaga `--raport-tematyczny` w komendzie
- Follow-up: "pogrupuj", "raport tematyczny", "wzorce w orzeczeniach"
- Użytkownik przesyła `saos_judgments_*.json` z prośbą o grupowanie
**Minimum:** 5 orzeczeń (poniżej → zaproponuj `/porownanie-tresci`).
 
**Przed rozpoczęciem:** Odczytaj `references/thematic_report.md` w katalogu tego skilla. Zawiera algorytm klasyfikacji, strukturę raportu i szablon JS z gotowymi helperami.
 
**Krok 6a: Analiza danych**
 
Wczytaj JSON i wyciągnij z każdego orzeczenia cechy klasyfikacyjne (keywords, legalBases, referencedRegulations, textContent head, division, sygnatura).
 
**Krok 6b: Identyfikacja grup (adaptacyjna)**
 
Na podstawie danych zidentyfikuj klastry tematyczne. Algorytm NIE używa stałej listy kategorii — buduje grupy od nowa na podstawie sygnałów w zbiorze (hierarchia: keywords → legalBases → referencedRegulations → division → textContent). Szczegóły → `references/thematic_report.md` §2.
 
**Krok 6c: Generacja raportu DOCX**
 
Wygeneruj skrypt JS oparty o szablon z `references/thematic_report.md` §4. Kluczowe wymogi:
- Biblioteka: `npm install -g docx` (docx-js)
- Font: Aptos. Kolory: nagłówki tabel #1F4E79, wiersze #EAF2FA/#FFFFFF
- Polskie cudzysłowy: `const LQ='\u201E', RQ='\u201D'` — łącz konkatenacją, NIGDY w literałach
- PageNumber: `PageNumber.CURRENT` (enum, nie konstruktor)
- Guardy null: `|| []` / `|| {}` na polach SAOS API
Walidacja po generowaniu:
```bash
python3 <docx-skill-path>/scripts/office/validate.py output.docx
```
 
**Krok 6d: Dostarczenie raportu**
 
Skopiuj do outputs, użyj `present_files`. W czacie podsumuj:
- Liczbę grup i ich nazwy (tabela)
- Dominującą tematykę
- 1–2 kluczowe wnioski
- Rekomendację dalszych kroków
**Struktura raportu DOCX:**
 
```
STRONA TYTUŁOWA — tytuł, fraza, liczba orzeczeń/grup, data
 
CZĘŚĆ I — PODSUMOWANIE
  Kluczowa obserwacja (akapit)
  Tabela zbiorcza: Lp | Grupa | Liczba | Zakres dat
 
CZĘŚĆ II — PRZEGLĄD GRUP (nowa strona per grupa)
  Nagłówek grupy + opis
  Tabela orzeczeń: Lp | Sygnatura | Data | Typ | Sąd/Sędziowie | Keywords/Podstawy
  Analiza: top akty prawne [Nx], top sędziowie [Nx], rozkład sądów [Nx]
 
CZĘŚĆ III — WZORCE PRZEKROJOWE
  3.1 Najczęściej powoływane akty prawne (tabela globalna)
  3.2 Konteksty użycia frazy wyszukiwania (narracja)
  3.3 Wnioski i rekomendacje (lista numerowana)
 
ZASTRZEŻENIA — charakter analityczny, źródło SAOS, klasyfikacja przybliżona
```
 
---
 
## API Reference
 
Skrypt korzysta z dwóch endpointów SAOS. API nie wymaga autoryzacji, odpowiada w JSON (UTF-8).
 
### Search API
```
GET https://www.saos.org.pl/api/search/judgments
```
| Parametr | Typ | Opis |
|----------|-----|------|
| `all` | tekst | Fraza pełnotekstowa |
| `keywords` | tekst (powtarzalny) | Hasła tematyczne (AND). Tylko sądy powszechne |
| `pageSize` | 10–100 | Wyników na stronę |
| `pageNumber` | 0+ | Numer strony |
| `sortingField` | enum | `JUDGMENT_DATE`, `DATABASE_ID`, `REFERENCING_JUDGMENTS_COUNT` |
| `sortingDirection` | ASC/DESC | Kierunek sortowania |
| `judgmentDateFrom` / `To` | yyyy-MM-dd | Zakres dat |
| `judgeName` | tekst | Imię i nazwisko sędziego |
| `caseNumber` | tekst | Dokładna sygnatura akt |
| `courtType` | enum | `APPEAL`, `REGIONAL`, `DISTRICT` |
| `judgmentTypes` | enum (powtarzalny) | `SENTENCE`, `DECISION`, `RESOLUTION`, `REGULATION`, `REASONS` |
 
### Browse API
```
GET https://www.saos.org.pl/api/judgments/{id}
```
Zwraca: `{ data: { id, courtType, courtCases, textContent, judges, referencedRegulations, legalBases, decision, summary, keywords, ... } }`
 
---
 
## Pliki wyjściowe
 
### Fazy 1–5 (wyszukiwanie) — 4 pliki
 
| Plik | Zawartość |
|------|-----------|
| `saos_search_{fraza}_{ts}.json` | Metadane wyszukiwania, lista orzeczeń skrótowa |
| `saos_judgments_{fraza}_{ts}.json` | Pełne dane orzeczeń z textContent |
| `saos_search_{fraza}_{ts}.docx` | Sformatowana lista wyników |
| `saos_judgments_{fraza}_{ts}.docx` | Pełne treści orzeczeń, każde na nowej stronie |
 
### Faza 6 (raport tematyczny) — 1 plik
 
| Plik | Zawartość |
|------|-----------|
| `raport_grupowanie_{fraza}_{ts}.docx` | Grupowanie tematyczne: podsumowanie, przegląd grup, wzorce, wnioski |
 
---
 
## Obsługa błędów
 
| Scenariusz | Zachowanie |
|------------|-----------|
| HTTP 429 (rate limit) | Exponential backoff: 5s, 10s, 15s, max 3 próby |
| HTTP 5xx (błąd serwera) | Retry: 2s, 4s, 6s |
| Timeout | 30s timeout, 3 próby |
| Brak textContent | Graceful fallback — „Brak treści" w DOCX |
| division=null | Guardy `or {}` / `or []` |
| Względny URL w href | Konwersja na absolutny |
| Pusta fraza | Exit code 1, komunikat |
| <5 orzeczeń w raporcie tematycznym | Zaproponuj `/porownanie-tresci` |
| Brak keywords/legalBases | Klasyfikacja po regulacjach/treści; ostrzeżenie w raporcie |
 
---
 
## Ważne uwagi
 
- **Opóźnienie 0.5s** między requestami — nie zmniejszaj.
- **Tryb `keywords`** — tylko sądy powszechne. Dla SN, TK, KIO użyj `all`.
- **Wielokrotne keywords** — rozdziel przecinkami → AND.
- **Duże zbiory** — 500+ orzeczeń → rekomenduj `--max-results`.
- **Polskie cudzysłowy w JS** — `const LQ='\u201E', RQ='\u201D'` + konkatenacja. NIGDY bezpośrednio w stringach.
- **PageNumber docx 9.x** — enum `PageNumber.CURRENT`, nie konstruktor.
- **Guardy null** — `|| []` / `|| {}` na polach SAOS API (zwracają explicit `null`).
- **Klasyfikacja adaptacyjna** — grupy budowane od nowa per zbiór. Nie kopiuj z poprzednich sesji.
 
