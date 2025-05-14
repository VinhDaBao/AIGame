import pygame
import time
from collections import deque
from algorithm import Al_solution  # Giả sử bạn đã cài đặt thuật toán A*

pygame.init()

CELL_SIZE = 40
WIDTH, HEIGHT = 7, 5
screen_width = WIDTH * CELL_SIZE
screen_height = HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Race: Bot")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# MAZE với ô giá trị 2 để bot đi chậm hơn
MAZE = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 2, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

START_POS = (1, 3)
END_POS = (5, 1)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Giả sử thuật toán A* bạn đã import từ Al_solution
Al = Al_solution(START_POS, END_POS, MAZE)
bot_path = Al.a_star()  # Thuật toán A* trả về một danh sách các bước của bot
print(bot_path)
bot_pos = list(START_POS)
bot_step = 0

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

# Kiểm tra tốc độ của bot tại vị trí
def get_speed_at_position(x, y):
    if MAZE[y][x] == 2:  # Nếu bot vào ô có giá trị 2 (ô đi chậm)
        return slow_speed
    return normal_speed

def bot_game():
    global bot_pos, bot_step
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(BLACK)
        draw_maze()

        # Nếu bot đã đi hết đường đi
        if bot_step < len(bot_path):
            bot_pos = list(bot_path[bot_step])
            print(bot_pos)
            bot_step += 1

        # Vẽ bot
        pygame.draw.rect(screen, GREEN, (bot_pos[0] * CELL_SIZE, bot_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Điều chỉnh tốc độ di chuyển của bot
        speed = get_speed_at_position(bot_pos[0], bot_pos[1])
        pygame.display.flip()
        clock.tick(speed)  # Điều chỉnh tốc độ di chuyển

        # Dừng trò chơi khi bot đã đi hết đường
        if bot_step >= len(bot_path):
            running = False
        #     time.sleep(3)

    pygame.quit()

if __name__ == "__main__":
    bot_game()
