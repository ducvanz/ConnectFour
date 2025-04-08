# from copy import deepcopy
# import random
# import numpy as np

# import sys
# import os
# import numpy
# import math
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from Simulation.Board import ConnectFourBoard
# from Constant import RED, YELLOW, IDLE 



# class MinimaxAI:
#     def __init__(self, color=RED, timeout=None):
#         self.name = 'MinimaxAI'
#         self.color = color
    
#     def set_color(self, color: int):
#         """Set the color of the AI."""
#         self.color = color

#     def evaluate_window(self, window, piece):
#         """Evaluate a 4-cell window and return a score."""
#         score = 0
#         opp_piece = YELLOW if piece == RED else RED  # Opponent piece
#         if window.count(piece) == 4:
#             score += 100
#         elif window.count(piece) == 3 and window.count(IDLE) == 1:
#             score += 5
#         elif window.count(piece) == 2 and window.count(IDLE) == 2:
#             score += 2
#         if window.count(opp_piece) == 3 and window.count(IDLE) == 1:
#             score -= 4
#         return score

#     def evaluate(self, game: ConnectFourBoard):
#         """Evaluate the board state and return a score."""
#         score = 0
#         turn = game.turn  # Current player (RED or YELLOW)
        
#         # Evaluate center column
#         center_array = [int(i) for i in list(game.board[:, game.columns // 2])]
#         score += center_array.count(turn) * 3  # More pieces in the center is better
        
#         # Evaluate horizontal windows
#         for r in range(game.rows):
#             row_array = [int(i) for i in list(game.board[r, :])]
#             for c in range(game.columns - 3):
#                 window = row_array[c:c + 4]
#                 score += self.evaluate_window(window, turn)
        
#         # Evaluate vertical windows
#         for c in range(game.columns):
#             col_array = [int(i) for i in list(game.board[:, c])]
#             for r in range(game.rows - 3):
#                 window = col_array[r:r + 4]
#                 score += self.evaluate_window(window, turn)
        
#         # Evaluate diagonal windows (top-left to bottom-right)
#         for r in range(game.rows - 3):
#             for c in range(game.columns - 3):
#                 window = [game.board[r + i][c + i] for i in range(4)]
#                 score += self.evaluate_window(window, turn)
        
#         # Evaluate diagonal windows (bottom-left to top-right)
#         for r in range(3, game.rows):
#             for c in range(game.columns - 3):
#                 window = [game.board[r - i][c + i] for i in range(4)]
#                 score += self.evaluate_window(window, turn)
        
#         return score

#     def minimax(self, game: ConnectFourBoard, depth: int, alpha: float, beta: float, maximizingPlayer: bool):
#         """Minimax algorithm with alpha-beta pruning to find the best move."""
#         game = deepcopy(game)
#         valid_columns = game.get_available_columns() 
#         terminal = game.check_win(RED) or game.check_win(YELLOW) or game.is_full()

#         if depth == 0 or terminal:
#             if terminal: 
#                 if game.check_win(RED):
#                     return (None, float('inf'))  # RED wins
#                 elif game.check_win(YELLOW):
#                     return (None, float('-inf'))  # YELLOW wins
#                 else:
#                     return (None, 0)  # Tie or no moves left
#             else :
#                 return (None, self.evaluate( game))
        
        
#         if maximizingPlayer:  # RED player
#             value = -math.inf
#             best_column = np.random.choice(valid_columns)
#             for col in valid_columns:
#                 # Backup current state
#                 temp_board = game.board.copy()
#                 temp_turn = game.turn

#                 # Drop piece and recurse
#                 if game.drop_piece(col):  # Only drop if the column is not full
#                     result = self.minimax(game, depth - 1, alpha, beta, False)
#                     new_score = result[1]
#                     # Undo the move
#                     game.board = temp_board
#                     game.turn = temp_turn

#                     # Update the best score
#                     if new_score > value:
#                         value = new_score
#                         best_column = col
                    
#                     alpha = max(alpha, value)
#                     if alpha >= beta:
#                         break  # Prune
#             return best_column, value

#         else:  # YELLOW player
#             value = math.inf
#             best_column = np.random.choice(valid_columns)

#             for col in valid_columns:
#                 # Backup current state
#                 temp_board = game.board.copy()
#                 temp_turn = game.turn

#                 # Drop piece and recurse
#                 if game.drop_piece(col):
#                     new_score = self.minimax(game, depth - 1, alpha, beta, True)[1]

#                     # Undo the move
#                     game.board = temp_board
#                     game.turn = temp_turn

#                     # Update the best score
#                     if new_score < value:
#                         value = new_score
#                         best_column = col

#                     beta = min(beta, value)
#                     if alpha >= beta:
#                         break  # Prune
#             return best_column, value
    

#     def get_move(self, game: ConnectFourBoard):
#         """Get the best move for the AI using Minimax."""
#         return self.minimax(game, 6, -math.inf, math.inf, True)
        
from copy import deepcopy
import random
import numpy as np

