import heapq

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Các hướng di chuyển (lên, xuống, trái, phải)

class Al_solution():
    def __init__(self, start, end, maze):
        self.START = start
        self.END = end
        self.HEIGHT = len(maze)
        self.WIDTH = len(maze[0])
        self.MAZE = maze

    def ucs(self):
        priority_queue = [(0, self.START, [])]  # (cost, (x, y), path)
        visited = set()

        while priority_queue:
            cost, (x, y), path = heapq.heappop(priority_queue)

            if (x, y) in visited:
                continue

            visited.add((x, y))
            new_path = path + [(x, y)]

            if (x, y) == self.END:
                return new_path

            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and (self.MAZE[ny][nx] == 1 or self.MAZE[ny][nx] == 2):
                    heapq.heappush(priority_queue, (cost + 1, (nx, ny), new_path))

        return []

    def heuristic(self, current, end):
        # Hàm heuristic tính khoảng cách Manhattan từ current đến end
        return abs(current[0] - end[0]) + abs(current[1] - end[1])

    def a_star(self):
        priority_queue = [(0 + self.heuristic(self.START, self.END), 0, self.START, [])]  # (f(n), g(n), (x, y), path)
        visited = set()

        while priority_queue:
            f, g, (x, y), path = heapq.heappop(priority_queue)

            if (x, y) in visited:
                continue

            visited.add((x, y))
            new_path = path + [(x, y)]

            if (x, y) == self.END:
                return new_path

            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and (self.MAZE[ny][nx] == 1 or self.MAZE[ny][nx] == 2):
                    f_new = g + 1 + self.heuristic((nx, ny), self.END)  # f(n) = g(n) + h(n)
                    heapq.heappush(priority_queue, (f_new, g + 1, (nx, ny), new_path))

        return []

# Mê cung mới
maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2, 0],
    [0, 2, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0],
    [0, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 2, 1, 2, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 2, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 2, 0, 2, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 2, 0, 2, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 2, 1, 1, 2, 1, 0, 2, 1, 2, 1, 2, 0, 2, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

start = (0, 1)  # Điểm bắt đầu
end = (20, 9)    # Điểm kết thúc

# Khởi tạo đối tượng và chạy thử
solver = Al_solution(start, end, maze)

# Chạy UCS
ucs_path = solver.ucs()
print("Đường đi UCS:", ucs_path)
print("Độ dài đường đi UCS:", len(ucs_path))

# Chạy A*
astar_path = solver.a_star()
print("Đường đi A*:", astar_path)
print("Độ dài đường đi A*:", len(astar_path))

# In mê cung với đường đi
def print_maze_with_path(maze, path, title):
    maze_copy = [row[:] for row in maze]
    for x, y in path:
        if (x, y) != start and (x, y) != end:
            maze_copy[y][x] = '*'
    maze_copy[start[1]][start[0]] = 'S'
    maze_copy[end[1]][end[0]] = 'E'
    print(f"\n{title}:")
    for row in maze_copy:
        print(' '.join(str(cell) for cell in row))

print_maze_with_path(maze, ucs_path, "Mê cung với đường đi UCS")
print_maze_with_path(maze, astar_path, "Mê cung với đường đi A*")