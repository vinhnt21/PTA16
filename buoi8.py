from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class Buoi8(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("buoi8.ui", self)

        self.pushButton.clicked.connect(self.dangki)
    

    def dangki(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        confirm_password = self.lineEdit_3.text()
        
        if not username:
            QMessageBox.warning(self, "Lỗi", "Tên đăng nhập không được để trống")
            return
        if not password:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu không được để trống")
            return
        
        if not confirm_password:
            QMessageBox.warning(self, "Lỗi", "Xác nhận mật khẩu không được để trống")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu không trùng khớp")
            return

app = QApplication(sys.argv)
window = Buoi8()
window.show()
sys.exit(app.exec())
