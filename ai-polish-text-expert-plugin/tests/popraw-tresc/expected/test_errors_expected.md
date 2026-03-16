# Oczekiwane zachowanie: test_errors.txt

## Parametry wejścia
- Długość: ~180 słów, ~1100 znaków (poniżej limitu 15 000)
- Gatunek: korespondencja formalna / biznesowa

## Znane błędy do wykrycia

### Błędy ortograficzne [X]
1. „dzisiejczym" → „dzisiejszym" (zdanie 1)
2. „stycznie" → „stycznia" (zdanie 1)

### Błędy gramatyczne [X]
3. „rozwiązaniu" → „rozwiązania" (akapit 3, błąd fleksyjny — dopełniacz zamiast celownika)
4. „bardziej efektywniejsze" → „efektywniejsze" lub „bardziej efektywne" (podwójne stopniowanie, akapit 2)

### Brak interpunkcji [X]
5. „zmianach które go dotyczą" → „zmianach, które go dotyczą" (brak przecinka przed „które")

### Redundancje / pleonazmy [!]
6. „współpraca wzajemna" → „współpraca" (pleonazm)
7. „w okresie czasu" → „w okresie" (pleonazm)
8. „dokonanie implementacji" → „implementacja" lub „wdrożenie" (nominalizacja + redundancja)

### Styl / strona bierna [i]
9. „Decyzja została podjęta" → brak sprawcy — kto podjął decyzję?
10. „Pragniemy również zakomunikować, iż" → nadmiernie urzędowy ton, można uprościć

## Oczekiwane zachowanie agenta
- Skill powinien wykryć co najmniej 8 z 10 powyższych problemów
- Karta diagnostyczna powinna zawierać priorytety (WYSOKI dla błędów ortograficznych, ŚREDNI dla pleonazmów)
- Gatunek: korespondencja formalna — styl powinien być dostosowany
