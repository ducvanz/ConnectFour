from copy import deepcopy
import random

def get_move(game):
    """Enhanced AI that looks ahead three moves.
    
    Args:
        game: The game instance
        
    Returns:
        int: Column index for the move
    """
    turn = game.turn  # Use the game's current turn
    opponent = -turn
    
    # Try to win in one move
    for i in range(game.columns):
        game_clone = deepcopy(game)
        if game_clone.drop_piece(i) and game_clone.check_win(turn):
            return i
    
    # Block opponent's winning move
    for i in range(game.columns):
        game_clone = deepcopy(game)
        game_clone.turn = opponent  # Set the turn to opponent for the clone
        if game_clone.drop_piece(i) and game_clone.check_win(opponent):
            return i
    
    avoid = []
    # Look ahead to avoid moves that allow opponent to win next turn
    for i in range(game.columns):
        game_clone = deepcopy(game)
        if game_clone.drop_piece(i):  # This changes turn to opponent
            # Check if dropping in the same column would give opponent a win
            if game_clone.drop_piece(i) and game_clone.check_win(opponent):
                avoid.append(i)
    
    if avoid:
        valid_columns = [c for c in range(game.columns) if c not in avoid and game.board[0][c] == 0]
        return random.choice(valid_columns) if valid_columns else 0

    w3 = []
    # Look ahead three moves
    for i in range(game.columns):
        game_clone = deepcopy(game)
        if game_clone.drop_piece(i):  # This changes turn to opponent
            for j in range(game.columns):
                game_clone2 = deepcopy(game_clone)
                if game_clone2.drop_piece(j):  # This changes turn back to original player
                    for k in range(game.columns):
                        game_clone3 = deepcopy(game_clone2)
                        if game_clone3.drop_piece(k) and game_clone3.check_win(turn):
                            w3.append(i)
    
    # If no strategic move found, choose a random valid column
    valid_columns = [c for c in range(game.columns) if game.board[0][c] == 0]
    return random.choice(valid_columns) if valid_columns else 0
