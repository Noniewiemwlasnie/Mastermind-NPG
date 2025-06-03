#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

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

def sprawdz_kod(propozycja, tajny_kod, ilość_boxów):
    wynik = [None] * ilość_boxów
    tajny_kod_tmp = tajny_kod.copy()
    propozycja_tmp = propozycja.copy()

    # 1. Szukamy trafień idealnych ("w dobrym miejscu")
    for i in range(ilość_boxów):
        if propozycja[i] == tajny_kod[i]:
            wynik[i] = 'czarna'
            tajny_kod_tmp[i] = None
            propozycja_tmp[i] = None

    # 2. Szukamy trafień złą pozycją ("w złym miejscu")
    for i in range(ilość_boxów):
        if propozycja_tmp[i] is not None:
            try:
                idx = tajny_kod_tmp.index(propozycja_tmp[i])
                wynik[i] = 'biała'
                tajny_kod_tmp[idx] = None  # Oznaczamy jako już użyte
            except ValueError:
                pass  # Nie znaleziono w tajnym kodzie

    print(wynik)
    return wynik