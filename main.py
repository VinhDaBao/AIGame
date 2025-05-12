import random
import numpy as np

def create_dense_maze(rows, cols, extra_paths_ratio=0.5):
    """Tạo mê cung với nhiều đường đi tới đích bằng cách loại bỏ nhiều tường hơn."""
    # Khởi tạo mê cung toàn tường (1)
    maze = np.ones((rows, cols), dtype=int)

    # Chọn một ô ngẫu nhiên làm điểm bắt đầu
    start_x, start_y = random.randrange(1, rows, 2), random.randrange(1, cols, 2)
    maze[start_x, start_y] = 0  # Đánh dấu là đường đi

    # Danh sách biên (các tường có thể bị phá vỡ)
    frontier = [(start_x + dx, start_y + dy, start_x, start_y)
                for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]
                if 1 <= start_x + dx < rows and 1 <= start_y + dy < cols]

    while frontier:
        # Chọn ngẫu nhiên một ô biên
        fx, fy, px, py = random.choice(frontier)
        frontier.remove((fx, fy, px, py))

        # Nếu ô này vẫn là tường, biến nó thành đường
        if maze[fx, fy] == 1:
            maze[fx, fy] = 0
            maze[(fx + px) // 2, (fy + py) // 2] = 0  # Phá tường ở giữa

            # Thêm các ô lân cận vào danh sách biên
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = fx + dx, fy + dy
                if 1 <= nx < rows and 1 <= ny < cols and maze[nx, ny] == 1:
                    frontier.append((nx, ny, fx, fy))

    # Đảm bảo có một lối ra ở góc dưới bên phải
    maze[rows - 2, cols - 2] = 0

    # Loại bỏ thêm nhiều tường để tạo nhiều đường đi hơn
    num_extra_paths = int(extra_paths_ratio * (rows * cols))
    for _ in range(num_extra_paths):
        x, y = random.randrange(1, rows - 1, 2), random.randrange(1, cols - 1, 2)
        maze[x, y] = 0  # Phá tường để tạo nhiều lối đi hơn

    return maze

# Kích thước mê cung
rows, cols = 21, 21
maze = create_dense_maze(rows, cols, extra_paths_ratio=0.6)  # Tạo nhiều đường hơn

# In mê cung
for row in maze:
    print("".join("█" if cell == 1 else " " for cell in row))
