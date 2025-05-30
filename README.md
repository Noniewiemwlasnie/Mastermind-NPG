# Mastermind Game - README (Polska wersja)

## Opis projektu
Jest to implementacja klasycznej gry logicznej Mastermind w języku Python, wykorzystująca bibliotekę PySide6 do tworzenia interfejsu graficznego. Gracz musi odgadnąć sekretny kod kolorów w ograniczonej liczbie prób.

## Opis plików

### `boxy_kolorowe.py`
- Zawiera klasę `ColorBox` reprezentującą interaktywne kolorowe pola w grze.
- Funkcjonalności:
  - 6 różnych kolorów (Czerwony, Niebieski, Zielony, Żółty, Fioletowy, Pomarańczowy)
  - Klikalne pola zmieniające kolory w cyklu
  - Wizualna reprezentacja z nazwami kolorów i stylizowanym tłem

### `commity.csv`
- Historia commitów pokazująca:
  - Datę commita
  - Liczbę commitów danego dnia
  - Nazwiska współtwórców (M.Skowron, K.Salamon, J.Siuzdak)

### `interfejs.py`
- Główny interfejs gry (klasa `MyApp`)
- Funkcjonalności:
  - Interaktywna plansza z kolorowymi polami
  - Przycisk "Zatwierdź" do sprawdzania propozycji
  - Historia gry
  - Licznik pozostałych prób
  - Informacja zwrotna (kolory na dobrych i złych pozycjach)
  - Statystyki (wygrane/przegrane)
  - Integracja z menu

### `losowanie_kolorów.py`
- Zawiera logikę gry:
  - Klasa `Kolor` do losowego generowania kolorów
  - Funkcja `sprawdz_kod` porównująca propozycję gracza z kodem tajnym
  - Zwraca informację o poprawnych pozycjach i kolorach na złych pozycjach

### `main.py`
- Punkt wejścia do aplikacji
- Inicjalizuje i uruchamia aplikację Qt z głównym oknem gry

### `menu.py`
- Implementuje menu opcji gry (klasa `OptionsDialog`)
- Funkcjonalności:
  - Wybór trudności (8, 10 lub 12 prób)
  - Liczba pól do odgadnięcia (4-6)
  - Wyświetlanie statystyk
  - Konfiguracja ustawień

### `setup.py`
- Plik konfiguracyjny określający zależności (PyQt6 i PySide6)

### `statystyki.txt`
- Przechowuje statystyki gry:
  - Pierwsza linia: Liczba wygranych (7)
  - Druga linia: Liczba przegranych (24)

## Jak grać
1. Uruchom plik `main.py` aby rozpocząć grę
2. Wybierz poziom trudności i liczbę pól w menu
3. Klikaj na pola aby zmieniać kolory
4. Naciśnij "Zatwierdź" aby sprawdzić swoją propozycję
5. Otrzymaj informację zwrotną:
   - Czarne punkty: Poprawny kolor na dobrej pozycji
   - Białe punkty: Poprawny kolor na złej pozycji
6. Wygraj odgadując wszystkie kolory przed wyczerpaniem prób

## Funkcje gry
- Regulowana trudność (liczba prób i długość kodu)
- Śledzenie historii gry
- Statystyki wygranych i przegranych
- Responsywny interfejs graficzny
- Kolorowa informacja zwrotna

## Wymagania
- Python 3.x
- PySide6 (zainstaluje się automatycznie przez setup.py)

## Współtwórcy
- M.Skowron
- K.Salamon
- J.Siuzdak
- M. Sakłak
