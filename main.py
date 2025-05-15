from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit
from PySide6.QtGui import Qt
import sys
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wordle z kolorami")
        self.setGeometry(200, 200, 600, 400)

        # Losowanie tajnego kodu
        self.secret_code = [Kolor().get_liczba() for _ in range(4)]
        print(f"(DEBUG) Sekret: {self.secret_code}")  # Dla testów

        # Kolorowe boxy
        self.boxes = []
        for i in range(4):
            box = ColorBox(50 + i * 120, 50, self)
            self.boxes.append(box)

        # Przycisk
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.move(250, 180)
        self.submit_button.clicked.connect(self.sprawdz)

        # Label z wynikiem
        self.result_label = QLabel("", self)
        self.result_label.setGeometry(50, 250, 500, 50)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 24px;")

    def sprawdz(self):
        propozycja = [box.get_value() for box in self.boxes]
        wynik = sprawdz_kod(propozycja, self.secret_code)

        # Tworzenie wyniku w stylu Wordle
        wynik_ikony = ""
        for w in wynik:
            if w == "czarna":
                wynik_ikony += "🟩"
            elif w == "biała":
                wynik_ikony += "🟨"
            else:
                wynik_ikony += "⬜"

        self.result_label.setText(wynik_ikony)

        if wynik.count("czarna") == 4:
            self.result_label.setText("🎉 Zgadłeś! 🎉")

# Uruchomienie
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
