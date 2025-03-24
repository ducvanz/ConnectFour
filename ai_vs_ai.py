import pygame as pg
import time
import argparse
from AIconnect4 import ConnectFour, AIDifficulty
import random

class AIvsAI:
    # Colors
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    
    def __init__(self, ai1_level=AIDifficulty.LEVEL_3, ai2_level=AIDifficulty.LEVEL_3, 
                 display_game=True, delay=0.5, games=1, ai1_timeout=None, ai2_timeout=None):
        """Initialize the AI vs AI game runner.
        
        Args:
            ai1_level: Difficulty level for AI 1 (Red)
            ai2_level: Difficulty level for AI 2 (Yellow)
            display_game: Whether to show the game graphically
            delay: Delay between moves in seconds (for visualization)
            games: Number of games to play
            ai1_timeout: Maximum time in seconds for AI 1 to compute a move
            ai2_timeout: Maximum time in seconds for AI 2 to compute a move
        """
        self.game = ConnectFour()
        self.ai1_level = ai1_level
        self.ai2_level = ai2_level
        self.display_game = display_game
        self.delay = delay
        self.games = games
        self.ai1_timeout = ai1_timeout
        self.ai2_timeout = ai2_timeout
        self.stats = {"ai1_wins": 0, "ai2_wins": 0, "draws": 0}
        
        # AI level names for better readability
        self.ai_names = {
            AIDifficulty.LEVEL_1: "Think One",
            AIDifficulty.LEVEL_2: "Think Two",
            AIDifficulty.LEVEL_3: "Think Three",
            AIDifficulty.LEVEL_4: "Monte Carlo Tree Search"
        }
        
        # Initialize pygame if needed
        if self.display_game:
            pg.init()
            self.screen = pg.display.set_mode((self.game.width, self.game.height))
            pg.display.set_caption(f"AI vs AI - {self.ai_names[ai1_level]} vs {self.ai_names[ai2_level]}")
    
    def draw_game(self):
        """Draw the current game state on the screen."""
        if not self.display_game:
            return
            
        self.screen.fill(self.WHITE)
        
        # Draw turn indicator
        font = pg.font.Font(None, 40)
        ai1_name = f"Red ({self.ai_names[self.ai1_level]})"
        ai2_name = f"Yellow ({self.ai_names[self.ai2_level]})"
        text_surface = font.render(f"Turn: {ai1_name if self.game.turn == 1 else ai2_name}", True, self.BLACK)
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
    
    def show_win_notification(self, winner):
        """Display the winner notification."""
        if not self.display_game:
            return
            
        font = pg.font.Font(None, 64)
        if winner == 0:
            text = "Draw!"
            text_color = self.BLUE
        else:
            ai_name = self.ai_names[self.ai1_level if winner == 1 else self.ai2_level]
            text = f"{'Red' if winner == 1 else 'Yellow'} ({ai_name}) Wins!"
            text_color = self.RED if winner == 1 else self.YELLOW
            
        text_surface = font.render(text, True, text_color)
        # Add text shadow for better visibility
        shadow_surface = font.render(text, True, self.BLACK)
        shadow_rect = shadow_surface.get_rect(center=(self.game.width // 2 + 2, self.game.square // 2 + 2))
        text_rect = text_surface.get_rect(center=(self.game.width // 2, self.game.square // 2))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(text_surface, text_rect)
        pg.display.update()
    
    def show_stats(self):
        """Display statistics after all games."""
        ai1_name = self.ai_names[self.ai1_level]
        ai2_name = self.ai_names[self.ai2_level]
        
        if not self.display_game:
            print(f"\nResults after {self.games} games:")
            print(f"Red ({ai1_name}): {self.stats['ai1_wins']} ({self.stats['ai1_wins']/self.games*100:.1f}%)")
            print(f"Yellow ({ai2_name}): {self.stats['ai2_wins']} ({self.stats['ai2_wins']/self.games*100:.1f}%)")
            print(f"Draws: {self.stats['draws']} ({self.stats['draws']/self.games*100:.1f}%)")
            return
            
        self.screen.fill(self.WHITE)
        font = pg.font.Font(None, 50)
        
        title = f"Results after {self.games} games:"
        text1 = f"Red ({ai1_name}): {self.stats['ai1_wins']} ({self.stats['ai1_wins']/self.games*100:.1f}%)"
        text2 = f"Yellow ({ai2_name}): {self.stats['ai2_wins']} ({self.stats['ai2_wins']/self.games*100:.1f}%)"
        text3 = f"Draws: {self.stats['draws']} ({self.stats['draws']/self.games*100:.1f}%)"
        text4 = "Press any key to exit"
        
        y_pos = self.game.height // 2 - 100
        for text in [title, text1, text2, text3, text4]:
            text_surface = font.render(text, True, self.BLACK)
            text_rect = text_surface.get_rect(center=(self.game.width // 2, y_pos))
            self.screen.blit(text_surface, text_rect)
            y_pos += 50
        
        pg.display.update()
        
        waiting = True
        while waiting and self.display_game:
            for event in pg.event.get():
                if event.type in [pg.QUIT, pg.KEYDOWN]:
                    waiting = False
    
    def is_board_full(self):
        """Check if the board is full (draw condition)."""
        return all(self.game.board[0][c] != 0 for c in range(self.game.columns))
    
    def play_game(self):
        """Play a single game between two AI agents."""
        # Reset game state
        self.game.board = self.game.create_board()
        self.game.turn = 1  # Red goes first
        
        self.draw_game()
        game_over = False
        winner = 0
        
        # Process events to keep pygame responsive
        if self.display_game:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return None
        
        move_timeout = 1  # Maximum time in seconds to wait for an AI move
        
        # Main game loop
        while not game_over:
            # Set AI level and timeout based on whose turn it is
            current_timeout = None
            if self.game.turn == 1:
                self.game.ai_level = self.ai1_level
                current_ai_name = self.ai_names[self.ai1_level]
                current_timeout = self.ai1_timeout
            else:
                self.game.ai_level = self.ai2_level
                current_ai_name = self.ai_names[self.ai2_level]
                current_timeout = self.ai2_timeout
            
            # Get AI move and apply it
            current_player = self.game.turn
            
            # Use a timeout for the AI move to prevent hanging
            move_start_time = time.time()
            try:
                # Update caption to show thinking state
                if self.display_game:
                    pg.display.set_caption(f"AI vs AI - {current_ai_name} is thinking...")
                
                col = self.game.get_ai_move(timeout=current_timeout)
                
                # Reset caption
                if self.display_game and self.games > 1:
                    ai1_name = self.ai_names[self.ai1_level]
                    ai2_name = self.ai_names[self.ai2_level]
                    pg.display.set_caption(f"AI vs AI - {ai1_name} vs {ai2_name}")
                
                # Record actual compute time for debugging
                compute_time = time.time() - move_start_time
                if compute_time > 1.2:  # Only report if it took more than the threshold
                    print(f"{current_ai_name} computed move in {compute_time:.2f}s")
                    
                # Validate the move before applying
                if col < 0 or col >= self.game.columns or self.game.board[0][col] != 0:
                    # Invalid move, choose a random valid column
                    valid_columns = [c for c in range(self.game.columns) if self.game.board[0][c] == 0]
                    if valid_columns:
                        col = random.choice(valid_columns)
                    else:
                        # No valid moves, game is a draw
                        game_over = True
                        self.stats["draws"] += 1
                        continue
            
            except Exception as e:
                print(f"Error in AI move generation: {e}")
                # Choose a random valid column as fallback
                valid_columns = [c for c in range(self.game.columns) if self.game.board[0][c] == 0]
                if valid_columns:
                    col = random.choice(valid_columns)
                else:
                    # No valid moves, game is a draw
                    game_over = True
                    self.stats["draws"] += 1
                    continue
            
            if self.game.drop_piece(col):  # This also toggles the turn
                self.draw_game()
                
                # Check for win
                if self.game.check_win(current_player):
                    winner = current_player
                    game_over = True
                    if winner == 1:
                        self.stats["ai1_wins"] += 1
                    else:
                        self.stats["ai2_wins"] += 1
                
                # Check for draw
                elif self.is_board_full():
                    game_over = True
                    self.stats["draws"] += 1
                
                # Add delay for visualization
                if self.display_game and self.delay > 0:
                    time.sleep(self.delay)
        
        # Show the final state and winner
        if self.display_game:
            self.show_win_notification(winner)
            time.sleep(1)  # Give some time to see the winner
        
        return winner
    
    def run(self):
        """Run multiple games between the AI agents."""
        ai1_name = self.ai_names[self.ai1_level]
        ai2_name = self.ai_names[self.ai2_level]
        
        for i in range(self.games):
            if self.display_game and self.games > 1:
                pg.display.set_caption(f"AI vs AI - Game {i+1}/{self.games} - {ai1_name} vs {ai2_name}")
            
            result = self.play_game()
            if result is None:  # User quit
                break
                
            # Print progress if not displaying
            if not self.display_game and self.games > 1:
                print(f"Game {i+1}/{self.games} complete. " +
                      f"Red ({ai1_name}): {self.stats['ai1_wins']}, " +
                      f"Yellow ({ai2_name}): {self.stats['ai2_wins']}, " +
                      f"Draws: {self.stats['draws']}")
        
        self.show_stats()
        
        # Clean up pygame
        if self.display_game:
            pg.quit()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run AI vs AI Connect Four games')
    parser.add_argument('--ai1', type=int, choices=[1, 2, 3, 4], default=3,
                        help='AI level for player 1 (Red) (default: 3 - Think Three)')
    parser.add_argument('--ai2', type=int, choices=[1, 2, 3, 4], default=4,
                        help='AI level for player 2 (Yellow) (default: 4 - Monte Carlo Tree Search)')
    parser.add_argument('--nogui', action='store_true',
                        help='Run without graphical display')
    parser.add_argument('--delay', type=float, default=0.5,
                        help='Delay between moves in seconds (default: 0.5)')
    parser.add_argument('--games', type=int, default=1,
                        help='Number of games to play (default: 1)')
    parser.add_argument('--timeout1', type=float, 
                        help='Timeout for AI 1 in seconds (default: based on AI level)')
    parser.add_argument('--timeout2', type=float,
                        help='Timeout for AI 2 in seconds (default: based on AI level)')
    parser.add_argument('--timeout', type=float,
                        help='Timeout for both AIs in seconds (overrides individual timeouts)')
    
    args = parser.parse_args()
    
    # Handle timeouts
    ai1_timeout = args.timeout1
    ai2_timeout = args.timeout2
    
    # Global timeout overrides individual timeouts
    if args.timeout is not None:
        ai1_timeout = args.timeout
        ai2_timeout = args.timeout
    
    # Set up the AI vs AI game
    ai_vs_ai = AIvsAI(
        ai1_level=AIDifficulty(args.ai1),
        ai2_level=AIDifficulty(args.ai2),
        display_game=not args.nogui,
        delay=args.delay,
        games=args.games,
        ai1_timeout=ai1_timeout,
        ai2_timeout=ai2_timeout
    )
    
    # Run the games
    ai_vs_ai.run()

if __name__ == '__main__':
    main()
