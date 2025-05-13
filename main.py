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

print("Wylosowana liczba:", miejsce1.get_liczba(),
      miejsce2.get_liczba(),
      miejsce3.get_liczba(),
      miejsce4.get_liczba())

print("Kolor słownie:", miejsce1.get_kolor_slownie(),
      miejsce2.get_kolor_slownie(),
      miejsce3.get_kolor_slownie(),
      miejsce4.get_kolor_slownie())

wygrana = 0
print("Podaj 4 cyfrowy kod",
        "1: Czerwony",
        "2: Niebieski",
        "3: Zielony",
        "4: Żółty",
        "5: Fioletowy",
        "6: Pomarańczowy",sep="\n")
while wygrana != 1:
    try:
        a,b,c,d = input("Kod:")
    except Exception:
        print("Poprawne wpisanie kodu to np. 1234")
        continue
    i = 0
    if int(a)==miejsce1.get_liczba():
       print("Miejsce 1 poprawne")
       i += 1
    if int(b)==miejsce2.get_liczba():
       print("Miejsce 2 poprawne")
       i += 1
    if int(c)==miejsce3.get_liczba():
       print("Miejsce 3 poprawne")
       i += 1
    if int(d)==miejsce4.get_liczba():
       print("Miejsce 4 poprawne")
       i += 1
    if i==4:
        print("Gratulacje! Wygrales")
        wygrana = 1
