import random
from typing import List, Tuple
lista = [9,15,15,25,23,37]
mazetest = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 0, 2, 1, 1, 1, 1, 0, 1, 1, 2, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 2, 0, 0, 0, 1, 0, 1, 0],
    [0, 2, 1, 1, 2, 1, 1, 1, 0, 1, 2, 2, 0, 1, 0, 1, 0, 1, 2, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 1, 2, 1, 1, 0, 2, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 2, 1, 0, 2, 1, 1, 0, 1, 1, 2, 1, 2, 0],
    [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 2, 0],
    [0, 1, 0, 1, 0, 2, 0, 1, 1, 1, 1, 1, 0, 2, 0, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 2, 2, 0],
    [0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 2, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0],
    [0, 2, 1, 1, 0, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 1, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


class MazeGenerator:
    def __init__(self, width: int, height: int,test_mode = False):
        """
        Khởi tạo một mê cung mới với kích thước được chỉ định.
        
        Args:
            width: Chiều rộng của mê cung
            height: Chiều cao của mê cung
        """
        self.test_mode = test_mode
        # Đảm bảo kích thước lẻ để có tường bao quanh
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        # Khởi tạo ma trận mê cung với tất cả là tường (0)
        self.maze = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.entrance = (0, 1)
        self.exit_point = (self.width - 1, self.height - 2)
    def remove_wall(self, x1: int, y1: int, x2: int, y2: int):
        """
        Phá tường giữa hai ô.
        
        Args:
            x1, y1: Tọa độ ô thứ nhất
            x2, y2: Tọa độ ô thứ hai
        """
        # Đánh dấu cả hai ô là đường đi
        self.maze[y1][x1] = 1
        self.maze[y2][x2] = 1
        
        # Đánh dấu ô ở giữa (tường) là đường đi
        self.maze[(y1 + y2) // 2][(x1 + x2) // 2] = 1
    
    def generate(self, obstacle_percentage: float = 0) -> List[List[int]]:
        if self.test_mode ==True:
            if self.width == 23 and self.height == 37:
                print("TESSSSSSSSSSSSS")
                return mazetest
        """
        Tạo mê cung sử dụng thuật toán Depth-First Search,
        sau đó phá thêm tường ngẫu nhiên và thêm chướng ngại vật.
        
        Args:
            obstacle_percentage: Phần trăm đường đi sẽ trở thành chướng ngại vật (0-100)
            
        Returns:
            Mê cung dưới dạng ma trận với:
            - 0: tường
            - 1: đường đi
            - 2: chướng ngại vật
        """
        # Bắt đầu từ một điểm ngẫu nhiên (luôn là số lẻ để tránh các ô tường)
        start_x = random.randint(0, (self.width - 1) // 2) * 2 -1
        start_y = random.randint(0, (self.height - 1) // 2) * 2 - 1
        print(start_x,start_y)
        # Đánh dấu điểm bắt đầu là đường đi
        
        self.maze[start_y][start_x]= 1
        
        # Danh sách các ô đã ghé thăm nhưng chưa xét hết các hướng
        stack = [(start_x, start_y)]
        visited = set([(start_x, start_y)])
        
        # GIAI ĐOẠN 1: Tạo mê cung cơ bản bằng DFS
        while stack:
            x, y = stack[-1]
            
            # Các hướng có thể đi: phải, trái, xuống, lên (mỗi bước đi cách 2 ô)
            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            random.shuffle(directions)
            
            found = False
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                # Kiểm tra xem ô mới có nằm trong mê cung và chưa được thăm chưa
                if (0 < nx < self.width - 1 and 0 < ny < self.height - 1 and 
                    (nx, ny) not in visited):
                    
                    # Phá tường giữa ô hiện tại và ô mới
                    self.remove_wall(x, y, nx, ny)
                    
                    # Đánh dấu đã thăm và thêm vào stack
                    visited.add((nx, ny))
                    stack.append((nx, ny))
                    found = True
                    break
            
            # Nếu không tìm thấy hướng đi mới, quay lại
            if not found:
                stack.pop()
        
        # GIAI ĐOẠN 2: Phá thêm tường ngẫu nhiên (khoảng 25% tổng số ô)
        total_cells = (self.width // 2) * (self.height // 2)
        walls_to_remove = total_cells // 4
        
        for _ in range(walls_to_remove):
            # Chọn vị trí tường ngẫu nhiên (số chẵn)
            attempts = 0
            while attempts < 100:  # Giới hạn số lần thử để tránh vòng lặp vô hạn
                wall_x = random.randint(1, self.width - 2)
                wall_y = random.randint(1, self.height - 2)
                
                # Kiểm tra xem đây có phải là tường và có thể phá không
                if self.maze[wall_y][wall_x] == 0:
                    # Kiểm tra nếu là tường ngang
                    if wall_x % 2 == 1 and wall_y % 2 == 0:
                        # Đảm bảo có tường ở hai bên
                        if (self.maze[wall_y-1][wall_x] == 1 and 
                            self.maze[wall_y+1][wall_x] == 1):
                            self.maze[wall_y][wall_x] = 1
                            break
                    # Kiểm tra nếu là tường dọc
                    elif wall_x % 2 == 0 and wall_y % 2 == 1:
                        # Đảm bảo có tường ở hai bên
                        if (self.maze[wall_y][wall_x-1] == 1 and 
                            self.maze[wall_y][wall_x+1] == 1):
                            self.maze[wall_y][wall_x] = 1
                            break
                attempts += 1
        # Bọc lại hàng ngoài để tránh thủng tường ngoài
        rows = len(self.maze)
        cols = len(self.maze[0])

        for j in range(cols):
            self.maze[0][j] = 0           
            self.maze[rows - 1][j] = 0     

        for i in range(1, rows - 1):
            self.maze[i][0] = 0            
            self.maze[i][cols - 1] = 0  
        # Tạo lối vào, lối ra  
        entrance = (0, 1)
        exit_point = (self.width - 1, self.height - 2)
        self.maze[entrance[1]][entrance[0]] = 1  # Lối vào
        self.maze[exit_point[1]][exit_point[0]] = 1  # Lối ra
        
        # GIAI ĐOẠN 3: Thêm chướng ngại vật
        if obstacle_percentage > 0:
            # Tìm tất cả các ô đường đi
            path_cells = []
            for y in range(self.height):
                for x in range(self.width):
                    if self.maze[y][x] == 1 and (x, y) != entrance and (x, y) != exit_point:
                        path_cells.append((x, y))
            
            # Tính số lượng chướng ngại vật cần thêm
            num_obstacles = int(len(path_cells) * obstacle_percentage / 50)
            
            # Đảm bảo luôn có đường đi từ lối vào đến lối ra
            # Tìm đường đi trước khi thêm chướng ngại vật
            solution_path = self.solve()
            path_set = set(solution_path)
            
            # Loại bỏ các ô nằm trên đường đi chính để đảm bảo luôn có giải pháp
            safe_path_cells = [cell for cell in path_cells if cell not in path_set]
            
            # Thêm chướng ngại vật ngẫu nhiên
            if num_obstacles > 0 and safe_path_cells:
                # Đảm bảo không thêm nhiều hơn số ô an toàn
                num_obstacles = min(num_obstacles, len(safe_path_cells))
                obstacle_positions = random.sample(safe_path_cells, num_obstacles)
                
                for x, y in obstacle_positions:
                    self.maze[y][x] = 2  # Đánh dấu là chướng ngại vật
        
        return self.maze
    
    def print_maze(self):
        """
        In mê cung ra màn hình (0: tường, 1: đường đi, 2: chướng ngại vật)
        """
        for row in self.maze:
            print(' '.join(str(cell) for cell in row))
    
    def print_maze_visual(self):
        """
        In mê cung ra màn hình với ký hiệu dễ nhìn hơn
        '█' là tường, ' ' là đường đi, 'X' là chướng ngại vật
        """
        for row in self.maze:
            line = ''.join('█' if cell == 0 else ('X' if cell == 2 else ' ') for cell in row)
            print(line)
    
    def solve(self) -> List[Tuple[int, int]]:
        """
        Giải mê cung sử dụng thuật toán BFS, tránh các chướng ngại vật
        
        Returns:
            Đường đi từ lối vào đến lối ra
        """
        # Tìm điểm bắt đầu và kết thúc
        start = (0, 1)
        end = (self.width - 1, self.height - 2)
        
        # Kiểm tra nếu không có lối vào hoặc ra
        if self.maze[start[1]][start[0]] == 0 or self.maze[end[1]][end[0]] == 0:
            return []
            
        # Hàng đợi cho BFS
        queue = [start]
        # Lưu lại đường đi
        came_from = {start: None}
        
        # BFS
        while queue and end not in came_from:
            current = queue.pop(0)
                
            x, y = current
            # Các hướng có thể đi: phải, trái, xuống, lên
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                
                # Kiểm tra xem ô mới có nằm trong mê cung, là đường đi (không phải tường hoặc chướng ngại vật) và chưa được thăm
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    self.maze[ny][nx] == 1 and (nx, ny) not in came_from):
                    queue.append((nx, ny))
                    came_from[(nx, ny)] = current
        
        # Khôi phục đường đi
        if end not in came_from:
            return []  # Không tìm thấy đường đi
            
        path = []
        current = end
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        
        return path
    
    def print_solution(self, path: List[Tuple[int, int]]):
        """
        In mê cung với đường đi
        
        Args:
            path: Đường đi từ lối vào đến lối ra
        """
        if not path:
            print("Không có đường đi giữa lối vào và lối ra!")
            return
            
        solution = [[cell for cell in row] for row in self.maze]
        for x, y in path:
            # Chỉ đánh dấu đường đi trên các ô không phải chướng ngại vật
            if solution[y][x] != 2:
                solution[y][x] = 3  # Đánh dấu đường đi bằng số 3
            
        # In mê cung với đường đi
        for row in solution:
            line = ''.join('█' if cell == 0 else ('X' if cell == 2 else ('•' if cell == 3 else ' ')) for cell in row)
            print(line)


# Ví dụ sử dụng
if __name__ == "__main__":
    maze = MazeGenerator(23, 37)
    # Tạo mê cung với 5% đường đi là chướng ngại vật
    maze.generate(obstacle_percentage=5)
    
    print("Mê cung (0: tường, 1: đường đi, 2: chướng ngại vật):")
    maze.print_maze()
    
    print("\nMê cung (trực quan):")
    maze.print_maze_visual()
    
    print("\nĐường đi qua mê cung:")
    solution = maze.solve()
    maze.print_solution(solution)