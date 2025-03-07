from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton
from PyQt6 import uic
import sys
import cohere

# API key cho Cohere
API_KEY = ""


def get_answer(text, level):
    """
    Gửi bài viết đến Cohere API để đánh giá

    Args:
        text (str): Bài viết cần đánh giá
        level (str): Trình độ học sinh (Beginner/Intermediate/Advanced)

    Returns:
        str: Phản hồi từ AI
    """
    try:
        co = cohere.ClientV2(API_KEY)

        role_info = f"""
        Bạn là giáo viên chấm bài viết tiếng Anh.
        Bạn sẽ nhận được một bài viết tiếng Anh của học sinh trình độ {level}.
        Hãy đánh giá dựa trên level của học sinh và nhận xét theo các tiêu chí:
        - Ngữ pháp (Grammar)
        - Từ vựng (Vocabulary)
        - Cấu trúc (Structure) 
        - Ý tưởng (Ideas)
        - Gợi ý cải thiện (Suggestions for improvement)

        Cuối cùng, hãy cho điểm bài viết trên thang điểm 10.

        Trả về định dạng text cơ bản, chia các ý theo gạch đầu dòng, không dùng markdown.
        """

        question = (
            f"Đánh giá bài viết tiếng Anh này của học sinh trình độ {level}:\n\n{text}"
        )

        response = co.chat(
            model="command-r-plus",
            messages=[
                {"role": "system", "content": role_info},
                {"role": "user", "content": question},
            ],
        )

        assistant_message = response.message.content[0].text
        return assistant_message

    except Exception as e:
        return f"Lỗi khi kết nối với AI: {str(e)}"


