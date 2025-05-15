import heapq
import random
import numpy as np
from collections import defaultdict, deque
import maze
from maze import MazeGenerator
import time
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
        manhattan_distance = abs(current[0] - end[0]) + abs(current[1] - end[1])
        return manhattan_distance + 3 if self.MAZE[current[1]][current[0]] == 2 else manhattan_distance

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
        now = time.time()
        running = True
        def or_search(state, path, visited):
            nonlocal running
            intime = time.time()
            if intime - now >5:
                running = False
            if running == False:
                return []
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

    def genetic_algorithm(self, population_size=100, generations=700):
    # Hàm sinh đường đi ngẫu nhiên từ điểm bắt đầu
        def generate_path():
            path = [self.START]
            current = self.START
            visited = {current}
            stuck_count = 0
            
            while current != self.END and len(path) < self.WIDTH * self.HEIGHT * 2 and stuck_count < 20:
                x, y = current
                neighbors = [(x + dx, y + dy) for dx, dy in DIRECTIONS 
                            if 0 <= x + dx < self.WIDTH and 0 <= y + dy < self.HEIGHT 
                            and (self.MAZE[y + dy][x + dx] == 1 or self.MAZE[y + dy][x + dx] == 2)]
                
                # Ưu tiên các ô chưa thăm và gần đích
                unvisited = [n for n in neighbors if n not in visited]
                if unvisited:
                    # Có probability thấp để đi theo hướng tới đích
                    if random.random() < 0.3:
                        # Sắp xếp theo khoảng cách tới đích (ưu tiên gần đích)
                        unvisited.sort(key=lambda n: abs(n[0] - self.END[0]) + abs(n[1] - self.END[1]))
                        current = unvisited[0]
                    else:
                        current = random.choice(unvisited)
                    visited.add(current)
                    path.append(current)
                    stuck_count = 0
                elif neighbors:  # Nếu không có ô chưa thăm nhưng còn đường đi
                    current = random.choice(neighbors)
                    path.append(current)
                    stuck_count += 1
                else:
                    # Không còn đường đi, bị kẹt
                    break
                    
            return path

        # Đánh giá mức độ phù hợp của đường đi
        def fitness(path):
            if not path:
                return 0
                
            # Kiểm tra nếu đến đích
            if path[-1] == self.END:
                # Càng ngắn càng tốt
                return 1000.0 - len(path)
            
            # Nếu chưa đến đích, đánh giá khoảng cách Manhattan đến đích
            distance_to_goal = abs(path[-1][0] - self.END[0]) + abs(path[-1][1] - self.END[1])
            # Khuyến khích đường đi về hướng đích
            return 100.0 / (distance_to_goal + 1)

        # Lai ghép 2 đường đi
        def crossover(parent1, parent2):
            if len(parent1) < 2 or len(parent2) < 2:
                return parent1
                
            # Tìm điểm chung giữa 2 đường đi
            common_points = [point for point in parent1 if point in parent2]
            
            # Nếu không có điểm chung, chọn điểm ngẫu nhiên
            if not common_points:
                cut_point1 = random.randint(1, len(parent1) - 1)
                child = parent1[:cut_point1]
                return complete_path(child)
            
            # Chọn điểm chung làm điểm cắt
            common_point = random.choice(common_points)
            idx1 = parent1.index(common_point)
            idx2 = parent2.index(common_point)
            
            # Tạo con từ phần đầu của parent1 và phần sau của parent2
            child = parent1[:idx1] + parent2[idx2:]
            
            # Loại bỏ các điểm trùng lặp, giữ lại lần xuất hiện đầu tiên
            unique_child = []
            visited = set()
            for point in child:
                if point not in visited:
                    visited.add(point)
                    unique_child.append(point)
                
            return unique_child if unique_child else parent1

        # Hoàn thiện đường đi
        def complete_path(path):
            if not path:
                return generate_path()
                
            current = path[-1]
            visited = set(path)
            
            while current != self.END and len(path) < self.WIDTH * self.HEIGHT * 2:
                x, y = current
                neighbors = [(x + dx, y + dy) for dx, dy in DIRECTIONS 
                            if 0 <= x + dx < self.WIDTH and 0 <= y + dy < self.HEIGHT 
                            and (self.MAZE[y + dy][x + dx] == 1 or self.MAZE[y + dy][x + dx] == 2)]
                
                # Ưu tiên các ô chưa thăm
                unvisited = [n for n in neighbors if n not in visited]
                
                if unvisited:
                    # Có xác suất để ưu tiên hướng tới đích
                    if random.random() < 0.4:
                        unvisited.sort(key=lambda n: abs(n[0] - self.END[0]) + abs(n[1] - self.END[1]))
                        current = unvisited[0]
                    else:
                        current = random.choice(unvisited)
                    visited.add(current)
                    path.append(current)
                elif neighbors:
                    current = random.choice(neighbors)
                    path.append(current)
                else:
                    break
                    
            return path

        # Đột biến
        def mutate(path):
            if len(path) < 3:
                return path
                
            # Chọn đoạn để đột biến
            start_idx = random.randint(1, len(path) - 2)
            end_idx = random.randint(start_idx + 1, len(path) - 1)
            
            # Tạo đường đi mới từ điểm bắt đầu đến điểm đột biến
            new_path = path[:start_idx]
            
            # Tạo đoạn đột biến mới
            current = path[start_idx - 1]
            visited = set(new_path)
            
            # Tìm đường từ điểm đột biến đến cuối đường đi
            while current != path[end_idx] and len(new_path) < len(path) * 2:
                x, y = current
                neighbors = [(x + dx, y + dy) for dx, dy in DIRECTIONS 
                            if 0 <= x + dx < self.WIDTH and 0 <= y + dy < self.HEIGHT 
                            and (self.MAZE[y + dy][x + dx] == 1 or self.MAZE[y + dy][x + dx] == 2)]
                
                unvisited = [n for n in neighbors if n not in visited]
                if unvisited:
                    if random.random() < 0.3:
                        unvisited.sort(key=lambda n: abs(n[0] - path[end_idx][0]) + abs(n[1] - path[end_idx][1]))
                        current = unvisited[0]
                    else:
                        current = random.choice(unvisited)
                    visited.add(current)
                    new_path.append(current)
                elif neighbors:
                    current = random.choice(neighbors)
                    new_path.append(current)
                else:
                    break
            
            # Nếu không thể kết nối đến điểm cuối, trả về đường đi ban đầu
            if new_path[-1] != path[end_idx]:
                return path
                
            # Nối phần cuối của đường đi gốc
            new_path = new_path + path[end_idx:]
            
            return new_path

        # Tạo quần thể ban đầu
        population = []
        for _ in range(population_size):
            path = generate_path()
            if path[-1] == self.END:  # Chỉ chấp nhận đường đi đến đích vào quần thể ban đầu
                population.append(path)
            
        # Nếu không đủ đường đi đến đích, thêm đường đi chưa đến đích
        if len(population) < population_size // 2:
            while len(population) < population_size:
                path = generate_path()
                population.append(path)
        
        best_solution = None
        best_fitness = -1
        
        # Tiến hóa qua các thế hệ
        for gen in range(generations):
            # Tìm giải pháp tốt nhất trong quần thể hiện tại
            current_best = max(population, key=fitness)
            current_best_fitness = fitness(current_best)
            
            if current_best[-1] == self.END and (best_solution is None or current_best_fitness > best_fitness):
                best_solution = current_best
                best_fitness = current_best_fitness
            
            # Sắp xếp quần thể theo độ phù hợp
            population = sorted(population, key=fitness, reverse=True)
            
            # Chọn các cá thể tốt nhất
            elite = population[:population_size // 10]
            new_population = elite.copy()
            
            # Sinh ra quần thể mới
            while len(new_population) < population_size:
                # Chọn cha mẹ bằng tournament selection
                tournament_size = 5
                parents = random.sample(population[:population_size // 2], tournament_size)
                parent1 = max(parents, key=fitness)
                
                parents = random.sample(population[:population_size // 2], tournament_size)
                parent2 = max(parents, key=fitness)
                
                # Lai ghép
                child = crossover(parent1, parent2)
                
                # Đột biến với xác suất
                if random.random() < 0.3:
                    child = mutate(child)
                    
                # Đảm bảo đường đi hoàn chỉnh
                child = complete_path(child)
                
                new_population.append(child)
            
            population = new_population
        
        # Trả về đường đi tốt nhất
        if best_solution and best_solution[-1] == self.END:
            return best_solution
            
        # Nếu không tìm được đường đi đến đích, trả về đường gần đích nhất
        return max(population, key=fitness)

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
                    if next_state == self.END:
                        reward = 100 
                    elif self.MAZE[next_state[1]][next_state[0]]==2:
                        reward = -3
                    else:
                        reward =-1
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
        return path
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
    end = (8, 13)
    maze1 = MazeGenerator(9,15).generate(obstacle_percentage=5)
    # Khởi tạo và chạy thử
    solver = Al_solution(start, end, maze1)

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
    print("Đường đi Q-Learning:", solver.genetic_algorithm())
    print("Độ dài đường đi Q-Learning:", len(solver.genetic_algorithm()))
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

    print_maze_with_path(maze1, solver.ucs(), "Mê cung với đường đi UCS")
    print_maze_with_path(maze1, solver.a_star(), "Mê cung với đường đi A*")
    print_maze_with_path(maze1, solver.backtracking(), "Mê cung với đường đi backtracking")
    print_maze_with_path(maze1, solver.and_or_search(), "Mê cung với đường đi AND-OR Search")
    print_maze_with_path(maze1, solver.q_learning(), "Mê cung với đường đi Q-Learning")
    print_maze_with_path(maze1,solver.genetic_algorithm(),"Gen")
    
