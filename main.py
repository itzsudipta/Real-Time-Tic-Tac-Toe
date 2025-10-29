import math
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BoardData(BaseModel):
    board: List[str]

WIN_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

def check_winner(board, player):
    for a, b, c in WIN_COMBINATIONS:
        if board[a] == player and board[b] == player and board[c] == player:
            return True
    return False

def is_draw(board):
    return "_" not in board

def game_over(board):
    return check_winner(board, "X") or check_winner(board, "O") or is_draw(board)

def score(board):
    if check_winner(board, "X"):
        return 1
    elif check_winner(board, "O"):
        return -1
    return 0

def minimax(board, is_maximizing):
    if game_over(board):
        return score(board)

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == "_":
                board[i] = "X"
                val = minimax(board, False)
                board[i] = "_"
                best = max(best, val)
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == "_":
                board[i] = "O"
                val = minimax(board, True)
                board[i] = "_"
                best = min(best, val)
        return best

def find_best_move(board):
    best_val = -math.inf
    best_move = -1

    for i in range(9):
        if board[i] == "_":
            board[i] = "X"
            move_val = minimax(board, False)
            board[i] = "_"
            if move_val > best_val:
                best_val = move_val
                best_move = i

    return best_move


@app.post("/get_best_move")
async def get_best_move(data: BoardData):
    move = find_best_move(data.board)
    return {"success": True, "best_move": move}


if __name__ == "__main__":
    
   uvicorn.run("main:app", host="0.0.0.0", port=10000)
