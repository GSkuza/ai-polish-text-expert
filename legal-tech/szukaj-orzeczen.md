# Szukaj Orzeczeń v2.0

**Skill do Claude.ai / Claude Code** — przeszukiwanie polskich orzeczeń sądowych przez SAOS API z automatycznym grupowaniem tematycznym i generacją profesjonalnych raportów DOCX.

<p align="center">
  <img src="https://img.shields.io/badge/język-polski-red" alt="Polski">
  <img src="https://img.shields.io/badge/API-SAOS-blue" alt="SAOS API">
  <img src="https://img.shields.io/badge/output-DOCX%20%2B%20JSON-green" alt="DOCX + JSON">
  <img src="https://img.shields.io/badge/wersja-2.0-orange" alt="v2.0">
  <img src="https://img.shields.io/badge/python-3.8%2B-yellow" alt="Python 3.8+">
</p>

---

## Czym jest ten skill?

Skill pozwala przeszukiwać bazę **SAOS** (System Analizy Orzeczeń Sądowych — [saos.org.pl](https://www.saos.org.pl)) bezpośrednio z poziomu rozmowy z Claude. SAOS agreguje orzeczenia ze wszystkich polskich sądów: powszechnych (rejonowe, okręgowe, apelacyjne), Sądu Najwyższego, sądów administracyjnych, Trybunału Konstytucyjnego i Krajowej Izby Odwoławczej.

Skill działa w dwóch trybach:

1. **Wyszukiwanie** — znajduje orzeczenia po frazach, pobiera pełne treści, zapisuje wyniki do JSON i DOCX.
2. **Raport tematyczny** — analizuje pobrany zbiór orzeczeń, grupuje je w klastry tematyczne (po sygnaturach, hasłach, wydziałach, przepisach), przeprowadza text mining i generuje profesjonalny raport DOCX z tabelami, statystykami i wnioskami.

---

## Szybki start

### Instalacja w Claude.ai (Projekt)

1. Rozpakuj `szukaj-orzeczen-v2.zip` do katalogu `/mnt/skills/user/szukaj-orzeczen/`
2. W ustawieniach projektu dodaj `saos.org.pl` do **allowed domains** (Network settings)
3. Gotowe — skill aktywuje się automatycznie na komendy `/szukaj-orzeczen`, `/szukaj`, `/orzeczenia`

### Instalacja w Claude Code

1. Skopiuj folder `szukaj-orzeczen-v2/` do katalogu projektu (np. `.claude/skills/szukaj-orzeczen/`)
2. Claude Code ma bezpośredni dostęp do sieci — nie wymaga konfiguracji domen

### Wymagania

- Python 3.8+
- `python-docx` (instalowany automatycznie przy pierwszym uruchomieniu)
- Dostęp sieciowy do `saos.org.pl`

---

## Użycie

### Tryb 1: Wyszukiwanie orzeczeń

```
/szukaj-orzeczen "dobro dziecka"
```

Skill przejdzie przez 5 faz: parsowanie komendy → probe API (ile wyników?) → planowanie strategii → wyszukiwanie + pobieranie pełnych treści → dostarczenie plików.

**Zaawansowane opcje:**

```
/szukaj-orzeczen "naruszenie dóbr osobistych" --max-results 100
/szukaj-orzeczen "emerytura, renta" --mode keywords
/szukaj-orzeczen "błąd medyczny" --date-from 2023-01-01 --date-to 2025-12-31
```

**Pliki wyjściowe:**

| Plik | Zawartość |
|------|-----------|
| `saos_search_{fraza}_{ts}.json` | Metadane wyszukiwania + lista orzeczeń ze snippetami |
| `saos_search_{fraza}_{ts}.docx` | Sformatowana tabela wyników + fragmenty treści |
| `saos_judgments_{fraza}_{ts}.json` | Pełne dane orzeczeń z textContent |
| `saos_judgments_{fraza}_{ts}.docx` | Pełne treści orzeczeń, każde na osobnej stronie |

### Tryb 2: Raport tematyczny

```
/szukaj-orzeczen "pozbawienie władzy rodzicielskiej art. 111 kro" --raport-tematyczny
```

Albo po wcześniejszym wyszukiwaniu:

```
pogrupuj tematycznie
raport tematyczny
```

**Dodatkowy plik wyjściowy:**

| Plik | Zawartość |
|------|-----------|
| `raport_tematyczny_{fraza}_{ts}.docx` | Profesjonalny raport z grupowaniem, statystykami, wnioskami |

---

## Architektura

### Struktura katalogów

```
szukaj-orzeczen/
├── SKILL.md                          # Definicja skilla (trigger, workflow, API docs)
├── README.md                         # Ten plik
└── scripts/
    ├── szukaj_orzeczen.py            # Wyszukiwanie (SAOS Search API)
    ├── saos_fetch.py                 # Pobieranie pełnych treści (SAOS Browse API)
    └── raport_tematyczny.py          # Generator raportu tematycznego (DOCX)
```

### Pipeline

```
                    ┌─────────────────┐
                    │  szukaj_orzeczen │  Search API → JSON + DOCX
                    │      .py        │  (lista wyników)
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   saos_fetch    │  Browse API → JSON + DOCX
                    │      .py        │  (pełne treści)
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
     Tryb 1: DELIVER               Tryb 2: ANALIZA AI
     (JSON + DOCX pliki)                    │
                                            ▼
                               ┌─────────────────────┐
                               │  Claude analizuje    │
                               │  dane, grupuje,      │
                               │  tworzy JSON config  │
                               └────────┬────────────┘
                                        │
                                        ▼
                               ┌─────────────────────┐
                               │ raport_tematyczny.py │  JSON → DOCX
                               │                     │  (raport profesjonalny)
                               └─────────────────────┘
```

### Skrypty — szczegóły

#### `szukaj_orzeczen.py`

Wyszukiwanie orzeczeń przez SAOS Search API z paginacją.

```bash
# Pełne wyszukiwanie
python3 scripts/szukaj_orzeczen.py "dobro dziecka" --mode all --max-results 50

# Tylko sprawdzenie ile jest wyników (probe)
python3 scripts/szukaj_orzeczen.py "dobro dziecka" --probe-only

# Wyszukiwanie po hasłach tematycznych (AND)
python3 scripts/szukaj_orzeczen.py "alimenty, rozwód" --mode keywords

# Z ograniczeniem dat
python3 scripts/szukaj_orzeczen.py "błąd medyczny" --date-from 2023-01-01 --date-to 2025-12-31
```

| Parametr | Domyślnie | Opis |
|----------|-----------|------|
| `phrase` | (wymagany) | Fraza wyszukiwania |
| `--mode` | `all` | `all` = pełnotekstowe, `keywords` = hasła tematyczne (AND, tylko sądy powszechne) |
| `--max-results` | `50` | Limit wyników (0 = bez limitu) |
| `--output-dir` | `./saos-output` | Katalog wyjściowy |
| `--sort-field` | `JUDGMENT_DATE` | Pole sortowania |
| `--sort-dir` | `DESC` | Kierunek sortowania |
| `--date-from` | – | Orzeczenia od daty (YYYY-MM-DD) |
| `--date-to` | – | Orzeczenia do daty (YYYY-MM-DD) |
| `--probe-only` | – | Tylko sprawdź liczbę wyników, bez pobierania |

#### `saos_fetch.py`

Pobieranie pełnych treści orzeczeń z SAOS Browse API.

```bash
# Z pliku JSON (wynik szukaj_orzeczen.py)
python3 scripts/saos_fetch.py --input saos-output/saos_search_dobro_dziecka_*.json

# Po liście ID orzeczeń
python3 scripts/saos_fetch.py --ids 31345,227221,542282

# Tylko JSON, bez DOCX
python3 scripts/saos_fetch.py --input results.json --skip-docx
```

| Parametr | Opis |
|----------|------|
| `--input` | Plik JSON z wynikami search (wzajemnie wykluczający z `--ids`) |
| `--ids` | Lista ID orzeczeń oddzielonych przecinkami |
| `--output-dir` | Katalog wyjściowy (domyślnie `./saos-output`) |
| `--phrase` | Fraza do nazwy pliku wyjściowego (opcjonalny) |
| `--skip-docx` | Pomiń generację DOCX, zapisz tylko JSON |

#### `raport_tematyczny.py`

Generator raportu tematycznego DOCX na podstawie konfiguracji JSON przygotowanej przez Claude.

```bash
python3 scripts/raport_tematyczny.py --input raport_data.json --output raport.docx
```

| Parametr | Opis |
|----------|------|
| `--input` | Plik JSON ze strukturą raportu (przygotowany przez Claude) |
| `--output` | Ścieżka wyjściowa DOCX |

---

## Raport tematyczny — co zawiera?

Raport tematyczny to wielostronicowy dokument DOCX z profesjonalnym formatowaniem, składający się z trzech części:

### Strona tytułowa

- Tytuł: „RAPORT TEMATYCZNY" (28pt)
- Podtytuł: „Grupowanie orzeczeń sądowych"
- Temat: np. „dotyczących pozbawienia władzy rodzicielskiej (art. 111 KRO)"
- Metadane: fraza, liczba orzeczeń/grup, zakres dat, źródło, data raportu
- Nota źródłowa

### Część I — Podsumowanie

- Executive summary (narracyjne podsumowanie zbioru)
- Tabela zbiorcza grup: nazwa | liczba orzeczeń | zakres dat | % zbioru

### Część II — Grupy tematyczne

Dla każdej grupy osobna sekcja (z nagłówkiem na każdej stronie):

- **Statystyka**: „Liczba orzeczeń w grupie: 59 (30% zbioru)"
- **Opis**: narratywna charakterystyka grupy
- **Wzorce kontekstowe (text mining)**: tabela — wzorzec | wystąpień | % grupy | % zbioru
- **Wykaz orzeczeń**: tabela — Lp. | sygnatura | data | typ | sąd/wydział | hasła/podstawy
- **Najczęściej powoływane akty prawne**: tabela — akt | wystąpień | % grupy
- **Rozkład sądów**: tabela — sąd | orzeczeń | % grupy

### Część III — Wzorce przekrojowe

- **3.1** Najczęściej powoływane akty prawne (globalnie)
- **3.2** Sędziowie najczęściej orzekający
- **3.3** Rozkład sądów (globalnie)
- **3.4** Konteksty użycia frazy wyszukiwania (numerowana lista z opisami i statystykami)
- **3.5** Wnioski i rekomendacje
- **Zastrzeżenia**

### Formatowanie

- Font: **Aptos** (wszystkie elementy)
- Nagłówki tabel: `#1F4E79` (ciemnoniebieski) z białym tekstem
- Alternujące wiersze tabel: `#EAF2FA` / `#FFFFFF`
- Nagłówki stron: nazwa bieżącej sekcji (8pt, szary)
- Stopka: „Strona N" (wyśrodkowana)

---

## Metoda grupowania

Grupowanie orzeczeń w raporcie tematycznym jest **adaptacyjne** i wykorzystuje kombinację sygnałów:

| Sygnał | Przykład | Waga |
|--------|---------|------|
| **Sygnatura akt** | `Nsm` → opiekuńcze, `RC` → rodzinne, `K` → karne | Wysoka |
| **Hasła tematyczne** | `władza rodzicielska`, `alimenty`, `kontakty z dzieckiem` | Wysoka |
| **Wydział sądu** | Wydział Rodzinny, Karny, Cywilny, Pracy | Średnia |
| **Powołane przepisy** | art. 111 KRO, art. 138 KRO, art. 207 KK | Średnia |
| **Kontekst tekstowy** | Powtarzające się frazy w treściach: „kurator", „alkoholizm", „przemoc" | Uzupełniająca |

**Zasady:**
- Każde orzeczenie trafia do dokładnie jednej grupy
- Typowo 4–8 grup dla zbioru 100–300 orzeczeń
- Minimalna grupa: 5% zbioru (mniejsze → scalenie z „Pozostałe")
- Grupy sortowane malejąco po liczebności

---

## SAOS API — dokumentacja

Skill korzysta z dwóch publicznych endpointów SAOS. API nie wymaga autoryzacji i odpowiada w JSON (UTF-8).

### Search API — wyszukiwanie

```
GET https://www.saos.org.pl/api/search/judgments
```

| Parametr | Typ | Opis |
|----------|-----|------|
| `all` | tekst | Fraza pełnotekstowa — przeszukuje wszystkie pola |
| `keywords` | tekst (powtarzalny) | Hasła tematyczne, `keywords=X&keywords=Y` = AND. Tylko sądy powszechne |
| `pageSize` | 10–100 | Wyników na stronę |
| `pageNumber` | 0+ | Numer strony |
| `sortingField` | enum | `JUDGMENT_DATE`, `DATABASE_ID`, `REFERENCING_JUDGMENTS_COUNT` |
| `sortingDirection` | `ASC` / `DESC` | Kierunek sortowania |
| `judgmentDateFrom` | `yyyy-MM-dd` | Dolne ograniczenie daty |
| `judgmentDateTo` | `yyyy-MM-dd` | Górne ograniczenie daty |
| `judgeName` | tekst | Imię i nazwisko sędziego |
| `caseNumber` | tekst | Dokładna sygnatura akt |
| `judgmentTypes` | enum (powtarzalny) | `SENTENCE`, `DECISION`, `RESOLUTION`, `REGULATION`, `REASONS` |

**Odpowiedź:** `items[].textContent` zawiera fragment tekstu z podświetloną frazą (`<em>`).

### Browse API — pełne dane orzeczenia

```
GET https://www.saos.org.pl/api/judgments/{id}
```

Pełna treść orzeczenia w `data.textContent`. Powołane przepisy w `data.referencedRegulations`. Słowa kluczowe w `data.keywords`.

---

## Obsługa błędów i odporność

| Scenariusz | Zachowanie |
|------------|-----------|
| HTTP 429 (rate limit) | Exponential backoff: 5s → 10s → 15s, max 3 próby |
| HTTP 5xx (błąd serwera) | Retry z opóźnieniem: 2s → 4s → 6s |
| Timeout połączenia | 30s timeout, 3 próby z backoff |
| Brak `textContent` w orzeczeniu | Graceful fallback — sekcja „Brak treści" w DOCX |
| `division` = `null` w JSON | Guard `or {}` — nie crashuje |
| Pusta fraza wyszukiwania | Walidacja na wejściu, exit code 1 |
| Za mało danych na raport | Ostrzeżenie: raport <30 orzeczeń mało informatywny |
| Domena niedostępna | Komunikat o konieczności dodania `saos.org.pl` do allowed domains |

Wszystkie skrypty stosują opóźnienie **0.5s między requestami** — szanujemy API SAOS.

---

## Środowiska

### Claude.ai

- Skrypty uruchamiane przez `bash_tool`
- Pliki dostarczane przez `present_files` do `/mnt/user-data/outputs/`
- **Wymaga** dodania `saos.org.pl` do allowed domains w ustawieniach projektu
- Zależność `python-docx` instalowana automatycznie

### Claude Code

- Bezpośredni dostęp do terminala i sieci
- Pliki w katalogu roboczym projektu
- Opcjonalna integracja z Git:
  ```bash
  git add saos-output/
  git commit -m "saos: wyniki dla 'dobro dziecka' (50 orzeczeń)"
  ```

---

## Zasady bezpieczeństwa

- **Prompt injection** — fraza wyszukiwania jest sprawdzana pod kątem poleceń manipulacyjnych przed wykonaniem
- **Anti-hallucination** — skill NIE generuje fikcyjnych sygnatur, dat ani treści orzeczeń. Wszystkie dane pochodzą wyłącznie z API SAOS
- **Raport tematyczny** — każde orzeczenie w raporcie musi istnieć w źródłowym JSON. Grupowanie jest przybliżone i oznaczone jako automatyczne
- **Kodowanie** — UTF-8 na całej ścieżce

---

## Changelog

### v2.0

- Rozdzielenie na 3 skrypty: `szukaj_orzeczen.py`, `saos_fetch.py`, `raport_tematyczny.py`
- Nowy skrypt `saos_fetch.py` — dedykowany fetcher pełnych treści z Browse API (przyjmuje JSON lub listę ID)
- Nowy skrypt `raport_tematyczny.py` — generator raportów tematycznych DOCX
- Tryb `--probe-only` w `szukaj_orzeczen.py` do szybkiego sprawdzania skali wyników
- Workflow raportu tematycznego: search → fetch → analiza AI → JSON config → DOCX
- Struktura raportu: strona tytułowa, podsumowanie, grupy tematyczne (wzorce text mining, wykazy orzeczeń, akty prawne, rozkład sądów), wzorce przekrojowe, wnioski
- Nagłówki sekcji w headerach stron, stopki z numeracją
- Schemat JSON raportu umożliwiający powtarzalne generowanie

### v1.0

- Pojedynczy skrypt `szukaj_orzeczen.py` łączący search + fetch
- Wyszukiwanie z paginacją, JSON + DOCX
- Obsługa retry, backoff, null guards

---

## Licencja

Dane orzeczeń pochodzą z publicznego API SAOS (System Analizy Orzeczeń Sądowych) prowadzonego przez Ministerstwo Sprawiedliwości RP. API jest bezpłatne i nie wymaga autoryzacji.

Kod skryptów: do dowolnego użytku.

---

## Autor

#Grzegorz Skuza

skill stworzony jako element zestawu polskojęzycznych narzędzi AI do pracy z dokumentami prawnymi i profesjonalnymi.
