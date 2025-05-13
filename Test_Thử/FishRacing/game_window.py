import pygame
from settings import *
from maze import MazeGenerator
import os
from concurrent.futures import ThreadPoolExecutor

images = os.path.join(ASSETS_PATH,"images")
font_path = os.path.join("assets", "fonts", "PressStart2P-Regular.ttf")
cooldowns = 200
class GameWindow:
    def __init__(self, level="Easy", mode="Player vs Player", algo_left="UCS", algo_right="UCS"):
        # Kích thước cửa sổ game lớn hơn menu
        self.width = WIDTH * 2  # Gấp đôi chiều rộng menu
        self.height = HEIGHT * 1.5  # Tăng chiều cao lên 1.5 lần
        #Lưu chế độ chơi
        self.mode = mode
        #Lưu thuật toán
        self.algo_left = algo_left
        self.algo_right = algo_right
        print(f"GameWindow Init: Level={level}, Mode={mode}, AlgoLeft={self.algo_left}, AlgoRight={self.algo_right}")
        # Tạo trạng thái tham 
        self.player1 = False
        self.player2 = False
        self.com1 = False
        self.path1 = None
        self.com2 = False
        self.path2 = None

        # Lưu level hiện tại
        self.level = level
        # Lưu vị trí ban đầu 2 người chơi
        self.player_1_pos = [0,1]
        self.delay1time = 0
        self.player_2_pos = [0,1]
        self.delay2time = 0
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
        
        self.game_run = True
        self.end_game_time =  None

        # Tạo mê cung
        self.init_maze()
    def get_mode_settings(self):
        if self.algo_left == "Player":
            self.player1 = True
            self.com1 = False
            print("Player 1 (Left) is Human controlled.")
        else:
            self.player1 = False
            self.com1 = True
            print(f"Player 1 (Left) is COM controlled by {self.algo_left}.")

        if self.algo_right == "Player":
            self.player2 = True
            self.com2 = False
            print("Player 2 (Right) is Human controlled.")
        else:
            self.player2 = False
            self.com2 = True
            print(f"Player 2 (Right) is COM controlled by {self.algo_right}.")

        # self.mode có thể vẫn dùng để hiển thị thông tin chung, nhưng không quyết định control type nữa
        # if self.mode == "Player vs Player":
        #     print("OVO")
        #     self.player1 = True
        #     self.player2 = True
        # elif self.mode == "Player vs Machine":
        #     self.player1 = True
        #     self.com1 = True # Đây là lỗi logic cũ, nếu P vs M thì P1 là người, P2 là máy
        # else:
        #     self.com1 = True
        #     self.com2 = True
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
        
        # Đảm bảo kích thước tối thiểu
        maze_width = max(5, maze_width)
        maze_height = max(5, maze_height)
        
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
        self.scaled_background = pygame.transform.scale(self.background_img, (self.cell_size, self.cell_size))
        self.scaled_wall = pygame.transform.scale(self.wall_img, (self.cell_size, self.cell_size))
        self.scaled_obstacle = pygame.transform.scale(self.obstacle_img, (self.cell_size, self.cell_size))
    def draw_maze(self, offset_x=0):
        # Vẽ mê cung với offset_x để vẽ ở khung trái hoặc phải
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                cell = self.maze[y][x]
                rect_x = offset_x + self.maze_offset_x + x * self.cell_size
                rect_y = self.maze_offset_y + y * self.cell_size
                
                if cell == 0:  # Tường - sử dụng rock_wall image
                    self.screen.blit(self.scaled_wall, (rect_x, rect_y))
                elif cell == 1:  # Đường đi - sử dụng background image
                    self.screen.blit(self.scaled_background, (rect_x, rect_y))
                elif cell == 2:  # Chướng ngại vật - sử dụng dirty_water image
                    self.screen.blit(self.scaled_obstacle, (rect_x, rect_y))
    
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
    def draw_players(self,offset_x=0):
        if offset_x == 0:
            x,y = self.player_1_pos
            color_player = self.BLUE
        else:
            x,y = self.player_2_pos
            color_player = self.RED
        location_x = x * self.cell_size + self.maze_offset_x + offset_x
        location_y = y * self.cell_size +self.maze_offset_y
        pygame.draw.rect(self.screen,color_player,(location_x,location_y,self.cell_size,self.cell_size))
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Nhấn R để tạo mê cung mới
                        self.init_maze()
                    
            
            # Xóa màn hình
            self.screen.fill(self.BLACK)
            
            # Vẽ 2 khung và mê cung 
            self.draw_frames()
            if self.player1 == True:
                self.draw_players()
            if self.player2 == True:
                self.draw_players(self.frame_width)
            keys = pygame.key.get_pressed()
            if self.player_2_pos != self.goal_pos and self.player_1_pos != self.goal_pos:
                if now >= self.delay2time:
                    moved2 = False
                    if keys[pygame.K_LEFT]:
                        self.move(-1, 0,self.player_2_pos)
                        moved2 = True

                    elif keys[pygame.K_RIGHT]:
                        self.move(1, 0,self.player_2_pos)
                        moved2 = True

                    elif keys[pygame.K_UP]:
                        self.move(0, -1,self.player_2_pos)
                        moved2 = True

                    elif keys[pygame.K_DOWN]:
                        self.move(0, 1,self.player_2_pos)
                        moved2 = True
                    if (moved2):
                        x,y = self.player_2_pos
                        if self.maze[y][x] == 2:
                            self.delay2time = now + cooldowns

                if now >= self.delay1time:
                    moved1 = False
                
                    if keys[pygame.K_w]:
                        self.move(0, -1,self.player_1_pos)
                        moved1 = True
                    elif keys[pygame.K_s]:
                        self.move(0, 1,self.player_1_pos)
                        moved1 = True

                    elif keys[pygame.K_a]:
                        self.move(-1, 0,self.player_1_pos)
                        moved1 = True
                    elif keys[pygame.K_d]:
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
            
            if self.game_run == False:
                running = False
            # Cập nhật màn hình
            pygame.display.flip()
            clock.tick(FPS) 
        return True