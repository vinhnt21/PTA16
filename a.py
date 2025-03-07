import pygame
import time

# Khởi tạo pygame
pygame.init()
pygame.mixer.init()

# Đường dẫn đến file nhạc
music_file = "./a.mp3"  # Thay đổi đường dẫn này

# Load và phát nhạc
pygame.mixer.music.load(music_file)
pygame.mixer.music.play()

# Đợi cho đến khi nhạc phát xong
while pygame.mixer.music.get_busy():
    time.sleep(1)

# Dọn dẹp
pygame.mixer.quit()
pygame.quit()
