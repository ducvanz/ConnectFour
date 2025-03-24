import numpy as np
from enum import Enum

import think_one
import think_two
import think_three
import MCTS

# Enum for AI difficulty levels
class AIDifficulty(Enum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4

class ConnectFour:
    def __init__(self):
        """Initialize the Connect Four game."""
        # Board dimensions
        self.rows = 6
        self.columns = 7
        self.width = 800
        self.square = self.width // self.columns
        self.height = (self.rows + 1) * self.square
        self.radius = self.square // 2 - 5
        
        # Game state
        self.board = self.create_board()
        self.turn = 1  # 1: red, -1: yellow
        self.ai_level = AIDifficulty.LEVEL_3  # Default AI level
        self.ai_timeouts = {
            AIDifficulty.LEVEL_1: 0.5,
            AIDifficulty.LEVEL_2: 0.5,
            AIDifficulty.LEVEL_3: 1.0,
            AIDifficulty.LEVEL_4: 2.0
        }
        
    def create_board(self):
        """Create an empty game board."""
        return np.zeros((self.rows, self.columns), dtype=int)
    
    def drop_piece(self, column):
        """Attempt to drop a piece in the specified column.
        
        Args:
            column: Column index to drop the piece
            
        Returns:
            bool: True if the piece was successfully dropped, False otherwise
        """
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = self.turn
                self.turn *= -1  # Toggle turn after successful move
                return True
        return False
    
    def reset_game(self, player_choice, ai_level):
        """Reset the game to its initial state."""
        self.board = self.create_board()
        self.ai_level = ai_level
        self.turn = player_choice
        
        # If AI goes first, make its move
        if self.turn == -1:
            ai_col = self.get_ai_move()
            self.drop_piece(ai_col)  # This will toggle turn to 1 automatically
        return True
    
    def check_horizontal_win(self, turn):
        """Check for a horizontal win."""
        for r in range(self.rows):
            for c in range(self.columns - 3):
                if all(self.board[r][c + i] == turn for i in range(4)):
                    return True
        return False
    
    def check_vertical_win(self, turn):
        """Check for a vertical win."""
        for r in range(self.rows - 3):
            for c in range(self.columns):
                if all(self.board[r + i][c] == turn for i in range(4)):
                    return True
        return False
    
    def check_diagonal_down_win(self, turn):
        """Check for a diagonal win (top-left to bottom-right)."""
        for r in range(self.rows - 3):
            for c in range(self.columns - 3):
                if all(self.board[r + i][c + i] == turn for i in range(4)):
                    return True
        return False
    
    def check_diagonal_up_win(self, turn):
        """Check for a diagonal win (bottom-left to top-right)."""
        for r in range(3, self.rows):
            for c in range(self.columns - 3):
                if all(self.board[r - i][c + i] == turn for i in range(4)):
                    return True
        return False
    
    def check_win(self,turn):
        """Check if the given piece has won on the board."""
        return (self.check_horizontal_win(turn) or 
                self.check_vertical_win(turn) or 
                self.check_diagonal_down_win(turn) or 
                self.check_diagonal_up_win(turn))
    
    def get_ai_move(self, timeout=None):
        """Generate an AI move based on selected difficulty level.
        
        Args:
            timeout: Optional timeout in seconds for AI computation.
                    If None, use default timeout for AI level.
        """
        # Use provided timeout or default for AI level
        if timeout is None:
            timeout = self.ai_timeouts[self.ai_level]
            
        # Call the appropriate AI module based on difficulty level
        match self.ai_level:
            case AIDifficulty.LEVEL_1:
                return think_one.get_move(self)
            case AIDifficulty.LEVEL_2:
                return think_two.get_move(self)
            case AIDifficulty.LEVEL_3:
                return think_three.get_move(self, max_time=timeout)
            case AIDifficulty.LEVEL_4:
                return MCTS.mcts(self, max_time=timeout)
            case _:
                return think_three.get_move(self, max_time=timeout)  # Default case