#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import Qt

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