import sys
import os
import numpy
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Simulation.Board import ConnectFourBoard
from Constant import RED, YELLOW, IDLE 
from AI_AlphaGo.think_three import Think_Three


class MinimaxAI:
    def __init__(self, color=RED, timeout=None):
        self.name = 'MinimaxAI'
        self.color = color
        self.opponent_color = YELLOW if color == RED else RED
        self.think_instance = Think_Three()
    
    def set_color(self, color: int):
        """Set the color of the AI."""
        self.color = color
        self.opponent_color = YELLOW if color == RED else RED

    def evaluate_window(self, window, piece):
        """Evaluate a 4-cell window and return a score."""
        score = 0
        opp_piece = YELLOW if piece == RED else RED  # Opponent piece
        if window.count(piece) == 4:
            score += 1000000
        elif window.count(piece) == 3 and window.count(IDLE) == 1:
            score += 100000
        elif window.count(piece) == 2 and window.count(IDLE) == 2:
            score += 5
        if window.count(opp_piece) == 3 and window.count(IDLE) == 1:
            score -= 1000
        return score

    def evaluate(self, game: ConnectFourBoard):
        """Evaluate the board state and return a score."""
        score = 0
        turn = game.turn  
        
        # Tính giá trị ô trung tâm
        center_array = [int(i) for i in list(game.board[:, game.columns // 2])]
        score += center_array.count(turn) * 3  #Chọn những ô ở trung tâm thì tốt hơn
        
        # Đánh giá theo chiều ngang 
        for r in range(game.rows):
            row_array = [int(i) for i in list(game.board[r, :])]
            for c in range(game.columns - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, turn)
        
        # Đánh giá theo chiều dọc
        for c in range(game.columns):
            col_array = [int(i) for i in list(game.board[:, c])]
            for r in range(game.rows - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, turn)
        
        # Đánh giá theo đường chéo (từ trái trên xuống phải dưới)
        for r in range(game.rows - 3):
            for c in range(game.columns - 3):
                window = [game.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, turn)
        
        # Đánh giá theo đường chéo từ trái dưới lên phải trên
        for r in range(3, game.rows):
            for c in range(game.columns - 3):
                window = [game.board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, turn)
        
        return score

    def minimax(self, game: ConnectFourBoard, depth: int, alpha: float, beta: float, maximizingPlayer: bool):
        """Thuật toán minimax kết hợp cắt tỉa AB để tìm nước đi tốt nhất."""
        valid_columns = game.get_available_columns()
        terminal = game.check_win(RED) or game.check_win(YELLOW) or game.is_full()

        if depth == 0 or terminal:
            if terminal: 
                if game.check_win(RED):
                    return (None, float('inf'))  # Quân đỏ win
                elif game.check_win(YELLOW):
                    return (None, float('-inf'))  # Vàng win
                else:
                    return (None, 0)  # Hòa 
            else :
                return (None, self.evaluate( game))
        
        
        if maximizingPlayer:  # Lượt đỏ
            value = -math.inf
            best_column = np.random.choice(valid_columns)
            for col in valid_columns:
                # Sao lưu trạng thái hiện tại
                temp_board = game.board.copy()
                temp_turn = game.turn

                # Thả quân và quay lùi, giảm độ sâu để tìm tiếp
                if game.drop_piece(col):  # Only drop if the column is not full
                    result = self.minimax(game, depth - 1, alpha, beta, False)
                    new_score = result[1]
                    # Hoàn tác nước đi
                    game.board = temp_board
                    game.turn = temp_turn

                    # Cập nhật điểm tốt nhất
                    if new_score > value:
                        value = new_score
                        best_column = col
                    
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break 
            return best_column, value

        else:  
            value = math.inf
            best_column = np.random.choice(valid_columns)

            for col in valid_columns:
                
                temp_board = game.board.copy()
                temp_turn = game.turn
                
                if game.drop_piece(col):
                    new_score = self.minimax(game, depth - 1, alpha, beta, True)[1]

                
                    game.board = temp_board
                    game.turn = temp_turn


                    if new_score < value:
                        value = new_score
                        best_column = col

                    beta = min(beta, value)
                    if alpha >= beta:
                        break  # Prune
            return best_column, value

    def get_move(self, game: ConnectFourBoard):
        if (np.random.randint(2) % 2 ==0):
            return self.think_instance.get_move(game)


        """Get the best move for the AI using Minimax."""
        # Kiểm tra nước đi thắng ngay
        for col in game.get_available_columns():
            row = game.get_next_open_row(col)
            if row is not None:
                temp_game = deepcopy(game)
                temp_game.drop_piece(col)
                if temp_game.check_win(self.color):
                    return col, math.inf

        # Ngăn chặn đối thủ thắng
        for col in game.get_available_columns():
            row = game.get_next_open_row(col)
            if row is not None:
                temp_game = deepcopy(game)
                temp_game.drop_piece(col)
                if temp_game.check_win(self.opponent_color):
                    return col, -math.inf
        return self.minimax(game, 6 , -math.inf, math.inf, True)

