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