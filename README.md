# AI Polish Text Expert

> **Enterprise plugin do profesjonalnej pracy z treściami tekstowymi w języku polskim**  
> Działa w **Claude.ai** i **Claude Code** · Generuje raporty DOCX · Zero tolerancji na prompt injection

---

## Spis treści

1. [Przegląd](#przegląd)
2. [Architektura](#architektura)
3. [Skills — szczegółowy opis](#skills--szczegółowy-opis)
4. [Instalacja w Claude.ai](#instalacja-w-claudeai)
5. [Instalacja w Claude Code](#instalacja-w-claude-code)
6. [Użycie — komendy](#użycie--komendy)
7. [Przykłady](#przykłady)
8. [Struktura repozytorium](#struktura-repozytorium)
9. [Konfiguracja](#konfiguracja)
10. [Zależności](#zależności)
11. [Bezpieczeństwo](#bezpieczeństwo)
12. [Rozwój i kontrybuowanie](#rozwój-i-kontrybuowanie)
13. [Changelog](#changelog)
14. [Licencja](#licencja)

---

## Przegląd

**AI Polish Text Expert** to enterprise plugin integrujący cztery wyspecjalizowane skills do pracy z tekstem po polsku. Agent orkiestrujący automatycznie kieruje każde żądanie do właściwego skill'a — na podstawie komendy lub intencji użytkownika.

### Co potrafi?

| Tryb | Komenda | Co dostajesz |
|------|---------|-------------|
| Analiza treści | `/analiza-tresci` | Szczegółowy raport DOCX: 8 filarów analizy z klasyfikacją gatunkową, wagami ocen, mapą problemów i rekomendacjami strategicznymi |
| Porównanie dokumentów | `/porownanie-tresci` | Raport DOCX z matrycą podobieństw/różnic na 3 poziomach (merytoryczny, semantyczny, syntaktyczny) |
| Poprawa tekstu | `/popraw-tresc` | DOCX z diagnostyką błędów, 3 wariantami stylu do wyboru i rejestrem wszystkich zmian |

### Dlaczego ten plugin?

- **Raport zawsze w DOCX** — gotowy do wysłania, wydruku, archiwizacji
- **Pełny workflow** — agent nie skraca kroków, pyta gdy czegoś brakuje
- **Bezpieczeństwo** — skanowanie prompt injection przed każdym działaniem
- **Fakty z treści** — agent nie dodaje wiedzy własnej bez wyraźnego oznaczenia `[i] DO WERYFIKACJI`
- **Etapowość** — dłuższe teksty są dzielone na etapy, by zachować spójność stylu

---

## Architektura

```
ai-polish-text-expert/
 └─ ai-polish-text-expert-plugin/
      ├─ .claude/
      │    └─ commands/                 ← Komendy Claude Code (slash commands)
      │         ├─ ai-polish-text-expert.md
      │         ├─ analiza-tresci.md
      │         ├─ popraw-tresc.md
      │         └─ porownanie-tresci.md
      ├─ agents/
      │    └─ ai-polish-text-expert.md   ← Agent orkiestrujący (główny)
      ├─ skills/
      │    ├─ ai-polish-text-expert/     ← Skill główny (routing + wspólna logika)
      │    ├─ analiza-tresci/            ← Skill: analiza 1–5 dokumentów
      │    ├─ porownanie-tresci/         ← Skill: porównanie 2–3 dokumentów
      │    ├─ popraw-tresc/              ← Skill: refaktoryzacja i korekta
      │    └─ pdf-processor/             ← Skill pomocniczy: ekstrakcja z PDF
      ├─ commands/                       ← Komendy CLI (status, logs)
      ├─ hooks/                          ← Hooki pre/post-commit
      ├─ scripts/                        ← Narzędzia pomocnicze
      ├─ .claude-plugin/plugin.json      ← Manifest pluginu
      ├─ .mcp.json                       ← Definicje serwerów MCP
      ├─ .lsp.json                       ← Konfiguracja serwerów LSP
      └─ settings.json                   ← Ustawienia pluginu
```

### Przepływ danych

```
Użytkownik
    │  komenda lub intencja
    ▼
Agent orkiestrujący (ai-polish-text-expert.md)
    │
    ├─ Krok 0: Skanowanie prompt injection ──────────── [STOP jeśli wykryto]
    │
    ├─ Krok 1: Routing (komenda / intencja / menu)
    │
    ├─ Krok 2: Pre-flight (format, rozmiar, PDF→text)
    │
    ├──┬──────────────────┬──────────────────┐
    ▼  ▼                  ▼                  ▼
analiza-    porownanie-    popraw-       pdf-processor
tresci      tresci         tresc         (pomocniczy)
    │              │            │
    └──────┬────────┘            │
           ▼                     ▼
    Raport DOCX → /mnt/user-data/outputs/ → present_files
           │
    Podsumowanie w czacie (3–6 zdań)
```

---

## Skills — szczegółowy opis

### 1. `ai-polish-text-expert` — Skill orkiestrujący

**Plik:** `skills/ai-polish-text-expert/ai-polish-text-expert.skill`

Główny skill zawierający wspólną logikę dla wszystkich trybów:
- Routing do właściwego trybu na podstawie komendy lub intencji
- Wspólna konfiguracja generacji DOCX (paleta kolorów, fonty, odznaki statusu)
- Zasady bezpieczeństwa (prompt injection)
- Metody ekstrakcji tekstu (PDF, DOCX, TXT)

**Wewnętrzna struktura (wewnątrz archiwum .skill):**
```
polski-tekst/
├── SKILL.md             ← Manifest i routing
└── references/
    ├── analiza-tresci.md
    ├── porownanie-tresci.md
    └── popraw-tresc.md
```

---

### 2. `analiza-tresci` — Analiza treści

**Plik:** `skills/analiza-tresci/analiza-tresci.skill`  
**Komenda:** `/analiza-tresci`

#### Wejście
- Formaty: `.txt`, `.docx`, `.pdf`, `.md`, `.json`, wklejona treść
- Liczba plików: 1–5 jednocześnie
- Jeden raport DOCX per materiał

#### Klasyfikacja gatunkowa

Przed analizą skill identyfikuje gatunek materiału (raport, artykuł, marketing, dokumentacja techniczna, tekst prawny, materiał edukacyjny, transkrypt, korespondencja, social media, tekst naukowy) i dobiera wagi ocen do jego specyfiki.

#### 8 filarów analizy

| Filar | Opis |
|-------|------|
| **1. Identyfikacja i kontekst** | Temat, intencja, odbiorcy, mapa pojęć kluczowych |
| **2. Architektura strukturalna** | Makro- i mikrostruktura, progresja tematyczna, konektory, łańcuchy anaforyczne |
| **3. Jakość argumentacji** | Mapa argumentów, błędy logiczne, ocena jakości dowodów |
| **4. Warstwa językowa** | Poprawność normatywna, styl/rejestr, metryki czytelności (FOG, SLD, strona bierna) |
| **5. Analiza retoryczna** | Ethos/logos/pathos, techniki retoryczne, ton emocjonalny |
| **6. Ocena punktowa** | 8 kryteriów z wagami gatunkowymi → wynik 1–10, werdykt ✅ / ⚠️ / ❌ |
| **7. Mapa problemów** | Tabela [P1]/[P2]/[P3] z lokalizacją, typem i działaniem naprawczym |
| **8. Podsumowanie eksperckie** | Diagnoza, mocne strony, ryzyka, rekomendacje (Natychmiast / Następna iteracja / Perspektywicznie) |

#### Workflow
```
KROK 0: Bezpieczeństwo (prompt injection)
KROK 1: Ekstrakcja treści (PDF/DOCX/TXT/MD/JSON)
KROK 2: Potwierdzenie listy materiałów z użytkownikiem
KROK 3: Analiza każdego materiału osobno (klasyfikacja gatunkowa + 8 filarów)
KROK 4: Weryfikacja faktów przed publikacją raportu
KROK 5: Generacja raportu DOCX per materiał (font Aptos, tabele z wagami)
KROK 6: Walidacja DOCX + dostarczenie pliku + podsumowanie
```

---

### 3. `porownanie-tresci` — Porównanie dokumentów

**Plik:** `skills/porownanie-tresci/porownanie-tresci.skill`  
**Komenda:** `/porownanie-tresci`

#### Wejście
- Formaty: `.txt`, `.docx`, `.pdf`, wklejona treść
- Liczba dokumentów: **dokładnie 2 lub 3**
- Jeden zbiorczy raport DOCX

#### Trójwarstwowa analiza

| Warstwa | Co bada |
|---------|---------|
| **Merytoryczna** | Wiedza domenowa, fakty, argumenty, dane liczbowe |
| **Semantyczna** | Znaczenie, pojęcia, konteksty, metafory |
| **Syntaktyczna** | Struktura zdań, długość, styl, interpunkcja |

#### Matryca zgodności

Raport zawiera macierz N×N pokazującą procentowe podobieństwo każdej pary dokumentów na każdej warstwie analizy.

#### Workflow
```
KROK 0: Bezpieczeństwo (każdy dokument osobno)
KROK 1: Przyjęcie dokumentów + doprecyzowanie zakresu
KROK 2: Analiza indywidualna każdego dokumentu
KROK 3: Ekstrakcja encji (osoby, instytucje, daty, kwoty)
KROK 4: Porównanie trójwarstwowe
KROK 5: Budowa matrycy zgodności
KROK 6: Generacja zbiorczego raportu DOCX
KROK 7: Dostarczenie pliku + podsumowanie
```

---

### 4. `popraw-tresc` — Poprawa i refaktoryzacja

**Plik:** `skills/popraw-tresc/popraw-tresc.skill`  
**Komenda:** `/popraw-tresc`

#### Wejście
- Formaty: `.txt`, `.docx`, `.pdf`, wklejona treść
- **Jeden plik / jedna treść** na raz
- Limit: **10 000 znaków ze spacjami** na etap (dłuższe teksty → podział etapowy)

#### Pipeline

```
DIAGNOSTYKA  →  ODBIORCA  →  PRÓBKI STYLU  →  WYBÓR  →  PRZEPISANIE  →  DOCX
```

| Etap | Opis |
|------|------|
| **Diagnostyka** | Błędy gramatyczne, ortograficzne, kalki językowe, kalki składniowe, nieścisłości merytoryczne |
| **Profil odbiorcy** | Kim jest odbiorca? Formalność, wiedza domenowa, oczekiwania |
| **3 warianty stylu** | Formalny / Neutralny / Swobodny — próbka 200–300 słów każdy |
| **Wybór użytkownika** | Użytkownik wybiera wariant lub podaje modyfikacje |
| **Przepisanie** | Pełna treść w wybranym stylu — od nowa, nie patch |
| **Raport DOCX** | Treść oryginalna / Treść poprawiona / Rejestr zmian z kategoryzacją |

#### Rejestr zmian w raporcie

| Kategoria | Badge | Opis |
|-----------|-------|------|
| Błąd gramatyczny | `[X]` | Niepoprawna forma |
| Błąd ortograficzny | `[X]` | Literówka, zapis |
| Kalka językowa | `[!]` | Dosłowne tłumaczenie |
| Nieścisłość merytoryczna | `[!]` | Nieprecyzyjne sformułowanie |
| Poprawa stylistyczna | `[i]` | Ulepszenie bez błędu |

---

### 5. `pdf-processor` — Przetwarzanie PDF (skill pomocniczy)

**Lokalizacja:** `skills/pdf-processor/`

Skill pomocniczy uruchamiany automatycznie przez agenta, gdy wejście zawiera plik PDF. Nie jest wywoływany bezpośrednio przez użytkownika.

#### Metody ekstrakcji

```python
# Priorytet 1: pdfplumber (natywny tekst)
import pdfplumber
with pdfplumber.open(path) as pdf:
    text = "\n".join(
        f"\n--- Strona {i+1} ---\n{p.extract_text()}"
        for i, p in enumerate(pdf.pages) if p.extract_text()
    )

# Fallback: OCR (skany i obrazy w PDF)
# pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path
pages = convert_from_path(path, dpi=300)
text = "\n".join(pytesseract.image_to_string(p, lang='pol') for p in pages)
```

#### Obsługiwane przypadki

| Typ PDF | Metoda |
|---------|--------|
| PDF z natywnym tekstem | `pdfplumber` |
| PDF ze skanem (obraz) | OCR: `pytesseract` + `pdf2image` |
| PDF mieszany | `pdfplumber` strona po stronie, OCR dla pustych stron |

---

## Instalacja w Claude.ai

Są **dwa sposoby** instalacji skills — przez panel **customizacji konta** (globalne, działają w każdej konwersacji) lub przez **ustawienia projektu** (tylko w wybranym projekcie).

---

### Sposób 1 — Customizacja konta (zalecany)

Skills zainstalowane tą metodą są dostępne **we wszystkich konwersacjach** na Twoim koncie Claude.ai — nie musisz tworzyć projektu.

#### Wymagania
- Konto Claude.ai (Free, Pro lub Team)

#### Kroki instalacji

1. **Otwórz panel customizacji skills** w przeglądarce:
   ```
   https://claude.ai/customize/skills
   ```
   Alternatywnie: kliknij swój awatar (prawy górny róg) → **Ustawienia** → **Skills** (lub **Umiejętności**)

2. **Dodaj skill główny** (wymagany jako pierwszy):
   ```
   Kliknij  "Dodaj umiejętność"  →  "Wgraj plik .skill"
   → Wybierz: ai-polish-text-expert-plugin/skills/ai-polish-text-expert/ai-polish-text-expert.skill
   → Potwierdź
   ```

3. **Dodaj pozostałe skills** w ten sam sposób (kolejność dowolna):

   | Plik do wgrania | Skill |
   |-----------------|-------|
   | `skills/analiza-tresci/analiza-tresci.skill` | Analiza treści |
   | `skills/porownanie-tresci/porownanie-tresci.skill` | Porównanie dokumentów |
   | `skills/popraw-tresc/popraw-tresc.skill` | Poprawa i refaktoryzacja tekstu |

4. **Upewnij się, że skills są aktywne** — każdy powinien mieć przełącznik w pozycji **włączony** (zielony)

5. **Weryfikacja** — otwórz **nową konwersację** i wpisz:
   ```
   /analiza-tresci
   ```
   Agent powinien odpowiedzieć prośbą o dostarczenie pliku/treści.

#### Zarządzanie skills

| Akcja | Jak |
|-------|-----|
| Wyłącz skill (tymczasowo) | Przełącznik → wyłączony na stronie [customize/skills](https://claude.ai/customize/skills) |
| Usuń skill | Kliknij ikonę kosza obok skill'a |
| Zaktualizuj skill | Usuń starą wersję → wgraj nowy plik `.skill` |
| Sprawdź zainstalowane | Otwórz [claude.ai/customize/skills](https://claude.ai/customize/skills) |

#### Uwagi (customizacja konta)

- Skills z customizacji działają **globalnie** — w każdej nowej konwersacji, bez potrzeby tworzenia projektu
- Możesz mieć jednocześnie skills globalne (customizacja) i projektowe (sposób 2)
- Przy konflikcie nazw komend — skill projektowy ma wyższy priorytet

---

### Sposób 2 — W ustawieniach projektu (opcjonalny)

Jeśli chcesz ograniczyć skills do konkretnego projektu:

#### Wymagania
- Konto Claude.ai z dostępem do **projektów**
- Uprawnienia do dodawania skills w projekcie

#### Kroki instalacji

1. **Utwórz projekt** (lub otwórz istniejący) w Claude.ai

2. **Przejdź do ustawień projektu** → zakładka **Skills / Umiejętności**

3. **Dodaj skill główny** (wymagany jako pierwszy):
   ```
   Kliknij "Dodaj umiejętność z pliku"
   → Wybierz: ai-polish-text-expert-plugin/skills/ai-polish-text-expert/ai-polish-text-expert.skill
   → Potwierdź instalację
   ```

4. **Dodaj pozostałe skills** (kolejność nie ma znaczenia):
   ```
   ai-polish-text-expert-plugin/skills/analiza-tresci/analiza-tresci.skill
   ai-polish-text-expert-plugin/skills/porownanie-tresci/porownanie-tresci.skill
   ai-polish-text-expert-plugin/skills/popraw-tresc/popraw-tresc.skill
   ```

5. **Weryfikacja** — po instalacji w oknie czatu wpisz:
   ```
   /analiza-tresci
   ```
   Agent powinien odpowiedzieć prośbą o dostarczenie pliku/treści.

---

### Uwagi wspólne

- Pliki DOCX generowane przez skills są zapisywane w `/mnt/user-data/outputs/` i udostępniane przez Claude
- Zainstalowane skills nie wymagają ponownej konfiguracji przy każdej sesji
- Pliki `.skill` to archiwa ZIP — nie rozpakowuj ich przed wgraniem

---

## Instalacja w Claude Code

### Wymagania
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) zainstalowany lokalnie (`npm install -g @anthropic-ai/claude-code`)
- Node.js ≥ 18 lub Python ≥ 3.10 (dla skryptów pomocniczych)

### Kroki instalacji

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/GSkuza/ai-polish-text-expert.git
cd ai-polish-text-expert

# 2. Zainstaluj zależności Python (dla przetwarzania PDF)
pip install pdfplumber pytesseract pdf2image

# 3. Zainstaluj zależności Node.js (dla generowania DOCX)
npm install -g docx

# 4. (Opcjonalnie) Sprawdź dostępność pandoc
pandoc --version
```

### Uruchomienie Claude Code

```bash
# Uruchom Claude Code w katalogu repozytorium
cd ai-polish-text-expert
claude
```

Claude Code automatycznie odczyta:
- **`CLAUDE.md`** — instrukcje projektowe (jeśli istnieje w katalogu głównym)
- **`.mcp.json`** — definicje serwerów MCP w `ai-polish-text-expert-plugin/`
- **`ai-polish-text-expert-plugin/agents/`** — dokumentację agentów jako kontekst
- **`ai-polish-text-expert-plugin/.claude/commands/`** — slash-komendy (`/analiza-tresci`, `/popraw-tresc`, `/porownanie-tresci`) dostępne bezpośrednio w Claude Code

### Praca z pluginem w Claude Code

W sesji interaktywnej Claude Code możesz:

```bash
# Poproś o analizę pliku
> Przeanalizuj plik ai-polish-text-expert-plugin/README.md pod kątem językowym

# Poproś o porównanie dokumentów
> Porównaj pliki doc1.txt i doc2.txt

# Poproś o poprawę tekstu
> Popraw tekst w pliku artykul.md — ma być w stylu formalnym

# Załaduj kontekst agenta
> @ai-polish-text-expert-plugin/agents/ai-polish-text-expert.md — użyj tego workflow do analizy
```

> **Wskazówka:** W Claude Code możesz używać slash-komend (`/analiza-tresci`, `/popraw-tresc`, `/porownanie-tresci`) zdefiniowanych w `.claude/commands/` — lub opisać zadanie naturalnym językiem, a Claude Code dobierze odpowiedni workflow.

### Różnice: Claude.ai vs Claude Code

| Aspekt | Claude.ai | Claude Code |
|--------|-----------|-------------|
| Skills `.skill` | Wgrywasz przez UI | Nie dotyczy — używasz plików `.md` jako kontekst |
| Komendy | `/analiza-tresci`, `/popraw-tresc` | Opisy naturalne: „przeanalizuj...", „popraw..." |
| Output DOCX | `/mnt/user-data/outputs/` | Lokalny katalog projektu |
| Praca z plikami | Załączasz w czacie | Agent czyta/zapisuje bezpośrednio |

### Konfiguracja hooks (opcjonalnie)

Hooks pre-commit i pre-push są zdefiniowane w `hooks/hooks.json`. Aby je aktywować:

```bash
# Aktywuj hooks git
cp ai-polish-text-expert-plugin/hooks/hooks.json .git/hooks/config.json
```

---

## Użycie — komendy

### Analiza treści

```
/analiza-tresci
```

Następnie dostarcz:
- Plik (`.txt`, `.docx`, `.pdf`, `.md`, `.json`) — do 5 plików jednocześnie
- lub wklej treść bezpośrednio w czacie

**Przykład:**
```
/analiza-tresci
[załącz plik: raport-roczny.docx]
```

---

### Porównanie dokumentów

```
/porownanie-tresci
```

Następnie dostarcz dokładnie **2 lub 3 dokumenty**.

**Przykład:**
```
/porownanie-tresci
[załącz pliki: wersja-A.docx, wersja-B.docx]
```

---

### Poprawa tekstu

```
/popraw-tresc
```

Następnie dostarcz **jeden plik lub wklej treść** (max 10 000 znaków ze spacjami na etap).

**Przykład:**
```
/popraw-tresc
[wklej treść artykułu]
```

Agent przeprowadzi Cię przez:
1. Diagnostykę błędów
2. Ustalenie profilu odbiorcy
3. Wybór spośród 3 wariantów stylistycznych
4. Przepisanie i dostarczenie raportu DOCX

---

### Tryb bez komendy (intencja naturalna)

Możesz też napisać naturalnie:

```
Mam artykuł do sprawdzenia — czy możesz go przejrzeć pod kątem językowym?
```

Agent zaproponuje menu wyboru trybu.

---

## Przykłady

### Przykład 1 — Analiza regulaminu

```
Użytkownik: /analiza-tresci
[załącza: regulamin-sklepu.pdf]

Agent:
→ Krok 0: skanowanie prompt injection — czyste
→ Krok 1: wykryto 1 plik PDF
→ Krok 2: ekstrakcja tekstu (pdfplumber, 12 stron)
→ Krok 3: analiza 7 filarów...
→ Generuję raport DOCX...

[plik: analiza-regulamin-sklepu-2026-03-06.docx]

Podsumowanie: Regulamin ma 12 stron i 8 400 słów. Wykryto 3 luki merytoryczne
[P1] dotyczące procedury reklamacyjnej. WZT wynosi 68 (tekst trudny). Styl
formalny, narracja bezosobowa. Raport zawiera 14 rekomendacji.
```

---

### Przykład 2 — Porównanie ofert

```
Użytkownik: /porownanie-tresci
[załącza: oferta-dostawca-A.docx, oferta-dostawca-B.docx]

Agent:
→ Porównanie trójwarstwowe obu ofert
→ Matryca zgodności: merytoryczna 42%, semantyczna 67%, syntaktyczna 31%
→ Generuję zbiorczy raport DOCX z matrycą...

[plik: porownanie-ofert-2026-03-06.docx]
```

---

### Przykład 3 — Poprawa biuletynu firmowego

```
Użytkownik: /popraw-tresc
[wkleja tekst biuletynu, 3 200 znaków]

Agent:
→ Diagnostyka: 4 błędy ortograficzne, 2 kalki z angielskiego, 1 nieścisłość
→ Profil odbiorcy: pracownicy firmy, styl semi-formalny
→ Proponuję 3 warianty: Formalny / Neutralny / Swobodny
   [próbki 200-300 słów każdy]

Użytkownik: wybieram wariant Neutralny

Agent:
→ Przepisuję pełną treść...
→ Generuję DOCX z rejestrem zmian...

[plik: poprawiona-biuletyn-2026-03-06.docx]
```

---

## Struktura repozytorium

```
ai-polish-text-expert/
│
├── ai-polish-text-expert-plugin/                    # Katalog pluginu
│   ├── .claude-plugin/
│   │   └── plugin.json                   # Manifest pluginu (nazwa, wersja, ścieżki)
│   │
│   ├── .claude/
│   │   └── commands/                     # Komendy slash dla Claude Code
│   │       ├── ai-polish-text-expert.md  # Komenda: /ai-polish-text-expert
│   │       ├── analiza-tresci.md         # Komenda: /analiza-tresci
│   │       ├── popraw-tresc.md           # Komenda: /popraw-tresc
│   │       └── porownanie-tresci.md      # Komenda: /porownanie-tresci
│   │
│   ├── agents/
│   │   ├── ai-polish-text-expert.md      # ← Agent orkiestrujący (główny)
│   │   ├── security-reviewer.md          # Agent: przegląd bezpieczeństwa kodu
│   │   ├── performance-tester.md         # Agent: testowanie wydajności
│   │   └── compliance-checker.md         # Agent: zgodność RODO/zasady językowe
│   │
│   ├── skills/
│   │   ├── ai-polish-text-expert/
│   │   │   └── ai-polish-text-expert.skill   # Skill główny (ZIP): routing + logika wspólna
│   │   ├── analiza-tresci/
│   │   │   └── analiza-tresci.skill          # Skill: analiza 1–5 dokumentów
│   │   ├── porownanie-tresci/
│   │   │   └── porownanie-tresci.skill       # Skill: porównanie 2–3 dokumentów
│   │   ├── popraw-tresc/
│   │   │   └── popraw-tresc.skill            # Skill: refaktoryzacja i korekta
│   │   └── pdf-processor/
│   │       ├── SKILL.md                      # Dokumentacja skill'a pomocniczego
│   │       └── scripts/
│   │           └── README.md
│   │
│   ├── commands/
│   │   ├── status.md                     # Komenda: /status — stan pluginu
│   │   └── logs.md                       # Komenda: /logs — logi pluginu
│   │
│   ├── hooks/
│   │   ├── hooks.json                    # Hooki pre/post-commit, pre-push
│   │   └── security-hooks.json           # Hooki bezpieczeństwa (audit, SAST)
│   │
│   ├── scripts/
│   │   ├── security-scan.sh              # Skanowanie bezpieczeństwa (gitleaks, bandit)
│   │   ├── format-code.py                # Formatowanie kodu (black, flake8, prettier)
│   │   └── deploy.js                     # Deployment i server MCP
│   │
│   ├── settings.json                     # Ustawienia pluginu (AI, features, logging)
│   ├── .mcp.json                         # Definicje serwerów MCP
│   ├── .lsp.json                         # Konfiguracja serwerów LSP
│   ├── LICENSE                           # Licencja MIT
│   └── CHANGELOG.md                      # Historia zmian
│
├── skill-plugin.json                     # Schemat struktury pluginu (dokumentacja)
└── README.md                             # Ten plik
```

---

## Konfiguracja

### settings.json

Główny plik konfiguracyjny pluginu:

```jsonc
{
  "plugin": {
    "name": "ai-polish-text-expert",
    "version": "1.0.0",
    "locale": "pl-PL",           // Lokalizacja: polskie locale
    "timezone": "Europe/Warsaw"
  },
  "ai": {
    "temperature": 0.01,         // Niska temperatura = deterministyczne odpowiedzi
    "maxTokens": 8192,           // Limit tokenów per odpowiedź
    "systemPrompt": "..."        // Prompt systemowy agenta
  },
  "features": {
    "spellCheck": true,          // Sprawdzanie ortografii
    "grammarCheck": true,        // Sprawdzanie gramatyki
    "styleAnalysis": true,       // Analiza stylistyczna
    "readabilityScore": true,    // WZT — Wskaźnik Zawiłości Tekstu
    "plagiarismDetection": false // Wykrywanie plagiatów (domyślnie wyłączone)
  },
  "output": {
    "format": "markdown",        // Format odpowiedzi w czacie
    "includeExplanations": true, // Dołącz wyjaśnienia do każdej zmiany
    "language": "pl"             // Język raportów
  },
  "logging": {
    "level": "info",             // Poziom logowania: debug|info|warn|error
    "maxFiles": 10,              // Rotacja logów
    "maxSize": "10m"             // Maks. rozmiar pliku logu
  }
}
```

### .mcp.json — Serwery MCP

```json
{
  "mcpServers": {
    "polish-text-server": {
      "command": "node",
      "args": ["./scripts/deploy.js", "--mode=mcp"],
      "env": { "LOCALE": "pl-PL" }
    },
    "pdf-processor-server": {
      "command": "python",
      "args": ["-m", "pdf_processor.server"],
      "env": { "PYTHONPATH": "./skills/pdf-processor/scripts" }
    }
  }
}
```

### .lsp.json — Serwery LSP

Konfiguracja Language Server Protocol dla środowisk deweloperskich:
- `polish-language-server` — sprawdzanie pisowni w plikach `.md`, `.txt`
- `python` — `pylsp` dla plików `.py` w projekcie

---

## Zależności

### Python

```bash
pip install pdfplumber pytesseract pdf2image --break-system-packages
```

| Pakiet | Wersja min. | Zastosowanie |
|--------|------------|-------------|
| `pdfplumber` | ≥ 0.9 | Ekstrakcja tekstu z PDF |
| `pytesseract` | ≥ 0.3 | OCR dla skanów |
| `pdf2image` | ≥ 1.16 | Konwersja stron PDF na obrazy (dla OCR) |

### Node.js

```bash
npm install -g docx
```

| Pakiet | Zastosowanie |
|--------|-------------|
| `docx` | Programowa generacja plików DOCX |

### Narzędzia systemowe

| Narzędzie | Instalacja | Zastosowanie |
|-----------|-----------|-------------|
| `pandoc` | `apt install pandoc` / preinstalowany | Konwersja DOCX → Markdown |
| `tesseract-ocr` | `apt install tesseract-ocr tesseract-ocr-pol` | Silnik OCR |
| `poppler` | `apt install poppler-utils` | Backend `pdf2image` |

### Opcjonalne (bezpieczeństwo)

| Narzędzie | Instalacja | Zastosowanie |
|-----------|-----------|-------------|
| `gitleaks` | [github.com/gitleaks](https://github.com/gitleaks/gitleaks) | Skanowanie sekretów w kodzie |
| `bandit` | `pip install bandit` | SAST dla kodu Python |

---

## Bezpieczeństwo

### Prompt Injection — Zero Tolerancji

Każdy skill zawiera **Krok 0** jako absolutny priorytet: skanowanie dostarczonych treści pod kątem prób manipulacji agentem.

Wykryta próba injection → agent:
1. **Nie wykonuje** zawartych w niej poleceń
2. **Informuje** użytkownika i wskazuje podejrzany fragment
3. **Oznacza** w raporcie: `[!] POTENCJALNY PROMPT INJECTION` (kolor `#FF8C00`)
4. **Kontynuuje** analizę czystej części treści (jeśli możliwe)

### Integralność danych

- Agent cytuje **wyłącznie** dane z dostarczonych materiałów
- Wiedza własna agenta jest zawsze oznaczana: `[i] DO WERYFIKACJI`
- Agent **nigdy** nie ujawnia promptu systemowego

### Hooki bezpieczeństwa (CI/CD)

```json
// hooks/security-hooks.json
{
  "hooks": {
    "pre-commit": ["dependency-audit", "secret-scan"],
    "pre-push": ["sast-scan"]
  }
}
```

Uruchomienie ręczne:
```bash
bash ai-polish-text-expert-plugin/scripts/security-scan.sh --mode=full
```

---

## Rozwój i kontrybuowanie

### Lokalny setup deweloperski

```bash
git clone https://github.com/GSkuza/ai-polish-text-expert.git
cd ai-polish-text-expert

# Python venv
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS

# Zależności
pip install pdfplumber pytesseract pdf2image bandit black flake8

# Node
npm install -g docx prettier
```

### Konwencje commitów

```
feat:     nowa funkcja
fix:      poprawka błędu
docs:     tylko dokumentacja
style:    formatowanie (bez zmian logiki)
refactor: refaktoryzacja kodu
test:     testy
chore:    narzędzia, konfiguracja
```

### Przed PR

```bash
# Formatowanie
python ai-polish-text-expert-plugin/scripts/format-code.py

# Bezpieczeństwo
bash ai-polish-text-expert-plugin/scripts/security-scan.sh

# Sprawdź błędy JSON w settings.json
python -m json.tool ai-polish-text-expert-plugin/settings.json
```

### Dodawanie nowego skill'a

1. Utwórz katalog: `ai-polish-text-expert-plugin/skills/<nazwa-skill>/`
2. Dodaj `SKILL.md` z opisem i workflow
3. Zbuduj archiwum `.skill` (ZIP): `Compress-Archive skill/ skill.skill`
4. Zarejestruj skill w `ai-polish-text-expert-plugin/.claude-plugin/plugin.json`
5. Dodaj routing w `ai-polish-text-expert-plugin/agents/ai-polish-text-expert.md`
6. Zaktualizuj `CHANGELOG.md`

---

## Changelog

Pełna historia zmian: [ai-polish-text-expert-plugin/CHANGELOG.md](ai-polish-text-expert-plugin/CHANGELOG.md)

### v1.0.1 (2026-03-07)

- `analiza-tresci`: rozbudowa z 7 do **8 filarów analizy eksperckiej**
- Dodano klasyfikację gatunkową materiału z 10 typami (raport, marketing, prawo, nauka…)
- Dodano tabele wag gatunkowych dla oceny punktowej (każdy gatunek ma inne wagi kryteriów)
- Rozszerzono Filar 2 o analizę mikrostruktury (progresja tematyczna, konektory, łańcuchy anaforyczne)
- Nowy Filar 3: szczegółowa mapa błędów logicznych (10 typów) + tabela jakości dowodów
- Nowy Filar 4: metryki czytelności (FOG, SLD, gęstość terminologiczna, odsetek strony biernej)
- Nowy Filar 5: analiza retoryczna (ethos/logos/pathos, techniki retoryczne, mapa tonu)
- Krok 4: weryfikacja wiedzy przed publikacją raportu
- Zaktualizowano `.claude/commands/analiza-tresci.md` i `analiza-tresci.skill`

### v1.0.0 (2026-03-06)

- Inicjalna struktura ai-polish-text-expert-plugin
- Agent orkiestrujący (`ai-polish-text-expert.md`) z pełnym workflow routingu
- 4 skills: `ai-polish-text-expert`, `analiza-tresci`, `porownanie-tresci`, `popraw-tresc`
- Skill pomocniczy `pdf-processor`
- Konfiguracja MCP, LSP, hooks
- Skrypty: `security-scan.sh`, `format-code.py`, `deploy.js`

---

## Licencja

MIT — szczegóły w [ai-polish-text-expert-plugin/LICENSE](ai-polish-text-expert-plugin/LICENSE)

```
Copyright (c) 2026 GSkuza
```

---

*Repozytorium: [github.com/GSkuza/ai-polish-text-expert](https://github.com/GSkuza/ai-polish-text-expert)*
