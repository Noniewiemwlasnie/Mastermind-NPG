#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QLabel, QDialog, QPushButton, QScrollArea, QVBoxLayout, QWidget
from PySide6.QtGui import Qt

from losowanie_kolorów import Kolor, sprawdz_kod
from menu import OptionsDialog
from boxy_kolorowe import ColorBox

#hello


# Główne okno
class MyApp(QWidget):

    def show_options_dialog(self):
        dialog = OptionsDialog()
        if dialog.exec() == QDialog.Accepted: #type: ignore
            # Zapisujemy stare wartości do porównania
            old_max_attempts = self.max_attempts
            old_ilość_boxów = self.ilość_boxów
            
            # Aktualizujemy wartości
            self.max_attempts = dialog.max_attempts
            self.ilość_boxów = dialog.ilość_boxów
            
            # Resetujemy grę tylko jeśli trudność się zmieniła
            if old_max_attempts != self.max_attempts or old_ilość_boxów != self.ilość_boxów:
                self.reset_game()

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
        self.current_attempt = 0

        #staty
        self.statystyki_plik = "statystyki.txt"
        self.wygrane = 0
        self.przegrane = 0
        self.wczytaj_statystyki()

        # Przycisk zatwierdz
        self.submit_button = QPushButton("Zatwierdź", self)
        self.submit_button.setFixedSize(100, 40)
        self.submit_button.move(200, 200)
        self.submit_button.clicked.connect(self.sprawdz)

        #licznik prób
        self.attempts_label = QLabel(f"Pozostało prób: {self.max_attempts}", self)
        self.attempts_label.move(10, 10)
        self.attempts_label.setStyleSheet("font-size: 16px;")
        self.attempts_label.adjustSize()

        # Label z wynikiem
        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter) #type: ignore
        self.result_label.setStyleSheet("font-size: 24px;")

        # Obszar historii wyników
        self.history_scroll = QScrollArea(self)
        self.history_scroll.setWidgetResizable(True)

        self.history_widget = QWidget()
        self.history_layout = QVBoxLayout(self.history_widget)
        self.history_scroll.setWidget(self.history_widget)

        # Inicjalizacja historii
        self.history_entries = []

        # Przycisk menu
        self.menu_button = QPushButton("Menu", self)
        self.menu_button.setFixedSize(80, 25)
        self.menu_button.clicked.connect(self.show_options_dialog)

        self.ustawienie_wielkości_interfejsu()

        self.reset_game()

    def wczytaj_statystyki(self):
        try:
            with open(self.statystyki_plik, "r") as f:
                linie = f.readlines()
                self.wygrane = int(linie[0].strip())
                self.przegrane = int(linie[1].strip())
        except (FileNotFoundError, IndexError, ValueError):
            self.wygrane = 0
            self.przegrane = 0

    def zapisz_statystyki(self):
        with open(self.statystyki_plik, "w") as f:
            f.write(f"{self.wygrane}\n{self.przegrane}")

    def tajny_kod_na_emoji(self):
            emoji = {
                1: "🟥",
                2: "🟦",
                3: "🟩",
                4: "🟨",
                5: "🟪",
                6: "🟧"
            }

            self.kod_emoji = []
            for liczba in self.secret_code:
                self.kod_emoji += emoji[liczba]
            return ''.join(self.kod_emoji)

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

        # Przesunięcie przycisku menu
        self.menu_button.move(self.width() - 95, 10)

        # Przesunięcie przycisku zatwierdz
        wspolrzedna_x = (self.width() - self.submit_button.width()) // 2
        wspolrzedna_y = 200
        self.submit_button.move(wspolrzedna_x, wspolrzedna_y)

        # Ustawienie result_label na środku
        self.result_label.setFixedWidth(self.width() - 40)  # Zostawiamy marginesy po 20px z każdej strony
        self.result_label.move((self.width() - self.result_label.width()) // 2, 250)

    def reset_game(self):
        # Usuwamy stare boxy jeśli istnieją
        for box in getattr(self, 'boxes', []):
            box.deleteLater()

        # Losowanie tajnego kodu
        self.secret_code = [Kolor().get_liczba() for _ in range(self.ilość_boxów)]
        # Kod słownie
        self.secret_code_słownie = [Kolor().get_kolor_slownie() for _ in range(self.ilość_boxów)] 

        print(f"(DEBUG) Sekret: {self.secret_code_słownie}")

        # Tworzymy nowe boxy
        self.boxes = []
        for i in range(self.ilość_boxów):
            box = ColorBox(50 + i * 120, 50, self)
            box.show()
            self.boxes.append(box)

        # Usuwanie historii
        for entry in self.history_entries:
            entry.deleteLater()
        self.history_entries.clear()

        # Resetujemy licznik prób
        self.current_attempt = 0
        self.pozostalo = self.max_attempts  # Używamy aktualnej wartości max_attempts
        self.attempts_label.setText(f"Pozostało prób: {self.pozostalo}")
        self.attempts_label.adjustSize()

        # Resetowanie wyniku
        self.result_label.setText("")

        # Aktywujemy przycisk zatwierdzania
        self.submit_button.setEnabled(True)

        # Ustawienie wielkości interfejsu
        self.ustawienie_wielkości_interfejsu()

    def sprawdz(self):
        # Sprawdzamy czy przycisk jest aktywny (żeby uniknąć podwójnego wywołania)
        if not self.submit_button.isEnabled():
            return

        propozycja = [box.get_value() for box in self.boxes]
        wynik = sprawdz_kod(propozycja, self.secret_code, self.ilość_boxów)

        czarna = wynik.count('czarna') #type: ignore
        biała = wynik.count('biała') #type: ignore

        # Aktualizacja prób - tylko current_attempt
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
            self.result_label.setText(f"😭Przegrałeś😭 Kod: {self.tajny_kod_na_emoji()}")
            self.submit_button.setEnabled(False)
            self.przegrane+=1
            self.zapisz_statystyki()









