import pygame as pg
import numpy as np
import random
from copy import deepcopy
from enum import Enum

# Import AI modules with new names
import level1
import level2
import level3

# Enum for AI difficulty levels
class AIDifficulty(Enum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3

class ConnectFour:
    # Colors
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    
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
        
        # Initialize pygame
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Connect Four")
        
    def create_board(self):
        """Create an empty game board."""
        return np.zeros((self.rows, self.columns), dtype=int)
    
    def drop_piece(self, board, col, piece):
        """Attempt to drop a piece in the specified column.
        
        Args:
            board: The game board
            col: Column index to drop the piece
            piece: Player piece (1 for red, -1 for yellow)
            
        Returns:
            bool: True if the piece was successfully dropped, False otherwise
        """
        for row in range(self.rows - 1, -1, -1):
            if board[row][col] == 0:
                board[row][col] = piece
                return True
        return False
    
    def draw_game(self):
        """Draw the current game state on the screen."""
        self.screen.fill(self.WHITE)
        
        # Draw turn indicator
        font = pg.font.Font(None, 50)
        text_surface = font.render(f"Turn: {'Red' if self.turn == 1 else 'Yellow'}", True, self.BLACK)
        self.screen.blit(text_surface, (20, 20))
        
        # Draw board and pieces
        for c in range(self.columns):
            for r in range(self.rows):
                pg.draw.rect(self.screen, self.BLUE, (c * self.square, (r + 1) * self.square, self.square, self.square))
                color = self.BLACK
                if self.board[r][c] == 1:
                    color = self.RED
                elif self.board[r][c] == -1:
                    color = self.YELLOW
                pg.draw.circle(self.screen, color, 
                               (c * self.square + self.square // 2, (r + 1) * self.square + self.square // 2), 
                               self.radius)
        pg.display.update()
    
    def show_player_order_prompt(self):
        """Display prompt for player to choose order and get their choice."""
        self.screen.fill(self.WHITE)
        font = pg.font.Font(None, 50)
        
        # Split the text into two lines
        text1 = "Choose your turn:"
        text2 = "Press 1 for Red (First) or 2 for Yellow (Second)"
        
        # Create surfaces for both lines with shadows
        shadow_surface1 = font.render(text1, True, self.BLACK)
        text_surface1 = font.render(text1, True, self.BLUE)
        shadow_surface2 = font.render(text2, True, self.BLACK)
        text_surface2 = font.render(text2, True, self.BLUE)
        
        # Position both lines in the center with proper spacing
        shadow_rect1 = shadow_surface1.get_rect(center=(self.width // 2 + 2, self.height // 2 - 30))
        text_rect1 = text_surface1.get_rect(center=(self.width // 2, self.height // 2 - 32))
        shadow_rect2 = shadow_surface2.get_rect(center=(self.width // 2 + 2, self.height // 2 + 30))
        text_rect2 = text_surface2.get_rect(center=(self.width // 2, self.height // 2 + 28))
        
        # Draw both lines with shadows
        self.screen.blit(shadow_surface1, shadow_rect1)
        self.screen.blit(text_surface1, text_rect1)
        self.screen.blit(shadow_surface2, shadow_rect2)
        self.screen.blit(text_surface2, text_rect2)
        
        pg.display.update()
        
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        return 1
                    elif event.key == pg.K_2:
                        return -1
                elif event.type == pg.QUIT:
                    return None
        return None

    def show_ai_level_prompt(self):
        """Display prompt for AI difficulty level selection."""
        self.screen.fill(self.WHITE)
        font = pg.font.Font(None, 50)
        
        text1 = "Choose AI Difficulty:"
        text2 = "Press 1 (Level 1), 2 (Level 2), or 3 (Level 3)"
        
        shadow_surface1 = font.render(text1, True, self.BLACK)
        text_surface1 = font.render(text1, True, self.BLUE)
        shadow_surface2 = font.render(text2, True, self.BLACK)
        text_surface2 = font.render(text2, True, self.BLUE)
        
        shadow_rect1 = shadow_surface1.get_rect(center=(self.width // 2 + 2, self.height // 2 - 30))
        text_rect1 = text_surface1.get_rect(center=(self.width // 2, self.height // 2 - 32))
        shadow_rect2 = shadow_surface2.get_rect(center=(self.width // 2 + 2, self.height // 2 + 30))
        text_rect2 = text_surface2.get_rect(center=(self.width // 2, self.height // 2 + 28))
        
        self.screen.blit(shadow_surface1, shadow_rect1)
        self.screen.blit(text_surface1, text_rect1)
        self.screen.blit(shadow_surface2, shadow_rect2)
        self.screen.blit(text_surface2, text_rect2)
        
        pg.display.update()
        
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key in [pg.K_1, pg.K_2, pg.K_3]:
                        return AIDifficulty(int(event.unicode))
                elif event.type == pg.QUIT:
                    return None
        return None

    def reset_game(self):
        """Reset the game to its initial state."""
        self.board = self.create_board()
        
        # Select AI level
        ai_level = self.show_ai_level_prompt()
        if ai_level is None:
            return False
        self.ai_level = ai_level
        
        # Select player order
        player_choice = self.show_player_order_prompt()
        if player_choice is None:
            return False
        self.turn = player_choice
        
        # If AI goes first, make its move
        if self.turn == -1:
            ai_col = self.get_ai_move(self.turn)
            self.drop_piece(self.board, ai_col, self.turn)
            self.turn = 1
        return True
    
    def check_horizontal_win(self, board, piece):
        """Check for a horizontal win."""
        for r in range(self.rows):
            for c in range(self.columns - 3):
                if all(board[r][c + i] == piece for i in range(4)):
                    return True
        return False
    
    def check_vertical_win(self, board, piece):
        """Check for a vertical win."""
        for r in range(self.rows - 3):
            for c in range(self.columns):
                if all(board[r + i][c] == piece for i in range(4)):
                    return True
        return False
    
    def check_diagonal_down_win(self, board, piece):
        """Check for a diagonal win (top-left to bottom-right)."""
        for r in range(self.rows - 3):
            for c in range(self.columns - 3):
                if all(board[r + i][c + i] == piece for i in range(4)):
                    return True
        return False
    
    def check_diagonal_up_win(self, board, piece):
        """Check for a diagonal win (bottom-left to top-right)."""
        for r in range(3, self.rows):
            for c in range(self.columns - 3):
                if all(board[r - i][c + i] == piece for i in range(4)):
                    return True
        return False
    
    def check_win(self, board, piece):
        """Check if the given piece has won on the board."""
        return (self.check_horizontal_win(board, piece) or 
                self.check_vertical_win(board, piece) or 
                self.check_diagonal_down_win(board, piece) or 
                self.check_diagonal_up_win(board, piece))
    
    def show_win_notification(self, winner):
        """Display the winner notification."""
        font = pg.font.Font(None, 74)
        text = f"{'Red' if winner == 1 else 'Yellow'} Wins!"
        # Change text color to match the winner's color
        text_color = self.RED if winner == 1 else self.YELLOW
        text_surface = font.render(text, True, text_color)
        # Add text shadow for better visibility
        shadow_surface = font.render(text, True, self.BLACK)
        shadow_rect = shadow_surface.get_rect(center=(self.width // 2 + 2, self.square // 2 + 2))
        text_rect = text_surface.get_rect(center=(self.width // 2, self.square // 2))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(text_surface, text_rect)
        pg.display.update()

    def show_continue_prompt(self):
        """Display continue/quit prompt and get user choice."""
        font = pg.font.Font(None, 50)
        text = "Press SPACE to continue or ESC to quit"
        # Add text shadow for better visibility
        shadow_surface = font.render(text, True, self.BLACK)
        text_surface = font.render(text, True, self.BLUE)
        shadow_rect = shadow_surface.get_rect(center=(self.width // 2 + 2, self.height // 2 + 2))
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(text_surface, text_rect)
        pg.display.update()
        
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return True
                    elif event.key == pg.K_ESCAPE:
                        return False
                elif event.type == pg.QUIT:
                    return False
        return False

    def win_game(self, board, piece):
        """Handle win condition and reset game if needed."""
        if self.check_win(board, piece):
            self.show_win_notification(piece)
            pg.time.delay(1000)
            if not self.show_continue_prompt():
                return "quit"
            self.reset_game()
            return True
        return False
    
    def get_ai_move(self, turn):
        """Generate an AI move based on selected difficulty level."""
        # Call the appropriate AI module based on difficulty level
        if self.ai_level == AIDifficulty.LEVEL_1:
            return level1.get_move(self, turn)
        elif self.ai_level == AIDifficulty.LEVEL_2:
            return level2.get_move(self, turn)
        else:
            return level3.get_move(self, turn)
    
    def run(self):
        """Main game loop."""
        if not self.reset_game():  # Initial game setup with player order selection
            return
        self.draw_game()
        running = True
        
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    continue
                    
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button (button 1)
                    # Player's turn
                    pos_x = event.pos[0]
                    col = pos_x // self.square
                    
                    if self.drop_piece(self.board, col, self.turn):
                        self.draw_game()
                        win_status = self.win_game(self.board, self.turn)
                        if win_status == "quit":
                            running = False
                            break
                        if not win_status:
                            self.turn *= -1
                            
                            # AI's turn
                            if self.turn == -1:
                                ai_col = self.get_ai_move(self.turn)
                                if self.drop_piece(self.board, ai_col, self.turn):
                                    self.draw_game()
                                    win_status = self.win_game(self.board, self.turn)
                                    if win_status == "quit":
                                        running = False
                                        break
                                    if not win_status:
                                        self.turn *= -1
                                        
                        self.draw_game()
                        
        pg.quit()

# Start the game
if __name__ == "__main__":
    game = ConnectFour()
    game.run()