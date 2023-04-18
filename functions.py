import numpy as np


def get_possible_moves(board):
    return [col for col in range(7) if (board[:, col] == 0).any()]


def create_board(board_string):
    board = np.zeros((6, 7), dtype=int)
    for i, char in enumerate(board_string):
        row = i % 6
        col = i // 6
        if char == 'm':
            board[row, col] = 1
        elif char == 'h':
            board[row, col] = -1

    return np.flip(board, axis=0)


def get_aligned_checkers(board, player):
    player_aligned = np.diff(np.concatenate(([False], board == player, [False])).astype(int))
    return np.flatnonzero(player_aligned == -1) - np.flatnonzero(player_aligned == 1), \
           np.flatnonzero(player_aligned == 1) - np.flatnonzero(player_aligned == -1)


def update_score(board, player, scores, scores_array, diagonal=False):
    for_range = range(-(len(board) - 1), len(board) + 1) if diagonal else range(len(board))
    for row in for_range:
        play, opp = get_aligned_checkers(board.diagonal(row) if diagonal else board[row], player)
        for score in play:
            scores[0] += scores_array[0][min(len(scores_array[0]) - 1, score)]
        for score in opp:
            scores[1] += scores_array[1][min(len(scores_array[1]) - 1, score)]
    return scores


def evaluate_board(board, player, depth):
    scores = [0, 0]
    scores_array = [np.array([0, 1, 10, 100, 1000]), np.array([0, 2, 20, 200, 2000])]

    # horizontal check
    scores = update_score(board, player, scores, scores_array)

    # vertical check
    scores = update_score(board.transpose(), player, scores, scores_array)

    # diagonal check (positive slope)
    scores = update_score(board, player, scores, scores_array, diagonal=True)

    # diagonal check (negative slope)
    scores = update_score(np.fliplr(board), player, scores, scores_array, diagonal=True)

    return (scores[1] - scores[0]) * depth


def get_best_move(board, depth, alpha, beta, maximizing_player, current_player):
    # check if game is over or depth limit reached
    if depth == 0 or is_game_over(board):
        return None, evaluate_board(board, maximizing_player, depth + 1)

    # get possible moves
    possible_moves = get_possible_moves(board)

    # if there are no possible moves, return the evaluation of the current board
    if len(possible_moves) == 0:
        return None, evaluate_board(board, maximizing_player, depth + 1)

    # initialize best move and score
    if maximizing_player:
        best_move = possible_moves[0]
        best_score = float('-inf')
    else:
        best_move = possible_moves[0]
        best_score = float('inf')

    score = evaluate_board(board, maximizing_player, depth + 1)

    # iterate through possible moves
    for move in possible_moves:
        # make a copy of the board and play the move
        new_board = np.copy(board)
        play_move(new_board, current_player, move)

        # recursively get the best score for the next player
        score += get_best_move(new_board, depth - 1, alpha, beta, maximizing_player, -current_player)[1]

        # update alpha and beta values
        if maximizing_player:
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)

        # check for alpha-beta pruning
        if alpha >= beta:
            break

    return best_move, best_score


def is_game_over(board):
    # horizontal check
    for row in range(len(board)):
        play, opp = get_aligned_checkers(board[row], 1)
        if 4 in play or 4 in opp:
            return True

    # vertical check
    transposed_board = board.transpose()
    for row in range(len(board)):
        play, opp = get_aligned_checkers(transposed_board[row], 1)
        if 4 in play or 4 in opp:
            return True

    # diagonal check (positive slope)
    for row in range(-(len(board) - 1), len(board) + 1):
        play, opp = get_aligned_checkers(board.diagonal(row), 1)
        if 4 in play or 4 in opp:
            return True

    # diagonal check (negative slope)
    for row in range(-(len(board) - 1), len(board) + 1):
        play, opp = get_aligned_checkers(np.fliplr(board).diagonal(row), 1)
        if 4 in play or 4 in opp:
            return True

    # Check for tie game
    if np.count_nonzero(board) == 42:
        return True

    # Game is not over yet
    return False


def play_move(board, player, col):
    for row in range(5, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            return board
    return board  # column is full, return original board
