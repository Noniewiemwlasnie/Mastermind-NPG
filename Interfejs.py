from PySide6.QtWidgets import QSizePolicy, QSpacerItem, QLabel, QDialog, QPushButton, QLineEdit, QScrollArea, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtGui import Qt
from Kolor import Kolor, sprawdz_kod

# Menu
class OptionsDialog(QDialog):

    # wybór trudności - łatwy, średni, trudny
    def wybierz_trudnosc(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Wybierz poziom trudności gry")
        msg_box.setText("Proszę wybrać poziom trudności gry:")

        # poziomy
        poziom1 = msg_box.addButton("Poziom łatwy", QMessageBox.AcceptRole)
        poziom2 = msg_box.addButton("Poziom średni", QMessageBox.AcceptRole)
        poziom3 = msg_box.addButton("Poziom trudny", QMessageBox.AcceptRole)

        msg_box.exec()

        if msg_box.clickedButton() == poziom1:
            self.selected_difficulty = 12
        elif msg_box.clickedButton() == poziom2:
            self.selected_difficulty = 10
        elif msg_box.clickedButton() == poziom3:
            self.selected_difficulty = 8
        self.accept()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Menu")
        self.setFixedSize(200, 150)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Marginesy

        # Etykieta w lewym górnym rogu
        label = QLabel("Wybierz opcję:")
        layout.addWidget(label, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Przycisk opcje
        self.opcje_button = QPushButton("Ustawienia")
        layout.addWidget(self.opcje_button)

        # Przycisk statystyki
        self.statystyki_button = QPushButton("Statystyki")
        self.statystyki_button.clicked.connect(self.pokaz_statystyki)
        layout.addWidget(self.statystyki_button)

        # Przycisk poziom trudności
        self.poziom_trud_button = QPushButton("Poziom trudności")
        layout.addWidget(self.poziom_trud_button)
        self.poziom_trud_button.clicked.connect(self.wybierz_trudnosc)

        # Spacer aby przyciski nie rozciągały się na całą wysokość  
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        self.setLayout(layout)

    #pokazuje staty
    def pokaz_statystyki(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Statystyki gry")
        msg.setText(
            f"Wygrane: {self.parent().wygrane}\nPrzegrane: {self.parent().przegrane}"
        )
        msg.exec()
# Box kolorowy
class ColorBox(QLineEdit):
    COLORS = {
        1: ("Czerwony", "#8B0000"),
        2: ("Niebieski", "#00008B"),
        3: ("Zielony", "#006400"),
        4: ("Żółty", "#CCCC00"),
        5: ("Fioletowy", "#4B0082"),
        6: ("Pomarańczowy", "#CC5500")
    }

    def __init__(self, x, y, parent=None):
        super().__init__("", parent)
        self.setFixedSize(100, 100)
        self.move(x, y)
        self.setReadOnly(True)
        self.setAlignment(Qt.AlignCenter)
        self.color_index = 1
        self.update_color()

    def mousePressEvent(self, event):
        self.color_index = self.color_index + 1 if self.color_index < 6 else 1
        self.update_color()

    def update_color(self):
        name, color = self.COLORS[self.color_index]
        self.setText(name)
        self.setStyleSheet(f"""
            background-color: {color};
            color: white;
            font-weight: bold;
            border: 2px solid black;
            border-radius: 8px;
        """)

    def get_value(self):
        return self.color_index

# Główne okno
class MyApp(QWidget):
    #wybieranie poziomy trudnosci na starcie
    def wybierz_trudnosc_na_start(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Wybierz poziom trudności")
        msg_box.setText("Proszę wybrać poziom trudności gry:")

        poziom1 = msg_box.addButton("Łatwy (12 prób)", QMessageBox.AcceptRole)
        poziom2 = msg_box.addButton("Średni (10 prób)", QMessageBox.AcceptRole)
        poziom3 = msg_box.addButton("Trudny (8 prób)", QMessageBox.AcceptRole)

        msg_box.exec()

        if msg_box.clickedButton() == poziom1:
            return 12
        elif msg_box.clickedButton() == poziom2:
            return 10
        elif msg_box.clickedButton() == poziom3:
            return 8
        else:
            return 10

    #Do menu
    def show_options_dialog(self):
        dialog = OptionsDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.max_attempts = dialog.selected_difficulty
            self.reset_game()

    #Główna część "Mastermind"
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gra mastermind")
        self.setFixedSize(560,800)#do poprawy

        #staty
        self.statystyki_plik = "statystyki.txt"
        self.wygrane = 0
        self.przegrane = 0
        self.wczytaj_statystyki()

        #ilosc prób
        self.max_attempts = self.wybierz_trudnosc_na_start()
        self.current_attempt = 0

        # Losowanie tajnego kodu
        self.secret_code = [Kolor().get_liczba() for _ in range(4)]
        print(f"(DEBUG) Sekret: {self.secret_code}")  # Dla testów

        # Kolorowe boxy
        self.boxes = []
        for i in range(4):
            box = ColorBox(50 + i * 120, 50, self)
            self.boxes.append(box)

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
        from random import randint
        self.secret_code = [randint(1, 6) for _ in range(4)]
        print(f"(DEBUG) Sekret: {self.secret_code}")
        self.current_attempt = 0
        self.result_label.setText("")
        self.submit_button.setEnabled(True)
        self.attempts_label.setText(f"Pozostało prób: {self.max_attempts}")
        self.attempts_label.adjustSize()

        for entry in self.history_entries:
            entry.deleteLater()
        self.history_entries.clear()

    def sprawdz(self):
        propozycja = [box.get_value() for box in self.boxes]
        wynik = sprawdz_kod(propozycja, self.secret_code)

        # Obliczanie wyniku
        czarna = wynik.count("czarna")
        biała = wynik.count("biała")

        #wypisywanie pozostałych prób
        self.current_attempt += 1
        pozostalo = self.max_attempts - self.current_attempt
        self.attempts_label.setText(f"Pozostało prób: {pozostalo}")
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

        if czarna == 4:
            self.result_label.setText("😁Wygrałeś😁")
            self.submit_button.setEnabled(False)
            self.wygrane+=1
            self.zapisz_statystyki()
        elif self.current_attempt >= self.max_attempts:
            self.result_label.setText(f"😭Przegrałeś😭 Kod: {self.secret_code}")
            self.przegrane+=1
            self.zapisz_statystyki()
