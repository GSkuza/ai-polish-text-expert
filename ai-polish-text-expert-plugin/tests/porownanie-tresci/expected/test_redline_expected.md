# Oczekiwane zachowanie: test_redline (V1 vs V2)

## Parametry wejścia
- Dwa dokumenty: raport CRM V1 i V2 (wersje tego samego dokumentu)
- Tryb: --redline powinien być sugerowany automatycznie (>70% wspólnej treści)

## Oczekiwane wykrycia w trybie redline

### Zmiany kluczowe
1. **Termin zakończenia zmieniony**: 30 września → 31 października (zmiana)
2. **Postęp**: 65% → 85% (zmiana danych liczbowych)
3. **Moduł raportowania**: „w fazie testów" → „przeszedł testy, wdrożony produkcyjnie" (zmiana statusu)
4. **Integracja ERP**: „wymaga dodatkowych prac" → „ukończona 20 sierpnia" (zmiana statusu)
5. **Nowa sekcja**: „4. Budżet" — dodana w V2 (brak w V1)
6. **Rekomendacje zmienione**: inne zalecenia w V2

### Statystyki zmian
- Fragmenty dodane: sekcja Budżet, szczegóły dat ukończenia modułów
- Fragmenty usunięte: wzmianka o 3-tygodniowym szacunku prac ERP
- Fragmenty zmienione: termin, procent realizacji, status ryzyk

## Oczekiwane zachowanie agenta
- Agent powinien zasugerować tryb --redline (dokumenty to wersje)
- Raport powinien zawierać wizualny diff z kolorami
- Statystyki zmian powinny być w Części I raportu
