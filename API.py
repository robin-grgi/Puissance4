from fastapi import FastAPI, HTTPException
import functions

app = FastAPI()


def handle_error(status_code, message):
    raise HTTPException(status_code=status_code, detail=message)


def handle_invalid_board(board):
    board_valid, board_status = functions.is_board_valid(board)
    if not board_valid:
        handle_error(400, board_status)


def handle_game_over(board, player):
    game_over, status = functions.is_game_over(board, player)
    if game_over and status == "tie":
        handle_error(422, "Board full")
    elif game_over and status == "player":
        handle_error(422, "machine won")
    elif game_over and status == "opponent":
        handle_error(422, "human won")


@app.get("/move")
def get_best_move(b: str):
    handle_invalid_board(b)
    board = functions.create_board(b)
    player = 1
    handle_game_over(board, player)
    depth = 4
    alpha = float('-inf')
    beta = float('inf')
    best_move, best_score = functions.get_best_move(board, depth, alpha, beta, True, player, player)
    return best_move + 1
