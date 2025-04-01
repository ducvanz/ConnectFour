import numpy as np
import random

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from Constant import RED, YELLOW, VOID, IDLE

Three_Line = np.array([1, 1, 1, 1])
Two_type1 = np.array([0, 1, 1, 0])
Two_type2 = np.array([0, 1, 0, 1, 0])


CONNECT4 = 8                # Place we must block immediately
BENEATH_CONNECT4 = -2       # Place that don't touching it
TWO_SIDE = 4                # Place that should block soon

class Detection:
    def __init__(self, game) :
        self.matrix = game.board
        self.rows, self.cols = self.matrix.shape
        padding = np.full((1, self.cols), VOID)
        self.matrix = np.vstack((self.matrix, padding))

        self.insight = {
            RED: [set(), set(), set(), set(), set()],
            YELLOW: [set(), set(), set(), set(), set()]
        }
        
        self.visual = {RED: np.zeros(shape=(self.rows, self.cols), dtype=int),
                       YELLOW: np.zeros(shape=(self.rows, self.cols), dtype=int)}

    def three_straight(self, color:int) :
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

        for r in range(self.rows-4, -1, -1) :
            for c in range(self.cols-3) :
                crop = self.matrix[r:r+4, c:c+4]

                for i in range(4) :
                    # Horizontal
                    s = np.nonzero(crop[i,:] - Three_Line * color)[0]     # index 3 RED pieces thẳng hàng
                    if (len(s) == 1) and (crop[i, s[0]] == IDLE) :  # YELLOW
                        self.insight[color][0].add((r+i, int(c+s[0])))

                    # Vertical
                    s = np.nonzero(crop[:, i].T - Three_Line * color)[0] 
                    if (len(s) == 1) and (crop[s[0], i] == IDLE) :
                        self.insight[color][0].add((int(r+s[0]), c+i))

                # diagonal
                main_diag = np.diag(crop)           # chéo chính
                anti_diag = np.fliplr(crop).diagonal()        # chéo phụ

                # diagonal down \
                s = np.nonzero(main_diag - Three_Line * color)[0] 
                if (len(s) == 1) and (crop[s[0], s[0]] == IDLE) :
                    self.insight[color][0].add((int(r+s[0]), int(c+s[0])))
                
                # diagonal up /
                s = np.nonzero(anti_diag - Three_Line * color)[0] 
                if (len(s) == 1) and (crop[s[0], 3-s[0]] == IDLE) :
                    self.insight[color][0].add((int(r+s[0]), int(c+3-s[0])))

    def two_straight_type_1(self, color) : 
        """
        Detect two pieces straight up with open head, type 1. 
        Somekind like: _**_

        Args:
            color:      The color we want to looking at. Constant.RED or Constant.YELLOW.
        
        Side Effect:
            insight(color)[1] will store 2 tuple of 2 empty position
        """

        for r in range(self.rows-4, -1, -1) :
            for c in range(self.cols-3) :
                crop = self.matrix[r:r+4, c:c+4]

                for i in range(4) :
                    # Horizontal
                    if (np.count_nonzero(self.matrix[r+i+1, c:c+4]) != 4) :
                        continue
                    s = np.nonzero(crop[i,:] - Two_type1 * color)[0]  
                    if (len(s) == 0) :
                        self.insight[color][1].add(((r+i, c), (r+i, c+3)))

                # diagonal
                main_diag = np.diag(crop)           # chéo chính
                anti_diag = np.fliplr(crop).diagonal()        # chéo phụ
                beneath = self.matrix[r+1:r+5, c:c+4]

                if (np.count_nonzero(np.diag(beneath)) == 4) :
                    # diagonal down \
                    s = np.nonzero(main_diag - Two_type1 * color)[0]
                    if (len(s) == 0) :
                        self.insight[color][1].add(((r, c), (r+3, c+3)))
                
                if (np.count_nonzero(np.fliplr(beneath).diagonal()) == 4) :
                    # diagonal up /
                    s = np.nonzero(anti_diag - Two_type1 * color)[0]
                    if (len(s) == 0) :
                        self.insight[color][1].add(((r+3, c), (r, c+3)))

    def two_straight_type_2(self, color) : 
        """
        Detect two pieces straight up with open head, type 2. 
        Somekind like: _*_*_

        Args:
            color:      The color we want to looking at. Constant.RED or Constant.YELLOW.
        
        Side effect:
            insight(color)[2] will store 3 tuple of 3 empty position
        """

        for r in range(self.rows-5, -1, -1) :
            for c in range(self.cols-4) :
                crop = self.matrix[r:r+5, c:c+5]

                for i in range(5) :
                    # Horizontal
                    if (np.count_nonzero(self.matrix[r+i+1, c:c+5]) != 5) :
                        continue
                    s = np.nonzero(crop[i,:] - Two_type2 * color)[0] 
                    if (len(s) == 0) :
                        self.insight[color][2].add(((r+i, c), (r+i, c+2), (r+i, c+4)))

                # diagonal
                main_diag = np.diag(crop)           # chéo chính
                anti_diag = np.fliplr(crop).diagonal()        # chéo phụ
                beneath = self.matrix[r+1:r+6, c:c+5]

                if (np.count_nonzero(np.diag(beneath)) == 5) :
                    # diagonal down \
                    s = np.nonzero(main_diag - Two_type2 * color)[0]
                    if (len(s) == 0) :
                        self.insight[color][2].add(((r, c), (r+2, c+2), (r+4, c+4)))
                
                if (np.count_nonzero(np.fliplr(beneath).diagonal()) == 5) :
                    # diagonal up /
                    s = np.nonzero(anti_diag - Two_type2 * color)[0]
                    if (len(s) == 0) :
                        self.insight[color][2].add(((r+4, c), (r+2, c+2), (r, c+4)))

    def make_visualize(self, color) :
        x = self.visual[color]
        insight = self.insight[color]
        matrix = self.matrix

        for p in insight[0] :
            if matrix[p[0] + 1, p[1]] != IDLE :
                x[p[0], p[1]] += CONNECT4
            else :
                x[p[0] + 1, p[1]] += BENEATH_CONNECT4
        
        for p in insight[1] :
            x[p[0][0], p[0][1]] += TWO_SIDE
            x[p[1][0], p[1][1]] += TWO_SIDE

        for p in insight[2] :
            x[p[0][0], p[0][1]] += TWO_SIDE
            x[p[1][0], p[1][1]] += TWO_SIDE * 1.5
            x[p[2][0], p[2][1]] += TWO_SIDE

    def get_visualize(self, color) :
        return self.visual[color]

    def run(self, color) :
        self.three_straight(color)
        self.two_straight_type_1(color)
        self.two_straight_type_2(color)

        self.make_visualize(color)


def get_move(game, color=None) :

    if color is None:
        color = game.turn

    detect = Detection(game)
    detect.run(-color)
    prior = detect.get_visualize(-color)

    available = game.get_available()
    if (len(available) == 0) :
        return random.choice(range(7))

    for i in range(prior.shape[1]) :
        if i not in available :
            prior.T[i] = np.zeros(shape=(prior.shape[0],))
    
    row, col = np.unravel_index(np.argmax(prior), prior.shape)

    if (prior[row, col] <= 0) :
        col = random.choice(available)

    return col


#Test
# test = ConnectFour()
# test.board = np.array([ [0, 0, 1, 1, 0, 0, 0, 0, 0],
#                         [0, 7, 7, 7, 7, 0, 0, 0, 0],
#                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                         [1, 1, 0, 0, 0, 0, 0, 0, 0],
#                         [1, 1, 1, 0, 0, 0, 0, 0, 0],
#                         [1, 1, 1, 0, 0, 1, 0, 1, 0]])

# detect = Detection(test)
# detect.run(1)
# print(detect.insight)
# print(detect.get_visualize(1))



