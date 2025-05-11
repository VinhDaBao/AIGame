import pygame
import time

pygame.init()

CELL_SIZE = 40
WIDTH, HEIGHT = 7, 5
screen_width = WIDTH * CELL_SIZE
screen_height = HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Race: Player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

MAZE = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 2, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

START_POS = (1, 1)
player_pos = list(START_POS)

# Tốc độ di chuyển
normal_speed = 10
slow_speed = 5

def draw_maze():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if MAZE[y][x] == 0:
                color = WHITE
            elif MAZE[y][x] == 1:
                color = BLACK
            elif MAZE[y][x] == 2:
                color = (150, 150, 150)  # Màu sắc khác cho ô đi chậm
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def is_valid_move(x, y):
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return False
    if MAZE[y][x] == 1:  # Kiểm tra nếu là tường
        return False
    return True

def get_speed_at_position(x, y):
    if MAZE[y][x] == 2:  # Nếu ô có giá trị 2 (ô đi chậm)
        return slow_speed
    return normal_speed

# Vòng lặp chính
def player_game():
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(BLACK)
        draw_maze()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        speed = get_speed_at_position(player_pos[0], player_pos[1])

        # Di chuyển lên
        if keys[pygame.K_UP]:
            new_pos = (player_pos[0], player_pos[1] - 1)
            if is_valid_move(new_pos[0], new_pos[1]):
                player_pos[1] -= 1
        # Di chuyển xuống
        if keys[pygame.K_DOWN]:
            new_pos = (player_pos[0], player_pos[1] + 1)
            if is_valid_move(new_pos[0], new_pos[1]):
                player_pos[1] += 1
        # Di chuyển sang trái
        if keys[pygame.K_LEFT]:
            new_pos = (player_pos[0] - 1, player_pos[1])
            if is_valid_move(new_pos[0], new_pos[1]):
                player_pos[0] -= 1
        # Di chuyển sang phải
        if keys[pygame.K_RIGHT]:
            new_pos = (player_pos[0] + 1, player_pos[1])
            if is_valid_move(new_pos[0], new_pos[1]):
                player_pos[0] += 1

        pygame.draw.rect(screen, BLUE, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        clock.tick(speed)  # Điều chỉnh tốc độ di chuyển

    pygame.quit()

if __name__ == "__main__":
    player_game()
    print("hello")
    print("hello from remote")
