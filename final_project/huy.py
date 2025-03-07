from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
)
from PyQt6 import uic
from PyQt6.QtCore import Qt
import sys
import cohere

# API key cho Cohere
API_KEY = ""


def generate_questions(text, num_questions):
    """
    Gửi nội dung đến Cohere API để tạo câu hỏi trắc nghiệm

    Args:
        text (str): Nội dung cần tạo câu hỏi
        num_questions (int): Số lượng câu hỏi cần tạo

    Returns:
        tuple: (nội dung câu hỏi, đáp án đúng)
    """
    try:
        co = cohere.ClientV2(API_KEY)

        role_info = f"""
        Bạn là giáo viên, hãy tạo {num_questions} câu hỏi trắc nghiệm dựa trên nội dung được cung cấp.
        Mỗi câu hỏi có 4 đáp án (A, B, C, D), trong đó chỉ có 1 đáp án đúng.

        Định dạng trả về:
        Câu 1: [Nội dung câu hỏi]
        A. [Đáp án A]
        B. [Đáp án B]
        C. [Đáp án C]
        D. [Đáp án D]

        Câu 2: [Nội dung câu hỏi]
        ...

        Trả về định dạng text cơ bản, không dùng markdown.
        """

        question = f"Tạo câu hỏi trắc nghiệm từ nội dung sau: {text}"

        response = co.chat(
            model="command-r-plus",
            messages=[
                {"role": "system", "content": role_info},
                {"role": "user", "content": question},
            ],
        )

        questions_text = response.message.content[0].text

        # Lấy đáp án đúng từ AI
        role_info_answers = f"""
        Dưới đây là {num_questions} câu hỏi trắc nghiệm. Hãy cho biết đáp án đúng cho mỗi câu.
        Trả về theo định dạng:
        1-[A/B/C/D]
        2-[A/B/C/D]
        ...
        Chỉ trả về đáp án, không giải thích.
        """

        response_answers = co.chat(
            model="command-r-plus",
            messages=[
                {"role": "system", "content": role_info_answers},
                {"role": "user", "content": questions_text},
            ],
        )

        correct_answers = response_answers.message.content[0].text.strip()

        return (questions_text, correct_answers)

    except Exception as e:
        print(f"Lỗi khi kết nối với AI: {str(e)}")
        return ("Lỗi khi tạo câu hỏi. Vui lòng thử lại!", "")


def check_answers(questions_text, correct_answers, user_answers):
    """
    Kiểm tra đáp án của học sinh và trả về kết quả

    Args:
        questions_text (str): Nội dung câu hỏi
        correct_answers (str): Đáp án đúng
        user_answers (str): Đáp án của học sinh

    Returns:
        tuple: (điểm số, giải thích)
    """
    try:
        co = cohere.ClientV2(API_KEY)

        # Tạo nội dung để gửi đến AI
        content = f"""
        Đánh giá bài làm của học sinh:

        Câu hỏi:
        {questions_text}

        Đáp án đúng:
        {correct_answers}

        Đáp án của học sinh:
        {user_answers}
        """

        role_info = """
        Bạn là giáo viên, hãy đánh giá bài làm của học sinh và đưa ra nhận xét chi tiết.
        1. Tính điểm: mỗi câu đúng được 1 điểm, quy đổi thành thang điểm 10
        2. Liệt kê từng câu, đáp án đúng, đáp án của học sinh, và giải thích tại sao đáp án đó đúng
        3. Đưa ra lời khuyên để học sinh cải thiện

        Trả về kết quả theo định dạng:
        ĐIỂM SỐ: [X/10]

        ĐÁNH GIÁ CHI TIẾT:
        Câu 1:
        - Đáp án đúng: [A/B/C/D]
        - Đáp án của bạn: [A/B/C/D]
        - Giải thích: [Giải thích tại sao đáp án này đúng]

        Câu 2:
        ...

        LỜI KHUYÊN:
        [Lời khuyên cho học sinh]
        """

        response = co.chat(
            model="command-r-plus",
            messages=[
                {"role": "system", "content": role_info},
                {"role": "user", "content": content},
            ],
        )

        result = response.message.content[0].text

        return result

    except Exception as e:
        print(f"Lỗi khi kết nối với AI: {str(e)}")
        return (0, f"Lỗi khi đánh giá bài làm: {str(e)}")


class ResultDialog(QDialog):
    def __init__(self, parent=None, title="", content=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(600, 500)

        layout = QVBoxLayout(self)

        # Tiêu đề
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Nội dung
        result_text = QTextEdit()
        result_text.setReadOnly(True)
        result_text.setPlainText(content)
        result_text.setStyleSheet("font-size: 14px;")
        layout.addWidget(result_text)

        # Nút đóng
        close_button = QPushButton("Đóng")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("huy.ui", self)

        # Kết nối các nút với hàm xử lý
        self.generateButton.clicked.connect(self.generate_quiz)
        self.submitButton.clicked.connect(self.submit_answers)

        # Khởi tạo biến lưu trữ
        self.questions_text = ""
        self.correct_answers = ""
        self.submitButton.setEnabled(False)

    def generate_quiz(self):
        # Lấy nội dung từ text edit
        content = self.inputTextEdit.toPlainText().strip()
        if not content:
            QMessageBox.warning(
                self, "Cảnh báo", "Vui lòng nhập nội dung để tạo câu hỏi!"
            )
            return

        # Lấy số lượng câu hỏi
        num_questions = self.numQuestionsSpinBox.value()

        if num_questions <= 0:
            QMessageBox.warning(
                self, "Cảnh báo", "Vui lòng chọn số lượng câu hỏi lớn hơn 0!"
            )
            return

        # Hiển thị thông báo đang tạo câu hỏi
        self.scoreLabel.setText("Đang tạo câu hỏi...")
        QApplication.processEvents()  # Cập nhật giao diện

        # Tạo câu hỏi từ nội dung
        self.questions_text, self.correct_answers = generate_questions(
            content, num_questions
        )

        # Hiển thị câu hỏi
        self.questionsTextEdit.setPlainText(self.questions_text)

        if self.questions_text and not self.questions_text.startswith("Lỗi"):
            self.submitButton.setEnabled(True)
            self.scoreLabel.setText("Hãy nhập đáp án của bạn và nộp bài")
        else:
            self.submitButton.setEnabled(False)
            self.scoreLabel.setText("Không thể tạo câu hỏi. Vui lòng thử lại!")

    def submit_answers(self):
        # Lấy đáp án của học sinh
        user_answers = self.answersTextEdit.toPlainText().strip()
        if not user_answers:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đáp án của bạn!")
            return

        # Hiển thị thông báo đang chấm điểm
        self.scoreLabel.setText("Đang chấm điểm...")
        QApplication.processEvents()  # Cập nhật giao diện

        # Chấm điểm và hiển thị kết quả
        explanation = check_answers(
            self.questions_text, self.correct_answers, user_answers
        )

        self.scoreLabel.setText("")
        # Hiển thị giải thích trong dialog lớn hơn
        result_dialog = ResultDialog(self, f"Kết quả", explanation)
        result_dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
