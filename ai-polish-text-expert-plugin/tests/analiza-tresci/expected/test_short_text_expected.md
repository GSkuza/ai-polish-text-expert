# Oczekiwane zachowanie: test_short_text.txt

## Parametry wejścia
- Długość: ~70 słów (poniżej progu 500 słów)
- Gatunek: tekst publicystyczny / marketingowy

## Oczekiwane zachowanie agenta
1. **Tryb C (quick check)** powinien się aktywować automatycznie
2. Agent powinien wyświetlić komunikat o trybie quick check
3. Odpowiedź powinna być w czacie (bez DOCX)
4. Jeśli użytkownik powie „pełna analiza" — przejście do 8 filarów

## Kluczowe punkty do wykrycia
- Gatunek: artykuł publicystyczny lub tekst marketingowy
- Argument z autorytetu: „Zdaniem ekspertów" — brak wskazania których ekspertów
- Styl: mieszany (informacyjny + perswazyjny)
- Brak danych źródłowych
