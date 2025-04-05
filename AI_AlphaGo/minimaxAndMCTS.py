import random
import numpy as np
import math
import time
from math import sqrt, log
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Simulation.Board import ConnectFourBoard
from AI_AlphaGo.MCTS import select, backpropagate, simulate, expand
from Constant import RED, YELLOW, IDLE 

class minimaxAndMcts:
    def __init__(self, color=RED, timeout=5):
        self.name = "Enhanced Minimax + MCTS"
        self.color = color
        self.max_time = timeout
        self.exploration_factor = sqrt(2)  # tham so cho UCT
        self.max_simulations = 1000
        self.min_simulations = 100 
        self.heuristic_weights = { # tính điểm cho hàm heuristic
            'win': 100,
            'three_in_row': 5,
            'two_in_row': 2,
            'center_control': 3,
            'potential_threats': 6
        }
        self.stats = defaultdict(lambda: {'count': 0, 'wins': 0, 'losses': 0})
        
    def set_color(self, color: int):
        self.color = color
    
    def get_move(self, game: ConnectFourBoard):
        start_time = time.time()
        self.stats.clear()  # Reset stats trước mỗi lượt
        best_move = None
        best_value = -math.inf if self.color == RED else math.inf
        
        available_moves = self.order_moves_by_heuristic(game)
        # print(f"Available moves ordered: {available_moves}")  # Debug
        
        for move in available_moves:
            if time.time() - start_time > self.max_time * 0.9:
                break
                
            temp_game = game.copy()
            temp_game.drop_piece(move)
            
            move_value = self.parallel_mcts(temp_game)
            # print(f"Move {move} value: {move_value}")  # Debug
            
            # Sửa lại logic so sánh CHÍNH XÁC
            if (self.color == RED and move_value > best_value) or \
            (self.color == YELLOW and move_value < best_value) or \
            (best_move is None):
                best_value = move_value
                best_move = move
                # print(f"New best move: {best_move} (value: {best_value})")  # Debug
        
        # Đảm bảo luôn có nước đi hợp lệ
        if best_move is None and available_moves:
            best_move = available_moves[0]
        
        return best_move, best_value
    
    def calculate_depth(self, game:ConnectFourBoard, start_time: time):
        """lấy độ sâu dựa vào thời điểm, càng về sau tính càng lớn"""
        remaining_time = self.max_time - (time.time() - start_time)
        remaining_moves = game.columns - len(game.get_available_columns())
        depth = 0
        if remaining_moves < 5:  # Endgame
            depth = 7
        elif remaining_moves < 10:
            depth = 6
        else:
            depth = 5
        
        # Điều chỉnh theo thời gian còn lại
        time_per_move = remaining_time / (remaining_moves + 1)
        if time_per_move > 0.5:  # Nhiều thời gian thì tăng depth
            depth += 1
        elif time_per_move < 0.2:  # Ít thời gian thì giảm depth
            depth = max(2, depth - 1)
    
    def order_moves_by_heuristic(self, game: ConnectFourBoard):
        """Lấy danh sách các nước đi, ưu tiên cột trung tâm"""
        moves = game.get_available_columns()        # get_columns sắp xếp phân kỳ sẵn rồi.
        return moves
    
    def parallel_mcts(self, game_state):
        start_time = time.time()
        local_stats = self.stats
        
        with ThreadPoolExecutor() as executor:
            futures = []
            for _ in range(self.max_simulations):
                if time.time() - start_time > self.max_time * 0.8:
                    break
                futures.append(executor.submit(
                    self.run_single_simulation, 
                    game_state.copy())
                )
            
            for future in as_completed(futures):
                move, result = future.result()
                if move is not None:
                    local_stats[move]['count'] += 1
                    if result == game_state.turn:
                        local_stats[move]['wins'] += 1
                    elif result != IDLE:
                        local_stats[move]['losses'] += 1
        
        # Merge local stats vào global stats (atomic update)
        for move in local_stats:
            for key in ['count', 'wins', 'losses']:
                self.stats[move][key] += local_stats[move][key]
        
        # Tính toán giá trị trung bình CHÍNH XÁC
        move_values = []
        for move in local_stats:
            if local_stats[move]['count'] > 0:
                value = (local_stats[move]['wins'] - local_stats[move]['losses']) / local_stats[move]['count']
                move_values.append(value)
        
        return sum(move_values)/len(move_values) if move_values else 0
    
    def run_single_simulation(self, game_state: ConnectFourBoard):
        """Run one complete MCTS simulation"""
        current_state = game_state.copy()
        move = self.select_move(current_state)
        result = simulate(expand(current_state, move))
        return move, result
    
    def select_move(self, game_state):
        """Chọn nước đi tốt nhất bằng UCT"""
        legal_moves = list(game_state.get_available_columns())
        if not legal_moves:
            return None
        
        # print(f"Legal moves: {legal_moves}")  # Debug
        # print(f"Current stats: { {m: self.stats[m] for m in legal_moves} }")  # Debug
        
        # Đảm bảo ít nhất 1 move được thử nghiệm
        unexplored = [m for m in legal_moves if self.stats[m]['count'] == 0]
        if unexplored:
            return random.choice(unexplored)
    
        # Chọn theo UCT
        best_move = max(legal_moves, key=lambda m: self.uct_value(game_state, m))
        # print(f"Selected move: {best_move}")  # Debug
        return best_move
    
    def uct_value(self, game_state, move):
        parent_visits = sum(self.stats[m]['count'] for m in game_state.get_available_columns())
        if parent_visits == 0:
            return float('inf')
        
        move_stats = self.stats[move]
        if move_stats['count'] == 0:
            return float('inf')
        
        win_rate = move_stats['wins'] / move_stats['count']
        exploration = self.exploration_factor * sqrt(log(parent_visits) / move_stats['count'])
        return win_rate + exploration

    
    def select_by_heuristic(self, game_state):
        legal_moves = list(game_state.get_available_columns())
        center = game_state.columns // 2
        
        # Ưu tiên cột gần trung tâm nhất
        distances = [(abs(m - center), m) for m in legal_moves]
        _, best_move = min(distances, key=lambda x: x[0])
        
        # Thêm 20% xác suất chọn ngẫu nhiên để đa dạng hóa
        if random.random() < 0.2 and len(legal_moves) > 1:
            legal_moves.remove(best_move)
            return random.choice(legal_moves)
        
        return best_move 
    
    def enhanced_evaluate(self, game):
        """Advanced heuristic evaluation of board state"""
        if game.check_win(RED):
            return self.heuristic_weights['win'] * (1 if self.color == RED else -1)
        if game.check_win(YELLOW):
            return self.heuristic_weights['win'] * (1 if self.color == YELLOW else -1)
        
        score = 0
        
        # Mỗi viên ở giữa đc cộng 50 điểm - cho AI
        center_col = game.columns // 2
        center_count = sum(1 for row in range(game.rows) 
                          if game.board[row][center_col] == self.color)
        score += center_count * self.heuristic_weights['center_control']
        
        # Đếm số đường cho những nước đi có 2, 3, 4 quân liên tiếp
        red_score, yellow_score = self.count_potential_lines(game)
        
        # nếu AI đg chơi thì điểm bằng res - yell và ngược lại
        if self.color == RED:
            score += red_score * self.heuristic_weights['three_in_row']
            score += yellow_score * -self.heuristic_weights['potential_threats']
        else:
            score += yellow_score * self.heuristic_weights['three_in_row']
            score += red_score * -self.heuristic_weights['potential_threats']
        
        return score
    
    def count_potential_lines(self, game):
        """Đếm nước đi tiềm năng"""
        red_score = 0
        yellow_score = 0
        
        # Check horizontal, vertical, and diagonal lines
        for row in range(game.rows):
            for col in range(game.columns):
                if game.board[row][col] == RED:
                    red_score += self.evaluate_position(game, row, col, RED)
                elif game.board[row][col] == YELLOW:
                    yellow_score += self.evaluate_position(game, row, col, YELLOW)
        
        return red_score, yellow_score
    
    def evaluate_position(self, game, row, col, color):
        """đánh giá điểm cho mỗi ô"""
        score = 0
        
        # đánh giá 4 hướng: ngang, dọc, chéo trái, chéo phải
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            line_length = 1 # sô quân
            empty_spaces = 0 # ô trống
            
            r, c = row + dr, col + dc
            while 0 <= r < game.rows and 0 <= c < game.columns:
                if game.board[r][c] == color:
                    line_length += 1
                elif game.board[r][c] == IDLE:
                    empty_spaces += 1
                    break  # Only count consecutive pieces
                else:
                    break
                r += dr
                c += dc
            
            r, c = row - dr, col - dc
            while 0 <= r < game.rows and 0 <= c < game.columns:
                if game.board[r][c] == color:
                    line_length += 1
                elif game.board[r][c] == IDLE:
                    empty_spaces += 1
                    break  # Only count consecutive pieces
                else:
                    break
                r -= dr
                c -= dc
            
            if line_length >= 4:
                score += 1000  # lớn hơn 4 thì win
            elif line_length == 3 and empty_spaces >= 1:
                score += 100  # gần win
            elif line_length == 2 and empty_spaces >= 2:
                score += 10   # bình thường
        
        return score