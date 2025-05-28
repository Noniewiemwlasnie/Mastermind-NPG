#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QSizePolicy, QSpacerItem, QLabel, QDialog, QPushButton, QLineEdit, QScrollArea, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtGui import Qt


# Menu
class OptionsDialog(QDialog):

    # wybór trudności - łatwy, średni, trudny
    def wybierz_trudnosc(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Wybierz poziom trudności gry")
        msg_box.setText("Proszę wybrać poziom trudności gry:")

        # poziomy
        poziom_łatwy = msg_box.addButton("Poziom łatwy", QMessageBox.AcceptRole)
        poziom_średni = msg_box.addButton("Poziom średni", QMessageBox.AcceptRole)
        poziom_trudny = msg_box.addButton("Poziom trudny", QMessageBox.AcceptRole)

        msg_box.exec()
        # po wyborze poziomu zmienia się liczba okienek z kolorami do zgadnięcia - zmienna n

        if msg_box.clickedButton() == poziom_łatwy:
            self.max_attempts = 12
            self.ilość_boxów = 3
        elif msg_box.clickedButton() == poziom_średni:
            self.max_attempts = 10
            self.ilość_boxów = 4
        elif msg_box.clickedButton() == poziom_trudny:
            self.max_attempts = 8
            self.ilość_boxów = 5
        else:
            self.max_attempts = 10
            self.ilość_boxów = 4

        self.accept()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.max_attempts = 10
        self.ilość_boxów = 4
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

    # pokazuje staty
    def pokaz_statystyki(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Statystyki gry")
        msg.setText(
            f"Wygrane: {self.parent().wygrane}\nPrzegrane: {self.parent().przegrane}"
        )
        msg.exec()