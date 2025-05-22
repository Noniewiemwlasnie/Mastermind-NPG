from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit
from PySide6.QtGui import Qt
from Kolor import Kolor, sprawdz_kod

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
        self.setWindowTitle("Gra mastermind")
        self.setFixedSize(560,800)#do poprawy

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
        self.result_label.setGeometry(30, 250, 500, 60)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 24px;")

    def sprawdz(self):
        propozycja = [box.get_value() for box in self.boxes]
        wynik = sprawdz_kod(propozycja, self.secret_code)

        # Tworzenie wyniku w stylu Wordle
        wynik_ikony = ""
        czarna = 0
        biała = 0
        for element in wynik:
            if element == "czarna":
                czarna += 1
            elif element == "biała":
                biała += 1
        wynik_ikony += "Czarne: "+str(czarna)+"\nBiałe: "+str(biała)
        self.result_label.setText(wynik_ikony)
        if wynik.count("czarna") == 4:
            self.result_label.setText("🎉 Zgadłeś! 🎉")
