from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6.QtCore import Qt
from PyQt6 import uic
import sys
import os
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, QTimer


class PianoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("bach.ui", self)

        self.setWindowTitle("Piano Simulator")

        # Mặc định chỉ chơi được quãng 4, 5, 6
        self.octave_start = 4  # Bắt đầu từ quãng 4

        # Thiết lập các phím đàn
        self.setup_piano_keys()

        # Khởi tạo media player và audio output
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)

        # Kết nối nút Play Sequence
        self.btnPlaySequence.clicked.connect(self.play_sequence)

        # Biến để lưu trữ chuỗi note đang phát
        self.current_sequence = []
        self.sequence_index = 0

        # Thiết lập phím tắt
        self.key_mapping = {
            Qt.Key.Key_A: 0,  # C
            Qt.Key.Key_W: 1,  # C#
            Qt.Key.Key_S: 2,  # D
            Qt.Key.Key_E: 3,  # D#
            Qt.Key.Key_D: 4,  # E
            Qt.Key.Key_F: 5,  # F
            Qt.Key.Key_T: 6,  # F#
            Qt.Key.Key_G: 7,  # G
            Qt.Key.Key_Y: 8,  # G#
            Qt.Key.Key_H: 9,  # A
            Qt.Key.Key_U: 10,  # A#
            Qt.Key.Key_J: 11,  # B
            Qt.Key.Key_K: 12,  # C (next octave)
            Qt.Key.Key_O: 13,  # C#
            Qt.Key.Key_L: 14,  # D
            Qt.Key.Key_P: 15,  # D#
            Qt.Key.Key_Semicolon: 16,  # E
        }

    def setup_piano_keys(self):
        # Tìm tất cả các nút phím đàn trong UI
        for child in self.findChildren(QPushButton):
            if child.objectName().startswith("key_"):
                note_index = int(child.objectName().split("_")[1])
                child.clicked.connect(
                    lambda checked, idx=note_index: self.play_note(idx)
                )

    def play_note(self, relative_index):
        # Tính toán chỉ số note thực tế dựa trên quãng
        notes_per_octave = 12
        actual_index = ((self.octave_start - 1) * notes_per_octave) + relative_index + 1

        # Đảm bảo chỉ số nằm trong phạm vi hợp lệ (1-88)
        if 1 <= actual_index <= 88:
            sound_path = f"piano/{actual_index}.mp3"
            if os.path.exists(sound_path):
                # Dừng âm thanh đang phát
                self.media_player.stop()
                # Phát âm thanh mới
                self.media_player.setSource(
                    QUrl.fromLocalFile(os.path.abspath(sound_path))
                )
                self.media_player.play()

                # Cập nhật hiển thị note
                note_names = [
                    "C",
                    "C#",
                    "D",
                    "D#",
                    "E",
                    "F",
                    "F#",
                    "G",
                    "G#",
                    "A",
                    "A#",
                    "B",
                ]
                octave = (actual_index - 1) // 12 + 1
                note_name = note_names[(actual_index - 1) % 12]
                self.labelCurrentNote.setText(
                    f"Note: {note_name}{octave} (Key {actual_index})"
                )

    def play_sequence(self):
        # Lấy chuỗi note từ textbox
        sequence_text = self.txtNoteSequence.text().strip()
        if not sequence_text:
            self.labelStatus.setText("Please enter a note sequence")
            return

        # Phân tích chuỗi note
        self.current_sequence = self.parse_note_sequence(sequence_text)
        if not self.current_sequence:
            self.labelStatus.setText("Invalid note sequence format")
            return

        # Bắt đầu phát chuỗi
        self.sequence_index = 0
        self.labelStatus.setText(f"Playing sequence: {sequence_text}")
        self.play_next_in_sequence()

    def parse_note_sequence(self, sequence_text):
        # Phân tích chuỗi note (ví dụ: "C4 D4 E4 F4 G4")
        notes = []
        note_names = {
            "C": 0,
            "C#": 1,
            "Db": 1,
            "D": 2,
            "D#": 3,
            "Eb": 3,
            "E": 4,
            "F": 5,
            "F#": 6,
            "Gb": 6,
            "G": 7,
            "G#": 8,
            "Ab": 8,
            "A": 9,
            "A#": 10,
            "Bb": 10,
            "B": 11,
        }

        parts = sequence_text.split()
        for part in parts:
            # Tìm vị trí của số (quãng)
            octave_pos = -1
            for i, char in enumerate(part):
                if char.isdigit():
                    octave_pos = i
                    break

            if octave_pos == -1:
                continue  # Bỏ qua nếu không tìm thấy quãng

            note_name = part[:octave_pos]
            try:
                octave = int(part[octave_pos:])
                if note_name in note_names and 1 <= octave <= 7:
                    note_index = note_names[note_name]
                    relative_index = note_index
                    notes.append((relative_index, octave))
            except ValueError:
                continue

        return notes

    def play_next_in_sequence(self):
        if self.sequence_index < len(self.current_sequence):
            relative_index, octave = self.current_sequence[self.sequence_index]

            # Tính toán chỉ số note thực tế dựa trên quãng được chỉ định
            notes_per_octave = 12
            actual_index = ((octave - 1) * notes_per_octave) + relative_index + 1

            # Phát note
            sound_path = f"piano/{actual_index}.mp3"
            if os.path.exists(sound_path):
                self.media_player.stop()
                self.media_player.setSource(
                    QUrl.fromLocalFile(os.path.abspath(sound_path))
                )
                self.media_player.play()

                # Cập nhật hiển thị note
                note_names = [
                    "C",
                    "C#",
                    "D",
                    "D#",
                    "E",
                    "F",
                    "F#",
                    "G",
                    "G#",
                    "A",
                    "A#",
                    "B",
                ]
                note_name = note_names[relative_index]
                self.labelCurrentNote.setText(
                    f"Note: {note_name}{octave} (Key {actual_index})"
                )

            self.sequence_index += 1
            # Đặt hẹn giờ cho note tiếp theo (500ms)
            QTimer.singleShot(500, self.play_next_in_sequence)
        else:
            # Kết thúc chuỗi
            self.labelStatus.setText("Sequence completed")

    def keyPressEvent(self, event):
        # Xử lý phím tắt
        if event.key() in self.key_mapping:
            relative_index = self.key_mapping[event.key()]
            self.play_note(relative_index)
        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PianoApp()
    window.show()
    sys.exit(app.exec())
