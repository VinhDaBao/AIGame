# menu.py
# Quản lý menu

import pygame
import os
from settings import *
from settings import TEXT_BUTTON_COLOR, TEXT_BUTTON_HOVER_COLOR, TEXT_BUTTON_SELECTED_COLOR, TEXT_TITLE_COLOR
from utils import load_image, draw_text

# Đường dẫn đến font Press Start 2P
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts", "PressStart2P-Regular.ttf")

# Màu sắc
TITLE_COLOR = (8, 50, 50)  # Màu mới cho tiêu đề

# Algorithm Menu Colors
ALGO_MENU_GREEN = (85, 150, 85) # Background color for algorithm menu
ALGO_MENU_BORDER_COLOR = (200, 200, 200) # Border color for algorithm menu

class ModeMenu:
    def __init__(self, screen, sound_manager=None):
        self.screen = screen
        self.sound_manager = sound_manager
        
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
            if self.sound_manager:
                self.sound_manager.play_sound("CLICK")
            return "back"
        
        # Kiểm tra các nút chế độ chơi
        for button in self.mode_buttons:
            button['is_pressed'] = button['rect'].collidepoint(mouse_pos) and mouse_pressed
            
            if button['rect'].collidepoint(mouse_pos) and mouse_just_released:
                if self.sound_manager:
                    self.sound_manager.play_sound("CLICK")
                return button['text']
        
        return None

class LevelMenu:
    
    def __init__(self, screen, sound_manager=None):
        self.screen = screen
        self.sound_manager = sound_manager
        
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
            if self.sound_manager:
                self.sound_manager.play_sound("CLICK")
            return "back"
        
        # Kiểm tra các nút level
        for button in self.level_buttons:
            button['is_pressed'] = button['rect'].collidepoint(mouse_pos) and mouse_pressed
            
            if button['rect'].collidepoint(mouse_pos) and mouse_just_released:
                if self.sound_manager:
                    self.sound_manager.play_sound("CLICK")
                return button['text']
        
        return None


