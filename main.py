from PySide6.QtWidgets import QApplication
import sys
from Interfejs import MyApp

# Uruchomienie
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
