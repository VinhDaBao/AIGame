import heapq
import random
import numpy as np
from collections import defaultdict, deque

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
    
    # Thuật toán Genetic
    def genetic_algorithm(self, population_size=100, generations=100, mutation_rate=0.2, max_path_length=None):
        if max_path_length is None:
            # Ước lượng chiều dài đường đi tối đa
            max_path_length = self.HEIGHT * self.WIDTH
        
        def create_individual():
            # Tạo một chuỗi các hướng đi ngẫu nhiên
            return [random.randint(0, 3) for _ in range(random.randint(self.heuristic(self.START, self.END), max_path_length))]
        
        def decode_path(individual):
            # Giải mã chuỗi hướng đi thành một đường đi thực sự
            x, y = self.START
            path = [(x, y)]
            
            for gene in individual:
                dx, dy = DIRECTIONS[gene]
                nx, ny = x + dx, y + dy
                
                # Chỉ di chuyển nếu vị trí mới hợp lệ
                if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and self.MAZE[ny][nx] != 1:
                    x, y = nx, ny
                    path.append((x, y))
                    
                    # Đã tìm thấy đích
                    if (x, y) == self.END:
                        break
            
            return path
        
        def fitness(individual):
            path = decode_path(individual)
            
            # Nếu đường đi không đến được đích
            if path[-1] != self.END:
                # Trả về giá trị fitness dựa trên khoảng cách tới đích
                return -self.heuristic(path[-1], self.END) - len(path) * 0.01
            
            # Nếu đường đi đến được đích, ưu tiên đường đi ngắn nhất
            return 1000 - len(path)
        
        def crossover(parent1, parent2):
            # Lai ghép hai cá thể
            if len(parent1) > 2 and len(parent2) > 2:
                crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
                child1 = parent1[:crossover_point] + parent2[crossover_point:]
                child2 = parent2[:crossover_point] + parent1[crossover_point:]
                return child1, child2
            return parent1, parent2
        
        def mutate(individual):
            # Đột biến một cá thể
            result = individual.copy()
            for i in range(len(result)):
                if random.random() < mutation_rate:
                    result[i] = random.randint(0, 3)
            
            # Thêm hoặc xóa một gene ngẫu nhiên
            if random.random() < mutation_rate and len(result) > 1:
                if random.random() < 0.5:
                    result.append(random.randint(0, 3))
                else:
                    del result[random.randint(0, len(result) - 1)]
            
            return result
        
        # Khởi tạo quần thể
        population = [create_individual() for _ in range(population_size)]
        
        best_individual = None
        best_fitness = float('-inf')
        
        for generation in range(generations):
            # Đánh giá quần thể
            fitness_scores = [(fitness(individual), individual) for individual in population]
            fitness_scores.sort(reverse=True)
            
            # Lưu lại cá thể tốt nhất
            if fitness_scores[0][0] > best_fitness:
                best_fitness = fitness_scores[0][0]
                best_individual = fitness_scores[0][1]
                
                # Nếu đã tìm được đường đi đến đích
                best_path = decode_path(best_individual)
                if best_path[-1] == self.END:
                    if best_fitness > 900:  # Ngưỡng cho đường đi tốt
                        return best_path
            
            # Chọn lọc
            selected = [ind for _, ind in fitness_scores[:population_size // 2]]
            
            # Lai ghép và đột biến
            next_population = selected.copy()
            while len(next_population) < population_size:
                parent1 = random.choice(selected)
                parent2 = random.choice(selected)
                child1, child2 = crossover(parent1, parent2)
                next_population.append(mutate(child1))
                if len(next_population) < population_size:
                    next_population.append(mutate(child2))
            
            population = next_population
        
        # Trả về đường đi tốt nhất tìm được sau khi kết thúc
        return decode_path(best_individual) if best_individual else []
    
    # Thuật toán Partially Observable (POMDP-based exploration)
    def partially_observable(self, visibility_radius=2, max_steps=1000):
        # Khởi tạo bản đồ quan sát được (1 là tường, 0 là đường đi, -1 là chưa khám phá)
        observed_maze = [[-1 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        
        def update_observation(x, y):
            # Cập nhật vùng có thể nhìn thấy từ vị trí hiện tại
            for dy in range(-visibility_radius, visibility_radius + 1):
                for dx in range(-visibility_radius, visibility_radius + 1):
                    # Kiểm tra khoảng cách Manhattan để tạo vùng quan sát hình thoi
                    if abs(dx) + abs(dy) <= visibility_radius:
                        nx, ny = x + dx, y + dy
                        if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH:
                            observed_maze[ny][nx] = self.MAZE[ny][nx]
        
        def get_frontier_cells(visited):
            # Tìm các ô biên (đã thăm và gần với ô chưa thăm)
            frontier = []
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    if (x, y) in visited and observed_maze[y][x] == 0:
                        # Kiểm tra các ô xung quanh
                        for dx, dy in DIRECTIONS:
                            nx, ny = x + dx, y + dy
                            if (0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and 
                                observed_maze[ny][nx] == -1):
                                frontier.append((x, y))
                                break
            return frontier
        
        def partial_path_to(start, target, observed):
            # Tìm đường đi từ start đến target dựa trên bản đồ đã quan sát được
            queue = deque([(start, [start])])
            visited = {start}
            
            while queue:
                (x, y), path = queue.popleft()
                
                if (x, y) == target:
                    return path
                
                for dx, dy in DIRECTIONS:
                    nx, ny = x + dx, y + dy
                    if (0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and 
                        observed[ny][nx] == 0 and (nx, ny) not in visited):
                        queue.append(((nx, ny), path + [(nx, ny)]))
                        visited.add((nx, ny))
            
            return []
        
        x, y = self.START
        visited = {(x, y)}
        full_path = [(x, y)]
        steps = 0
        
        # Khám phá mê cung
        while steps < max_steps:
            # Cập nhật vùng quan sát
            update_observation(x, y)
            
            # Kiểm tra xem có thể nhìn thấy đích chưa
            if observed_maze[self.END[1]][self.END[0]] == 0 or observed_maze[self.END[1]][self.END[0]] == 2:
                # Tìm đường đi đến đích
                end_path = partial_path_to((x, y), self.END, observed_maze)
                if end_path:
                    return full_path[:-1] + end_path
            
            # Tìm các ô biên để khám phá
            frontier = get_frontier_cells(visited)
            
            # Nếu không còn ô biên nào để khám phá
            if not frontier:
                # Tìm các ô chưa khám phá và gần nhất
                min_dist = float('inf')
                next_target = None
                
                for y_idx in range(self.HEIGHT):
                    for x_idx in range(self.WIDTH):
                        if observed_maze[y_idx][x_idx] == -1:
                            # Tìm ô đã thăm gần nhất
                            for vy, vx in visited:
                                dist = abs(vx - x_idx) + abs(vy - y_idx)
                                if dist < min_dist:
                                    min_dist = dist
                                    next_target = (vx, vy)
                
                if next_target is None:
                    # Không còn ô nào để khám phá
                    break
                
                # Di chuyển đến ô gần nhất có thể quan sát thêm
                next_x, next_y = next_target
                if (next_x, next_y) != (x, y):
                    next_path = partial_path_to((x, y), (next_x, next_y), observed_maze)
                    if next_path:
                        full_path = full_path[:-1] + next_path
                        x, y = next_x, next_y
                        visited.add((x, y))
                        steps += len(next_path) - 1
                    else:
                        break
                else:
                    break
            else:
                # Chọn ô biên gần nhất
                target = min(frontier, key=lambda pos: self.heuristic((x, y), pos))
                next_path = partial_path_to((x, y), target, observed_maze)
                
                if next_path:
                    full_path = full_path[:-1] + next_path
                    x, y = target
                    visited.add((x, y))
                    steps += len(next_path) - 1
                else:
                    break
        
        # Nếu không tìm thấy đường đi đến đích
        return []
    
    # Thuật toán Q-learning
    def q_learning(self, episodes=1000, max_steps=1000, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.3):
        # Khởi tạo Q-table
        q_table = defaultdict(lambda: [0, 0, 0, 0])  # [UP, DOWN, LEFT, RIGHT]
        
        # Định nghĩa reward
        def get_reward(x, y):
            if (x, y) == self.END:
                return 100  # Phần thưởng lớn khi đến đích
            elif self.MAZE[y][x] == 1:
                return -100  # Phạt nặng khi đâm vào tường
            else:
                return -1  # Chi phí nhỏ cho mỗi bước đi
        
        best_path = []
        best_steps = float('inf')
        
        for episode in range(episodes):
            # Bắt đầu từ vị trí khởi đầu
            x, y = self.START
            path = [(x, y)]
            
            for step in range(max_steps):
                # Chọn hành động (epsilon-greedy)
                if random.random() < exploration_rate:
                    action = random.randint(0, 3)  # Khám phá
                else:
                    action = np.argmax(q_table[(x, y)])  # Khai thác
                
                # Thực hiện hành động
                dx, dy = DIRECTIONS[action]
                nx, ny = x + dx, y + dy
                
                # Kiểm tra tính hợp lệ của hành động
                if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH:
                    if self.MAZE[ny][nx] != 1:  # Không phải tường
                        x, y = nx, ny
                        path.append((x, y))
                
                # Nhận phần thưởng
                reward = get_reward(x, y)
                
                # Cập nhật Q-table
                next_max_q = max(q_table[(x, y)])
                q_table[(x[0], y[0])][action] = (1 - learning_rate) * q_table[(x[0], y[0])][action] + \
                                          learning_rate * (reward + discount_factor * next_max_q)
                
                # Kiểm tra xem đã đến đích chưa
                if (x, y) == self.END:
                    # Cập nhật đường đi tốt nhất
                    if len(path) < best_steps:
                        best_path = path.copy()
                        best_steps = len(path)
                    break
            
            # Giảm tỷ lệ khám phá theo thời gian
            exploration_rate = max(0.01, exploration_rate * 0.99)
        
        # Nếu không tìm thấy đường đi
        if not best_path:
            # Tạo đường đi dựa trên Q-table
            x, y = self.START
            path = [(x, y)]
            
            for _ in range(max_steps):
                action = np.argmax(q_table[(x, y)])
                dx, dy = DIRECTIONS[action]
                nx, ny = x + dx, y + dy
                
                if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and self.MAZE[ny][nx] != 1:
                    x, y = nx, ny
                    path.append((x, y))
                    
                    if (x, y) == self.END:
                        return path
                else:
                    # Nếu hành động dẫn đến vị trí không hợp lệ, chọn hành động khác
                    valid_actions = []
                    for i, (dx, dy) in enumerate(DIRECTIONS):
                        nx, ny = x + dx, y + dy
                        if 0 <= ny < self.HEIGHT and 0 <= nx < self.WIDTH and self.MAZE[ny][nx] != 1:
                            valid_actions.append(i)
                    
                    if valid_actions:
                        action = max(valid_actions, key=lambda a: q_table[(x, y)][a])
                        dx, dy = DIRECTIONS[action]
                        nx, ny = x + dx, y + dy
                        x, y = nx, ny
                        path.append((x, y))
                        
                        if (x, y) == self.END:
                            return path
                    else:
                        break
            
            return path
        
        return best_path
    
    