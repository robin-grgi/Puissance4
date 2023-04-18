from functions import create_board, get_best_move


def play_game(board_string):
    board = create_board(board_string)
    depth = 4
    alpha = float('-inf')
    beta = float('inf')
    player = 1  # or -1 for the second player
    print(board)
    best_move, best_score = get_best_move(board, depth, alpha, beta, player, player)
    print("Next move is : "+str(best_move))


if __name__ == "__main__":
    play_game("m00000h00000mm0000hmh000h00000h00000000000")