#<--------------------------------Algorithm Menu------------------------------------>
class AlgorithmMenu:
    def __init__(self, screen, sound_manager=None, show_left_select=True, show_right_select=True):
        self.screen = screen
        self.sound_manager = sound_manager
        self.sprite_sheet = load_image("Menu.png") # Reusing menu background sprite
        self.FRAME_WIDTH = 400
        self.FRAME_HEIGHT = 400
        sheet_width = self.sprite_sheet.get_width()
        self.NUM_FRAMES = sheet_width // self.FRAME_WIDTH

        if self.NUM_FRAMES == 0:
            print("AlgorithmMenu: Sprite sheet Menu.png không hợp lệ, sử dụng background mặc định")
            self.frames = [pygame.Surface((WIDTH, HEIGHT))]
            self.frames[0].fill((0,0,0))
        else:
            self.frames = [
                self.sprite_sheet.subsurface(pygame.Rect(i * self.FRAME_WIDTH, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT))
                for i in range(self.NUM_FRAMES)
            ]
        
        self.frame_index = 0
        self.frame_delay = 10 
        self.frame_counter = 0

        self.menu_frame = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT))
        self.menu_frame.fill(ALGO_MENU_GREEN) # Use the new green color
        pygame.draw.rect(self.menu_frame, ALGO_MENU_BORDER_COLOR, self.menu_frame.get_rect(), 2) # Draw border
        self.menu_frame_rect = self.menu_frame.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        try:
            self.font = pygame.font.Font(FONT_PATH, 10)        # Was 12 (For buttons UCS, A*, Confirm, Back)
            self.small_font = pygame.font.Font(FONT_PATH, 7)   # Was 8 (For labels Fish 1, Fish 2)
            self.title_font = pygame.font.Font(FONT_PATH, 14)  # Was 16 (For "Select Algorithms" title)
        except Exception as e:
            print(f"Font loading error in AlgorithmMenu: {e}")
            self.font = pygame.font.Font(None, 15)       # Was 18
            self.small_font = pygame.font.Font(None, 11) # Was 14
            self.title_font = pygame.font.Font(None, 18) # Was 22

        self.show_left_select = show_left_select
        self.show_right_select = show_right_select
        self.algorithms = ["UCS", "A*", "Backtracking", "AND-OR", "Genetic", "Q-Learning"] # Updated list
            
        if self.show_left_select:
            self.selected_algo_left = self.algorithms[0] 
        else:
            self.selected_algo_left = "Player" # Mark as Player controlled
            
        if self.show_right_select:
            self.selected_algo_right = self.algorithms[0]
        else:
            self.selected_algo_right = "Player" # Mark as Player controlled

        self.buttons = []
        self._create_buttons() 

    def _create_buttons(self):
        self.buttons = [] 
        button_width = 80
        button_height = 30
        column_spacing = 130 
        
        # Adjust column positions based on visibility
        if self.show_left_select and self.show_right_select:
            left_column_center_x = WIDTH // 2 - column_spacing // 2
            right_column_center_x = WIDTH // 2 + column_spacing // 2
        elif self.show_left_select:
            left_column_center_x = WIDTH // 2
            right_column_center_x = -WIDTH # Effectively hide if not used
        elif self.show_right_select:
            left_column_center_x = -WIDTH # Effectively hide if not used
            right_column_center_x = WIDTH // 2
        else: # Neither shown (this state should ideally not load the menu)
            left_column_center_x = -WIDTH
            right_column_center_x = -WIDTH
        
        title_height = self.menu_frame_rect.top + 25 # Y-coordinate of the title's center
        
        # Determine button_start_y based on whether one or two columns are shown
        if self.show_left_select and self.show_right_select:
            # Both columns shown: position buttons below fish labels
            label_y_offset = title_height + 45 # Y-coordinate for fish labels (Fish1, Fish2)
            button_start_y = label_y_offset + 40 # Start Y for algorithm buttons
        else:
            # Only one column shown (or neither, though this menu shouldn't be active then):
            # Position buttons closer to the main title, as fish labels will be hidden
            button_start_y = title_height + 60 # Start Y for algorithm buttons, closer to title
            
        button_y_spacing = 35

        # Algorithm selection buttons for Left Frame (Fish 1)
        if self.show_left_select:
            for i, algo_name in enumerate(self.algorithms):
                rect = pygame.Rect(0, 0, button_width, button_height)
                rect.center = (left_column_center_x, button_start_y + i * button_y_spacing)
                self.buttons.append({"text": algo_name, "id": f"left_{algo_name}", "rect": rect, "frame": "left"})

        # Algorithm selection buttons for Right Frame (Fish 2)
        if self.show_right_select:
            for i, algo_name in enumerate(self.algorithms):
                rect = pygame.Rect(0, 0, button_width, button_height)
                rect.center = (right_column_center_x, button_start_y + i * button_y_spacing)
                self.buttons.append({"text": algo_name, "id": f"right_{algo_name}", "rect": rect, "frame": "right"})
        
        # Confirm button
        confirm_rect = pygame.Rect(0,0, 100, 35) # Width/Height can be adjusted if needed
        confirm_rect.center = (WIDTH // 2, self.menu_frame_rect.bottom - 60) # Moved down
        self.buttons.append({"text": "Confirm", "id": "confirm", "rect": confirm_rect, "frame": "action"})

        # Back button
        back_rect = pygame.Rect(0,0, 80, 30) # Width/Height can be adjusted if needed
        back_rect.center = (WIDTH // 2, self.menu_frame_rect.bottom - 30) # Moved down
        self.buttons.append({"text": "Back", "id": "back", "rect": back_rect, "frame": "action"})

    def update_animation(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % self.NUM_FRAMES
            self.frame_counter = 0

    def draw(self):
        self.screen.blit(self.frames[self.frame_index], (0, 0))
        self.screen.blit(self.menu_frame, self.menu_frame_rect)

        title_text = ""
        if self.show_left_select and self.show_right_select:
            title_text = "Algorithms"
        elif self.show_left_select:
            title_text = "Left Fish: Algorithm"
        elif self.show_right_select:
            title_text = "Right Fish: Algorithm"
        
        if title_text: # Only draw title if there's something to select
            draw_text(self.screen, title_text, self.title_font, TITLE_COLOR, WIDTH // 2, self.menu_frame_rect.top + 25, center=True)
        
        column_spacing = 130 
        left_column_center_x = WIDTH // 2 - column_spacing // 2
        right_column_center_x = WIDTH // 2 + column_spacing // 2
        label_y_pos = self.menu_frame_rect.top + 70

        # Draw Fish1/Fish2 labels ONLY IF BOTH selection columns are active
        if self.show_left_select and self.show_right_select:
            current_left_column_center_x = WIDTH // 2 - column_spacing // 2
            current_right_column_center_x = WIDTH // 2 + column_spacing // 2
            label_y_pos = self.menu_frame_rect.top + 25 + 45 # Position labels relative to title
            draw_text(self.screen, "Fish 1 (Left)", self.small_font, TEXT_TITLE_COLOR, current_left_column_center_x, label_y_pos, center=True)
            draw_text(self.screen, "Fish 2 (Right)", self.small_font, TEXT_TITLE_COLOR, current_right_column_center_x, label_y_pos, center=True)
        # If only one (or none) is shown, the main title ("Select Algorithm for Left/Right Fish") is sufficient.


        mouse_pos = pygame.mouse.get_pos()
        for button_info in self.buttons:
            text = button_info["text"]
            rect = button_info["rect"]
            frame_type = button_info["frame"]

            color = TEXT_BUTTON_COLOR # Default color
            if rect.collidepoint(mouse_pos):
                color = TEXT_BUTTON_HOVER_COLOR # Hover color
            
            # Selected color
            if frame_type == "left" and self.selected_algo_left == text:
                color = TEXT_BUTTON_SELECTED_COLOR
            elif frame_type == "right" and self.selected_algo_right == text:
                color = TEXT_BUTTON_SELECTED_COLOR
            
            draw_text(self.screen, text, self.font, color, rect.centerx, rect.centery, center=True)
            # pygame.draw.rect(self.screen, (255,0,0), rect, 1) # For debugging button rects - uncomment if needed

    def handle_events(self, mouse_pos, mouse_pressed, mouse_just_released):
        if mouse_just_released: 
            for button_info in self.buttons:
                if button_info["rect"].collidepoint(mouse_pos):
                    if self.sound_manager:
                        self.sound_manager.play_sound("CLICK")
                    button_id = button_info["id"]
                    button_text = button_info["text"]
                    frame_type = button_info["frame"]

                    if frame_type == "left" and self.show_left_select:
                        self.selected_algo_left = button_text
                        # print(f"Selected Left Algorithm: {self.selected_algo_left}")
                        return None # Stay on this menu to reflect selection
                    elif frame_type == "right" and self.show_right_select:
                        self.selected_algo_right = button_text
                        # print(f"Selected Right Algorithm: {self.selected_algo_right}")
                        return None # Stay on this menu to reflect selection
                    elif button_id == "confirm":
                        if self.selected_algo_left and self.selected_algo_right:
                            # print(f"Algorithms confirmed: Left - {self.selected_algo_left}, Right - {self.selected_algo_right}")
                            return {"action": "confirm", "left_algo": self.selected_algo_left, "right_algo": self.selected_algo_right}
                        else:
                            # This case should not be hit if defaults are set and UI prevents deselection
                            print("Error: Algorithm selection somehow missing. Both must be selected.") 
                            return None # Stay on menu, or provide on-screen error
                    elif button_id == "back":
                        # print("Back to Main Menu from AlgorithmMenu")
                        return {"action": "back"}
        return None
#<--------------------------------End Algorithm Menu-------------------------------->


class MainMenu:
    def __init__(self, screen, sound_manager=None):
        self.screen = screen
        self.sound_manager = sound_manager
        
        # Play menu background music
        if self.sound_manager:
            self.sound_manager.play_background("MENU_BACKGROUND")
            
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
            if self.sound_manager:
                self.sound_manager.play_sound("CLICK")
            return "play"
        elif mode_on_button and mouse_just_released:
            print("Mode button clicked!")
            if self.sound_manager:
                self.sound_manager.play_sound("CLICK")
            return "mode"
        elif level_on_button and mouse_just_released:
            print("Level button clicked!")
            if self.sound_manager:
                self.sound_manager.play_sound("CLICK")
            return "level"
        return None