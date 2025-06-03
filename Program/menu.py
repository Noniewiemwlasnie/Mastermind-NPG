#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QSizePolicy, QSpacerItem, QLabel, QDialog, QPushButton, QSpinBox, QVBoxLayout,  QMessageBox, QDialogButtonBox
from PySide6.QtGui import Qt



# Menu
class OptionsDialog(QDialog):
    
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

        self.ilość_boxów = 3
        self.max_attempts = 10

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        

        layout.addItem(spacer)
        self.setLayout(layout)

        


    def wybierz_trudnosc(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ustawienia poziomu trudności")
        dialog.setModal(True)
        dialog.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        
        # Liczba prób
        layout.addWidget(QLabel("Maksymalna liczba prób:"))
        attempts_spinbox = QSpinBox()
        attempts_spinbox.setRange(5, 20)
        attempts_spinbox.setValue(self.max_attempts)
        layout.addWidget(attempts_spinbox)
        
        # Liczba pól do zgadnięcia
        layout.addWidget(QLabel("Ilość pól do zgadnięcia:"))
        difficulty_spinbox = QSpinBox()
        difficulty_spinbox.setRange(3, 6)
        difficulty_spinbox.setValue(self.ilość_boxów)
        layout.addWidget(difficulty_spinbox)
        
        # Przyciski OK i Anuluj
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            self.max_attempts = attempts_spinbox.value()
            self.ilość_boxów = difficulty_spinbox.value()
            self.accept()  # Dodajemy tę linijkę aby zamknąć główne okno menu


    def pokaz_statystyki(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Statystyki gry")
        msg.setText(
            f"Wygrane: {self.parent().wygrane}\nPrzegrane: {self.parent().przegrane}" #type: ignore
        )
        msg.exec()