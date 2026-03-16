# Changelog

All notable changes to **AI Polish Text Expert** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.1.0] - 2026-03-16

### Added
- **analiza-tresci**: tryb `--auto` (pomija krok 2 dla pojedynczego pliku)
- **analiza-tresci**: quick check — uproszczona analiza (tryb C) dla tekstów < 500 słów
- **analiza-tresci**: rozszerzona tabela wag o 4 gatunki (Transkrypt, Korespondencja, Social media, Tekst naukowy)
- **popraw-tresc**: tryb `--preserve-format` — edycja in-place DOCX z zachowaniem formatowania (tabele, nagłówki, obrazki) via python-docx
- **popraw-tresc**: automatyczny podział długich tekstów na etapy (bez interakcji użytkownika)
- **porownanie-tresci**: tryb `--redline` — wizualne porównanie wersji z oznaczonymi zmianami (dodane/usunięte/zmienione)
- **porownanie-tresci**: sekcja „Metodologia Oceny Zgodności" — transparentny opis heurystyki obliczania procentów
- **agent**: disambiguacja drugiego poziomu — precyzujące pytania przy niejednoznacznych frazach
- **shared/**: konfiguracja współdzielona (badges.json, theme.json) — jedno źródło prawdy dla kolorów i odznak
- **tests/**: przypadki testowe dla wszystkich skills + testy routingu intencji

### Changed
- **popraw-tresc**: limit znaków podniesiony z 10 000 do 15 000 na etap
- **settings.json**: usunięto placeholdery GPT-4 (model, temperature, maxTokens), zastąpiono konfiguracją natywną dla Claude
- **settings.json**: wersja → 1.1.0, format wyjściowy → docx
- Zaktualizowano CLAUDE.md i README.md o nowe funkcje i strukturę katalogów

---

## [1.0.0] - 2026-03-06

### Added
- Plugin manifest (`.claude-plugin/plugin.json`)
- Commands: `status`, `logs`
- Agents: `security-reviewer`, `performance-tester`, `compliance-checker`
- Skills: `code-reviewer`, `pdf-processor`
- Hook configurations: `hooks.json`, `security-hooks.json`
- MCP server definitions (`.mcp.json`)
- LSP server configurations (`.lsp.json`)
- Utility scripts: `security-scan.sh`, `format-code.py`, `deploy.js`
- Default plugin settings (`settings.json`)
- MIT License
