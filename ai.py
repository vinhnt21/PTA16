KEY = "9MHD0XvvmkJQGfQpogAmNw6ozsZalaZa57OVFMPE"

import cohere


def get_answer(question):

    co = cohere.ClientV2(KEY)
    response = co.chat(
        model="command-r-plus",
        messages=[
            {
                "role": "system",
                "content": """
                Bạn là chuyên gia thần số học, bạn sẽ nhận được ngày tháng năm sinh, hãy phân tích vừa đưa ra dự đoán về tương lai của người đó.
                """,
            },
            {"role": "user", "content": question},
        ],
    )

    return response.message.content[0].text


from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys
import pygame

pygame.init()
pygame.mixer.init()


class AI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ai.ui", self)
        self.pushButton.clicked.connect(self.ask)

    def ask(self):
        question = self.lineEdit.text()
        if question == "":
            QErrorMessage(self, "Lỗi", "Hỏi thì phải hỏi chứ, không được để trống")
        self.label.setText("Đợi anh tí nhé eim zai 😚😚")
        print(question)
        answer = get_answer(question)

        self.label.setText(answer)
        self.lineEdit.setText("")


app = QApplication(sys.argv)
window = AI()
window.show()
sys.exit(app.exec())
