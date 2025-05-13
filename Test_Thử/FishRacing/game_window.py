import pygame
from settings import *
from maze import MazeGenerator
import os
images = os.path.join(ASSETS_PATH,"images")
class GameWindow:
    def __init__(self, level="Easy",mode ="PVP"):
        # Kích thước cửa sổ game lớn hơn menu
        self.width = WIDTH * 2  # Gấp đôi chiều rộng menu
        self.height = HEIGHT * 1.5  # Tăng chiều cao lên 1.5 lần
        self.mode = mode
        # Lưu level hiện tại
        self.level = level
        
        # Màu sắc
        self.BLACK = (0, 0, 0)
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
        
        # Tạo mê cung
        self.init_maze()
        
    def get_level_settings(self):
        """Trả về các thiết lập dựa trên level."""
        if self.level == "Easy":
            return {
                "cell_size": 25,  # Ô lớn hơn, dễ di chuyển
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
    def draw_players(self):
        pass
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Nhấn R để tạo mê cung mới
                        self.init_maze()
            
            # Xóa màn hình
            self.screen.fill(self.BLACK)
            
            # Vẽ 2 khung và mê cung
            self.draw_frames()
            
            # Cập nhật màn hình
            pygame.display.flip()
            clock.tick(FPS) 