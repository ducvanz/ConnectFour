from copy import deepcopy
import random

def get_move(game, turn):
    """Simple AI that checks for immediate winning moves.
    
    Args:
        game: The game instance
        turn: The current turn (1 for red, -1 for yellow)
        
    Returns:
        int: Column index for the move
    """
    # Try to win in one move
    for i in range(game.columns):
        ai_board = deepcopy(game.board) 
        if game.drop_piece(ai_board, i, turn) and game.check_win(ai_board, turn):
            return i
    
    # If no winning move found, choose a random valid column
    valid_columns = [c for c in range(game.columns) if game.board[0][c] == 0]
    return random.choice(valid_columns) if valid_columns else 0
