import pygame
import random
import sys
from collections import deque

# Xử lý lỗi Pygame không khởi tạo được

pygame.init()


# Kích thước cửa sổ trò chơi
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Tạo cửa sổ trò chơi
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mê cung Python")
    clock = pygame.time.Clock()
except pygame.error as e:
    print(f"Lỗi tạo màn hình: {e}")
    pygame.quit()
    sys.exit(1)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False
        self.is_obstacle = False
        self.is_start = False
        self.is_end = False

    def draw(self, screen):
        try:
            x, y = self.x * CELL_SIZE, self.y * CELL_SIZE
            
            if self.is_start:
                pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
            elif self.is_end:
                pygame.draw.rect(screen, RED, (x, y, CELL_SIZE, CELL_SIZE))
            elif self.is_obstacle:
                pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
            
            if self.walls["top"]:
                pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)
            if self.walls["right"]:
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
            if self.walls["bottom"]:
                pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
            if self.walls["left"]:
                pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), 2)
        except pygame.error as e:
            print(f"Lỗi vẽ ô: {e}")

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.move_cooldown = 0
    
    def draw(self, screen):
        try:
            x_center = self.x * CELL_SIZE + CELL_SIZE // 2
            y_center = self.y * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, YELLOW, (x_center, y_center), CELL_SIZE // 3)
        except pygame.error as e:
            print(f"Lỗi vẽ người chơi: {e}")
    
    def move(self, direction, grid):
        if self.move_cooldown > 0:
            return
        
        new_x, new_y = self.x, self.y
        
        if direction == "up" and not grid[self.y][self.x].walls["top"]:
            new_y -= 1
        elif direction == "right" and not grid[self.y][self.x].walls["right"]:
            new_x += 1
        elif direction == "down" and not grid[self.y][self.x].walls["bottom"]:
            new_y += 1
        elif direction == "left" and not grid[self.y][self.x].walls["left"]:
            new_x -= 1
        
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            if not grid[new_y][new_x].is_obstacle:
                self.x, self.y = new_x, new_y
                self.move_cooldown = 5

def remove_wall(current, next_cell, direction):
    opposite_walls = {"top": "bottom", "right": "left", "bottom": "top", "left": "right"}
    current.walls[direction] = False
    next_cell.walls[opposite_walls[direction]] = False

def generate_maze(grid):
    # Khởi tạo mảng 2D với đối tượng Cell
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            grid[y][x] = Cell(x, y)
    
    # Tạo mê cung bằng thuật toán DFS
    start_x, start_y = 0, 0
    stack = [(start_x, start_y)]
    grid[start_y][start_x].visited = True
    
    while stack:
        x, y = stack[-1]
        current = grid[y][x]
        
        # Tìm các ô kề chưa thăm
        neighbors = []
        
        # Kiểm tra 4 hướng
        if y > 0 and not grid[y-1][x].visited:
            neighbors.append(("top", grid[y-1][x]))
        if x < GRID_WIDTH - 1 and not grid[y][x+1].visited:
            neighbors.append(("right", grid[y][x+1]))
        if y < GRID_HEIGHT - 1 and not grid[y+1][x].visited:
            neighbors.append(("bottom", grid[y+1][x]))
        if x > 0 and not grid[y][x-1].visited:
            neighbors.append(("left", grid[y][x-1]))
        
        if neighbors:
            # Chọn một ô kề ngẫu nhiên
            direction, next_cell = random.choice(neighbors)
            # Phá tường giữa hai ô
            remove_wall(current, next_cell, direction)
            # Đánh dấu ô kề đã thăm
            next_cell.visited = True
            stack.append((next_cell.x, next_cell.y))
        else:
            # Quay lui nếu không có ô kề chưa thăm
            stack.pop()
    
    # Tạo thêm đường đi bằng cách phá ngẫu nhiên thêm tường
    # Đặt lại trạng thái thăm
    for row in grid:
        for cell in row:
            cell.visited = False
    
    # Phá thêm nhiều tường để tạo nhiều đường đi
    num_walls_to_remove = (GRID_WIDTH * GRID_HEIGHT) // 4  # 25% số tường
    
    for _ in range(num_walls_to_remove):
        # Chọn một ô ngẫu nhiên
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        cell = grid[y][x]
        
        # Chọn một hướng ngẫu nhiên để phá tường
        walls = []
        
        if y > 0 and cell.walls["top"]:  # Tường phía trên
            walls.append(("top", grid[y-1][x]))
        if x < GRID_WIDTH - 1 and cell.walls["right"]:  # Tường phía phải
            walls.append(("right", grid[y][x+1]))
        if y < GRID_HEIGHT - 1 and cell.walls["bottom"]:  # Tường phía dưới
            walls.append(("bottom", grid[y+1][x]))
        if x > 0 and cell.walls["left"]:  # Tường phía trái
            walls.append(("left", grid[y][x-1]))
        
        if walls:
            direction, neighbor = random.choice(walls)
            remove_wall(cell, neighbor, direction)

