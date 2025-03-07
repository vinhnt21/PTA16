from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys
import pygame

pygame.init()
pygame.mixer.init()


class Buoi7(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("buoi7.ui", self)

        self.pushButton.clicked.connect(self.play_music)
        self.pushButton_2.clicked.connect(self.stop_music)

    def play_music(self):
        music_file = "./a.mp3"
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def khenJackDepTrai(self):
        QMessageBox.information(self, "Khen Jack", "Jack đẹp trai quá đi mất")


app = QApplication(sys.argv)
window = Buoi7()
window.show()
sys.exit(app.exec())
