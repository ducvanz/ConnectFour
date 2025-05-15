# ConnectFour
ConnectFour là một trò chơi Cờ Bốn (Connect Four) được phát triển bằng Python, tích hợp trí tuệ nhân tạo (AI) với nhiều cấp độ khó khác nhau. Dự án hỗ trợ chế độ người chơi đối đầu với AI hoặc hai AI đối đầu nhau, sử dụng các thuật toán như Minimax với cắt tỉa alpha-beta, Monte Carlo Tree Search (MCTS) và ứng dụng mô hình học sâu (Deep learning) để tìm nước đi tối ưu.
![image](https://github.com/user-attachments/assets/775c0e78-3464-4b1f-9535-d8bfe795bf2a)

# Ý tưởng chính của nhóm
- Xây dựng các mô hình AI khác nhau dựa trên nền tảng chính là 2 thuật toán minimax (được học trong nội dung môn học) và thuật toán Monte Carlo Tree Search (MCTS) sau đó sử dụng chính hai thuật toán này lấy dữ liệu để đưa vào mô hình học sâu (Deep learning).
- Ứng dụng mô hình học sâu cho:
  + Trực tiếp sử dụng mô hình như là một AI thông thường để trả về nước đi tối ưu sau khi nhận bàn cờ là đầu vào.
  + Sử dụng Deep Learning như là một hàm đánh giá cho 2 thuật toán bên trên (tối ưu về thời gian và hạn chế những sai xót khi tự định nghĩa hàm đánh giá)
Phương pháp làm được nhóm tham khảo từ quyển sách ![AlphagoSimpled](https://drive.google.com/file/d/1GOLnD0mIPZDWMdVE3WDmm5effnih66Bd/view?usp=drive_link)

# Quá trình phát triển

## Xây dựng giao diện thử nghiệm code, thiết kế cấu trúc chung dự án
## Xây dựng các mô hình AI bằng thuật toán
## Thử nghiệm - tối ưu
## Ứng dụng deep learning
## Tích hợp deep learning vào thuật toán

# Cấu trúc code

- Bao gồm 3 thư mục chính: AI_AlphaGo, DL, Simulation trong đó:
  + AI_AlphaGo: gồm các mô hình AI mà nhóm đã xây dựng (Think_one, Think_two, Think_three, minimax....)
  + DL: dữ liệu training cho mô hình, định nghĩa mô hình và mô hình sau khi training (do quá trình chạy thực tế để lấy dữ liệu training không ngắn nên đã chia làm các file khác nhau tương ứng với mỗi lần chạy)
  + Simulation: nơi định nghĩa giao diện, logic của game sử dụng cho việc thử nghiệm các mô hình.

# Cách triển chạy

- Thực hiện clone code về và chạy file MatchMaker.py
Lưu ý: Cần cài python và thư viện tensorflow trước.
 
# Thành viên nhóm thực hiện

Mai Đức Văn - 23021746 (nhóm trường)
Nguyễn Kim Trung Đức - 23021533
Ngọ Viết Thuyết - 23021730
Nguyễn Trường Sơn - 23021686


