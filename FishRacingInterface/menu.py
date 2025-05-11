# menu.py
# Quản lý menu

import pygame
import os
from settings import *
from utils import load_image, draw_text

# Đường dẫn đến font Press Start 2P
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts", "PressStart2P-Regular.ttf")

# Màu sắc
TITLE_COLOR = (8, 50, 50)  # Màu mới cho tiêu đề

class ModeMenu:
    def __init__(self, screen):
        self.screen = screen
        
        # Load sprite sheet background
        self.sprite_sheet = load_image("Menu.png")
        
        # Kích thước mỗi frame trong sprite sheet
        self.FRAME_WIDTH = 400
        self.FRAME_HEIGHT = 400
        # Tính số frame trong sprite sheet
        sheet_width = self.sprite_sheet.get_width()
        self.NUM_FRAMES = sheet_width // self.FRAME_WIDTH
        
        # Kiểm tra nếu sprite sheet không hợp lệ
        if self.NUM_FRAMES == 0:
            print("Sprite sheet Menu.png không hợp lệ, sử dụng background mặc định")
            self.frames = [pygame.Surface((WIDTH, HEIGHT))]
            self.frames[0].fill((0,0,0))
        else:
            # Cắt các frame từ sprite sheet
            self.frames = [
                self.sprite_sheet.subsurface(pygame.Rect(i * self.FRAME_WIDTH, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT))
                for i in range(self.NUM_FRAMES)
            ]
        
        # Biến điều khiển animation
        self.frame_index = 0
        self.frame_delay = 5
        self.frame_counter = 0
        
        # Load nút Back
        self.back_button = load_image("back_button.png")
        self.back_button_pressed = load_image("back_button_pressed.png")
        self.back_button_rect = self.back_button.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.back_is_pressed = False
        
        # Load menu background
        self.menu_frame = load_image("menu_background.png")
        self.menu_frame_rect = self.menu_frame.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Tạo các nút chế độ chơi với ảnh
        self.mode_buttons = []
        mode_images = {
            "Player vs Player": ("PVP_button.png", "PVP_button_pressed.png"),
            "Player vs Machine": ("PVM_button.png", "PVM_button_pressed.png"),
            "Machine vs Machine": ("MVM_button.png", "MVM_button_pressed.png")
        }
        
        # Load nút đầu tiên để lấy kích thước
        first_button = load_image(mode_images["Player vs Player"][0])
        button_height = first_button.get_height()
        
        # Tính toán vị trí cho các nút
        # Bắt đầu từ vị trí 1/4 chiều cao của khung menu
        start_y = self.menu_frame_rect.top + (self.menu_frame_rect.height // 4)
        
        # Tạo các nút
        button_y = start_y
        for mode, (normal_img, pressed_img) in mode_images.items():
            button = {
                'text': mode,
                'normal': load_image(normal_img),
                'pressed': load_image(pressed_img),
                'rect': None,
                'is_pressed': False
            }
            # Đặt nút ở giữa khung menu theo chiều ngang và vị trí y đã tính
            button['rect'] = button['normal'].get_rect(center=(self.menu_frame_rect.centerx, button_y))
            self.mode_buttons.append(button)
            # Tăng vị trí y cho nút tiếp theo
            button_y += 45  # Giảm khoảng cách giữa các nút
        
        # Font cho text
        try:
            self.font = pygame.font.Font(FONT_PATH, 16)
            print(f"Đã load font từ: {FONT_PATH}")
        except Exception as e:
            print(f"Không thể load font Press Start 2P: {e}")
            print(f"Đường dẫn font: {FONT_PATH}")
            self.font = pygame.font.Font(None, 36)
    
    def update_animation(self):
        # Cập nhật frame sau mỗi `frame_delay` vòng lặp
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % self.NUM_FRAMES
            self.frame_counter = 0
        
    def draw(self):
        # Vẽ frame hiện tại của background
        self.screen.blit(self.frames[self.frame_index], (0, 0))
        
        # Vẽ menu background
        self.screen.blit(self.menu_frame, self.menu_frame_rect)
        
        # Vẽ tiêu đề với màu mới
        title = "Select Game Mode"
        draw_text(self.screen, title, self.font, TITLE_COLOR, WIDTH // 2, 50, center=True)
        
        # Vẽ các nút chế độ chơi
        for button in self.mode_buttons:
            if button['is_pressed']:
                self.screen.blit(button['pressed'], button['rect'])
            else:
                self.screen.blit(button['normal'], button['rect'])
        
        # Vẽ nút Back
        if self.back_is_pressed:
            self.screen.blit(self.back_button_pressed, self.back_button_rect)
        else:
            self.screen.blit(self.back_button, self.back_button_rect)
    
    def handle_events(self, mouse_pos, mouse_pressed, mouse_just_released):
        # Kiểm tra nút Back
        back_on_button = self.back_button_rect.collidepoint(mouse_pos)
        self.back_is_pressed = back_on_button and mouse_pressed
        
        if back_on_button and mouse_just_released:
            return "back"
        
        # Kiểm tra các nút chế độ chơi
        for button in self.mode_buttons:
            button['is_pressed'] = button['rect'].collidepoint(mouse_pos) and mouse_pressed
            
            if button['rect'].collidepoint(mouse_pos) and mouse_just_released:
                return button['text']
        
        return None

class LevelMenu:
    def __init__(self, screen):
        self.screen = screen
        
        # Load sprite sheet background
        self.sprite_sheet = load_image("Menu.png")
        
        # Kích thước mỗi frame trong sprite sheet
        self.FRAME_WIDTH = 400
        self.FRAME_HEIGHT = 400
        # Tính số frame trong sprite sheet
        sheet_width = self.sprite_sheet.get_width()
        self.NUM_FRAMES = sheet_width // self.FRAME_WIDTH
        
        # Kiểm tra nếu sprite sheet không hợp lệ
        if self.NUM_FRAMES == 0:
            print("Sprite sheet Menu.png không hợp lệ, sử dụng background mặc định")
            self.frames = [pygame.Surface((WIDTH, HEIGHT))]
            self.frames[0].fill((0,0,0))
        else:
            # Cắt các frame từ sprite sheet
            self.frames = [
                self.sprite_sheet.subsurface(pygame.Rect(i * self.FRAME_WIDTH, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT))
                for i in range(self.NUM_FRAMES)
            ]
        
        # Biến điều khiển animation
        self.frame_index = 0
        self.frame_delay = 5
        self.frame_counter = 0
        
        # Load nút Back
        self.back_button = load_image("back_button.png")
        self.back_button_pressed = load_image("back_button_pressed.png")
        self.back_button_rect = self.back_button.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.back_is_pressed = False
        
        # Load menu background
        self.menu_frame = load_image("menu_level_background.png")
        self.menu_frame_rect = self.menu_frame.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Tạo các nút level với ảnh
        self.level_buttons = []
        level_images = {
            "Easy": ("easy_button.png", "easy_button_pressed.png"),
            "Mid": ("mid_button.png", "mid_button_pressed.png"),
            "Hard": ("hard_button.png", "hard_button_pressed.png")
        }
        
        # Load nút đầu tiên để lấy kích thước
        first_button = load_image(level_images["Easy"][0])
        button_height = first_button.get_height()
        
        # Tính toán vị trí cho các nút
        # Bắt đầu từ vị trí 1/4 chiều cao của khung menu
        start_y = self.menu_frame_rect.top + (self.menu_frame_rect.height // 4)
        
        # Tạo các nút
        button_y = start_y
        for level, (normal_img, pressed_img) in level_images.items():
            button = {
                'text': level,
                'normal': load_image(normal_img),
                'pressed': load_image(pressed_img),
                'rect': None,
                'is_pressed': False
            }
            # Đặt nút ở giữa khung menu theo chiều ngang và vị trí y đã tính
            button['rect'] = button['normal'].get_rect(center=(self.menu_frame_rect.centerx, button_y))
            self.level_buttons.append(button)
            # Tăng vị trí y cho nút tiếp theo
            button_y += 45  # Khoảng cách giữa các nút
        
        # Font cho text
        try:
            self.font = pygame.font.Font(FONT_PATH, 16)
            print(f"Đã load font từ: {FONT_PATH}")
        except Exception as e:
            print(f"Không thể load font Press Start 2P: {e}")
            print(f"Đường dẫn font: {FONT_PATH}")
            self.font = pygame.font.Font(None, 36)
    
    def update_animation(self):
        # Cập nhật frame sau mỗi `frame_delay` vòng lặp
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % self.NUM_FRAMES
            self.frame_counter = 0
        
    def draw(self):
        # Vẽ frame hiện tại của background
        self.screen.blit(self.frames[self.frame_index], (0, 0))
        
        # Vẽ menu background
        self.screen.blit(self.menu_frame, self.menu_frame_rect)
        
        # Vẽ tiêu đề với màu mới
        title = "Select Level"
        draw_text(self.screen, title, self.font, TITLE_COLOR, WIDTH // 2, 50, center=True)
        
        # Vẽ các nút level
        for button in self.level_buttons:
            if button['is_pressed']:
                self.screen.blit(button['pressed'], button['rect'])
            else:
                self.screen.blit(button['normal'], button['rect'])
        
        # Vẽ nút Back
        if self.back_is_pressed:
            self.screen.blit(self.back_button_pressed, self.back_button_rect)
        else:
            self.screen.blit(self.back_button, self.back_button_rect)
    
    def handle_events(self, mouse_pos, mouse_pressed, mouse_just_released):
        # Kiểm tra nút Back
        back_on_button = self.back_button_rect.collidepoint(mouse_pos)
        self.back_is_pressed = back_on_button and mouse_pressed
        
        if back_on_button and mouse_just_released:
            return "back"
        
        # Kiểm tra các nút level
        for button in self.level_buttons:
            button['is_pressed'] = button['rect'].collidepoint(mouse_pos) and mouse_pressed
            
            if button['rect'].collidepoint(mouse_pos) and mouse_just_released:
                return button['text']
        
        return None

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        
        # Load sprite sheet background
        self.sprite_sheet = load_image("Menu.png")
        
        # Kích thước mỗi frame trong sprite sheet
        self.FRAME_WIDTH = 400
        self.FRAME_HEIGHT = 400
        # Tính số frame trong sprite sheet
        sheet_width = self.sprite_sheet.get_width()
        self.NUM_FRAMES = sheet_width // self.FRAME_WIDTH
        
        # Kiểm tra nếu sprite sheet không hợp lệ
        if self.NUM_FRAMES == 0:
            print("Sprite sheet Menu.png không hợp lệ, sử dụng background mặc định")
            self.frames = [pygame.Surface((WIDTH, HEIGHT))]
            self.frames[0].fill((0,0,0))
        else:
            # Cắt các frame từ sprite sheet
            self.frames = [
                self.sprite_sheet.subsurface(pygame.Rect(i * self.FRAME_WIDTH, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT))
                for i in range(self.NUM_FRAMES)
            ]
        
        # Biến điều khiển animation
        self.frame_index = 0
        self.frame_delay = 5
        self.frame_counter = 0
        
        # Load title game
        self.title_image = load_image("title_game.png")
        self.title_rect = self.title_image.get_rect(center=(WIDTH // 2, HEIGHT // 4))  # Đặt ở 1/4 màn hình
        
        # Load nút Play
        self.play_button = load_image("play_button.png")
        self.play_button_pressed = load_image("play_button_pressed.png")
        self.play_button_rect = self.play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Đặt ở giữa màn hình
        
        # Load nút Mode
        self.mode_button = load_image("mode.png")
        self.mode_button_pressed = load_image("mode_pressed.png")
        self.mode_button_rect = self.mode_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))  # Đặt dưới nút Play
        
        # Load nút Level
        self.level_button = load_image("level_button.png")
        self.level_button_pressed = load_image("level_button_pressed.png")
        self.level_button_rect = self.level_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))  # Đặt dưới nút Mode

        # Trạng thái của các nút
        self.play_is_pressed = False
        self.mode_is_pressed = False
        self.level_is_pressed = False

    def update_animation(self):
        # Cập nhật frame sau mỗi `frame_delay` vòng lặp
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % self.NUM_FRAMES
            self.frame_counter = 0
    
    def draw(self):
        # Vẽ frame hiện tại của background
        self.screen.blit(self.frames[self.frame_index], (0, 0))
        
        # Vẽ title game
        self.screen.blit(self.title_image, self.title_rect)
        
        # Vẽ nút Play
        if self.play_is_pressed:
            self.screen.blit(self.play_button_pressed, self.play_button_rect)
        else:
            self.screen.blit(self.play_button, self.play_button_rect)
            
        # Vẽ nút Mode
        if self.mode_is_pressed:
            self.screen.blit(self.mode_button_pressed, self.mode_button_rect)
        else:
            self.screen.blit(self.mode_button, self.mode_button_rect)
            
        # Vẽ nút Level
        if self.level_is_pressed:
            self.screen.blit(self.level_button_pressed, self.level_button_rect)
        else:
            self.screen.blit(self.level_button, self.level_button_rect)
    
    def handle_events(self, mouse_pos, mouse_pressed, mouse_just_released):
        # Kiểm tra xem chuột có đang nhấn trên các nút không
        play_on_button = self.play_button_rect.collidepoint(mouse_pos)
        mode_on_button = self.mode_button_rect.collidepoint(mouse_pos)
        level_on_button = self.level_button_rect.collidepoint(mouse_pos)

        # Cập nhật trạng thái nhấn
        if play_on_button and mouse_pressed:
            self.play_is_pressed = True
        else:
            self.play_is_pressed = False
            
        if mode_on_button and mouse_pressed:
            self.mode_is_pressed = True
        else:
            self.mode_is_pressed = False
            
        if level_on_button and mouse_pressed:
            self.level_is_pressed = True
        else:
            self.level_is_pressed = False

        # Kiểm tra sự kiện thả chuột (mouse up) trên các nút
        if play_on_button and mouse_just_released:
            print("Play button clicked!")
            return "play"
        elif mode_on_button and mouse_just_released:
            print("Mode button clicked!")
            return "mode"
        elif level_on_button and mouse_just_released:
            print("Level button clicked!")
            return "level"
        return None