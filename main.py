import numpy as np


def evaluate_board(board, player):
    # définir les poids pour chaque élément de la fonction
    weights = [3, 4, 5, 7, 1000]

    # calculer le nombre de pions alignés dans toutes les directions possibles
    rows = np.sum(board == player, axis=1)
    cols = np.sum(board == player, axis=0)
    diags = [np.sum(np.diagonal(board, i) == player) for i in range(-2, 4)]
    antidiags = [np.sum(np.diagonal(np.fliplr(board), i) == player) for i in range(-3, 3)]
    aligned = np.max([np.max(rows), np.max(cols), np.max(diags), np.max(antidiags)])

    # détecter les positions bloquées pour chaque joueur
    blocked = np.sum(np.logical_and(board != 0, np.logical_not(np.isin(board, [player, 0]))), axis=0)

    # détecter les positions stratégiques
    center_cols = [2, 3, 4, 5]
    center_rows = [np.sum(board[:, col] != 0) for col in center_cols]
    strategic = np.sum(np.multiply(weights[0], center_rows))

    # détecter les menaces potentielles de l'adversaire
    opponent = 'm' if player == 'h' else 'h'
    opponent_rows = np.sum(board == opponent, axis=1)
    opponent_cols = np.sum(board == opponent, axis=0)
    opponent_diags = [np.sum(np.diagonal(board, i) == opponent) for i in range(-2, 4)]
    opponent_antidiags = [np.sum(np.diagonal(np.fliplr(board), i) == opponent) for i in range(-3, 3)]
    opponent_threats = np.max(
        [np.max(opponent_rows), np.max(opponent_cols), np.max(opponent_diags), np.max(opponent_antidiags)])
    threats = np.multiply(weights[4], opponent_threats)

    # calculer le score final
    score = np.sum(np.dot(weights[1:5], [aligned, strategic, np.sum(blocked), threats]))
    print(player)
    print(score)
    return score


def alpha_beta_pruning(board, depth, alpha, beta, maximizing_player, evaluation_function):
    if depth == 0:
        player = 'h' if maximizing_player else 'm'
        return None, evaluation_function(board, player)

    if maximizing_player:
        max_eval = -np.inf
        best_move = None
        print("Shape "+str(board.shape[1]))
        for col in range(board.shape[1]):
            print("Col " + str(col))
            if np.count_nonzero(board[:,col]) < board.shape[0]:
                row = np.count_nonzero(board[:, col])
                board[row, col] = 1

                _, eval_score = alpha_beta_pruning(board, depth - 1, alpha, beta, False, evaluation_function)
                board[row, col] = 0
                print("Maximizing " + eval_score)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = col

                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break

        return best_move, max_eval

    else:
        min_eval = np.inf
        best_move = None
        print("Shape "+board.shape[1])

        for col in range(board.shape[1]):
            print("Col " + col)

            if np.count_nonzero(board[:, col]) < board.shape[0]:
                row = np.count_nonzero(board[:, col])
                board[row, col] = 2

                _, eval_score = alpha_beta_pruning(board, depth - 1, alpha, beta, True, evaluation_function)
                board[row, col] = 0
                print("Minimizing " + eval_score)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = col

                beta = min(beta, min_eval)
                if beta <= alpha:
                    break

        return best_move, min_eval


def next_move(board, depth, evaluation_function):
    maximizing_player = True if np.count_nonzero(board) % 2 == 0 else False
    move, _ = alpha_beta_pruning(board, depth, -np.inf, np.inf, maximizing_player, evaluation_function)
    return move


board = np.array([
    ['h', 0, 0, 0, 0, 0, 0],
    ['m', 'h', 0, 0, 0, 0, 0],
    ['h', 'm', 0, 0, 0, 0, 0],
    ['h', 'm', 0, 0, 0, 0, 0],
    ['m', 'h', 'm', 0, 0, 0, 0],
    ['h', 'm', 'h', 0, 0, 0, 0]
])

depth = 5
evaluation_function = evaluate_board

print("Next move : " + str(next_move(board, depth, evaluation_function)))
