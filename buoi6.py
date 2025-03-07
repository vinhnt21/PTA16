from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class Buoi6(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("buoi6.ui", self)


app = QApplication(sys.argv)
window = Buoi6()
window.show()
sys.exit(app.exec())
