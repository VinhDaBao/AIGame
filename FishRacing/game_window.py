import pygame
from settings import *
from maze import MazeGenerator
import os
from concurrent.futures import ThreadPoolExecutor
import algorithm
import utils # Thêm import utils
import copy
images = os.path.join(ASSETS_PATH,"images")
font_path = os.path.join("assets", "fonts", "PressStart2P-Regular.ttf")
cooldowns = 200
executor = ThreadPoolExecutor(max_workers=1)
aldelay = 100

# Fish animation constants
FISH_FRAME_WIDTH = 64
FISH_FRAME_HEIGHT = 64
FISH_NUM_FRAMES = 7
FISH_ANIM_DELAY = 5 
class GameWindow:
    def __init__(self, level="Easy", mode="Player vs Player", algo_left="UCS", algo_right="UCS", sound_manager=None):
        self.sound_manager = sound_manager
        
        # Switch to gameplay background music
        if self.sound_manager:
            self.sound_manager.stop_background()
            self.sound_manager.play_background("BACKGROUND")
            
        # Kích thước cửa sổ game lớn hơn menu
        self.width = WIDTH * 2  # Gấp đôi chiều rộng menu
        self.height = HEIGHT * 1.5  # Tăng chiều cao lên 1.5 lần
        #Lưu chế độ chơi
        self.mode = mode
        self.test_mode = False
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
        self.com1_algo = algo_left
        self.com_2_pos = [0,1]
        self.com_2_index = 0
        self.com2_slow = 0
        self.com2_algo = algo_right
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
        self.background_img = pygame.image.load(os.path.join(images,"background.png"))
        self.wall_img = pygame.image.load(os.path.join(images, "rock_wall.png"))
        self.obstacle_img = pygame.image.load(os.path.join(images, "dirty_water.png"))
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
        self.player_1_orientation = "up"
        self.player_2_orientation = "up"
        self.com_1_orientation = "up"
        self.com_2_orientation = "up"
        
        self.game_run = True
        self.end_game_time =  None

        # Tạo mê cung
        self.init_maze()


    def get_mode_settings(self):
        AI = algorithm.Al_solution(tuple(self.com_1_pos),tuple(self.goal_pos),self.maze)
        lll =["UCS", "A*", "Backtracking", "AND-OR", "Genetic", "Q-Learning"]         
        if self.mode == "Player vs Player":
            self.player1 = True
            self.player2 = True
        elif self.mode == "Player vs Machine":
            self.player1 = True
            self.com2 = True
            if self.com2_algo == "UCS":
                self.solver2 = executor.submit(AI.ucs)
            elif self.com2_algo == "A*":
                self.solver2 = executor.submit(AI.a_star)
            elif self.com2_algo =="Backtracking":
                self.solver2 = executor.submit(AI.backtracking)
            elif self.com2_algo =="AND-OR":
                self.solver2 = executor.submit(AI.and_or_search)
            elif self.com2_algo =="Genetic":
                self.solver2 = executor.submit(AI.genetic_algorithm)
            else:
                self.solver2 = executor.submit(AI.q_learning)
        else:
            self.com1 = True
            if self.com1_algo == "UCS":
                self.solver1 = executor.submit(AI.ucs)
            elif self.com1_algo == "A*":
                self.solver1 = executor.submit(AI.a_star)
            elif self.com1_algo =="Backtracking":
                self.solver1 = executor.submit(AI.backtracking)
            elif self.com1_algo =="AND-OR":
                self.solver1 = executor.submit(AI.and_or_search)
            elif self.com1_algo =="Genetic":
                self.solver1 = executor.submit(AI.genetic_algorithm)
            else:
                self.solver1 = executor.submit(AI.q_learning)

            self.com2 = True
            if self.com2_algo == "UCS":
                self.solver2 = executor.submit(AI.ucs)
            elif self.com2_algo == "A*":
                self.solver2 = executor.submit(AI.a_star)
            elif self.com2_algo =="Backtracking":
                self.solver2 = executor.submit(AI.backtracking)
            elif self.com2_algo =="AND-OR":
                self.solver2 = executor.submit(AI.and_or_search)
            elif self.com2_algo =="Genetic":
                self.solver2 = executor.submit(AI.genetic_algorithm)
            else:
                self.solver2 = executor.submit(AI.q_learning)
    def _update_animations(self):
        self.fish_anim_timer += 1
        if self.fish_anim_timer >= FISH_ANIM_DELAY:
            self.fish_anim_timer = 0
            if self.fish_left_frames: # Only update if frames exist
                self.fish_left_anim_idx = (self.fish_left_anim_idx + 1) % len(self.fish_left_frames)
            if self.fish_right_frames: # Only update if frames exist
                self.fish_right_anim_idx = (self.fish_right_anim_idx + 1) % len(self.fish_right_frames)

    def update_orientation(self, dx, dy, player_type):
        # Update orientation based on movement direction
        if dx > 0:
            new_orientation = "right"
        elif dx < 0:
            new_orientation = "left"
        elif dy > 0:
            new_orientation = "down"
        elif dy < 0:
            new_orientation = "up"
        else:
            return  # No movement, no orientation change

        # Update the appropriate orientation variable
        if player_type == "player1":
            self.player_1_orientation = new_orientation
        elif player_type == "player2":
            self.player_2_orientation = new_orientation
        elif player_type == "com1":
            self.com_1_orientation = new_orientation
        elif player_type == "com2":
            self.com_2_orientation = new_orientation

    def get_level_settings(self):
        """Trả về các thiết lập dựa trên level."""
        if self.level == "Easy":
            return {
                "cell_size": 35,  # Ô lớn hơn, dễ di chuyển
                "obstacle_percentage": 5,  # Ít chướng ngại vật
                "extra_paths": 30  # Nhiều đường đi phụ
            }
        elif self.level == "Mid":
            return {
                "cell_size": 25,
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
        
        # Đảm bảo kích thước tối thiểu
        maze_width = max(5, maze_width)
        maze_height = max(5, maze_height)
        
        print(f"Creating {self.level} maze with dimensions: {maze_width}x{maze_height}")
        print(f"Settings: {settings}")
        
        # Tạo mê cung với thiết lập theo level
        self.maze_generator = MazeGenerator(maze_width, maze_height,test_mode=self.test_mode)
        self.maze = self.maze_generator.generate(
            obstacle_percentage=settings["obstacle_percentage"]
        )
        self.maze2 = copy.deepcopy(self.maze)
        print(self.maze2)
        self.goal_pos = [maze_width -1, maze_height -2]

        # Tính toán vị trí bắt đầu để căn giữa mê cung trong mỗi khung
        self.maze_offset_x = int((self.frame_width - maze_width * self.cell_size) // 2)
        self.maze_offset_y = int((self.frame_height - maze_height * self.cell_size) // 2)
        
        # Scale tất cả ảnh to cell size
        self.scaled_background = pygame.transform.scale(self.background_img, (self.cell_size, self.cell_size))
        self.scaled_wall = pygame.transform.scale(self.wall_img, (self.cell_size, self.cell_size))
        self.scaled_obstacle = pygame.transform.scale(self.obstacle_img, (self.cell_size, self.cell_size))
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
                cell2 = self.maze2[y][x]
                rect_x = offset_x + self.maze_offset_x + x * self.cell_size
                rect_y = self.maze_offset_y + y * self.cell_size
                
                if cell == 0:  # Tường - sử dụng rock_wall image
                    self.screen.blit(self.scaled_wall, (rect_x, rect_y))
                elif cell == 1:  # Đường đi - sử dụng background image
                    self.screen.blit(self.scaled_background, (rect_x, rect_y))
                elif cell == 2: # Chướng ngại vật - sử dụng dirty_water image
                    self.screen.blit(self.scaled_obstacle, (rect_x, rect_y))
                if cell2 == 3 and self.test_mode == True and offset_x != 0:
                    pygame.draw.rect(self.screen,self.RED,(rect_x,rect_y,self.cell_size,self.cell_size))
    
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
            color_player = self.RED
        location_x = x * self.cell_size + self.maze_offset_x + offset_x
        location_y = y * self.cell_size +self.maze_offset_y
        current_fish_image = None
        fallback_color = self.BLACK
        orientation_state = "right" # Default orientation

        if offset_x == 0: # Khung bên trái (Player 1 or COM 1)
            if self.fish_left_frames:
                current_fish_image = self.fish_left_frames[self.fish_left_anim_idx]
            if isplayer:
                fallback_color = self.BLUE
                orientation_state = self.player_1_orientation
            else:
                fallback_color = self.BLACK
                orientation_state = self.com_1_orientation
        else: # Khung bên phải (Player 2 or COM 2)
            if self.fish_right_frames:
                current_fish_image = self.fish_right_frames[self.fish_right_anim_idx]
            if isplayer:
                fallback_color = self.RED
                orientation_state = self.player_2_orientation
            else:
                fallback_color = self.RED
                orientation_state = self.com_2_orientation

        image_to_draw = current_fish_image
        if current_fish_image:
            if orientation_state == "down": # Original is UP, target is DOWN
                image_to_draw = pygame.transform.rotate(current_fish_image, 180)
            elif orientation_state == "left": # Original is UP, target is LEFT
                image_to_draw = pygame.transform.rotate(current_fish_image, 90) # Rotate 90 deg counter-clockwise
            elif orientation_state == "right": # Original is UP, target is RIGHT
                image_to_draw = pygame.transform.rotate(current_fish_image, -90) # Rotate -90 deg (or 270 deg counter-clockwise)
            # If orientation_state is "up", no transformation needed as it matches the assumed original sprite orientation
            self.screen.blit(image_to_draw, (location_x, location_y))
        else:
            pygame.draw.rect(self.screen, fallback_color, (location_x, location_y, self.cell_size, self.cell_size))
    
    
    def move(self,dx, dy,player):
        new_x = player[0] + dx
        new_y = player[1] + dy
        if 0 <=new_x and new_x < len(self.maze[0]) and 0 <= new_y and new_y <= len(self.maze):
            if self.maze[new_y][new_x] != 0:  
                player[0], player[1] = new_x, new_y
                # Determine which player is moving and update orientation
                if player == self.player_1_pos:
                    self.update_orientation(dx, dy, "player1")
                elif player == self.player_2_pos:
                    self.update_orientation(dx, dy, "player2")
                
    def show_win_message(self, message):
        if self.end_game_time == None:
            self.end_game_time = pygame.time.get_ticks()
            if self.sound_manager:
                self.sound_manager.play_sound("WIN")
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
                    if self.sound_manager:
                        self.sound_manager.stop_background()
                        self.sound_manager.reload_sound_effects()  # Reload sound effects
                        self.sound_manager.play_background("MENU_BACKGROUND")
                    running = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Nhấn R để tạo mê cung mới
                        return True
                        
                    
            
            # Xóa màn hình
            self.screen.fill(self.BLACK)
            
            # Vẽ 2 khung và mê cung 
            self.draw_frames()
            self._update_animations()


            if self.player1 == True:
                self.draw_players()
            if self.player2 == True:
                self.draw_players(offset_x=self.frame_width)
            if self.player_2_pos != self.goal_pos and self.player_1_pos != self.goal_pos and  self.com_1_pos != self.goal_pos and  self.com_2_pos != self.goal_pos:

                if now >= self.com1_slow:
                    if self.com1 == True:
                        if self.solver1 is not None and self.solver1.done():
                            self.path1 = self.solver1.result()
                            self.solver1 = None

                        if self.path1 is not None:
                            next_pos = list( self.path1 [ self.com_1_index ] )
                            #Hướng di chuyển
                            dx = next_pos[0 ] - self.com_1_pos[0 ]
                            dy = next_pos[ 1 ] - self.com_1_pos[1 ]
                            
                            #Cập nhật vị trí và hướng
                            self.com_1_pos = next_pos
                            self.update_orientation(dx, dy, "com1")
                            #self.com_1_pos = list(self.path1[self.com_1_index])  ( cũ )
                            x,y= self.com_1_pos      

                            if self.com_1_index <  len(self.path1) - 1:
                                self.com1_slow = (now + aldelay) + (cooldowns if self.maze[y][x] == 2 else 0)
                                self.maze2[y][x] =3
                                self.com_1_index+=1

                if now >= self.com2_slow:
                    if self.com2 == True:
                        if self.solver2 is not None and self.solver2.done():
                            self.path2 = self.solver2.result()
                            print("done",self.path2)  
                            self.solver2 = None  

                        if self.path2 is not None:
                            next_pos = list(self.path2[self.com_2_index])
                            #Hướng di chuyển 
                            dx = next_pos[0 ] - self.com_2_pos[ 0 ]
                            dy=next_pos[ 1]  - self.com_2_pos[ 1 ]

                            #Cập nhật vị trí và hướng
                            self.com_2_pos = next_pos
                            self.update_orientation(dx, dy, "com2")
                            #self.com_2_pos = list(self.path2[self.com_2_index]) ( cũ )
                            x,y = self.com_2_pos
                            
                            if self.com_2_index < len(self.path2 ) - 1:
                                self.com2_slow = (now + aldelay) +( 200 if self.maze[y][x] == 2 else 0) 
                                self.maze2[y][x] =3
                                print(self.com_2_index)
                                self.com_2_index+=1
                                
            if self.com1 == True:                 
                self.draw_players(isplayer=False)
            if self.com2 == True:
                self.draw_players(self.frame_width, isplayer=False) 
            keys = pygame.key.get_pressed()
            if self.player_2_pos != self.goal_pos and self.player_1_pos != self.goal_pos and  self.com_1_pos != self.goal_pos and  self.com_2_pos != self.goal_pos:
                #Phím người chơi 2
                if now >= self.delay2time:
                    moved2 = False
                    if keys[pygame.K_LEFT]:  #trái
                        self.move(-1, 0,self.player_2_pos)
                        moved2 = True

                    elif keys[pygame.K_RIGHT]: #phải
                        self.move(1, 0,self.player_2_pos)
                        moved2 = True

                    elif keys[pygame.K_UP ]: #lên
                        self.move(0, -1,self.player_2_pos)
                        moved2 = True

                    elif keys[pygame.K_DOWN]:  #xuống
                        self.move(0, 1,self.player_2_pos)
                        moved2 = True

                    if (moved2):
                        x,y = self.player_2_pos
                        if self.maze[y][x] == 2:
                            self.delay2time = now + cooldowns


                #Phím người chơi1
                if now >= self.delay1time:
                    moved1 = False
                    if keys[pygame.K_w]:  #Lên
                        self.move(0, -1,self.player_1_pos)
                        moved1 = True

                    elif keys[pygame.K_s]:  #xuống
                        self.move(0, 1,self.player_1_pos)
                        moved1 = True

                    elif keys[pygame.K_a]:    #trái
                        self.move(-1, 0,self.player_1_pos)
                        moved1 = True

                    elif keys[pygame.K_d]:  #Phải
                        self.move(1, 0,self.player_1_pos)
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
