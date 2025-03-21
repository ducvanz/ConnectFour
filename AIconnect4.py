import pygame as pg
import numpy as np
import time as tm
import random as rand
from copy import deepcopy

width = 800
rows = 6
columns = 7
square = width // columns
height = (rows + 1) * square
radius = square // 2 - 5


turn = 1 # 1: do, 2: vang
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def create_board():
    return np.zeros((rows, columns), dtype = int)

def drop_piece(board, col, piece):
    for row in range(rows - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = piece
            return True
    return False

def draw_game():
    screen.fill(WHITE)
    font = pg.font.Font(None, 50)
    text_surface = font.render(f"Turn: {'Red' if turn == 1 else 'Yellow'}", True, BLACK)
    screen.blit(text_surface, (20, 20))
    
    for c in range(columns):
        for r in range(rows):
            pg.draw.rect(screen, BLUE, (c * square, (r + 1) * square, square, square))
            color = BLACK
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == -1:
                color = YELLOW
            pg.draw.circle(screen, color, (c * square + square // 2, (r + 1) * square + square // 2), radius)
    pg.display.update()

def reset_game():
    global board, turn
    board = create_board()
    turn = 1
def TH1(board, piece):
    for r in range(rows):
        for c in range(columns - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    return False

def TH2(board, piece):
    for r in range(rows - 3):  # Chỉ kiểm tra đến hàng (rows - 3)
        for c in range(columns):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    return False

def TH3(board, piece):
    for r in range(rows - 3):
        for c in range(columns - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    return False

def TH4(board, piece):
    for r in range(3, rows):
        for c in range(columns - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False

def win_game(board, piece):
    if check_win(board, piece):
        pg.time.delay(2000)
        reset_game()
        return True
    return False

def check_win(AI_board, piece):
    if TH1(AI_board, piece) or TH2(AI_board, piece) or TH3(AI_board, piece) or TH4(AI_board, piece):
        return True
    return False
# def evaluate_window(window, piece):
#     score = 0
#     opponent_piece = 1 if piece == -1 else -1
    
#     if window.count(piece) == 4:  # AI thắng
#         score += 10000
#     elif window.count(piece) == 3 and window.count(0) == 1:
#         score += 50
#     elif window.count(piece) == 2 and window.count(0) == 2:
#         score += 10

#     if window.count(opponent_piece) == 3 and window.count(0) == 1:
#         score -= 80  # Ngăn đối thủ chiến thắng

#     return score

# def score_position(board, piece):
    # score = 0
    
    # # Ưu tiên cột giữa
    # center_array = [int(i) for i in list(board[:, columns // 2])]
    # center_count = center_array.count(piece)
    # score += center_count * 6

    # # Kiểm tra hàng ngang
    # for r in range(rows):
    #     row_array = [int(i) for i in list(board[r, :])]
    #     for c in range(columns - 3):
    #         window = row_array[c:c+4]
    #         score += evaluate_window(window, piece)

    # # Kiểm tra cột dọc
    # for c in range(columns):
    #     col_array = [int(i) for i in list(board[:, c])]
    #     for r in range(rows - 3):
    #         window = col_array[r:r+4]
    #         score += evaluate_window(window, piece)

    # # Kiểm tra đường chéo \
    # for r in range(rows - 3):
    #     for c in range(columns - 3):
    #         window = [board[r+i][c+i] for i in range(4)]
    #         score += evaluate_window(window, piece)

    # # Kiểm tra đường chéo /
    # for r in range(3, rows):
    #     for c in range(columns - 3):
    #         window = [board[r-i][c+i] for i in range(4)]
    #         score += evaluate_window(window, piece)

    # return score

# def minimax(board, depth, alpha, beta, maximizingPlayer):
#     valid_locations = [c for c in range(columns) if board[0][c] == 0]  # Các cột còn trống
#     is_terminal = win_game(1) or win_game(-1) or len(valid_locations) == 0

#     if depth == 0 or is_terminal:
#         if win_game(-1):
#             return (None, 1000000)
#         elif win_game(1):
#             return (None, -1000000)
#         else:
#             return (None, score_position(board, -1))

#     if maximizingPlayer:
#         value = -np.inf
#         best_col = rand.choice(valid_locations)
#         for col in valid_locations:
#             temp_board = board.copy()
#             drop_piece(temp_board, col, -1)  # AI chơi
#             new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
#             if new_score > value:
#                 value = new_score
#                 best_col = col
#             alpha = max(alpha, value)
#             if alpha >= beta:
#                 break
#         return best_col, value
#     else:
#         value = np.inf
#         best_col = rand.choice(valid_locations)
#         for col in valid_locations:
#             temp_board = board.copy()
#             drop_piece(temp_board, col, 1)  # Người chơi
#             new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
#             if new_score < value:
#                 value = new_score
#                 best_col = col
#             beta = min(beta, value)
#             if alpha >= beta:
#                 break
#         return best_col, value


def gen_AI(turn):
    col = think_three(turn)
    if col != -1:
        return col
    return np.random.randint(0, columns) 

def think_one(turn):
    for i in range(columns):
        AI_board = deepcopy(board) 
        if drop_piece(AI_board, i, turn) and check_win(AI_board, turn):
            return i
    return -1

def think_two(turn):
    opponent = -turn  # Đối thủ là người chơi ngược lại

    # Kiểm tra nếu có nước đi thắng ngay
    for i in range(columns):
        AI_board = deepcopy(board)
        if drop_piece(AI_board, i, turn) and check_win(AI_board, turn):
            return i

    # Kiểm tra nếu có nước đi giúp đối thủ thắng, cần chặn ngay
    for i in range(columns):
        AI_board = deepcopy(board)
        if drop_piece(AI_board, i, opponent) and check_win(AI_board, opponent):
            return i

    return -1  # Không tìm thấy nước đi quan trọng

def think_three(turn):
    opponent = -turn  # Đối thủ là người chơi ngược lại

    # Kiểm tra nếu có nước đi thắng ngay
    for i in range(columns):
        AI_board = deepcopy(board)
        if drop_piece(AI_board, i, turn) and check_win(AI_board, turn):
            return i

    # Kiểm tra nếu có nước đi giúp đối thủ thắng, cần chặn ngay
    for i in range(columns):
        AI_board = deepcopy(board)
        if drop_piece(AI_board, i, opponent) and check_win(AI_board, opponent):
            return i  # Chọn nước đi để chặn đối thủ

    # Kiểm tra 2 bước tiếp theo
    for i in range(columns):
        AI_board = deepcopy(board)
        if drop_piece(AI_board, i, turn):
            for j in range(columns):
                AI_board_2 = deepcopy(AI_board)
                if drop_piece(AI_board_2, j, opponent) and check_win(AI_board_2, opponent):
                    return j 

    return -1


pg.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Demo connect four")
board = create_board()

draw_game()

running = True
while running:
    for event in pg.event.get():     
        if event.type == pg.QUIT:
            running = False
            continue
        elif event.type == pg.MOUSEBUTTONDOWN:
            col = None
            pos_x = event.pos[0]
            col = pos_x // square 
            if drop_piece(board, col, turn):
                draw_game()
                if not win_game(board, turn):
                    turn *= -1
                if turn == -1:
                    col = gen_AI(turn)
                    if drop_piece(board, col, turn):
                         draw_game()
                         if not win_game(board, turn):
                              turn *= -1
                print(board)
            draw_game()


