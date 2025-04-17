from copy import deepcopy
import random
import numpy as np
import numpy
import math


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Simulation.Board import ConnectFourBoard
from Constant import RED, YELLOW, IDLE 

DEFAULT_WEIGHT = [0.04, 0.02, 0.04, 0.02, 0.03, 0.9, 0.9]
"""
    0. Allies three straight
    1. Allies two straight
    2. Enemy three straight
    3. Enemy two straight
    4. Bonus point for take place at middle column
    -2. Allies enhance point
    -1. Enemy enhance point
"""


class MinimaxAI:
    def __init__(self, weight=DEFAULT_WEIGHT, depth=5, notPrunning=False, color=RED, timeout=None):
        self.name = 'MinimaxAI depth=' + str(depth)
        self.color = color
        self.depth = depth

        self.notPrunning = notPrunning
        self.weight = { 'allie': [weight[0], weight[1]], 
                        'enemy': [weight[2], weight[3]],
                       'center': weight[4]}
    
    def set_color(self, color: int):
        """Set the color of the AI."""
        self.color = color

    def evaluate_window(self, window, piece):
        """Evaluate a 4-cell window and return a score."""
        score = 0
        opp_piece = -piece  # Opponent piece

        if window.count(piece) == 3 and window.count(IDLE) == 1:
            score += self.weight['allie'][0]
        elif window.count(piece) == 2 and window.count(IDLE) == 2:
            score += self.weight['allie'][1]

        if (window.count(opp_piece)) == 3 and (window.count(IDLE) == 1) :
            score -= self.weight['enemy'][0]
        elif (window.count(opp_piece) == 2) and (window.count(IDLE) == 2) :
            score -= self.weight['enemy'][1]

        return score

    def evaluate(self, game: ConnectFourBoard):
        """Evaluate the board state and return a score."""
        score = 0
        turn = self.color  # Current player (RED or YELLOW)
        
        # Evaluate center column
        center = game.board[:, game.columns // 2]
        score += (np.sum(center == self.color) - np.sum(center == -self.color)) * self.weight['center']  # More pieces in the center is better
        
        # Evaluate horizontal windows
        for r in range(game.rows):
            row_array = [int(i) for i in list(game.board[r, :])]
            for c in range(game.columns - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, turn)
        
        # Evaluate vertical windows
        for c in range(game.columns):
            col_array = [int(i) for i in list(game.board[:, c])]
            for r in range(game.rows - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, turn)
        
        # Evaluate diagonal windows (top-left to bottom-right)
        for r in range(game.rows - 3):
            for c in range(game.columns - 3):
                window = [game.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, turn)
        
        # Evaluate diagonal windows (bottom-left to top-right)
        for r in range(3, game.rows):
            for c in range(game.columns - 3):
                window = [game.board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, turn)
        
        return score

    def order_columns(game: ConnectFourBoard):
        center = game.columns // 2
        valid_columns = game.get_available_columns()
        return sorted(valid_columns, key=lambda c: abs(center - c))

    def minimax(self, game: ConnectFourBoard, depth: int, maximizingPlayer: bool, Alpha:float=-math.inf, Beta:float=math.inf):
        """Minimax algorithm with alpha-beta pruning to find the best move."""

        if game.check_win(self.color) :
            return [1]
        elif game.check_win(-self.color) :
            return [-1]
        
        if game.is_full() :
            return [0.0]
        
        if depth == 0: 
            return [self.evaluate(game)]
        
        valid_columns = MinimaxAI.order_columns(game)

        if maximizingPlayer:  # RED player
            scores = [-1.5] * game.columns      # default value for invavlid_column or bad_evaluate_col. Just mean -1 because we won't need this kind of columns
            alpha = -math.inf
            
            for col in valid_columns:
                # Backup current state
                temp_game = game.copy()

                # Drop piece and recurse
                if temp_game.drop_piece(col):  # Only drop if the column is not full
                    e = self.minimax(temp_game, depth - 1, False, Alpha=alpha)
                    scores[col] = np.min(e).astype(float)

                    # if (depth == self.depth) :
                    #     print('Turn 1: ', col, scores[col] / 0.95)
                    
                    # Pruning
                    alpha = max(alpha, scores[col])
                    if (not self.notPrunning) and (alpha > Beta):
                        scores[col] += abs(scores[col]) * 0.1
                        break 
            return np.array(scores)

        else:  # YELLOW player
            scores = [1.5] * game.columns
            beta = math.inf

            for col in valid_columns:
                # Backup current state
                temp_game = game.copy()

                # Drop piece and recurse
                if temp_game.drop_piece(col):
                    e = self.minimax(temp_game, depth - 1, True, Beta=beta)
                    scores[col] = np.max(e).astype(float)

                    # if (depth == self.depth - 1) :
                    #     print('Turn 2: ', col, '\n', e, np.argmax(e)) 

                    # Pruning
                    beta = min(beta, scores[col])
                    if (not self.notPrunning) and (Alpha > beta) :
                        scores[col] -= abs(scores[col]) * 0.1
                        break 
            return np.array(scores) * 0.95

    def get_move(self, game: ConnectFourBoard):
        """Get the best move for the AI using Minimax."""
        evaluated = self.minimax(game, self.depth, True)

        # print(np.argmax(evaluated))
        # print(evaluated)

        return np.argmax(evaluated), evaluated


### Bản mở rộng chỉ cộng thêm điểm trong trường hợp tồn tại nhiều ô ***_ như thế, và các ô này nối tiếp nhau trên cùng 1 hàng
class EnhanceMinimaxAI(MinimaxAI) :
    ###
    ###     ***_ point like this if near each other in the same columns (playable or not) is critical point.
    ###     Normally, we can easy detect it effect with a MinimaxAI(depth=7), but it alway too slow at game start.
    ###     This Enhance edition hope to improve that.
    ###

    def __init__(self, weight=DEFAULT_WEIGHT, depth=5, notPrunning=False, color=RED, timeout=None) :
        super().__init__(weight=DEFAULT_WEIGHT, depth=5, notPrunning=False, color=RED, timeout=None)

        self.name = 'Enhance_MinimaxAI depth=' + str(depth)
        self.weight['allie'].append(weight[-2])
        self.weight['enemy'].append(weight[-1]) 


    def evaluate_window(self, window, piece):
        """Evaluate a 4-cell window and return a score."""
        score = 0
        opp_piece = -piece  # Opponent piece
        notice = {piece : [],
                  opp_piece : []}

        if window.count(piece) == 3 and window.count(IDLE) == 1:
            score += self.weight['allie'][0]
            notice[piece].extend([i for i, val in enumerate(window) if val == IDLE])
        elif window.count(piece) == 2 and window.count(IDLE) == 2:
            score += self.weight['allie'][1]
            notice[piece].extend([i for i, val in enumerate(window) if val == IDLE])

        if (window.count(opp_piece)) == 3 and (window.count(IDLE) == 1) :
            score -= self.weight['enemy'][0]
            notice[opp_piece].extend([i for i, val in enumerate(window) if val == IDLE])
        elif (window.count(opp_piece) == 2) and (window.count(IDLE) == 2) :
            score -= self.weight['enemy'][1]
            notice[opp_piece].extend([i for i, val in enumerate(window) if val == IDLE])

        return score, notice

    def evaluate(self, game):
        """
        Evaluate the board state and return a score. With some important addition: 
        """

        turn = self.color  # Current player (RED or YELLOW)
        notice = {turn : [set(), set(), set(), set(), set(), set(), set()],         # Quy ước là một điểm nguy hiểm cho quân màu nào thì key=màu_đó, index=column, value=row
                  -turn : [set(), set(), set(), set(), set(), set(), set()]}
        
        # Evaluate center column
        center = game.board[:, game.columns // 2]
        score = (np.sum(center == self.color) - np.sum(center == -self.color)) * self.weight['center']  # More pieces in the center is better
        
        # Evaluate horizontal windows ____
        for r in range(game.rows):
            row_array = game.board[r]
            for c in range(game.columns - 3):
                window = row_array[c:c + 4].tolist()
                this_score, this_notice = self.evaluate_window(window, turn)
                score += this_score
                for color in [turn, -turn] :        # Lưu lại vị trí các điểm nguy hiểm trên bàn cờ
                    for x in this_notice[color] :
                        notice[color][c + x].add(r)
        
        # Evaluate vertical windows |
        free_position = game.get_available()
        for c in range(game.columns):
            r = free_position[c]
            col_array = game.board.T[c]
            window = col_array[r:r + 4].tolist()
            this_score, this_notice = self.evaluate_window(window, turn)
            score += this_score
            for color in [turn, -turn] :        # Lưu lại vị trí các điểm nguy hiểm trên bàn cờ
                for x in this_notice[color] :
                    notice[color][c].add(r + x)
        
        # Evaluate diagonal windows (top-left to bottom-right) \
        for r in range(game.rows - 3):
            for c in range(game.columns - 3):
                window = [game.board[r + i][c + i] for i in range(4)]
                this_score, this_notice = self.evaluate_window(window, turn)
                score += this_score
                for color in [turn, -turn] :        # Lưu lại vị trí các điểm nguy hiểm trên bàn cờ
                    for x in this_notice[color] :
                        notice[color][c + x].add(r + x)
        
        # Evaluate diagonal windows (bottom-left to top-right)
        for r in range(3, game.rows):
            for c in range(game.columns - 3):
                window = [game.board[r - i][c + i] for i in range(4)]
                this_score, this_notice = self.evaluate_window(window, turn)
                score += this_score
                for color in [turn, -turn] :        # Lưu lại vị trí các điểm nguy hiểm trên bàn cờ
                    for x in this_notice[color] :
                        notice[color][c + x].add(r - x)
        
        # Điểm mở rộng
        for col in range(7):
            noti = sorted(notice[turn][col])       ## Đồng minh
            for i in range(len(noti) - 1) :
                if noti[i+1] - noti[i] == 1 :       # Nếu notice_position ở cột này sát nhau, cộng thêm điểm
                    score += self.weight['allie'][-1] * (0.9 ** (free_position[col] - noti[i+1]))

            noti = sorted(notice[turn][col])       ## Đối thủ
            for i in range(len(noti) - 1) :
                if noti[i+1] - noti[i] == 1 :       # Nếu notice_position ở cột này sát nhau, cộng thêm điểm
                    score -= self.weight['allie'][-1] * (0.9 ** (free_position[col] - noti[i+1]))
            

        return score