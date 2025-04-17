from fastapi import FastAPI, HTTPException
import random
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

import numpy as np
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AI_AlphaGo.minimaxVsABPrunning import MinimaxAI
from AI_AlphaGo.minimaxAndRandom import MinimaxAndRandom
from Simulation.Board import ConnectFourBoard

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameState(BaseModel):
    board: List[List[int]]
    current_player: int
    valid_moves: List[int]

class AIResponse(BaseModel):
    move: int

def solution(game_state):
    board = game_state.board
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 2:
                board[i][j] = -1
    return board


from AI_AlphaGo.minimaxVsABPrunning import MinimaxAI, EnhanceMinimaxAI
from AI_AlphaGo.minimaxAndMCTS import minimaxAndMcts
from AI_AlphaGo.minimaxDepthInc import minimaxDepthInc
from Simulation.Board import ConnectFourBoard

@app.post("/api/connect4-move")
async def make_move(game_state: GameState)  -> AIResponse:
    st = time.time()
    try:
        if not game_state.valid_moves:
            raise ValueError("Không có nước đi hợp lệ")
        print(game_state.board)
        game = ConnectFourBoard()
        game.board = np.array(solution(game_state))
        print(game.board)
        myAI = EnhanceMinimaxAI(depth=5)
        if game_state.current_player == 2:
            myAI.set_color(-1)
            game.turn = -1
        else:
            myAI.set_color(1)
            game.turn = 1
        selected_move = myAI.get_move(game)[0]
        print(selected_move)
        print(time.time() - st)
        return AIResponse(move=selected_move)
    except Exception as e:
        if game_state.valid_moves:
            return AIResponse(move=game_state.valid_moves[1])
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)