from algorithm import Al_solution
import numpy as np
import matplotlib.pyplot as plt
import time

# Tạo một mê cung đơn giản để test
def create_test_maze(size=10):
    # Tạo mê cung trống
    maze = np.zeros((size, size), dtype=int)
    
    # Thêm một số tường
    # Tường ngang
    maze[2, 2:8] = 1
    maze[5, 3:7] = 1
    maze[7, 1:9] = 1
    
    # Tường dọc
    maze[1:6, 3] = 1
    maze[3:8, 6] = 1
    
    # Đặt điểm bắt đầu và kết thúc
    start = (1, 1)
    end = (8, 8)
    
    return maze, start, end

# Hàm vẽ mê cung và đường đi
def visualize_maze_and_path(maze, start, end, path=None, title="Maze"):
    plt.figure(figsize=(10, 10))
    plt.imshow(maze, cmap='binary')
    
    # Đánh dấu điểm bắt đầu và kết thúc
    plt.plot(start[0], start[1], 'go', markersize=10)
    plt.plot(end[0], end[1], 'ro', markersize=10)
    
    # Vẽ đường đi nếu có
    if path:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        plt.plot(path_x, path_y, 'b-', linewidth=2)
        plt.plot(path_x, path_y, 'bo', markersize=5)
    
    plt.grid(True)
    plt.title(title)
    plt.show()

# Hàm test từng thuật toán
def test_algorithm(algorithm_name, solver, **kwargs):
    print(f"\nTesting {algorithm_name}...")
    start_time = time.time()
    
    if algorithm_name == "UCS":
        path = solver.ucs()
    elif algorithm_name == "A*":
        path = solver.a_star()
    elif algorithm_name == "Genetic":
        path = solver.genetic_algorithm(**kwargs)
    elif algorithm_name == "Partially Observable":
        path = solver.partially_observable(**kwargs)
    elif algorithm_name == "Q-learning":
        path = solver.q_learning(**kwargs)
    
    end_time = time.time()
    
    if path:
        print(f"Đường đi tìm được có {len(path)} bước")
        print(f"Tọa độ đầu tiên: {path[0]}, Tọa độ cuối cùng: {path[-1]}")
    else:
        print("Không tìm thấy đường đi!")
    
    print(f"Thời gian thực thi: {end_time - start_time:.4f} giây")
    
    return path

# Chương trình chính
if __name__ == "__main__":
    # Tạo mê cung để test
    maze, start, end = create_test_maze(size=10)
    
    # Khởi tạo solver
    solver = Al_solution(start, end, maze)
    
    # Vẽ mê cung ban đầu
    visualize_maze_and_path(maze, start, end, title="Test Maze")
    
    # Test từng thuật toán
    
    # 1. UCS
    ucs_path = test_algorithm("UCS", solver)
    if ucs_path:
        visualize_maze_and_path(maze, start, end, ucs_path, "UCS Path")
    
    # 2. A*
    astar_path = test_algorithm("A*", solver)
    if astar_path:
        visualize_maze_and_path(maze, start, end, astar_path, "A* Path")
    
    # 3. Genetic Algorithm
    genetic_path = test_algorithm("Genetic", solver, population_size=50, generations=50, mutation_rate=0.2)
    if genetic_path:
        visualize_maze_and_path(maze, start, end, genetic_path, "Genetic Algorithm Path")
    
    # 4. Partially Observable
    po_path = test_algorithm("Partially Observable", solver, visibility_radius=2)
    if po_path:
        visualize_maze_and_path(maze, start, end, po_path, "Partially Observable Path")
    
    # 5. Q-learning
    q_path = test_algorithm("Q-learning", solver, episodes=200, max_steps=200)
    if q_path:
        visualize_maze_and_path(maze, start, end, q_path, "Q-learning Path")
    
    # So sánh các thuật toán
    print("\n=== So sánh độ dài đường đi ===")
    algorithms = ["UCS", "A*", "Genetic", "Partially Observable", "Q-learning"]
    paths = [ucs_path, astar_path, genetic_path, po_path, q_path]
    
    for alg, path in zip(algorithms, paths):
        if path:
            print(f"{alg}: {len(path)} bước")
        else:
            print(f"{alg}: Không tìm thấy đường đi")