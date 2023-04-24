import numpy as np
import re


def get_possible_moves(board):
    return [col for col in range(7) if (board[:, col] == 0).any()]


def is_board_valid(board_string):
    if len(board_string) != 42:
        return False, "Invalid board length"

    for char in board_string:
        if char not in ['m', 'h', '0']:
            return False, "Invalid character in board"

    if board_string.count("h") != (board_string.count("m") + 1):
        return False, "Invalid game state"

    for col in range(7):
        start = col * 6

        end = start + 6
        if re.search("@*0[mh]", board_string[start:end]):
            return False, "Invalid board configuration"

    return True, "Valid board"


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
    opponent_aligned = np.diff(np.concatenate(([False], board == -player, [False])).astype(int))
    return np.flatnonzero(player_aligned == -1) - np.flatnonzero(player_aligned == 1), \
           np.flatnonzero(opponent_aligned == -1) - np.flatnonzero(opponent_aligned == 1)


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

    return (scores[0] - scores[1]) * depth


def get_best_move(board, depth, alpha, beta, maximizing_player, study_player, current_player):
    # check if game is over or depth limit reached
    status, message = is_game_over(board, current_player)
    if depth == 0 or status:
        return None, evaluate_board(board, study_player, depth + 1)

    # get possible moves
    possible_moves = get_possible_moves(board)

    # if there are no possible moves, return the evaluation of the current board
    if len(possible_moves) == 0:
        return None, evaluate_board(board, study_player, depth + 1)

    # initialize best move and score
    if maximizing_player:
        best_move = possible_moves[0]
        best_score = float('-inf')
    else:
        best_move = possible_moves[0]
        best_score = float('inf')

    # if current player is opponent, simulate his best move
    if current_player != study_player:
        board = play_opponent(board, possible_moves, current_player, depth)

    # iterate through possible moves
    for move in possible_moves:
        # make a copy of the board and play the move
        new_board = np.copy(board)
        play_move(new_board, current_player, move)

        # recursively get the best score for the next player
        score = get_best_move(new_board, depth - 1, alpha, beta, not maximizing_player, study_player, -current_player)[1]

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


def is_game_over(board, player):
    # horizontal check
    for row in range(len(board)):
        play, opp = get_aligned_checkers(board[row], player)
        if 4 in play:
            return True, "player"
        elif 4 in opp:
            return True, "opponent"

    # vertical check
    transposed_board = board.transpose()
    for row in range(len(board)):
        play, opp = get_aligned_checkers(transposed_board[row], player)
        if 4 in play:
            return True, "player"
        elif 4 in opp:
            return True, "opponent"

    # diagonal check (positive slope)
    for row in range(-(len(board) - 1), len(board) + 1):
        play, opp = get_aligned_checkers(board.diagonal(row), player)
        if 4 in play:
            return True, "player"
        elif 4 in opp:
            return True, "opponent"

    # diagonal check (negative slope)
    for row in range(-(len(board) - 1), len(board) + 1):
        play, opp = get_aligned_checkers(np.fliplr(board).diagonal(row), player)
        if 4 in play:
            return True, "player"
        elif 4 in opp:
            return True, "opponent"

    # Check for tie game
    if np.count_nonzero(board) == 42:
        return True, "tie"

    # Game is not over yet
    return False, None


def play_move(board, player, col):
    for row in range(5, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            return board
    return board  # column is full, return original board


def play_opponent(board, possible_moves, current_player, depth):
    best_opp_board = np.copy(board)
    best_opp_score = 0
    for move in possible_moves:
        new_board = np.copy(board)
        play_move(new_board, current_player, move)
        tmp_score = evaluate_board(new_board, current_player, depth)
        if tmp_score > best_opp_score:
            best_opp_score = tmp_score
            best_opp_board = np.copy(new_board)
    return best_opp_board
