from copy import deepcopy
import random

def get_move(game, turn):
    """AI that checks for winning moves and blocks opponent's winning moves.
    
    Args:
        game: The game instance
        turn: The current turn (1 for red, -1 for yellow)
        
    Returns:
        int: Column index for the move
    """
    opponent = -turn
    
    # Try to win in one move
    for i in range(game.columns):
        game_clone = deepcopy(game)
        if game_clone.drop_piece(i, turn) and game_clone.check_win(turn):
            return i
    
    # Block opponent's winning move
    for i in range(game.columns):
        game_clone = deepcopy(game)
        if game_clone.drop_piece(i, opponent) and game_clone.check_win(opponent):
            return i

    avoid = []
    # Look ahead to avoid moves that allow opponent to win next turn
    for i in range(game.columns):
        game_clone = deepcopy(game)
        if game_clone.drop_piece(i, turn):
            if game_clone.drop_piece(i, opponent) and game_clone.check_win(opponent):
                avoid.append(i)
    
    if avoid:
        valid_columns = [c for c in range(game.columns) if c not in avoid and game.board[0][c] == 0]
        return random.choice(valid_columns) if valid_columns else 0

    # If no strategic move found, choose a random valid column
    valid_columns = [c for c in range(game.columns) if game.board[0][c] == 0]
    return random.choice(valid_columns) if valid_columns else 0
