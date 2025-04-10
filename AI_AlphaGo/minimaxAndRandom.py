import numpy as np
import random

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Simulation.Board import ConnectFourBoard
from AI_AlphaGo.minimaxVsABPrunning import MinimaxAI, DEFAULT_WEIGHT
from Constant import RED, YELLOW, IDLE 

class MinimaxAndRandom :
    def __init__ (self, random_percent_start=0.5, random_percent_end=0.1, depth=5, weight=DEFAULT_WEIGHT, notPrunning=False, eor=0.8) :
        self.rand_range = random_percent_start - random_percent_end
        self.rand_min = random_percent_end

        self.org_name = 'Randomize Minimax'
        self.name = self.org_name
        self.color = IDLE

        self.runner = [Random(),
                       MinimaxAI(weight=weight, depth=depth, notPrunning=notPrunning)]

        self.eor = eor      # Board được phủ kín bao nhiêu % thì ngừng giảm tỉ lệ random. Càng lớn thì tỉ lệ random kéo dài càng cao

        self.stat = {'Random': 0,
                     'Minimax': 0}

    def set_color(self, color) :
        self.color = color

    def get_move(self, game:ConnectFourBoard) :
        empty_percent = np.sum(game.board == IDLE) / (game.rows * game.columns)
        p = self.rand_min + self.rand_range * empty_percent * self.eor

        if random.random() < p :
            current_runner = self.runner[0]
            self.stat['Random'] += 1
        else :
            current_runner = self.runner[1]
            self.stat['Minimax'] += 1

        self.name = self.org_name + ':' + current_runner.name
        current_runner.set_color(self.color)
        return current_runner.get_move(game)


class Random :
    """
    A kind of ThinkTwo, but more sensitive with critical move
    """

    def __init__ (self) :
        self.color = IDLE
        self.name = 'Clever Random'
    
    def set_color(self, color) :
        self.color = color

    def get_move(self, game:ConnectFourBoard):
        temp, near_end = three_straight(game, self.color)       # if enemy not blocking, make him pay
        if (temp != None) :
            return temp, None

        temp, avoid = three_straight(game, -self.color)        # _*** defense
        if (temp != None) :
            return temp, None
        
        for i in near_end :             # if a move is critical, but no need to avoid, pressing it
            if i not in avoid :
                return i, None
            
        temp = two_straight_type_1(game, self.color)   # _**_ attack
        if (temp != None) :
            return temp, None
        
        temp = two_straight_type_2(game, self.color)   # _*_*_ attack
        if (temp != None) :
            return temp, None

        temp = two_straight_type_1(game, -self.color)   # _**_ defense
        if (temp != None) :
            return temp, None
        
        temp = two_straight_type_2(game, -self.color)   # _*_*_ defense
        if (temp != None) :
            return temp, None
        
        valid_move = game.get_available_columns()
        i = 0
        while i < len(valid_move):
            if valid_move[i] in avoid :
                valid_move.pop(i)
            else :
                i += 1

        if len(valid_move) == 0 :
            return random.choice(game.get_available_columns()), None
        return random.choice(valid_move), None

def three_straight(game:ConnectFourBoard, color:int) :
    """
    Detect three pieces straight up. 
    Somekind like: **_*.
    We don't care about  fifth element, because even so, it's too late to fight back
    Find 2 position like this, dead end
    Args:
        color:      The color we want to looking at. Constant.RED or Constant.YELLOW.
        
    Side Effect:
        insight(color)[0] store the position must have to be filled. No other option
    """

    def detection(arr:np.array) :
        if (np.sum(arr == color) == 3) :
            res = np.where(arr == IDLE)[0]
            if (res.size == 1) :
                return res[0].astype(int)
            else :
                return None
                 
    avoid = set()
    for r in range(game.rows) :
        for c in range(game.columns - 3):
            temp = None
            temp = detection(game.board[r, c:c+4])
            if (temp != None) :
                if (r+1 == game.rows) or (game.board[r+1, c+temp] != IDLE ) :
                    return c + temp, None
                if (r+2 == game.rows) or (game.board[r+2, c+temp] != IDLE ) :
                    avoid.add(c+temp)
    for r in range(game.rows - 3) :
        for c in range(game.columns) :
            temp = None            
            temp = detection(game.board[r:r+4, c])
            if (temp != None) :
                return c, None
    for r in range(game.rows - 3) :
        for c in range(game.columns - 3):
            temp = None
            temp = detection(np.diag(game.board[r:r+4, c:c+4]))
            if (temp != None) :
                if (r+temp+1 == game.rows) or (game.board[r+temp+1, c+temp] != IDLE) :
                    return c + temp, None
                if (r+temp+2 == game.rows) or (game.board[r+temp+2, c+temp] != IDLE) :
                    avoid.add(c+temp)
        for c in range(4, game.columns+1):
            temp = None
            temp = detection(np.diag(np.fliplr(game.board[r:r+4, c-4:c])))
            if (temp != None) :
                if (r+temp+1 == game.rows) or (game.board[r+temp+1, c-1-temp] != IDLE) :
                    return c - 1 - temp, None
                if (r+temp+2 == game.rows) or (game.board[r+temp+2, c-1-temp] != IDLE) :
                    avoid.add(c-1-temp)
    return None, avoid

