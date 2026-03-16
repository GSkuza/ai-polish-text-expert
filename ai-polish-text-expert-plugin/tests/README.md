# Tests — Walidacja Skills

Ten katalog zawiera przykładowe teksty i oczekiwane wyniki do testowania skills po każdej zmianie promptów.

## Struktura

```
tests/
├── README.md                 ← Ten plik
├── analiza-tresci/
│   ├── test_short_text.txt   ← Tekst <500 słów (powinien uruchomić quick check)
│   ├── test_long_text.txt    ← Tekst >3000 słów (powinien podzielić na partie)
│   └── expected/
│       └── test_short_text_expected.md  ← Oczekiwane zachowanie
├── popraw-tresc/
│   ├── test_errors.txt       ← Tekst ze znanymi błędami
│   ├── test_long_15k.txt     ← Tekst >15k znaków (powinien auto-podzielić)
│   └── expected/
│       └── test_errors_expected.md
├── porownanie-tresci/
│   ├── test_doc_v1.txt       ← Wersja 1 dokumentu (do testu redline)
│   ├── test_doc_v2.txt       ← Wersja 2 dokumentu
│   └── expected/
│       └── test_redline_expected.md
└── integration/
    └── test_intent_routing.md  ← Przypadki testowe routingu intencji
```

## Jak uruchamiać

Testy są manualne — polegają na podaniu tekstu testowego do skilla i porównaniu wyniku z oczekiwanym zachowaniem opisanym w `expected/`.

## Konwencja

- Każdy test ma plik wejściowy (`.txt`) i opis oczekiwanego wyniku (`.md` w `expected/`)
- W opisie oczekiwanego wyniku wskazane są: oczekiwany tryb, kluczowe wykryte problemy, zachowanie agenta