def add_obstacles_and_points(grid):
    # Đặt điểm bắt đầu và kết thúc
    start_x, start_y = 0, 0
    end_x, end_y = GRID_WIDTH - 1, GRID_HEIGHT - 1
    
    grid[start_y][start_x].is_start = True
    grid[end_y][end_x].is_end = True
    
    # Thêm chướng ngại vật ngẫu nhiên
    obstacles_count = (GRID_WIDTH * GRID_HEIGHT) // 20  # Khoảng 5% số ô
    
    # Hàm kiểm tra có đường đi từ điểm bắt đầu đến điểm kết thúc
    def has_path():
        visited = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        queue = deque([(start_x, start_y)])
        visited[start_y][start_x] = True
        
        while queue:
            x, y = queue.popleft()
            if x == end_x and y == end_y:
                return True
            
            # Kiểm tra 4 hướng
            if y > 0 and not grid[y][x].walls["top"] and not visited[y-1][x] and not grid[y-1][x].is_obstacle:
                visited[y-1][x] = True
                queue.append((x, y-1))
            if x < GRID_WIDTH - 1 and not grid[y][x].walls["right"] and not visited[y][x+1] and not grid[y][x+1].is_obstacle:
                visited[y][x+1] = True
                queue.append((x+1, y))
            if y < GRID_HEIGHT - 1 and not grid[y][x].walls["bottom"] and not visited[y+1][x] and not grid[y+1][x].is_obstacle:
                visited[y+1][x] = True
                queue.append((x, y+1))
            if x > 0 and not grid[y][x].walls["left"] and not visited[y][x-1] and not grid[y][x-1].is_obstacle:
                visited[y][x-1] = True
                queue.append((x-1, y))
        
        return False
    
    # Đặt chướng ngại vật
    for _ in range(obstacles_count):
        attempts = 0
        while attempts < 50:  # Giới hạn số lần thử
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            if not grid[y][x].is_start and not grid[y][x].is_end and not grid[y][x].is_obstacle:
                # Thử đặt chướng ngại vật
                grid[y][x].is_obstacle = True
                
                # Kiểm tra nếu vẫn có đường đi
                if has_path():
                    break
                else:
                    grid[y][x].is_obstacle = False  # Bỏ chướng ngại vật nếu không có đường đi
            
            attempts += 1

def main():
    try:
        # Tạo lưới mê cung
        grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Tạo mê cung
        generate_maze(grid)
        
        # Thêm chướng ngại vật và điểm đầu/cuối
        add_obstacles_and_points(grid)
        
        # Khởi tạo người chơi
        player = Player(0, 0)
        
        # Vòng lặp trò chơi
        running = True
        won = False
        
        print("Mê cung đã được tạo thành công!")
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if not won:
                        if event.key == pygame.K_UP:
                            player.move("up", grid)
                        elif event.key == pygame.K_RIGHT:
                            player.move("right", grid)
                        elif event.key == pygame.K_DOWN:
                            player.move("down", grid)
                        elif event.key == pygame.K_LEFT:
                            player.move("left", grid)
                    
                    if event.key == pygame.K_r:
                        # Tạo mê cung mới
                        print("Đang tạo mê cung mới...")
                        grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                        generate_maze(grid)
                        add_obstacles_and_points(grid)
                        player = Player(0, 0)
                        won = False
                        print("Mê cung mới đã được tạo!")
                    
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Giảm thời gian chờ di chuyển
            if player.move_cooldown > 0:
                player.move_cooldown -= 1
            
            # Kiểm tra chiến thắng
            if grid[player.y][player.x].is_end:
                won = True
            
            # Vẽ màn hình
            screen.fill(WHITE)
            
            # Vẽ mê cung
            for row in grid:
                for cell in row:
                    cell.draw(screen)
            
            # Vẽ người chơi
            player.draw(screen)
            
            # Hiển thị hướng dẫn
            try:
                font = pygame.font.SysFont("Arial", 24)
                help_text = font.render("Dùng phím mũi tên để di chuyển, R để tạo mê cung mới", True, BLACK)
                screen.blit(help_text, (10, 10))
            except pygame.error as e:
                print(f"Lỗi vẽ text: {e}")
            
            # Hiển thị thông báo chiến thắng
            if won:
                try:
                    font = pygame.font.SysFont("Arial", 48)
                    win_text = font.render("Chiến thắng! Nhấn R để chơi lại", True, BLACK)
                    text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    screen.blit(win_text, text_rect)
                except pygame.error as e:
                    print(f"Lỗi vẽ thông báo chiến thắng: {e}")
            
            # Cập nhật màn hình
            pygame.display.flip()
            clock.tick(60)
    
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()