def two_straight_type_1(game:ConnectFourBoard, color:int) : 
    """
    Detect two pieces straight up with open head, type 1. 
    Somekind like: _**_
    Args:
        color:      The color we want to looking at. Constant.RED or Constant.YELLOW.
        
    Side Effect:
        insight(color)[1] will store 2 tuple of 2 empty position
    """

    def detection(arr:np.array) :
        if np.sum(arr - np.array([IDLE, color, color, IDLE]) == 0) == 4:
            return True
        return False
    
    for r in range(game.rows) :
        for c in range(game.columns-3) :
            if detection(game.board[r, c:c+4]) :
                    if (r == game.rows-1) or ((game.board[r+1,c] != IDLE) and (game.board[r+1,c+3] != IDLE)) :
                        if c + 2 > game.columns // 2 :
                            if game.board[r, c-1] == IDLE:
                                return c
                            return c + 3
                        else :
                            if game.board[r, c+4] == IDLE :
                                return c+3
                            return c
    for r in range(game.rows - 3) :
        for c in range(game.columns - 3):
            if detection(np.diag(game.board[r:r+4, c:c+4])) :
                if  (game.board[r+1,c] != IDLE) and ((r+4 == game.rows) or (game.board[r+4,c+3] != IDLE)) :
                    if c+1 > game.columns // 2 :
                        if r > 0 and game.board[r-1, c-1] == IDLE:
                            return c
                        return c + 3
                    else :
                        if r + 5 < game.rows and game.board[r+5, c+4] == IDLE :
                            return c+3
                        return c
        for c in range(4, game.columns+1):
            if detection(np.diag(np.fliplr(game.board[r:r+4, c-4:c]))) :
                if (game.board[r+1, c-1] != IDLE) and ((r+4 == game.rows) or (game.board[r+4, c-4] != IDLE)) :
                    if c-3 > game.columns // 2 :
                        if r + 5 < game.rows and game.board[r+5, c-5] == IDLE:
                            return c - 4
                        return c - 1
                    else :
                        if r > 0 and game.board[r-1, c] == IDLE :
                            return c-1
                        return c-4
    return None

def two_straight_type_2(game:ConnectFourBoard, color:int) : 
    """
    Detect two pieces straight up with open head, type 2. 
    Somekind like: _*_*_
    Args:
        color:      The color we want to looking at. Constant.RED or Constant.YELLOW.
        
    Side effect:
        insight(color)[2] will store 3 tuple of 3 empty position
    """

    def detection(arr:np.array) :
        if np.sum(arr - np.array([IDLE, color, IDLE, color, IDLE]) == 0) == 5:
            return True
        return False
    
    for r in range(game.rows) :
        for c in range(game.columns - 4) :
            if detection(game.board[r, c:c+5]) :
                if (r+1 == game.rows) or ((game.board[r+1,c] != IDLE) and (game.board[r+1,c+2] != IDLE) and (game.board[r+1,c+4] != IDLE)) :
                    return c + 2
                 
    for r in range(game.rows - 4) :
        for c in range(game.columns - 4):
            if detection(np.diag(game.board[r:r+5, c:c+5])) :
                if  (game.board[r+1,c] != IDLE) and (game.board[r+3,c+2] != IDLE) and ((r+5 == game.rows) or (game.board[r+5,c+4] != IDLE)) :
                    return c + 2
        for c in range(5, game.columns+1):
                if detection(np.diag(np.fliplr(game.board[r:r+5, c-5:c]))) :
                    if (game.board[r+1, c-1] != IDLE) and (game.board[r+3, c-3] != IDLE) and ((r+5 == game.rows) or (game.board[r+5, c-5] != IDLE)) :
                        return c - 3
    return None