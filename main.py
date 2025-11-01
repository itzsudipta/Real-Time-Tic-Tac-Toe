import math
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

#main FastAPI application
app = FastAPI()

#CORS middleware configuration for allowing cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#this is the pydentic moder for validating the input data
class BoardData(BaseModel):
    board: List[str]

#this is thewinnning combinations
WIN_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

#check if a player has won
def check_winner(board, player):
    try:
        for a, b, c in WIN_COMBINATIONS:
            if board[a] == player and board[b] == player and board[c] == player:
                return True
        return False
    except Exception as e:
        print(f"Error in check_winner: {e}")
        return False

#check if the game is a draw
def is_draw(board):
    try:
        # No empty spaces left
        return " " not in board
    except Exception as e:
        print(f"Error in is_draw: {e}")
        return False

#check if the game is over
def game_over(board):
    try:
        return check_winner(board, "X") or check_winner(board, "O") or is_draw(board)
    except Exception as e:
        print(f"Error in game_over: {e}")
        return True

#this function evaluates the board and returns a score
def score(board):
    try:
        if check_winner(board, "X"):
            return 1
        elif check_winner(board, "O"):
            return -1
        return 0
    except Exception as e:
        print(f"Error in score: {e}")
        return 0
#This is the minimax algorithm implementation
def minimax(board, is_maximizing):
    try:
        if game_over(board):
            return score(board)

        if is_maximizing:
            best = -math.inf
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    val = minimax(board, False)
                    board[i] = " "
                    best = max(best, val)
            return best
        else:
            best = math.inf
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    val = minimax(board, True)
                    board[i] = " "
                    best = min(best, val)
            return best
    except Exception as e:
        print(f"Error in minimax: {e}")
        return 0
#this funtion finds the best move for the player
def find_best_move(board):
    try:
        best_val = -math.inf
        best_move = -1

        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                move_val = minimax(board, False)
                board[i] = " "
                if move_val > best_val:
                    best_val = move_val
                    best_move = i

        return best_move
    except Exception as e:
        print(f"Error in find_best_move: {e}")
        return -1

#FastAPI endpoint route for getting the best move from the backend

@app.post("/get_best_move")
async def get_best_move(data: BoardData):
    try:
        # Input validation
        if not isinstance(data.board, list) or len(data.board) != 9:
            raise HTTPException(status_code=400, detail="Board must be a list of 9 elements.")
        if any(cell not in ["X", "O", " "] for cell in data.board):
            raise HTTPException(status_code=400, detail="Invalid characters in board. Allowed: X, O, and blank space")

        move = find_best_move(data.board)

        if move == -1:
            return {"success": False, "message": "No valid moves found or error occurred."}

        return {"success": True, "best_move": move}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Unexpected error in /get_best_move: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=10000)
    except Exception as e:
        print(f"Failed to start server: {e}")
