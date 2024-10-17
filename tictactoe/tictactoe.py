"""
Tic Tac Toe Player
"""

import math, copy

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
    number_of_x = 0
    number_of_o = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                number_of_x += 1
            elif board[i][j] == O:
                number_of_o += 1
    if number_of_x == number_of_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_of_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                set_of_actions.add((i, j))
    return set_of_actions
  


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not (0 <= action[0] < len(board) and 0 <= action[1] < len(board[0])):
        raise ValueError("Invalid move: action is out of bounds.")
    if board[action[0]][action[1]] is not None:
        raise ValueError("Invalid move: cell is already occupied.")
    
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    Check Rows: See if any row has all the same non-empty values.
    Check Columns: See if any column has all the same non-empty values.
    Check Diagonals: See if either diagonal has all the same non-empty values.
    """
    for i in range(3):
        # Check Rows
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        # Check Columns
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
    # Check Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    return None
        


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    Winner: If there is a winner, the game is over.
    Full Board: If the board is full and there is no winner, the game is also over.
    """
    if winner(board) != None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    X wins: Return 1.
    O wins: Return -1.
    No winner: Return 0.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Determine player and strategy: X max, O min
    if player(board) == X:
        _, action = max_value(board)
        return action
    else:
        _, action = min_value(board)
        return action


def min_value(board):
    if terminal(board):
        return utility(board), None
    v = float("inf")
    best_action = None
    for action in actions(board):
        value, _ = max_value(result(board, action))
        if value < v:
            v = value
            best_action = action
    return v, best_action

def max_value(board):
    if terminal(board):
        return utility(board), None
    v = float("-inf")
    best_action = None
    for action in actions(board):
        value, _ = min_value(result(board, action))
        if value > v:
            v = value
            best_action = action
    return v, best_action