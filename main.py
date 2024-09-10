import sys
from PySide6.QtWidgets import QApplication
from tymon import Keys, Dane, Public_key
from aplikacja import Aplikacja

def main():
    app = QApplication(sys.argv)
    aplikacja = Aplikacja()
    aplikacja.show()
    app.exec()

if __name__ == "__main__":
    main()

