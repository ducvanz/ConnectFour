import sys
import os
import numpy as np
import tensorflow as tf

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Constant import RED, YELLOW, IDLE
from Simulation.Board import ConnectFourBoard

class Deep:
    def __init__(self, color=RED, timeout=None):
        self.name = 'DEEP AI'
        self.color = color
    
    def set_color(self, color: int):
        """Set the color of the AI."""
        self.color = color
    
    def get_move(self, game: ConnectFourBoard):
        model_path = os.path.abspath("./DL/Files/value_conn.h5")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        model = tf.keras.models.load_model(model_path)
        
        board_input = np.array(game.board, dtype=np.float32).reshape(1, *game.board.shape)
        col_probs = model.predict(board_input)[0]
        col = np.argmax(col_probs)

        return col, None