def ask_question(essay, feedback, question, level):
    """
    Gửi câu hỏi thêm về bài viết đến Cohere API

    Args:
        essay (str): Bài viết gốc
        feedback (str): Phản hồi đã có
        question (str): Câu hỏi của học sinh
        level (str): Trình độ học sinh

    Returns:
        str: Phản hồi từ AI
    """
    try:
        co = cohere.ClientV2(API_KEY)

        role_info = f"""
        Bạn là giáo viên tiếng Anh đang hỗ trợ học sinh trình độ {level}.
        Học sinh đã nộp bài viết và nhận được đánh giá, giờ họ có thêm câu hỏi.
        Hãy trả lời câu hỏi của học sinh một cách rõ ràng, dễ hiểu và phù hợp với trình độ của họ.
        """

        prompt = f"""
        Bài viết của học sinh:
        {essay}

        Đánh giá của bạn:
        {feedback}

        Câu hỏi của học sinh:
        {question}
        """

        response = co.chat(
            model="command-r-plus",
            messages=[
                {"role": "system", "content": role_info},
                {"role": "user", "content": prompt},
            ],
        )

        assistant_message = response.message.content[0].text
        return assistant_message

    except Exception as e:
        return f"Lỗi khi kết nối với AI: {str(e)}"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("nhatminh.ui", self)

        # Thiết lập emoji cho nút chuyển chế độ
        self.btnToggleMode.setText("☀️")
        self.btnToggleMode.setStyleSheet(
            """
            QPushButton {
                font-size: 18px;
                background-color: transparent;
                border: none;
            }
        """
        )
        self.dark_mode = False

        # Kết nối các sự kiện
        self.btnEvaluate.clicked.connect(self.evaluate_text)
        self.btnToggleMode.clicked.connect(self.toggle_dark_mode)
        self.btnAsk.clicked.connect(self.ask_additional_question)

        # Biến theo dõi chế độ tối và lưu trữ bài viết/phản hồi
        self.dark_mode = False
        self.current_essay = ""
        self.current_feedback = ""

        # Ẩn phần hỏi đáp ban đầu
        self.labelQuestion.setVisible(False)
        self.lineQuestion.setVisible(False)
        self.btnAsk.setVisible(False)

        self.toggle_dark_mode()

    def evaluate_text(self):
        """Xử lý khi người dùng nhấn nút đánh giá"""
        # Lấy nội dung bài viết
        text = self.textInput.toPlainText().strip()

        # Kiểm tra xem có nội dung không
        if not text:
            QMessageBox.warning(
                self, "Cảnh báo", "Vui lòng nhập bài viết cần đánh giá!"
            )
            return

        # Lấy trình độ từ combobox
        level = self.comboLevel.currentText()

        # Hiển thị thông báo đang xử lý
        self.textOutput.setPlainText("Đang đánh giá bài viết, vui lòng đợi...")
        QApplication.processEvents()  # Cập nhật giao diện

        # Gọi API để đánh giá
        result = get_answer(text, level)

        # Lưu bài viết và phản hồi hiện tại
        self.current_essay = text
        self.current_feedback = result

        # Hiển thị kết quả
        self.textOutput.setPlainText(result)

        # Hiển thị phần hỏi đáp
        self.labelQuestion.setVisible(True)
        self.lineQuestion.setVisible(True)
        self.btnAsk.setVisible(True)

    def ask_additional_question(self):
        """Xử lý khi người dùng đặt câu hỏi thêm"""
        # Kiểm tra xem đã có bài viết và phản hồi chưa
        if not self.current_essay or not self.current_feedback:
            QMessageBox.warning(
                self, "Cảnh báo", "Vui lòng đánh giá bài viết trước khi đặt câu hỏi!"
            )
            return

        # Lấy câu hỏi
        question = self.lineQuestion.text().strip()
        if not question:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập câu hỏi!")
            return

        # Lấy trình độ
        level = self.comboLevel.currentText()

        # Hiển thị thông báo đang xử lý
        current_text = self.textOutput.toPlainText()
        self.textOutput.setPlainText(
            current_text + "\n\nĐang xử lý câu hỏi, vui lòng đợi..."
        )
        QApplication.processEvents()  # Cập nhật giao diện

        # Gọi API để trả lời câu hỏi
        answer = ask_question(
            self.current_essay, self.current_feedback, question, level
        )

        # Hiển thị câu hỏi và câu trả lời
        self.textOutput.setPlainText(
            current_text + f"\n\nCâu hỏi: {question}\n\nTrả lời: {answer}"
        )

        # Xóa nội dung câu hỏi
        self.lineQuestion.clear()

    def toggle_dark_mode(self):
        """Chuyển đổi giữa chế độ sáng và tối"""
        self.dark_mode = not self.dark_mode

        # Thay đổi emoji
        if self.dark_mode:
            self.btnToggleMode.setText("🌙")

            # Áp dụng dark mode
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #1E1E1E;
                }
                QLabel {
                    color: #FFFFFF;
                }
                QLabel#labelTitle {
                    font-size: 28px;
                    font-weight: bold;
                    color: #64B5F6;
                }
                QPushButton {
                    background-color: #2979FF;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
                QTextEdit {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QComboBox {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                }
                QLineEdit {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 14px;
                }
                QWidget#mainContent {
                    background-color: #2D2D2D;
                    border-radius: 10px;
                    padding: 20px;
                }
                QPushButton#btnToggleMode {
                    font-size: 18px;
                    background-color: transparent;
                    border: none;
                }
            """
            )
        else:
            self.btnToggleMode.setText("☀️")

            # Áp dụng light mode
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #FFFFFF;
                }
                QLabel {
                    color: #333333;
                }
                QLabel#labelTitle {
                    font-size: 28px;
                    font-weight: bold;
                    color: #1976D2;
                }
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QTextEdit {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QComboBox {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                }
                QLineEdit {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 14px;
                }
                QWidget#mainContent {
                    background-color: #FFFFFF;
                    border-radius: 10px;
                    padding: 20px;
                }
                QPushButton#btnToggleMode {
                    font-size: 18px;
                    background-color: transparent;
                    border: none;
                }
            """
            )


# Khởi chạy ứng dụng
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
