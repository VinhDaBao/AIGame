# utils.py
# Hàm tiện ích

import pygame
import os
from settings import ASSETS_PATH
def load_image(filename):
    full_path = os.path.join(ASSETS_PATH, "images", filename)
    print(full_path)
    try:
        image = pygame.image.load(full_path).convert_alpha()
        return image
    except Exception as e:
        #print(f"Không thể tải hình ảnh: {full_path}. Lỗi: {str(e)}")
        return pygame.Surface((400, 400))  # Trả về surface mặc định nếu lỗi
def draw_text(screen, text, font, color, x, y, center=False):
    text_surf = font.render(text, True, color)
    if center:
        x -= text_surf.get_width() // 2
    screen.blit(text_surf, (x, y))
