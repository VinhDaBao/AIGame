#settings.py
#Cài đặt chung
import os
#Kích thước màn hình
WIDTH = 400
HEIGHT = 400



FPS = 30

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "assets")
# Các mức độ khó
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

# Các hình thức đua
RACE_MODES = ["Player vs Player", "Player vs Machine", "Machine vs Machine"]

# Màu sắc cho nút chữ (Text Button Colors)
TEXT_BUTTON_COLOR = (220, 220, 220)  # Màu chữ bình thường
TEXT_BUTTON_HOVER_COLOR = (255, 255, 0) # Màu chữ khi hover
TEXT_BUTTON_SELECTED_COLOR = (0, 255, 0) # Màu chữ khi được chọn
TEXT_TITLE_COLOR = (255, 255, 255) # Màu cho tiêu đề chọn thuật toán