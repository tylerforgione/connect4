import copy
import math

RED = 'R'
YELLOW = 'Y'
EMPTY = None

def initial_state():
    return [[EMPTY for _ in range(7)] for _ in range(6)]

def current_player(board):
    count = sum(1 for row in board for item in row if item is not EMPTY)
    return RED if count % 2 == 0 else YELLOW

def actions(board):
    """
    Returns the set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for col in range(7):
        if board[0][col] == EMPTY:
            for row in range(5, -1, -1):
                if board[row][col] == EMPTY:
                    actions.add((row, col))
                    break
    return actions

def result(board, action):
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception('Invalid move')
    if action[0] >= 6 or action[1] >= 7 or action[0] < 0 or action[1] < 0:
        raise Exception('Invalid move')
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = current_player(board)
    return new_board

def winner(board):
    # horizontal
    for row in range(6):
        for col in range(4):
            if board[row][col] != EMPTY:
                if all(board[row][col + i] == board[row][col] for i in range(4)):
                    return board[row][col]

    # vertical
    for col in range(7):
        for row in range(3):
            if board[row][col] != EMPTY:
                if all(board[row + i][col] == board[row][col] for i in range(4)):
                    return board[row][col]

    # diagonals
    for row in range(3):
        for col in range(4):
            # down-right diagonal (\)
            if board[row][col] != EMPTY:
                if all(board[row + i][col + i] == board[row][col] for i in range(4)):
                    return board[row][col]

            # down-left diagonal (/)
            if board[row][col + 3] != EMPTY:
                if all(board[row + i][col + 3 - i] == board[row][col + 3] for i in range(4)):
                    return board[row][col + 3]

    return None

def terminal(board):
    if winner(board) is not None:
        return True
    else:
        return sum(1 for row in board for item in row if item is not EMPTY) == 42

def utility(board):
    if winner(board) == RED:
        return 1000
    elif winner(board) == YELLOW:
        return -1000
    else:
        return 0

def evaluate(board):
    if terminal(board):
        return utility(board)

    score = 0
    score += evaluate_windows(board, RED) - evaluate_windows(board, YELLOW)

    return score

def evaluate_windows(board, player):
    """
    Determines all possible scoring windows based on the current state of the board.
    """
    score = 0
    # horizontal
    for row in range(6):
        for col in range(4):
            window = [board[row][col + i] for i in range(4)]
            score += score_window(window, player)

    # vertical
    for col in range(7):
        for row in range(3):
            window = [board[row+i][col] for i in range(4)]
            score += score_window(window, player)

    # down-right diag
    for row in range(3):
        for col in range(4):
            window = [board[row+i][col+i] for i in range(4)]
            score += score_window(window, player)

    # down-left diag
    for row in range(3):
        for col in range(3, 7):
            window = [board[row+i][col-i] for i in range(4)]
            score += score_window(window, player)

    return score

def score_window(window, player):
    """
    Returns the score of the given 4 tile window for the given player.
    """
    score = 0
    opp = YELLOW if player == RED else RED

    player_count = window.count(player)
    empty_count = window.count(EMPTY)
    opp_count = window.count(opp)

    # if opponent has a piece within scoring window, you can't score (0 points)
    if opp_count > 0:
        return 0

    # score based on number of checkers in a row + empty spaces
    if player_count == 4:
        score += 1000
    elif player_count == 3 and empty_count == 1:
        score += 100
    elif player_count == 2 and empty_count == 2:
        score += 10
    elif player_count == 1 and empty_count == 3:
        score += 1

    return score

# set depth to 7 by default so the game goes at a proper pace
def minimax(board, depth=7):
    """
    Returns the optimal action for the current player.
    """
    if terminal(board):
        return None

    p = current_player(board)
    optimal_value = -math.inf if p == RED else math.inf
    optimal_move = None

    for action in actions(board):
        if p is RED:
            value = min_value(result(board, action), depth-1)
            if value > optimal_value:
                optimal_value = value
                optimal_move = action
        else:
            value = max_value(result(board, action), depth-1)
            if value < optimal_value:
                optimal_value = value
                optimal_move = action

    return optimal_move

def max_value(board, depth, alpha=-math.inf, beta=math.inf):
    if terminal(board):
        return utility(board)

    if depth == 0:
        return evaluate(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), depth - 1))
        alpha = max(alpha, v)
        if alpha >= beta:
            break

    return v

def min_value(board, depth, alpha=-math.inf, beta=math.inf):
    if terminal(board):
        return utility(board)

    if depth == 0:
        return evaluate(board)

    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), depth - 1))
        beta = min(beta, v)
        if alpha >= beta:
            break

    return v