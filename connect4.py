import copy
import math
import time

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

def utility(board, depth):
    # give more points to quicker wins
    if winner(board) == RED:
        return 100000 - (depth * 100)
    # give less points to quicker losses
    elif winner(board) == YELLOW:
        return -100000 + (depth * 100)
    else:
        return 0

def evaluate(board, depth):
    if terminal(board):
        return utility(board, depth)

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
        score += 50
    elif player_count == 2 and empty_count == 2:
        score += 20
    elif player_count == 1 and empty_count == 3:
        score += 5

    return score

transpo_table = {}

# set depth to 7 by default so the game goes at a proper pace
def minimax(board, depth=7):
    """
    Returns the optimal action for the current player.
    Depth-limited, transposition table, alpha-beta pruning.
    """
    if terminal(board):
        return None

    board_key = tuple(tuple(row) for row in board)
    if board_key in transpo_table:
        stored_depth, stored_value, stored_move = transpo_table[board_key]
        if depth <= stored_depth:
            return stored_move

    s = time.time()

    p = current_player(board)
    optimal_value = -math.inf if p == RED else math.inf
    optimal_move = None

    # use move ordering at the root in order to save processing time
    possible_moves = actions(board)
    ordered_moves = move_ordering(board, possible_moves)

    for action in possible_moves:
        test_board = result(board, action)
        if winner(test_board) == p:
            print(f"Found winning move: {action}")
            return action

    for action in ordered_moves:
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

    e = time.time()
    print('Time elapsed: ' + str(e - s))

    transpo_table[board_key] = (depth, optimal_value, optimal_move)
    
    return optimal_move

def max_value(board, depth, alpha=-math.inf, beta=math.inf):
    """
    Maximizing function which tries to get the highest score possible
    """
    board_key = tuple(tuple(row) for row in board)
    if board_key in transpo_table:
        stored_depth, stored_value, stored_move = transpo_table[board_key]
        if depth <= stored_depth:
            return stored_value

    if terminal(board):
        return utility(board, depth)

    if depth == 0:
        return evaluate(board, depth)

    possible_moves = actions(board)

    v = -math.inf
    for action in possible_moves:
        v = max(v, min_value(result(board, action), depth - 1, alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:
            break

    transpo_table[board_key] = (depth, v, None)
    return v

def min_value(board, depth, alpha=-math.inf, beta=math.inf):
    """
    Minimizing function which tries to get the lowest score possible
    """
    board_key = tuple(tuple(row) for row in board)
    if board_key in transpo_table:
        stored_depth, stored_value, stored_move = transpo_table[board_key]
        if depth <= stored_depth:
            return stored_value

    if terminal(board):
        return utility(board, depth)

    if depth == 0:
        return evaluate(board, depth)

    possible_moves = actions(board)

    v = math.inf
    for action in possible_moves:
        v = min(v, max_value(result(board, action), depth - 1, alpha, beta))
        beta = min(beta, v)
        if alpha >= beta:
            break

    transpo_table[board_key] = (depth, v, None)
    return v

def move_ordering(board, actions_list):
    """
    Returns a list of moves sorted by priority.
    The higher priority moves will be played first.
    """
    if not actions_list:
        return []

    if isinstance(actions_list, set):
        actions_list = list(actions_list)

    action_scores = []

    # evaluate the priority of each move
    for action in actions_list:
        score = evaluate_action_priority(board, action)
        action_scores.append((action, score))

    # sort by score
    action_scores.sort(key=lambda x: x[1], reverse=True)

    return [move for move, score in action_scores]

def evaluate_action_priority(board, action):
    """
    Returns the score of the given action in the given board.
    """
    row, col = action
    prio = 0

    # check if can win immediately (best move)
    check_board = result(board, action)
    p = current_player(board)

    if winner(check_board) == p:
        return 1000000

    # center columns are worth more than surrounding
    center_bonus = {0: 0, 1: 10, 2: 30, 3: 50, 4: 30, 5: 10, 6: 0}
    prio += center_bonus.get(col, 0)

    # check if we can block opponent (second best move)
    opp = YELLOW if p == RED else RED

    for opp_action in actions(board):
        temp_result = result(board, opp_action)
        if winner(temp_result) == opp:
            if opp_action[1] == action[1]:
                prio += 500000
            break

    # determine how many threats are generated with this move
    # and assign priority based on this
    threats_generated = count_threats(board, action, p)
    prio += threats_generated*100

    # lower rows on the board are better because they are the foundation
    # for upper rows
    prio += (6-row) * 2

    return prio

def count_threats(board, action, p):
    """
    Returns the number of threats a player can generate with an action
    """
    test_board = result(board, action)
    threats = 0

    for next_move in actions(test_board):
        next_board = result(test_board, next_move)
        if winner(next_board) == p:
            threats += 1

    return threats