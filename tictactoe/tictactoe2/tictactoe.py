"""
Tic Tac Toe Player
"""

import math
import copy



X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return None

    counter = 0
    for row in board:
        for cell in row:
            if cell == X or cell == O:
                counter += 1
    if counter % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # (row, cell)
    possible_actions = set()
    current_row = 0
    for row in board:
        current_cell = 0
        for cell in row:
            if cell == EMPTY:
                possible_actions.add((current_row, current_cell))
            current_cell += 1
        current_row += 1

    else:
        return possible_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # action is (row, cell)
    if action not in actions(board):
        raise Exception('invalid action')

    action_row = action[0]
    action_cell = action[1]
    copyboard = copy.deepcopy(board)
    if copyboard[action_row][action_cell] == EMPTY:
        copyboard[action_row][action_cell] = player(copyboard)

    return copyboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for x in range(3):
        # horizontals
        if board[x][0] == board[x][1] == board[x][2] and None not in board[x]:
            return board[x][0]

        # verticals
        elif board[0][x] == board[1][x] == board[2][x] and board[0][x] != None:
            return board[0][x]


    # diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[1][1] != None:
        return board[1][1]

    if board[0][2] == board[1][1] == board[2][0] and board[1][1] != None:
        return board[1][1]



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == None and len(actions(board)) > 0:
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def maximize(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, minimize(result(board, action)))
    return v


def minimize(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, maximize(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif player(board) == X:
        possible_actions = []
        for action in actions(board):
            possible_actions.append((minimize(result(board, action)), action))
            possible_actions_sorted = sorted(possible_actions, key=lambda x: x[0])
        max_action = possible_actions_sorted[-1][-1]
        return max_action
    elif player(board) == O:
        possible_actions = []
        for action in actions(board):
            possible_actions.append((maximize(result(board, action)), action))
            possible_actions_sorted = sorted(possible_actions, key=lambda x: x[0])
        min_action = possible_actions_sorted[0][1]
        return min_action







