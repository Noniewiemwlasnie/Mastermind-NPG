#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QLabel, QDialog, QPushButton, QScrollArea, QVBoxLayout, QWidget
from PySide6.QtGui import Qt

from losowanie_kolorów import Kolor, sprawdz_kod
from menu import OptionsDialog
from boxy_kolorowe import ColorBox


# Główne okno
class MyApp(QWidget):
    #Do menu
    def show_options_dialog(self):
        dialog = OptionsDialog()
        if dialog.exec() == QDialog.Accepted:
            # Aktualizujemy wartości
            self.max_attempts = dialog.max_attempts
            self.ilość_boxów = dialog.ilość_boxów
            self.reset_game()


    #Główna część "Mastermind" - zwiększyłem okno, bo na poziomie trudnym brakowało miejsca
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gra mastermind")

        # Inicjalizujemy puste listy
        self.boxes = []
        self.history_entries = []

        # Pobieramy domyślne ustawienia trudności
        dialog = OptionsDialog()
        self.ilość_boxów = dialog.ilość_boxów
        self.max_attempts = dialog.max_attempts

        #staty
        self.statystyki_plik = "statystyki.txt"
        self.wygrane = 0
        self.przegrane = 0
        self.wczytaj_statystyki()

        # Przycisk zatwierdz
        self.submit_button = QPushButton("Zatwierdź", self)
        self.submit_button.setFixedSize(180, 60)

        #licznik prób
        self.attempts_label = QLabel(f"Pozostało prób: {self.max_attempts}", self)
        self.attempts_label.move(10, 10)
        self.attempts_label.setStyleSheet("font-size: 16px;")
        self.attempts_label.adjustSize()

        # Label z wynikiem
        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 24px;")

        # Obszar historii wyników
        self.history_scroll = QScrollArea(self)
        self.history_scroll.setWidgetResizable(True)

        self.history_widget = QWidget()
        self.history_layout = QVBoxLayout(self.history_widget)
        self.history_scroll.setWidget(self.history_widget)

        # Inicjalizacja historii
        self.history_entries = []

        # Ustawienie wielkości interfejsu dla ilości boxów
        self.ustawienie_wielkości_interfejsu()

        # Przycisk menu
        self.menu_button = QPushButton("Menu", self)
        self.submit_button.setFixedSize(120, 40)
        self.menu_button.clicked.connect(self.show_options_dialog)


        self.reset_game()

        # wczytywanie stat
    def wczytaj_statystyki(self):
        try:
            with open(self.statystyki_plik, "r") as f:
                linie = f.readlines()
                self.wygrane = int(linie[0].strip())
                self.przegrane = int(linie[1].strip())
        except (FileNotFoundError, IndexError, ValueError):
            self.wygrane = 0
            self.przegrane = 0

    # zapis stat
    def zapisz_statystyki(self):
        with open(self.statystyki_plik, "w") as f:
            f.write(f"{self.wygrane}\n{self.przegrane}")

    def ustawienie_wielkości_interfejsu(self):
        if self.ilość_boxów == 3:
            self.setFixedSize(440, 800)
            self.history_scroll.setGeometry(20, 300, 400, 480)
        elif self.ilość_boxów == 4:
            self.setFixedSize(560, 800)
            self.history_scroll.setGeometry(20, 300, 520, 480)
        elif self.ilość_boxów == 5:
            self.setFixedSize(680, 800)
            self.history_scroll.setGeometry(20, 300, 640, 480)
        elif self.ilość_boxów == 6:
            self.setFixedSize(800, 800)
            self.history_scroll.setGeometry(20, 300, 760, 480)
        else:
            self.setFixedSize(440, 800)
            self.history_scroll.setGeometry(20, 300, 400, 480)

        # Ustawienie result_label na środku
        self.result_label.setFixedWidth(self.width() - 40)  # Zostawiamy marginesy po 20px z każdej strony
        self.result_label.move((self.width() - self.result_label.width()) // 2, 250)

    #resetowanie gry
    def reset_game(self):
        # Najpierw usuwamy stare boxy jeśli istnieją
        for box in getattr(self, 'boxes', []):
            box.deleteLater()

        # Losowanie tajnego kodu
        self.secret_code = [Kolor().get_liczba() for _ in range(self.ilość_boxów)]
        print(f"(DEBUG) Sekret: {self.secret_code}")

        # Tworzymy nowe boxy
        self.boxes = []
        for i in range(self.ilość_boxów):
            box = ColorBox(50 + i * 120, 50, self)
            box.show()  # Upewniamy się, że boxy są widoczne
            self.boxes.append(box)

        # Usuwanie historii
        for entry in self.history_entries:
            entry.deleteLater()
        self.history_entries.clear()

        # Ustawienie domyślnej wartości prób
        self.current_attempt = 0

        # Resetowanie wyniku
        self.result_label.setText("")

        # Aktywujemy przycisk zatwierdzania
        self.submit_button.setEnabled(True)

        # Ustawienie wielkości interfejsu dla ilości boxów
        self.ustawienie_wielkości_interfejsu()

        # Przesunięcie przycisku menu
        self.menu_button.move(self.width() - 95, 10)

        # Przesunięcie przycisku zatwierdz
        wspolrzedna_x = (self.width() - self.submit_button.width()) // 2
        wspolrzedna_y = 200
        self.submit_button.move(wspolrzedna_x, wspolrzedna_y)
        self.submit_button.clicked.connect(self.sprawdz)


    def sprawdz(self):
        propozycja = [box.get_value() for box in self.boxes]
        wynik = sprawdz_kod(propozycja, self.secret_code, self.ilość_boxów)

        # Obliczanie wyniku
        czarna = wynik.count('czarna')
        biała = wynik.count('biała')

        # Wypisywanie pozostałych prób #tu jest problem
        self.current_attempt += 1
        self.pozostalo = self.max_attempts - self.current_attempt
        self.attempts_label.setText(f"Pozostało prób: {self.pozostalo}")
        self.attempts_label.adjustSize()

        # Dodanie do historii
        history_label = QLabel(f"{len(self.history_entries) + 1}. W dobrym miejscu: {czarna}    W złym miejscu: {biała}")
        history_label.setStyleSheet("font-size: 18px; margin: 5px;")
        self.history_layout.addWidget(history_label)
        self.history_entries.append(history_label)

        # Przewiń do dołu
        self.history_scroll.verticalScrollBar().setValue(
            self.history_scroll.verticalScrollBar().maximum()
        )

        if czarna == self.ilość_boxów:
            self.result_label.setText("😁Wygrałeś😁")
            self.submit_button.setEnabled(False)
            self.wygrane+=1
            self.zapisz_statystyki()
        elif self.current_attempt >= self.max_attempts:
            self.result_label.setText(f"😭Przegrałeś😭 Kod: {self.secret_code}")
            self.submit_button.setEnabled(False)
            self.przegrane+=1
            self.zapisz_statystyki()


