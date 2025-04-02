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



class MinimaxAI:
    def __init__(self, color=RED, timeout=None):
        self.name = 'MinimaxAI'
        self.color = color
    
    def set_color(self, color: int):
        """Set the color of the AI."""
        self.color = color

    def evaluate_window(self, window, piece):
        """Evaluate a 4-cell window and return a score."""
        score = 0
        opp_piece = YELLOW if piece == RED else RED  # Opponent piece
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(IDLE) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(IDLE) == 2:
            score += 2
        if window.count(opp_piece) == 3 and window.count(IDLE) == 1:
            score -= 4
        return score

    def evaluate(self, game: ConnectFourBoard):
        """Evaluate the board state and return a score."""
        score = 0
        turn = game.turn  # Current player (RED or YELLOW)
        
        # Evaluate center column
        center_array = [int(i) for i in list(game.board[:, game.columns // 2])]
        score += center_array.count(turn) * 3  # More pieces in the center is better
        
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

    def minimax(self, game: ConnectFourBoard, depth: int, alpha: float, beta: float, maximizingPlayer: bool):
        """Minimax algorithm with alpha-beta pruning to find the best move."""
        game = deepcopy(game)
        valid_columns = game.get_available_columns() 
        terminal = game.check_win(RED) or game.check_win(YELLOW) or game.is_full()

        if depth == 0 or terminal:
            if terminal: 
                if game.check_win(RED):
                    return (None, float('inf'))  # RED wins
                elif game.check_win(YELLOW):
                    return (None, float('-inf'))  # YELLOW wins
                else:
                    return (None, 0)  # Tie or no moves left
            else :
                return (None, self.evaluate( game))
        
        
        if maximizingPlayer:  # RED player
            value = -math.inf
            best_column = np.random.choice(valid_columns)
            for col in valid_columns:
                # Backup current state
                temp_board = game.board.copy()
                temp_turn = game.turn

                # Drop piece and recurse
                if game.drop_piece(col):  # Only drop if the column is not full
                    result = self.minimax(game, depth - 1, alpha, beta, False)
                    new_score = result[1]
                    # Undo the move
                    game.board = temp_board
                    game.turn = temp_turn

                    # Update the best score
                    if new_score > value:
                        value = new_score
                        best_column = col
                    
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break  # Prune
            return best_column, value

        else:  # YELLOW player
            value = math.inf
            best_column = np.random.choice(valid_columns)

            for col in valid_columns:
                # Backup current state
                temp_board = game.board.copy()
                temp_turn = game.turn

                # Drop piece and recurse
                if game.drop_piece(col):
                    new_score = self.minimax(game, depth - 1, alpha, beta, True)[1]

                    # Undo the move
                    game.board = temp_board
                    game.turn = temp_turn

                    # Update the best score
                    if new_score < value:
                        value = new_score
                        best_column = col

                    beta = min(beta, value)
                    if alpha >= beta:
                        break  # Prune
            return best_column, value
    

    def get_move(self, game: ConnectFourBoard):
        """Get the best move for the AI using Minimax."""
        return self.minimax(game, 6, -math.inf, math.inf, True)
        
