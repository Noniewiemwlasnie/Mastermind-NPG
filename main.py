from PySide6.QtWidgets import (QApplication,QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QComboBox)
import sys
import random
import csv
import os
import json

#TODO: Funkcjonalności:
#   Implementacja zasad gry.
#   Gra z komputerem.
#   Ustawienie poziomu trudności.
#   Statystyka wygranych parametrów.
#   Zapis/odczyt stanu gry.
#   Jedna zaproponowane przez grupę.

# Zasady gry

# Elementy gry:
# - Plansza z zasłoniętym rzędem na kod i 10 rzędami na próby.
# - Duże pionki w 6 kolorach (do kodu i prób).
# - Małe szpilki: białe i czarne (do oceny prób).

# Zasady rozgrywki:
# - Gra dla 2 osób; ustalają parzystą liczbę rund.
# - Jeden gracz układa tajny kod z 4 pionków (mogą się powtarzać).
# - Drugi gracz ma 10 prób na odgadnięcie kodu (kolory i kolejność).
# - Po każdej próbie kodujący ocenia ją szpilkami:
#   - Czarna – właściwy kolor i pozycja.
#   - Biała – właściwy kolor, zła pozycja.

# Zakończenie gry:
# - Gra kończy się po trafnym odgadnięciu kodu lub po 10 próbach.
# - Punktacja:
#   - Kodujący: 1 punkt za każdą próbę przeciwnika + 1 za nierozwiązany kod.
#   - Wygrywa gracz z większą liczbą punktów po ustalonej liczbie rund.

# Alternatywna punktacja:
# - Odgadujący: 1 punkt za każdą próbę; wygrywa gracz z mniejszą liczbą punktów.

# Dodatkowa zasada:
# - Jeśli kodujący popełni błąd w ocenie, gra jest powtarzana, a odgadujący dostaje +3 punkty.


#Losowanie liczb
class Kolor:
    def __init__(self):
        self.liczba = random.randint(1, 6)

    def get_kolor_slownie(self):
        switch = {
            1: "Czerwony",
            2: "Niebieski",
            3: "Zielony",
            4: "Żółty",
            5: "Fioletowy",
            6: "Pomarańczowy"
        }
        return switch.get(self.liczba, "Nieznany kolor")

    def get_liczba(self):
        return self.liczba

miejsce1 = Kolor()
miejsce2 = Kolor()
miejsce3 = Kolor()
miejsce4 = Kolor()

print("Wylosowana liczba:", miejsce1.get_liczba(),
      miejsce2.get_liczba(),
      miejsce3.get_liczba(),
      miejsce4.get_liczba())

print("Kolor słownie:", miejsce1.get_kolor_slownie(),
      miejsce2.get_kolor_slownie(),
      miejsce3.get_kolor_slownie(),
      miejsce4.get_kolor_slownie())
