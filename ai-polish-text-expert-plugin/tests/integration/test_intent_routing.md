# Przypadki testowe — Routing intencji agenta

Test waliduje, czy agent orkiestrujący poprawnie routuje wieloznaczne frazy.

## Przypadki jednoznaczne (powinny routować bezpośrednio)

| # | Fraza użytkownika | Oczekiwany skill | Uzasadnienie |
|---|-------------------|-----------------|-------------|
| 1 | „/analiza-tresci" + plik | analiza-tresci | Jawna komenda |
| 2 | „/popraw-tresc" + tekst | popraw-tresc | Jawna komenda |
| 3 | „/porownanie-tresci" + 2 pliki | porownanie-tresci | Jawna komenda |
| 4 | „przeanalizuj ten raport" + 1 plik | analiza-tresci (--auto) | Jednoznaczna intencja + 1 plik |
| 5 | „popraw mi ten tekst" + tekst | popraw-tresc | Jednoznaczna intencja |
| 6 | „porównaj te dwa dokumenty" + 2 pliki | porownanie-tresci | Jednoznaczna intencja + 2 pliki |

## Przypadki wieloznaczne (powinny wyzwolić pytanie precyzujące)

| # | Fraza użytkownika | Pasuje do | Oczekiwane pytanie |
|---|-------------------|-----------|-------------------|
| 7 | „sprawdź mi ten dokument" + 1 plik | analiza / popraw | „Chcesz raport analityczny czy poprawiony tekst?" |
| 8 | „przejrzyj to" + tekst | analiza / popraw | „Chcesz szczegółową analizę czy poprawienie treści?" |
| 9 | „co myślisz o tym tekście?" + tekst | analiza / popraw | Pytanie o cel: analiza vs poprawa |
| 10 | „porównaj i popraw" + 2 pliki | porownanie + popraw | „Zaczynam od porównania, potem poprawimy wybrany" |
| 11 | „sprawdź, czy mówią to samo" + 2 pliki | porownanie / analiza | „Porównanie tych dokumentów czy osobna analiza?" |

## Przypadki niejasne (powinny pokazać menu)

| # | Fraza użytkownika | Oczekiwane zachowanie |
|---|-------------------|---------------------|
| 12 | „pomóż mi z tym tekstem" + plik | Menu 3 trybów |
| 13 | „mam tu coś do obróbki" | Menu 3 trybów |
| 14 | „zajmij się tym dokumentem" + plik | Menu 3 trybów |
