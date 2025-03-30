import random
import time
from copy import deepcopy
from math import sqrt, log

def select(game, counts, wins, losses, temperature):
    """Select a move based on UCT score."""
    # Calculate the UCT score for all next moves
    scores = {}
    for k in range(game.columns):
        # Skip columns that are already full
        if game.board[0][k] != 0:
            continue
            
        # The ones not visited get the priority
        if counts.get(k, 0) == 0:
            scores[k] = 100000
        else:
            scores[k] = (wins.get(k, 0) - losses.get(k, 0)) / counts[k] + \
                temperature * sqrt(log(sum(counts.values())) / counts[k])
    
    # If no valid moves (all columns full), return a random column
    if not scores:
        return random.randint(0, game.columns - 1)
        
    # Select the next move with the highest UCT score
    return max(scores, key=scores.get)

def expand(game, move):
    """Create a new game state by applying the move."""
    game_copy = deepcopy(game)
    # Check if the move is valid before applying
    if move < 0 or move >= game_copy.columns or game_copy.board[0][move] != 0:
        # Return None for invalid moves
        return None
        
    game_copy.drop_piece(move)
    return game_copy

def is_board_full(game):
    """Check if the board is full (draw condition)."""
    return all(game.board[0][c] != 0 for c in range(game.columns))

def simulate(game_clone):
    """Simulate a random game from the current state until completion."""
    # Check if the game is already over
    if game_clone.check_win(-game_clone.turn):
        return -game_clone.turn
    
    # Check for a draw
    if is_board_full(game_clone):
        return 0
    
    # Limit simulation to a reasonable number of moves
    move_limit = 42  # Maximum possible moves in a 6x7 board
    move_count = 0
    
    # Make random moves until the game is over
    while move_count < move_limit:
        # Get all valid columns
        valid_columns = [c for c in range(game_clone.columns) if game_clone.board[0][c] == 0]
        
        # If no valid moves, it's a draw
        if not valid_columns:
            return 0
            
        move = random.choice(valid_columns)
        
        if game_clone.drop_piece(move):
            # Check if the last move resulted in a win
            if game_clone.check_win(-game_clone.turn):
                return -game_clone.turn
                
            # Check for a draw
            if is_board_full(game_clone):
                return 0
                
            move_count += 1
        else:
            # If move couldn't be made (column full), try another one
            continue
    
    # If we've reached the move limit without a conclusion, return a draw
    return 0
        
def backpropagate(turn, move, reward, counts, wins, losses):
    """Update the statistics for the move based on simulation result."""
    counts[move] = counts.get(move, 0) + 1
    if reward == turn:
        wins[move] = wins.get(move, 0) + 1
    elif reward != 0:  # Only count as loss if not a draw
        losses[move] = losses.get(move, 0) + 1
    return counts, wins, losses

def next_move(counts, wins, losses, valid_columns):
    """Determine the best move based on statistics."""
    # See which action is most promising
    scores = {}
    for k in valid_columns:
        if k not in counts or counts[k] == 0:
            scores[k] = 0
        else:
            # Calculate score as win rate
            scores[k] = (wins.get(k, 0) - losses.get(k, 0)) / counts[k]
    
    if not scores:
        return random.choice(valid_columns) if valid_columns else 0
        
    return max(scores, key=scores.get)

def get_move(game, num_rollouts=1000, temperature=sqrt(2), max_time=1.0):
    """Run Monte Carlo Tree Search to find the best move.
    
    Args:
        game: The ConnectFour game instance
        num_rollouts: Maximum number of simulations to run
        temperature: Exploration parameter
        max_time: Maximum time in seconds to run simulations
    
    Returns:
        The best move as column index
    """
    # Get valid columns (non-full columns)
    valid_columns = [c for c in range(game.columns) if game.board[0][c] == 0]
    
    # If only one valid move, return it immediately
    if len(valid_columns) == 1:
        return valid_columns[0]
    
    # If no valid moves, return a random column
    if not valid_columns:
        return random.randint(0, game.columns - 1)
    
    # Initialize statistics
    counts = {move: 0 for move in range(game.columns)}
    wins = {move: 0 for move in range(game.columns)}
    losses = {move: 0 for move in range(game.columns)}
    
    start_time = time.time()
    rollouts_completed = 0
    
    # Run simulations until we reach the limit or timeout
    while rollouts_completed < num_rollouts and (time.time() - start_time) < max_time:
        try:
            # Select a move to simulate
            move = select(game, counts, wins, losses, temperature)
            
            # Expand the game state with the selected move
            game_clone = expand(game, move)
            
            # Skip invalid moves
            if game_clone is None:
                continue
                
            # Simulate a random game from this state
            reward = simulate(game_clone)
            
            # Update statistics
            counts, wins, losses = backpropagate(game.turn, move, reward, counts, wins, losses)
            
            rollouts_completed += 1

            # print(counts.values(), ' ', wins.values(), ' ', losses.values(), '\n')
            
        except Exception as e:
            print(f"Error in MCTS simulation: {e}")
            break
    
    # Choose the best move based on the statistics
    return next_move(counts, wins, losses, valid_columns)