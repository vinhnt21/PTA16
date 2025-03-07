from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class Buoi5(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("buoi5.ui", self)
        self.pushButton.clicked.connect(self.on_click)

    def on_click(self):
        QMessageBox.information(self, "Thông Báo", " Fan J Thì Không Được Đăng Kí")


app = QApplication(sys.argv)
window = Buoi5()
window.show()
sys.exit(app.exec())
