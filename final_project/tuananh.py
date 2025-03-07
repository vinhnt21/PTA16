from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QListWidgetItem
from PyQt6.QtCore import QTimer, Qt
from PyQt6 import uic
import sys
import random


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("tuananh.ui", self)

        # Thiết lập thời gian
        self.work_time = 25 * 60  # 25 phút làm việc
        self.break_time = 5 * 60  # 5 phút nghỉ
        self.current_time = self.work_time
        self.is_working = True
        self.timer_running = False

        # Khởi tạo timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # Kết nối các nút với hàm xử lý
        self.button_start.clicked.connect(self.start_timer)
        self.button_pause.clicked.connect(self.pause_timer)
        self.button_reset.clicked.connect(self.reset_timer)
        self.button_add_task.clicked.connect(self.add_task)
        self.button_mark_done.clicked.connect(self.mark_task_done)

        # Danh sách thông báo động viên
        self.motivational_messages = [
            "Bạn đang làm rất tốt!",
            "Hãy tiếp tục cố gắng!",
            "Tập trung vào mục tiêu!",
            "Mỗi phút đều quan trọng!",
            "Bạn có thể làm được!",
            "Hãy kiên trì, thành công sẽ đến!",
            "Nghỉ ngơi đúng lúc giúp bạn hiệu quả hơn!",
        ]

        # Cập nhật giao diện ban đầu
        self.update_display()

    def update_timer(self):
        """Cập nhật thời gian mỗi giây"""
        self.current_time -= 1

        if self.current_time <= 0:
            self.timer.stop()
            self.timer_running = False

            if self.is_working:
                self.is_working = False
                self.current_time = self.break_time
                self.label_status.setText("Đang nghỉ ngơi")
                QMessageBox.information(self, "Thông báo", "Đã đến lúc nghỉ ngơi!")
            else:
                self.is_working = True
                self.current_time = self.work_time
                self.label_status.setText("Đang làm việc")
                QMessageBox.information(self, "Thông báo", "Đã đến lúc làm việc!")

            # Cập nhật thông báo động viên
            self.update_motivational_message()

        self.update_display()

    def update_display(self):
        """Cập nhật hiển thị thời gian"""
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        self.label_time.setText(f"{minutes:02d}:{seconds:02d}")

    def start_timer(self):
        """Bắt đầu đếm thời gian"""
        if not self.timer_running:
            self.timer.start(1000)  # 1000ms = 1s
            self.timer_running = True
            self.update_motivational_message()

    def pause_timer(self):
        """Tạm dừng đếm thời gian"""
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False

    def reset_timer(self):
        """Đặt lại thời gian"""
        self.timer.stop()
        self.timer_running = False
        self.is_working = True
        self.current_time = self.work_time
        self.label_status.setText("Đang làm việc")
        self.update_display()

    def add_task(self):
        """Thêm công việc mới vào danh sách"""
        task_text = self.line_edit_task.text().strip()
        if task_text:
            item = QListWidgetItem(task_text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget_tasks.addItem(item)
            self.line_edit_task.clear()

    def mark_task_done(self):
        """Đánh dấu công việc đã hoàn thành"""
        current_item = self.list_widget_tasks.currentItem()
        if current_item:
            if current_item.checkState() == Qt.CheckState.Unchecked:
                current_item.setCheckState(Qt.CheckState.Checked)
                current_text = current_item.text()
                current_item.setText(f"✓ {current_text}")
                QMessageBox.information(
                    self, "Chúc mừng", "Bạn đã hoàn thành một công việc!"
                )

    def update_motivational_message(self):
        """Cập nhật thông báo động viên ngẫu nhiên"""
        message = random.choice(self.motivational_messages)
        self.label_ai_message.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
