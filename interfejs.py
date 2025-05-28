from PySide6.QtWidgets import QLabel, QDialog, QPushButton, QScrollArea, QVBoxLayout, QWidget
from PySide6.QtGui import Qt
from losowanie_kolorów import Kolor, sprawdz_kod
from menu import OptionsDialog
from boxy_kolorowe import ColorBox

#dodana opcja wyboru trudności połączona z ilością boxów
'''
class OptionsDialog(QDialog): #zmień nazwę tej klasy bo wywala kod
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Opcje")

        layout = QVBoxLayout(self)

        self.difficulty_spinbox = QSpinBox()
        self.difficulty_spinbox.setRange(4, 6)
        self.difficulty_spinbox.setValue(4)
        layout.addWidget(QLabel("Ilość pól do zgadnięcia: "))
        layout.addWidget(self.difficulty_spinbox)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

    def liczba_boxy(self):
        return self.difficulty_spinbox.value()
'''

# Główne okno
class MyApp(QWidget):
    #Do menu
    def show_options_dialog(self):
        dialog = OptionsDialog()
        if dialog.exec() == QDialog.Accepted:
            # Aktualizujemy wartości
            self.ilość_boxów = dialog.ilość_boxów
            self.max_attempts = dialog.max_attempts
            self.reset_game()

    #Główna część "Mastermind"
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gra mastermind")
        self.setGeometry(100, 100, 800, 800)

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
        self.submit_button = QPushButton("Zatwierdz", self)
        self.submit_button.move(240, 180)
        self.submit_button.clicked.connect(self.sprawdz)

        # Przycisk menu
        self.menu_button = QPushButton("Menu", self)
        self.menu_button.move(470, 10)
        self.menu_button.clicked.connect(self.show_options_dialog)

        #licznik prób
        self.attempts_label = QLabel(f"Pozostało prób: {self.max_attempts}", self)
        self.attempts_label.move(20, 10)
        self.attempts_label.setStyleSheet("font-size: 16px;")
        self.attempts_label.adjustSize()

        # Label z wynikiem
        self.result_label = QLabel("", self)
        self.result_label.setGeometry(20, 250, 500, 30)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 24px;")

        # Obszar historii wyników
        self.history_scroll = QScrollArea(self)
        self.history_scroll.setGeometry(20, 300, 520, 480)
        self.history_scroll.setWidgetResizable(True)

        self.history_widget = QWidget()
        self.history_layout = QVBoxLayout(self.history_widget)
        self.history_scroll.setWidget(self.history_widget)

        # Inicjalizacja historii
        self.history_entries = []

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

        # Resetowanie prób
        self.pozostalo = self.max_attempts
        self.current_attempt = 0
        self.attempts_label.setText(f"Pozostało prób: {self.pozostalo}")
        self.attempts_label.adjustSize()

        # Resetowanie wyniku
        self.result_label.setText("")

        # Aktywujemy przycisk zatwierdzania
        self.submit_button.setEnabled(True)

    def sprawdz(self):
        propozycja = [box.get_value() for box in self.boxes]
        wynik = sprawdz_kod(propozycja, self.secret_code, self.ilość_boxów)

        # Obliczanie wyniku
        czarna = wynik.count('czarna')
        biała = wynik.count('biała')

        #wypisywanie pozostałych prób
        self.current_attempt += 1
        self.pozostalo = self.max_attempts - self.current_attempt
        self.attempts_label.setText(f"Pozostało prób: {self.pozostalo}")
        self.attempts_label.adjustSize()

        # Aktualizacja wyniku bieżącej próby
        wynik_tekst = f"Czarne: {czarna}    Białe: {biała}"
        self.result_label.setText(wynik_tekst)

        # Dodanie do historii
        history_label = QLabel(f"{len(self.history_entries) + 1}. Czarne: {czarna} Białe: {biała}")
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
            self.przegrane+=1
            self.zapisz_statystyki()
