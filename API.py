from fastapi import FastAPI, HTTPException
import logging
import functions

app = FastAPI()

def handle_error(statusCode, message):
    raise HTTPException(status_code=statusCode, detail=message)


def handle_invalid_board(board):
    board_valid, board_status = functions.is_board_valid(board)
    if not board_valid :
        handle_error(400, board_status)

def handle_game_over(board):
    game_over, status = functions.is_game_over(board)
    if game_over and status == "tie":
        handle_error(422, "Board full")
    elif game_over and status == "player":
        handle_error(422, "player won")
    elif game_over and status == "opponent":
        handle_error(422, "machine won")

@app.get("/move")
def get_best_move(b: str):
    handle_invalid_board(b)
    handle_game_over(b)
    board = functions.create_board(b)
    depth = 4
    alpha = float('-inf')
    beta = float('inf')
    player = 1
    best_move, best_score = functions.get_best_move(board, depth, alpha, beta, player, player)
    return best_move