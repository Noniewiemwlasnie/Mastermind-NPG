#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QSizePolicy, QSpacerItem, QLabel, QDialog, QPushButton, QSpinBox, QVBoxLayout,  QMessageBox
from PySide6.QtGui import Qt



# Menu
class OptionsDialog(QDialog):
    
    def wybierz_trudnosc(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Wybierz poziom trudności gry")
        msg_box.setText("Proszę wybrać ilość prób:")

        
        poziom_łatwy = msg_box.addButton("12", QMessageBox.AcceptRole)
        poziom_średni = msg_box.addButton("10", QMessageBox.AcceptRole)
        poziom_trudny = msg_box.addButton("8", QMessageBox.AcceptRole)

        msg_box.exec()

        if msg_box.clickedButton() == poziom_łatwy:
            self.max_attempts = 12
        elif msg_box.clickedButton() == poziom_średni:
            self.max_attempts = 10
        elif msg_box.clickedButton() == poziom_trudny:
            self.max_attempts = 8
        else:
            self.max_attempts = 10

        self.accept()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Menu")
        self.setFixedSize(200, 250)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Marginesy

        # Etykieta w lewym górnym rogu
        label = QLabel("Wybierz opcję:")
        layout.addWidget(label, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Przycisk ustawienia
        self.ustawienia_button = QPushButton("Ustawienia")
        layout.addWidget(self.ustawienia_button)

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

        #ustawienie domyśl wart. prób
        self.max_attempts = 10

        #ustawienie ilości pól do zgadnięcia
        self.difficulty_spinbox = QSpinBox()
        self.difficulty_spinbox.setRange(4, 6)
        layout.addWidget(QLabel("Ilość pól do zgadnięcia: "))
        layout.addWidget(self.difficulty_spinbox)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.ilość_boxów = self.difficulty_spinbox.value()
        self.difficulty_spinbox.valueChanged.connect(self.update_ilosc_boxow)

    def update_ilosc_boxow(self, value):
        self.ilość_boxów = value

    # pokazuje staty
    def pokaz_statystyki(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Statystyki gry")
        msg.setText(
            f"Wygrane: {self.parent().wygrane}\nPrzegrane: {self.parent().przegrane}"
        )
        msg.exec()