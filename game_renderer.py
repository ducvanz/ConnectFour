import pygame as pg
from AIconnect4 import ConnectFour, AIDifficulty

class GameRenderer:
    # Colors
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    
    def __init__(self, game):
        """Initialize the game renderer with a ConnectFour game instance."""
        self.game = game
        # Initialize pygame
        pg.init()
        self.screen = pg.display.set_mode((game.width, game.height))
        pg.display.set_caption("Connect Four")
    
    def draw_game(self):
        """Draw the current game state on the screen."""
        self.screen.fill(self.WHITE)
        
        # Draw turn indicator
        font = pg.font.Font(None, 50)
        text_surface = font.render(f"Turn: {'Red' if self.game.turn == 1 else 'Yellow'}", True, self.BLACK)
        self.screen.blit(text_surface, (20, 20))
        
        # Draw board and pieces
        for c in range(self.game.columns):
            for r in range(self.game.rows):
                pg.draw.rect(self.screen, self.BLUE, 
                            (c * self.game.square, (r + 1) * self.game.square, self.game.square, self.game.square))
                color = self.BLACK
                if self.game.board[r][c] == 1:
                    color = self.RED
                elif self.game.board[r][c] == -1:
                    color = self.YELLOW
                pg.draw.circle(self.screen, color, 
                            (c * self.game.square + self.game.square // 2, 
                            (r + 1) * self.game.square + self.game.square // 2), 
                            self.game.radius)
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
        shadow_rect1 = shadow_surface1.get_rect(center=(self.game.width // 2 + 2, self.game.height // 2 - 30))
        text_rect1 = text_surface1.get_rect(center=(self.game.width // 2, self.game.height // 2 - 32))
        shadow_rect2 = shadow_surface2.get_rect(center=(self.game.width // 2 + 2, self.game.height // 2 + 30))
        text_rect2 = text_surface2.get_rect(center=(self.game.width // 2, self.game.height // 2 + 28))
        
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
        text2 = "Press 1 to 4 for choosing AI level 1 to 4"
        
        shadow_surface1 = font.render(text1, True, self.BLACK)
        text_surface1 = font.render(text1, True, self.BLUE)
        shadow_surface2 = font.render(text2, True, self.BLACK)
        text_surface2 = font.render(text2, True, self.BLUE)
        
        shadow_rect1 = shadow_surface1.get_rect(center=(self.game.width // 2 + 2, self.game.height // 2 - 30))
        text_rect1 = text_surface1.get_rect(center=(self.game.width // 2, self.game.height // 2 - 32))
        shadow_rect2 = shadow_surface2.get_rect(center=(self.game.width // 2 + 2, self.game.height // 2 + 30))
        text_rect2 = text_surface2.get_rect(center=(self.game.width // 2, self.game.height // 2 + 28))
        
        self.screen.blit(shadow_surface1, shadow_rect1)
        self.screen.blit(text_surface1, text_rect1)
        self.screen.blit(shadow_surface2, shadow_rect2)
        self.screen.blit(text_surface2, text_rect2)
        
        pg.display.update()
        
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4]:
                        return AIDifficulty(int(event.unicode))
                elif event.type == pg.QUIT:
                    return None
        return None

    def show_win_notification(self, winner):
        """Display the winner notification."""
        font = pg.font.Font(None, 74)
        text = f"{'Red' if winner == 1 else 'Yellow'} Wins!"
        # Change text color to match the winner's color
        text_color = self.RED if winner == 1 else self.YELLOW
        text_surface = font.render(text, True, text_color)
        # Add text shadow for better visibility
        shadow_surface = font.render(text, True, self.BLACK)
        shadow_rect = shadow_surface.get_rect(center=(self.game.width // 2 + 2, self.game.square // 2 + 2))
        text_rect = text_surface.get_rect(center=(self.game.width // 2, self.game.square // 2))
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
        shadow_rect = shadow_surface.get_rect(center=(self.game.width // 2 + 2, self.game.height // 2 + 2))
        text_rect = text_surface.get_rect(center=(self.game.width // 2, self.game.height // 2))
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

    def setup_game(self):
        """Set up the game with AI level and player order selection."""
        # Select AI level
        ai_level = self.show_ai_level_prompt()
        if ai_level is None:
            return False
        
        # Select player order
        player_choice = self.show_player_order_prompt()
        if player_choice is None:
            return False
        
        # Reset the game with these choices
        self.game.reset_game(player_choice, ai_level)
        return True

    def handle_win(self, player):
        """Handle win condition and reset game if needed."""
        if self.game.check_win(player):
            self.show_win_notification(player)
            pg.time.delay(1000)
            if not self.show_continue_prompt():
                return "quit"
            if not self.setup_game():
                return "quit"
            return True
        return False

    def run(self):
        """Main game loop."""
        if not self.setup_game():  # Initial game setup with player order selection
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
                    col = pos_x // self.game.square
                    
                    current_player = self.game.turn  # Save current player before the move
                    
                    if self.game.drop_piece(col):  # This also toggles the turn
                        self.draw_game()
                        win_status = self.handle_win(current_player)
                        if win_status == "quit":
                            running = False
                            break
                        if not win_status:
                            # AI's turn (if it's now AI's turn after the player's move)
                            if self.game.turn == -1:
                                ai_col = self.game.get_ai_move()
                                current_ai = self.game.turn  # Save AI's turn
                                if self.game.drop_piece(ai_col):  # This also toggles the turn back to player
                                    self.draw_game()
                                    win_status = self.handle_win(current_ai)
                                    if win_status == "quit":
                                        running = False
                                        break
                                        
                        self.draw_game()
                        
        pg.quit()

# Start the game
if __name__ == "__main__":
    game = ConnectFour()
    renderer = GameRenderer(game)
    renderer.run()
