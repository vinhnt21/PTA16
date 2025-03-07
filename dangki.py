from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class DangKi(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("dangki.ui", self)

        self.pushButton.clicked.connect(self.dangki)

    def dangki(self):
        QMessageBox.information(self, "Thông báo", "Anh Jack ơi💚💚💚💚")


app = QApplication(sys.argv)
window = DangKi()
window.show()
sys.exit(app.exec())
