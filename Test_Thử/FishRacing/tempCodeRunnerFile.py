import pygame
import sys

# Cấu hình
TILE_SIZE = 40
WIDTH, HEIGHT = 600, 400
FPS = 30

# Mê cung: 1 là tường, 0 là đường đi, S là Start, E là End
maze = [
    "1111111111",
    "1S000000E1",
    "1011111101",
    "1000000001",
    "1111111111"
]

# Khởi tạo Pygame
pygame.init()
pygame.key.set_repeat(300, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Tìm vị trí start và end
for y, row in enumerate(maze):
    for x, cell in enumerate(row):
        if cell == 'S':
            player_pos = [x, y]
        elif cell == 'E':
            end_pos = (x, y)

def draw_maze():
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if cell == '1':
                pygame.draw.rect(screen, BLACK, rect)
            elif cell == 'E':
                pygame.draw.rect(screen, RED, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_player():
    x, y = player_pos
    rect = pygame.Rect(x * TILE_SIZE + 5, y * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10)
    pygame.draw.rect(screen, GREEN, rect)

def move(dx, dy):
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if maze[new_y][new_x] != '1':  # Không va vào tường
        player_pos[0], player_pos[1] = new_x, new_y

# Vòng lặp chính
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Di chuyển
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move(-1, 0)
    elif keys[pygame.K_RIGHT]:
        move(1, 0)
    elif keys[pygame.K_UP]:
        move(0, -1)
    elif keys[pygame.K_DOWN]:
        move(0, 1)

    # Kiểm tra thắng
    if tuple(player_pos) == end_pos:
        print("You win!")
        running = False

    # Vẽ màn hình
    screen.fill(WHITE)
    draw_maze()
    draw_player()
    pygame.display.flip()

pygame.quit()
sys.exit()
