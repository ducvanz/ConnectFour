from copy import deepcopy
import random

def get_move(game, turn):
    """Enhanced AI that looks ahead three moves.
    
    Args:
        game: The game instance
        turn: The current turn (1 for red, -1 for yellow)
        
    Returns:
        int: Column index for the move
    """
    opponent = -turn
    
    # Try to win in one move
    for i in range(game.columns):
        ai_board = deepcopy(game.board)
        if game.drop_piece(ai_board, i, turn) and game.check_win(ai_board, turn):
            return i
    
    # Block opponent's winning move
    for i in range(game.columns):
        ai_board = deepcopy(game.board)
        if game.drop_piece(ai_board, i, opponent) and game.check_win(ai_board, opponent):
            return i
    
    # Look ahead to avoid moves that allow opponent to win next turn
    for i in range(game.columns):
        ai_board = deepcopy(game.board)
        if game.drop_piece(ai_board, i, turn):
            # Check if this move creates a winning opportunity for opponent
            for j in range(game.columns):
                ai_board_2 = deepcopy(ai_board)
                if game.drop_piece(ai_board_2, j, opponent) and game.check_win(ai_board_2, opponent):
                    # Found a problematic move, avoid column i
                    break
            else:
                # No winning move for opponent after this move, so it's safe
                return i
    
    # If no strategic move found, choose a random valid column
    valid_columns = [c for c in range(game.columns) if game.board[0][c] == 0]
    return random.choice(valid_columns) if valid_columns else 0
