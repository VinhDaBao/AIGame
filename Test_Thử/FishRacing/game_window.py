import pygame
from settings import *
from maze import MazeGenerator
import os
from concurrent.futures import ThreadPoolExecutor
import algorithm
import utils # Thêm import utils
images = os.path.join(ASSETS_PATH,"images")
font_path = os.path.join("assets", "fonts", "PressStart2P-Regular.ttf")
cooldowns = 200
executor = ThreadPoolExecutor(max_workers=1)
aldelay = 100

# Fish animation constants
FISH_FRAME_WIDTH = 64
FISH_FRAME_HEIGHT = 64
FISH_NUM_FRAMES = 7
FISH_ANIM_DELAY = 5 # Adjust for animation speed (frames per game tick)

class GameWindow:
    def __init__(self, level="Easy",mode ="Player vs Player",algo_left = "UCS", algo_right= "UCS"):
        # Kích thước cửa sổ game lớn hơn menu
        self.width = WIDTH * 2  # Gấp đôi chiều rộng menu
        self.height = HEIGHT * 1.5  # Tăng chiều cao lên 1.5 lần
        #Lưu chế độ chơi
        self.mode = mode
        print(algo_left,algo_right)
        # Tạo trạng thái tham 
        self.player1 = False
        self.player2 = False
        self.com1 = False
        self.path1 = None
        self.solver1  = None
        self.com2 = False
        self.path2 = None
        self.solver2= None

        # Lưu level hiện tại
        self.level = level
        # Lưu vị trí ban đầu 2 người chơi
        self.player_1_pos = [0,1]
        self.delay1time = 0
        self.player_2_pos = [0,1]
        self.delay2time = 0
        # Lưu vị trí com
        self.com_1_pos = [0,1]
        self.com_1_index =0
        self.com1_slow = 0
        self.com_2_pos = [0,1]
        self.com_2_index = 0
        self.com2_slow = 0
        # Vị trí thắng
        self.goal_pos = None
        # Màu sắc
        self.BLACK = (0, 0, 0)
        self.BLUE = (0,0,255)
        self.RED = (255,0,0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        
        # Kích thước mỗi khung
        self.frame_width = self.width // 2
        self.frame_height = self.height
        
        # Tạo cửa sổ game
        self.screen = pygame.display.set_mode((int(self.width), int(self.height)))
        pygame.display.set_caption(f"Fish Racing - {level} Level")
        
        # Load tất cả ảnh
        self.background_img = utils.load_image("background.png") # Sử dụng utils.load_image
        self.wall_img = utils.load_image("rock_wall.png")       # Sử dụng utils.load_image
        self.obstacle_img = utils.load_image("dirty_water.png") # Sử dụng utils.load_image

        # Load sprite sheets cá
        self.fish_left_spritesheet = utils.load_image("fish_sprite1.png")
        self.fish_right_spritesheet = utils.load_image("fish_sprite_2.png")
        
        # Lists to hold animation frames for each fish
        self.fish_left_frames = []
        self.fish_right_frames = []

        # Animation state variables
        self.fish_left_anim_idx = 0
        self.fish_right_anim_idx = 0
        self.fish_anim_timer = 0

        # Fish orientation state (True if facing right, False if facing left)
        self.player_1_facing_right = True
        self.player_2_facing_right = True
        self.com_1_facing_right = True
        self.com_2_facing_right = True
        
        self.game_run = True
        self.end_game_time =  None

        # Tạo mê cung
        self.init_maze()
    def get_mode_settings(self):
        AI = algorithm.Al_solution(tuple(self.com_1_pos),tuple(self.goal_pos),self.maze)
        print(AI.ucs())
        if self.mode == "Player vs Player":
            self.player1 = True
            self.player2 = True
        elif self.mode == "Player vs Machine":
            self.player1 = True
            self.com2 = True
            self.solver2 = executor.submit(AI.ucs)
        else:
            self.com1 = True
            self.solver1 = executor.submit(AI.ucs)

            self.com2 = True
            self.solver2 = executor.submit(AI.ucs)
    def _update_animations(self):
        self.fish_anim_timer += 1
        if self.fish_anim_timer >= FISH_ANIM_DELAY:
            self.fish_anim_timer = 0
            if self.fish_left_frames: # Only update if frames exist
                self.fish_left_anim_idx = (self.fish_left_anim_idx + 1) % len(self.fish_left_frames)
            if self.fish_right_frames: # Only update if frames exist
                self.fish_right_anim_idx = (self.fish_right_anim_idx + 1) % len(self.fish_right_frames)

    def get_level_settings(self):
        """Trả về các thiết lập dựa trên level."""
        if self.level == "Easy":
            return {
                "cell_size": 35,  # Ô lớn hơn, dễ di chuyển
                "obstacle_percentage": 5,  # Ít chướng ngại vật
                "extra_paths": 30  # Nhiều đường đi phụ
            }
        elif self.level == "Medium":
            return {
                "cell_size": 20,
                "obstacle_percentage": 15,
                "extra_paths": 20
            }
        else:  # Hard
            return {
                "cell_size": 15,  # Ô nhỏ hơn, khó di chuyển
                "obstacle_percentage": 25,  # Nhiều chướng ngại vật
                "extra_paths": 10  # Ít đường đi phụ
            }
        
    def init_maze(self):
        # Lấy thiết lập theo level
        settings = self.get_level_settings()
        self.cell_size = settings["cell_size"]
        
        # Tính toán kích thước mê cung dựa trên kích thước khung
        maze_width = int((self.frame_width - 40) // self.cell_size)
        maze_height = int((self.frame_height - 40) // self.cell_size)
        
        # Đảm bảo kích thước lẻ
        maze_width = maze_width if maze_width % 2 == 1 else maze_width - 1
        maze_height = maze_height if maze_height % 2 == 1 else maze_height - 1
        
        print(f"Creating {self.level} maze with dimensions: {maze_width}x{maze_height}")
        print(f"Settings: {settings}")
        
        # Tạo mê cung với thiết lập theo level
        self.maze_generator = MazeGenerator(maze_width, maze_height)
        self.maze = self.maze_generator.generate(
            obstacle_percentage=settings["obstacle_percentage"]
        )
        self.goal_pos = [maze_width -1, maze_height -2]

        # Tính toán vị trí bắt đầu để căn giữa mê cung trong mỗi khung
        self.maze_offset_x = int((self.frame_width - maze_width * self.cell_size) // 2)
        self.maze_offset_y = int((self.frame_height - maze_height * self.cell_size) // 2)
        
        # Scale tất cả ảnh to cell size
        if self.background_img:
            try:
                self.scaled_background = pygame.transform.scale(self.background_img, (self.cell_size, self.cell_size))
            except Exception as e:
                print(f"Error scaling background.png: {e}")
                self.scaled_background = None # Fallback
        if self.wall_img:
            try:
                self.scaled_wall = pygame.transform.scale(self.wall_img, (self.cell_size, self.cell_size))
            except Exception as e:
                print(f"Error scaling rock_wall.png: {e}")
                self.scaled_wall = None # Fallback
        if self.obstacle_img:
            try:
                self.scaled_obstacle = pygame.transform.scale(self.obstacle_img, (self.cell_size, self.cell_size))
            except Exception as e:
                print(f"Error scaling dirty_water.png: {e}")
                self.scaled_obstacle = None # Fallback

        # Process fish sprite sheets for animation
        if self.fish_left_spritesheet:
            self.fish_left_frames = [] # Ensure list is empty
            for i in range(FISH_NUM_FRAMES):
                try:
                    frame_x = i * FISH_FRAME_WIDTH
                    original_frame = self.fish_left_spritesheet.subsurface(pygame.Rect(frame_x, 0, FISH_FRAME_WIDTH, FISH_FRAME_HEIGHT))
                    scaled_frame = pygame.transform.scale(original_frame, (self.cell_size, self.cell_size))
                    self.fish_left_frames.append(scaled_frame)
                except Exception as e:
                    print(f"Error processing frame {i} for fish_sprite1.png: {e}")
            if not self.fish_left_frames:
                 print("Warning: No animation frames loaded for left fish.")

        if self.fish_right_spritesheet:
            self.fish_right_frames = [] # Ensure list is empty
            for i in range(FISH_NUM_FRAMES):
                try:
                    frame_x = i * FISH_FRAME_WIDTH
                    original_frame = self.fish_right_spritesheet.subsurface(pygame.Rect(frame_x, 0, FISH_FRAME_WIDTH, FISH_FRAME_HEIGHT))
                    scaled_frame = pygame.transform.scale(original_frame, (self.cell_size, self.cell_size))
                    self.fish_right_frames.append(scaled_frame)
                except Exception as e:
                    print(f"Error processing frame {i} for fish_sprite_2.png: {e}")
            if not self.fish_right_frames:
                print("Warning: No animation frames loaded for right fish.")
    def draw_maze(self, offset_x=0):
        # Vẽ mê cung với offset_x để vẽ ở khung trái hoặc phải
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                cell = self.maze[y][x]
                rect_x = offset_x + self.maze_offset_x + x * self.cell_size
                rect_y = self.maze_offset_y + y * self.cell_size
                
                # Luôn vẽ background trước
                if self.scaled_background: # Kiểm tra nếu ảnh background load được
                    self.screen.blit(self.scaled_background, (rect_x, rect_y))
                else: # Fallback nếu ảnh background lỗi
                    pygame.draw.rect(self.screen, self.WHITE, (rect_x, rect_y, self.cell_size, self.cell_size))

                if cell == 0:  # Tường - sử dụng rock_wall image
                    if self.scaled_wall:
                        self.screen.blit(self.scaled_wall, (rect_x, rect_y))
                    # Không có fallback cho tường, vì nếu tường lỗi thì nền trắng sẽ hiện ra
                elif cell == 2:  # Chướng ngại vật - sử dụng dirty_water image
                    if self.scaled_obstacle:
                        self.screen.blit(self.scaled_obstacle, (rect_x, rect_y))
                    # Fallback cho chướng ngại vật có thể là một màu khác nếu muốn
                # Ô cell == 1 (đường đi) đã được xử lý bằng cách vẽ background ở trên
    
    def draw_frames(self):
        # Vẽ khung bên trái
        pygame.draw.rect(self.screen, self.WHITE, 
                        (0, 0, self.frame_width - 2, self.height))
        
        # Vẽ khung bên phải
        pygame.draw.rect(self.screen, self.WHITE,
                        (self.frame_width + 2, 0, self.frame_width - 2, self.height))
        
        # Vẽ đường phân cách ở giữa
        pygame.draw.rect(self.screen, self.GRAY,
                        (self.frame_width - 2, 0, 4, self.height))
        
        # Vẽ mê cung trong khung trái
        self.draw_maze(0)
        
        # Vẽ mê cung trong khung phải
        self.draw_maze(self.frame_width)
    def draw_players(self,offset_x=0,isplayer = True):
        if offset_x == 0 and isplayer:
            x,y = self.player_1_pos
            color_player = self.BLUE
        elif offset_x !=  0  and isplayer:
            x,y = self.player_2_pos
            color_player = self.RED
        elif offset_x == 0 and not isplayer:
            x,y = self.com_1_pos
            color_player = self.BLACK
        elif offset_x != 0 and not isplayer:
            x,y = self.com_2_pos
            # color_player = self.RED # Sẽ được xử lý bởi logic chọn ảnh/fallback bên dưới
            # print(x,y) # Loại bỏ dòng debug
        
        location_x = x * self.cell_size + self.maze_offset_x + offset_x
        location_y = y * self.cell_size + self.maze_offset_y

        current_fish_image = None
        fallback_color = self.BLACK
        facing_right_state = True # Default, assuming sprite faces right

        if offset_x == 0: # Khung bên trái
            if isplayer: # Player 1
                if self.fish_left_frames:
                    current_fish_image = self.fish_left_frames[self.fish_left_anim_idx]
                fallback_color = self.BLUE
                facing_right_state = self.player_1_facing_right
            else: # COM 1
                if self.fish_left_frames:
                    current_fish_image = self.fish_left_frames[self.fish_left_anim_idx]
                fallback_color = self.BLACK
                facing_right_state = self.com_1_facing_right
        else: # Khung bên phải
            if isplayer: # Player 2
                if self.fish_right_frames:
                    current_fish_image = self.fish_right_frames[self.fish_right_anim_idx]
                fallback_color = self.RED
                facing_right_state = self.player_2_facing_right
            else: # COM 2
                if self.fish_right_frames:
                    current_fish_image = self.fish_right_frames[self.fish_right_anim_idx]
                fallback_color = self.RED
                facing_right_state = self.com_2_facing_right

        image_to_draw = current_fish_image
        if current_fish_image:
            if not facing_right_state: # If should be facing left (and original sprite faces right)
                image_to_draw = pygame.transform.flip(current_fish_image, True, False)
            self.screen.blit(image_to_draw, (location_x, location_y))
        else:
            pygame.draw.rect(self.screen, fallback_color, (location_x, location_y, self.cell_size, self.cell_size))
    
    def move(self,dx, dy,player):
        new_x = player[0] + dx
        new_y = player[1] + dy
        if 0 <=new_x and new_x < len(self.maze[0]) and 0 <= new_y and new_y <= len(self.maze):
            if self.maze[new_y][new_x] != 0:  
                player[0], player[1] = new_x, new_y
                
    def show_win_message(self, message):
        if self.end_game_time == None:
            self.end_game_time =  pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.end_game_time >= 1000:
            self.game_run = False
        
        font = pygame.font.SysFont(font_path, 60)  
        text = font.render(message, True, (255, 215, 0))  # vàng
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
   
    def run(self):
        self.get_mode_settings()
        clock = pygame.time.Clock()
        running = True
        
        while running:
            now = pygame.time.get_ticks()
            #Đặt thuật toán lấy đường đi ở luồng khác tránh ngừng chương trình

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Nhấn R để tạo mê cung mới
                        self.init_maze()
                        self.get_mode_settings()
                        self.player_1_pos = [0,1]
                        self.player_2_pos = [0,1]
                        self.com_1_pos = [0,1]
                        self.com_2_pos = [0,1]

                    
            
            # Xóa màn hình
            self.screen.fill(self.BLACK)
            
            # Vẽ 2 khung và mê cung 
            self.draw_frames()
            self._update_animations() # Update fish animations
            if self.player1 == True:
                self.draw_players()
            if self.player2 == True:
                self.draw_players(offset_x=self.frame_width)
            if now >= self.com1_slow:
                if self.com1 == True:
                    if self.solver1 is not None and self.solver1.done():
                        self.path1 = self.solver1.result()
                        self.solver1 = None
                    if self.path1 is not None and self.com_1_index < len(self.path1):
                        old_x_com1 = self.com_1_pos[0]
                        self.com_1_pos = list(self.path1[self.com_1_index])
                        new_x_com1 = self.com_1_pos[0]
                        if new_x_com1 < old_x_com1:
                            self.com_1_facing_right = False
                        elif new_x_com1 > old_x_com1:
                            self.com_1_facing_right = True
                        self.com1_slow = now + aldelay
                        if self.com_1_index < len(self.path1)-1:
                            self.com_1_index+=1
            if now >= self.com2_slow:
                if self.com2 == True:
                    if self.solver2 is not None and self.solver2.done():
                        self.path2 = self.solver2.result()
                        print(self.path2)
                        self.solver2 = None
                    if self.path2 is not None and self.com_2_index < len(self.path2):
                        old_x_com2 = self.com_2_pos[0]
                        self.com_2_pos = list(self.path2[self.com_2_index])
                        new_x_com2 = self.com_2_pos[0]
                        if new_x_com2 < old_x_com2:
                            self.com_2_facing_right = False
                        elif new_x_com2 > old_x_com2:
                            self.com_2_facing_right = True
                        self.com2_slow = now + aldelay
                        if self.com_2_index < len(self.path2)-1:
                            self.com_2_index+=1
                                
            if self.com1 == True:                 
                self.draw_players(isplayer=False)
            if self.com2 == True:
                self.draw_players(self.frame_width, isplayer=False) 
            keys = pygame.key.get_pressed()
            if self.player_2_pos != self.goal_pos and self.player_1_pos != self.goal_pos and  self.com_1_pos != self.goal_pos and  self.com_2_pos != self.goal_pos:
                # Player 2 (Arrow keys)
                if now >= self.delay2time:
                    moved2 = False
                    if keys[pygame.K_LEFT]:
                        self.move(-1, 0, self.player_2_pos)
                        self.player_2_facing_right = False # Moved left
                        moved2 = True
                    elif keys[pygame.K_RIGHT]:
                        self.move(1, 0, self.player_2_pos)
                        self.player_2_facing_right = True  # Moved right
                        moved2 = True
                    elif keys[pygame.K_UP]:
                        self.move(0, -1,self.player_2_pos) # Vertical move, no change
                        moved2 = True
                    elif keys[pygame.K_DOWN]:
                        self.move(0, 1,self.player_2_pos)  # Vertical move, no change
                        moved2 = True
                    if (moved2):
                        x,y = self.player_2_pos
                        if self.maze[y][x] == 2:
                            self.delay2time = now + cooldowns
                
                # Player 1 (WASD)
                if now >= self.delay1time:
                    moved1 = False
                    if keys[pygame.K_a]:
                        self.move(-1, 0, self.player_1_pos)
                        self.player_1_facing_right = False # Moved left
                        moved1 = True
                    elif keys[pygame.K_d]:
                        self.move(1, 0, self.player_1_pos)
                        self.player_1_facing_right = True  # Moved right
                        moved1 = True
                    elif keys[pygame.K_w]:
                        self.move(0, -1,self.player_1_pos) # Vertical move, no change in horizontal facing
                        moved1 = True
                    elif keys[pygame.K_s]:
                        self.move(0, 1,self.player_1_pos)  # Vertical move, no change in horizontal facing
                        moved1 = True
                    if (moved1):
                        x,y = self.player_1_pos
                        if self.maze[y][x] == 2:
                            self.delay1time = now + cooldowns
                            print(self.delay1time)



            if self.player_1_pos == self.goal_pos:

                self.show_win_message("Player 1 Win!")

            if self.player_2_pos == self.goal_pos:

                self.show_win_message("Player 2 Win!")
            if self.com_1_pos == self.goal_pos:
                self.show_win_message("Computer 1 Win!")
            if self.com_2_pos == self.goal_pos:
                self.show_win_message("Computer 2 Win!")
            if self.game_run == False:
                running = False
            # Cập nhật màn hình
            pygame.display.flip()
            clock.tick(FPS) 
        return True