# AIGame
# Phát Biểu Bài Toán

## Mục Tiêu
Xây dựng trò chơi đua cá trong mê cung nhằm minh họa và so sánh hiệu quả của các thuật toán tìm đường. Mỗi "con cá" đại diện cho một người chơi hoặc một thuật toán tìm kiếm, với mục tiêu di chuyển nhanh nhất từ điểm xuất phát đến đích, vượt qua các chướng ngại vật trong mê cung. Trò chơi không chỉ mang tính giải trí mà còn giúp người dùng trực quan hóa hiệu quả, tốc độ và hành vi của các thuật toán tìm kiếm.

## Mô Tả Trò Chơi
- **Cơ chế**: Người chơi hoặc thuật toán điều khiển cá di chuyển trong mê cung, tránh chướng ngại vật để đến đích nhanh nhất.
- **Mục đích**: So sánh hiệu quả của các thuật toán tìm kiếm thông qua hành vi và thời gian hoàn thành của các con cá.

## Chế Độ Chơi
Trò chơi cung cấp ba chế độ chơi để trải nghiệm và đánh giá:
1. **P vs P (Người vs Người)**: 
   - Hai người chơi điều khiển cá bằng bàn phím.
   - Mục tiêu: Thi đấu để xem ai đến đích trước.
2. **P vs M (Người vs Máy)**:
   - Một người chơi điều khiển cá, đấu với cá do thuật toán điều khiển.
   - Mục tiêu: So sánh khả năng của người chơi với thuật toán.
3. **M vs M (Máy vs Máy)**:
   - Hai cá đều do thuật toán điều khiển.
   - Mục tiêu: Quan sát và so sánh hiệu quả của hai thuật toán khác nhau.



# Các Thuật Toán Tìm Kiếm Sử Dụng Trong Dự Án

Dự án sử dụng 6 thuật toán tìm kiếm thuộc 6 nhóm khác nhau để giải quyết bài toán. Dưới đây là mô tả ngắn gọn về từng thuật toán:

## 1. Uniform Cost Search (UCS)
- **Loại**: Tìm kiếm không có thông tin (Uninformed Search).
- **Mô tả**: Tìm đường đi ngắn nhất dựa trên chi phí, ưu tiên mở rộng trạng thái có chi phí thấp nhất.
- **Ứng dụng**: Đảm bảo đường đi tối ưu trong môi trường có chi phí thay đổi.
![UCS](https://github.com/user-attachments/assets/c78cb03f-c4b4-47c3-b8cd-8308b5e00927)


## 2. A*
- **Loại**: Tìm kiếm có thông tin (Informed Search).
- **Mô tả**: Kết hợp chi phí đã đi (`g`) và ước lượng chi phí đến đích (`h`) với hàm `f(n) = g(n) + h(n)`. Ưu tiên trạng thái có chi phí thấp nhất.
- **Ứng dụng**: Hiệu quả trong tìm kiếm không gian lớn, đảm bảo tính tối ưu.
![Astar](https://github.com/user-attachments/assets/3a26a05b-cc22-474d-9eae-2d3da3702175)

## 3. Backtracking
- **Loại**: Tìm kiếm dựa trên thử và sai.
- **Mô tả**: Thử các lựa chọn, quay lại khi gặp ngõ cụt để thử lựa chọn khác.
- **Ứng dụng**: Phù hợp với bài toán tổ hợp hoặc tìm đường trong mê cung.
![Backtracking](https://github.com/user-attachments/assets/3a355b32-7052-4cba-b4b6-672e49e2f607)

## 4. AND-OR Search
- **Loại**: Tìm kiếm trong không gian trạng thái phức tạp.
- **Mô tả**: Phân chia bài toán thành nhánh AND (thỏa mãn tất cả điều kiện) và OR (thỏa mãn một điều kiện).
- **Ứng dụng**: Xử lý bài toán có sự phụ thuộc giữa các hành động.
![ANDOR](https://github.com/user-attachments/assets/8b995468-2999-4fd9-b789-134e0580e125)

## 5. Genetic Algorithm
- **Loại**: Tìm kiếm dựa trên tiến hóa tự nhiên.
- **Mô tả**: Sử dụng chọn lọc, lai ghép, đột biến để tìm lời giải tối ưu qua các thế hệ.
- **Ứng dụng**: Tìm chiến lược di chuyển tối ưu trong trò chơi đua cá.
![GEN](https://github.com/user-attachments/assets/bc39f4c5-79a9-4b77-ae87-54b1d8b49aa7)

## 6. Q-Learning
- **Loại**: Học tăng cường (Reinforcement Learning).
- **Mô tả**: Tác nhân học tối ưu hành động qua phản hồi (thưởng/phạt) từ môi trường.
- **Ứng dụng**: Tối ưu đường đi từ xuất phát đến đích qua nhiều lần thử nghiệm.
![Q](https://github.com/user-attachments/assets/13cdfdb2-8e6d-44bf-b530-2da0130826c1)

---
*Ghi chú*: Các thuật toán được lựa chọn dựa trên đặc điểm của bài toán và yêu cầu tối ưu hóa hiệu suất.
