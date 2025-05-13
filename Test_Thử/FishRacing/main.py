#main.py
#File chính của game

import pygame
import sys
from settings import *
from menu import MainMenu, ModeMenu, LevelMenu
from game_window import GameWindow

os.environ['SDL_VIDEO_CENTERED'] = '1'
# Khởi tạo Pygame
pygame.init()

def init_menu():
    # Thiết lập cửa sổ menu
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fish Racing - Menu")
    return screen

# Thiết lập cửa sổ ban đầu
screen = init_menu()

# Tạo clock để kiểm soát FPS
clock = pygame.time.Clock()

#Tạo các menu
main_menu = MainMenu(screen)
mode_menu = ModeMenu(screen)
level_menu = LevelMenu(screen)

# Trạng thái game
current_menu = "main"  # "main", "mode" hoặc "level"
selected_mode = None
selected_level = "Easy"

# Vòng lặp chính
running = True
mouse_just_released = False
previous_mouse_state = False

while running:
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lấy vị trí chuột và trạng thái nhấn chuột
    mouse_pos = pygame.mouse.get_pos()
    current_mouse_state = pygame.mouse.get_pressed()[0]  # True nếu nhấn chuột trái
    
    # Kiểm tra xem chuột có vừa được thả không
    mouse_just_released = previous_mouse_state and not current_mouse_state
    previous_mouse_state = current_mouse_state  # Cập nhật trạng thái chuột trước đó
    
    # Xử lý sự kiện menu
    if current_menu == "main":
        result = main_menu.handle_events(mouse_pos, current_mouse_state, mouse_just_released)
        if result == "play":
            # Tạo và chạy cửa sổ game mới
            endless =  True
            while endless:
                game_window = GameWindow(level=selected_level)
                endless = game_window.run()  # Chạy cửa sổ game
            
            # Sau khi game kết thúc, khởi tạo lại menu
            screen = init_menu()
            main_menu = MainMenu(screen)
            mode_menu = ModeMenu(screen)
            level_menu = LevelMenu(screen)
        elif result == "mode":
            current_menu = "mode"
            print("Opening mode selection...")
        elif result == "level":
            current_menu = "level"
            print("Opening level selection...")
    elif current_menu == "mode":
        result = mode_menu.handle_events(mouse_pos, current_mouse_state, mouse_just_released)
        if result == "back":
            current_menu = "main"
            print("Returning to main menu...")
        elif result in RACE_MODES:
            selected_mode = result
            print(f"Selected mode: {selected_mode}")
    elif current_menu == "level":
        result = level_menu.handle_events(mouse_pos, current_mouse_state, mouse_just_released)
        if result == "back":
            current_menu = "main"
            print("Returning to main menu...")
        elif result in ["Easy", "Mid", "Hard"]:
            selected_level = result
            print(f"Selected level: {selected_level}")
    
    # Cập nhật và vẽ menu hiện tại
    if current_menu == "main":
        main_menu.update_animation()
        main_menu.draw()
    elif current_menu == "mode":
        mode_menu.update_animation()
        mode_menu.draw()
    elif current_menu == "level":
        level_menu.update_animation()
        level_menu.draw()
    
    # Cập nhật màn hình
    pygame.display.flip()
    
    # Kiểm soát FPS
    clock.tick(FPS)

# Thoát Pygame
pygame.quit()
sys.exit()