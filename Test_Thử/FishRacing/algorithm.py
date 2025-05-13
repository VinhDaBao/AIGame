import heapq
import random
import numpy as np
from collections import defaultdict, deque
import maze
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

        return None

    def heuristic(self, current, end):
        # Hàm heuristic tính khoảng cách Manhattan
        return abs(current[0] - end[0]) + abs(current[1] - end[1]) + 3 if self.MAZE[current[1]][current[0]] == 2 else 0 

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
                    f_new = g + 1 + self.heuristic((nx, ny), self.END)
                    heapq.heappush(priority_queue, (f_new, g + 1, (nx, ny), new_path))

        return None

    def backtracking(self):
        """
        Thuật toán backtracking để tìm đường đi trong mê cung
        """
        def dfs(current, path, visited):
            if current == self.END:
                return path + [current]
            
            visited.add(current)
            x, y = current
            
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and 
                    (self.MAZE[ny][nx] == 1 or self.MAZE[ny][nx] == 2) and 
                    (nx, ny) not in visited):
                    result = dfs((nx, ny), path + [current], visited.copy())
                    if result:
                        return result
            
            return None
        
        result = dfs(self.START, [], set())
        return result if result else None


    def and_or_search(self):
        def or_search(state, path, visited):
            if state == self.END:
                return [path + [state]]
            if state in visited:
                return []
            visited.add(state)
            solutions = []
            for dx, dy in DIRECTIONS:
                nx, ny = state[0] + dx, state[1] + dy
                if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and (self.MAZE[ny][nx] == 1 or self.MAZE[ny][nx] == 2):
                    and_solutions = and_search((nx, ny), path + [state], visited.copy())
                    solutions.extend(and_solutions)
            return solutions

        def and_search(state, path, visited):
            return or_search(state, path, visited)

        solutions = or_search(self.START, [], set())
        return solutions[0] if solutions else None

    def genetic_algorithm(self, population_size=50, generations=100):
        def generate_path():
            path = [self.START]
            current = self.START
            while current != self.END and len(path) < self.WIDTH * self.HEIGHT:
                x, y = current
                neighbors = [(x + dx, y + dy) for dx, dy in DIRECTIONS 
                             if 0 <= x + dx < self.WIDTH and 0 <= y + dy < self.HEIGHT 
                             and self.MAZE[y + dy][x + dx] in [1, 2] and (x + dx, y + dy) not in path]
                if not neighbors:
                    break
                current = random.choice(neighbors)
                path.append(current)
            return path

        def fitness(path):
            if path[-1] != self.END:
                return 1 / (self.heuristic(path[-1], self.END) + len(path) + 1)
            return 1 / (len(path) + 1)

        def crossover(parent1, parent2):
            if len(parent1) < 2 or len(parent2) < 2:
                return parent1
            cut = random.randint(1, min(len(parent1), len(parent2)) - 1)
            child = parent1[:cut]
            current = child[-1]
            x, y = current
            while current != self.END and len(child) < self.WIDTH * self.HEIGHT:
                neighbors = [(x + dx, y + dy) for dx, dy in DIRECTIONS 
                             if 0 <= x + dx < self.WIDTH and 0 <= y + dy < self.HEIGHT 
                             and self.MAZE[y + dy][x + dx] in [1, 2] and (x + dx, y + dy) not in child]
                if not neighbors:
                    break
                current = random.choice(neighbors)
                x, y = current
                child.append(current)
            return child

        def mutate(path):
            if len(path) < 2:
                return path
            idx = random.randint(1, len(path) - 1)
            new_path = path[:idx]
            current = new_path[-1]
            x, y = current
            while current != self.END and len(new_path) < self.WIDTH * self.HEIGHT:
                neighbors = [(x + dx, y + dy) for dx, dy in DIRECTIONS 
                             if 0 <= x + dx < self.WIDTH and 0 <= y + dy < self.HEIGHT 
                             and self.MAZE[y + dy][x + dx] in [1, 2] and (x + dx, y + dy) not in new_path]
                if not neighbors:
                    break
                current = random.choice(neighbors)
                x, y = current
                new_path.append(current)
            return new_path

        population = [generate_path() for _ in range(population_size)]
        for _ in range(generations):
            population = sorted(population, key=fitness, reverse=True)
            new_population = population[:10]
            while len(new_population) < population_size:
                parent1, parent2 = random.choices(population[:20], k=2)
                child = crossover(parent1, parent2)
                if random.random() < 0.1:
                    child = mutate(child)
                new_population.append(child)
            population = new_population
        best_path = max(population, key=fitness)
        if best_path[-1] == self.END:
            return best_path
        return None

    def q_learning(self, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
        q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])  # [up, down, left, right]
        actions = list(range(len(DIRECTIONS)))

        def get_action(state):
            if random.random() < epsilon:
                return random.choice(actions)
            return np.argmax(q_table[state])

        for _ in range(episodes):
            state = self.START
            while state != self.END:
                action = get_action(state)
                dx, dy = DIRECTIONS[action]
                nx, ny = state[0] + dx, state[1] + dy
                if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and (self.MAZE[ny][nx] == 1 or self.MAZE[ny][nx] == 2):
                    next_state = (nx, ny)
                    reward = 100 if next_state == self.END else -1
                    q_table[state][action] = (1 - alpha) * q_table[state][action] + alpha * (
                        reward + gamma * max(q_table[next_state])
                    )
                    state = next_state
                else:
                    q_table[state][action] = (1 - alpha) * q_table[state][action] + alpha * (-10)

        # Tìm đường đi từ Q-table
        path = [self.START]
        state = self.START
        while state != self.END and len(path) < self.WIDTH * self.HEIGHT:
            action = np.argmax(q_table[state])
            dx, dy = DIRECTIONS[action]
            nx, ny = state[0] + dx, state[1] + dy
            if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and (self.MAZE[ny][nx] == 1 or self.MAZE[ny][nx] == 2):
                state = (nx, ny)
                path.append(state)
            else:
                break
        if path[-1] == self.END:
            return path
        return None
if __name__ =="__main__":
    # Mê cung
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

    start = (0, 1)
    end = (20, 9)

    # Khởi tạo và chạy thử
    solver = Al_solution(start, end, maze)

    # Chạy các thuật toán
    print("Đường đi UCS:", solver.ucs())
    print("Độ dài đường đi UCS:", len(solver.ucs()))
    print("Đường đi A*:", solver.a_star())
    print("Độ dài đường đi A*:", len(solver.a_star()))
    print("Đường đi backtracking:", solver.backtracking())
    print("Độ dài đường đi backtracking:", len(solver.backtracking()))
    print("Đường đi AND-OR Search:", solver.and_or_search())
    print("Độ dài đường đi AND-OR Search:", len(solver.and_or_search()))
    print("Đường đi Q-Learning:", solver.q_learning())
    print("Độ dài đường đi Q-Learning:", len(solver.q_learning()))

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

    print_maze_with_path(maze, solver.ucs(), "Mê cung với đường đi UCS")
    print_maze_with_path(maze, solver.a_star(), "Mê cung với đường đi A*")
    print_maze_with_path(maze, solver.backtracking(), "Mê cung với đường đi backtracking")
    print_maze_with_path(maze, solver.and_or_search(), "Mê cung với đường đi AND-OR Search")
    print_maze_with_path(maze, solver.q_learning(), "Mê cung với đường đi Q-Learning")