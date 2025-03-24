import random
from copy import deepcopy
from math import sqrt, log

def select(game,counts,wins,losses,temperature):
    # calculate the uct score for all next moves
    scores={}
    for k in range(game.columns):
        # the ones not visited get the priority
        if counts.get(k,0)==0:
            scores[k]=100000
        else:
            scores[k]=(wins.get(k,0)-losses.get(k,0))/counts[k] + \
                temperature*sqrt(log(sum(counts.values()))/counts[k])
    # Select the next move with the highest UCT score
    return max(scores,key=scores.get)

def expand(game,move):
    game_copy=deepcopy(game)
    game_copy.drop_piece(move)
    return game_copy

def simulate(game_clone):
    # Check if the game is over
    if game_clone.check_win(-game_clone.turn):
        return -game_clone.turn
    while True:
        move=random.choice(range(game_clone.columns))
        if game_clone.drop_piece(move):
            if game_clone.check_win(-game_clone.turn):
                return -game_clone.turn
        if all(game_clone.board[0][c] != 0 for c in range(game_clone.columns)):
            return 0
        
def backpropagate(turn,move,reward,counts,wins,losses):
    counts[move]=counts.get(move,0)+1
    if reward==turn:
        wins[move]=wins.get(move,0)+1
    else:
        losses[move]=losses.get(move,0)+1
    return counts,wins,losses

def next_move(counts,wins,losses):
    # See which action is most promising
    scores={}
    for k,v in counts.items():
        if v==0:
            scores[k]=0
        else:
            scores[k]=(wins.get(k,0)-losses.get(k,0))/v
    return max(scores,key=scores.get)

def mcts(game,num_rollouts=1000,temperature=sqrt(2)):
    counts={}
    wins={}
    losses={}
    for move in range(game.columns):
        counts[move]=0
        wins[move]=0
        losses[move]=0
    for _ in range(num_rollouts):
        move=select(game,counts,wins,losses,temperature)
        game_clone=expand(game,move)
        reward=simulate(game_clone)
        counts,wins,losses=backpropagate(game.turn,move,reward,counts,wins,losses)
    return next_move(counts,wins,losses)