from logging import exception

from PySide6.QtWidgets import (QApplication,QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QComboBox)
import sys
import random
import csv
import os
import json


#Losowanie kolorów
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

#Przykład użycia
print("Wylosowana liczba:", miejsce1.get_liczba(),
      miejsce2.get_liczba(),
      miejsce3.get_liczba(),
      miejsce4.get_liczba())

#print("Kolor słownie:", miejsce1.get_kolor_slownie(),
#      miejsce2.get_kolor_slownie(),
#      miejsce3.get_kolor_slownie(),
#      miejsce4.get_kolor_slownie())


# Przykład tajnego kodu
tajny_kod = [miejsce1.get_liczba(), miejsce2.get_liczba(), miejsce3.get_liczba(), miejsce4.get_liczba()]

def sprawdz_kod(propozycja, tajny_kod):
    wynik = [None] * 4
    tajny_kod_tmp = tajny_kod.copy()
    propozycja_tmp = propozycja.copy()

    # 1. Szukamy trafień idealnych ("czarna")
    for i in range(4):
        if propozycja[i] == tajny_kod[i]:
            wynik[i] = 'czarna'
            tajny_kod_tmp[i] = None
            propozycja_tmp[i] = None

    # 2. Szukamy trafień złą pozycją ("biała")
    for i in range(4):
        if propozycja_tmp[i] is not None and propozycja_tmp[i] in tajny_kod_tmp:
            idx = tajny_kod_tmp.index(propozycja_tmp[i])
            wynik[i] = 'biała'
            tajny_kod_tmp[idx] = None

    return wynik

# Główna pętla gry
wygrana = False
while not wygrana:
    kod_str = input("Podaj 4-cyfrowy kod (np. 1234): ")
    if len(kod_str) != 4 or not kod_str.isdigit():
        print("Poprawny format to np. 1234")
        continue

    propozycja = [int(c) for c in kod_str]
    wynik = sprawdz_kod(propozycja, tajny_kod)

    print(f"Wynik: {wynik}")

    if wynik.count('czarna') == 4:
        print("Gratulacje! Wygrałeś!")
        wygrana = True
