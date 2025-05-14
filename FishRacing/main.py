#main.py
#File chính của game

import pygame
import sys
from settings import *
from menu import MainMenu, ModeMenu, LevelMenu, AlgorithmMenu
from game_window import GameWindow
from sound_manager import SoundManager
os.environ['SDL_VIDEO_CENTERED'] = '1'
# Khởi tạo Pygame và âm thanh
pygame.init()
pygame.mixer.init()

def init_menu():
    # Thiết lập cửa sổ menu
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fish Racing - Menu")
    return screen

# Thiết lập cửa sổ ban đầu
screen = init_menu()

# Tạo clock để kiểm soát FPS
clock = pygame.time.Clock()

# Khởi tạo sound manager
sound_manager = SoundManager()
sound_manager.play_background()

# Tạo các menu
main_menu = MainMenu(screen, sound_manager)
mode_menu = ModeMenu(screen, sound_manager)
level_menu = LevelMenu(screen, sound_manager)
algorithm_menu = None # Sẽ được khởi tạo động

# Trạng thái game
current_menu = "main"  # "main", "mode", "level" hoặc "algorithm_selection"
selected_mode = "Player vs Player" # Giá trị mặc định
selected_level = "Easy"
selected_algorithm_left = "UCS"  # Thuật toán mặc định cho cá trái
selected_algorithm_right = "UCS" # Thuật toán mặc định cho cá phải

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
            print(f"Play clicked. Current mode: {selected_mode}")
            if selected_mode == "Player vs Player":
                selected_algorithm_left = "Player"
                selected_algorithm_right = "Player"
                print(f"Mode is Player vs Player. Skipping Algorithm Menu. Algorithms set to: Left - {selected_algorithm_left}, Right - {selected_algorithm_right}")
                # Trực tiếp bắt đầu game
                print(f"Starting game with Left: {selected_algorithm_left}, Right: {selected_algorithm_right}, Mode: {selected_mode}, Level: {selected_level}")
                endless = True
                while endless:
                    game_window = GameWindow(level=selected_level, mode=selected_mode, algo_left=selected_algorithm_left, algo_right=selected_algorithm_right, sound_manager=sound_manager)
                    endless = game_window.run()
                screen = init_menu() # Khởi tạo lại màn hình và các menu sau khi game kết thúc
                main_menu = MainMenu(screen, sound_manager)
                mode_menu = ModeMenu(screen, sound_manager)
                level_menu = LevelMenu(screen, sound_manager)
                algorithm_menu = None # Đặt lại algorithm_menu
                current_menu = "main"
            else:
                # Các chế độ khác cần chọn thuật toán
                show_left_select = False
                show_right_select = False
                if selected_mode == "Player vs Machine": # Player (Left) vs Machine (Right)
                    show_left_select = False
                    show_right_select = True
                elif selected_mode == "Machine vs Player": # Machine (Left) vs Player (Right) - Thêm nếu muốn
                    show_left_select = True
                    show_right_select = False
                elif selected_mode == "Machine vs Machine":
                    show_left_select = True
                    show_right_select = True
                
                if show_left_select or show_right_select: # Chỉ hiển thị nếu có ít nhất một bên cần chọn
                    algorithm_menu = AlgorithmMenu(screen, show_left_select=show_left_select, show_right_select=show_right_select)
                    current_menu = "algorithm_selection"
                    print(f"Opening algorithm selection for mode: {selected_mode} (L:{show_left_select}, R:{show_right_select})")
                else: # Trường hợp không rõ ràng hoặc không cần chọn (ví dụ: Player vs Player đã xử lý)
                    print(f"No algorithm selection needed for mode: {selected_mode}. This case should be handled.")
                    # Có thể quay lại main menu hoặc xử lý khác nếu selected_mode không hợp lệ
                    current_menu = "main" 

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
    elif current_menu == "algorithm_selection":
        result = algorithm_menu.handle_events(mouse_pos, current_mouse_state, mouse_just_released)
        if isinstance(result, dict): # Kiểm tra kết quả là dictionary (confirm hoặc back)
            if result.get("action") == "confirm":
                selected_algorithm_left = result.get("left_algo", "UCS")
                selected_algorithm_right = result.get("right_algo", "UCS") # UCS là fallback, nhưng nên là Player nếu không hiển thị
                print(f"Algorithms confirmed: Left - {selected_algorithm_left}, Right - {selected_algorithm_right}")
                
                print(f"Starting game with Left: {selected_algorithm_left}, Right: {selected_algorithm_right}, Mode: {selected_mode}, Level: {selected_level}")
                endless = True
                while endless:
                    game_window = GameWindow(level=selected_level, mode=selected_mode, algo_left=selected_algorithm_left, algo_right=selected_algorithm_right, sound_manager=sound_manager)
                    endless = game_window.run()  # Chạy cửa sổ game
                
                screen = init_menu()
                main_menu = MainMenu(screen, sound_manager)
                mode_menu = ModeMenu(screen, sound_manager)
                level_menu = LevelMenu(screen, sound_manager)
                algorithm_menu = None # Đặt lại algorithm_menu
                current_menu = "main"

            elif result.get("action") == "back":
                current_menu = "main"
                print("Returning to main menu from algorithm selection...")
    
    # Cập nhật và vẽ menu hiện tại
    if current_menu == "main":
        if main_menu: main_menu.update_animation()
        if main_menu: main_menu.draw()
    elif current_menu == "mode":
        if mode_menu: mode_menu.update_animation()
        if mode_menu: mode_menu.draw()
    elif current_menu == "level":
        if level_menu: level_menu.update_animation()
        if level_menu: level_menu.draw()
    elif current_menu == "algorithm_selection":
        if algorithm_menu: # Kiểm tra algorithm_menu tồn tại trước khi dùng
            algorithm_menu.update_animation()
            algorithm_menu.draw()
    
    # Cập nhật màn hình
    pygame.display.flip()
    
    # Kiểm soát FPS
    clock.tick(FPS)

# Thoát Pygame
pygame.quit()
sys.exit()