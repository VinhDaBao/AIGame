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
                if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and self.MAZE[ny][nx] == 0:
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
                if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and self.MAZE[ny][nx] == 0 or self.MAZE[ny][nx] == 2:
                    f_new = g + 1 + self.heuristic((nx, ny), self.END)  # f(n) = g(n) + h(n)
                    heapq.heappush(priority_queue, (f_new, g + 1, (nx, ny), new_path))

        return []
