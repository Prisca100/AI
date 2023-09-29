"""
Tic Tac Toe Player
"""
import math
import random

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


# Player done


def player(board):
    """
    Returns player who has the next turn on a board_array.
    """
    if board is initial_state():
        return X
    counts = {"X": 0, "O": 0}
    for row in board:
        for char in row:
            if char is not None:
                counts[char] += 1
    return O if counts[X] > counts[O] else X


# Actions done


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board_array.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                possible_actions.add((i, j))
    return possible_actions


# Result done
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board_array.
    """
    import copy
    possible_actions = actions(board)
    if action not in possible_actions:
        raise Exception("Invalid action")
    row, col = action
    _player = player(board)
    new_board_state = copy.deepcopy(board)
    new_board_state[row][col] = _player
    return new_board_state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    import numpy as np
    size = len(board)
    board_array = np.array(board)

    for i in range(size):
        # Row
        if (board_array[:, i] == board_array[0][i]).all() and board_array[0][i] is not None:
            return board[0][i]

        # column
        if (board_array[i] == board_array[i][0]).all() and board_array[i][0] is not None:
            return board_array[i][0]

    # Major and reverse diagonal
    if np.all(np.diag(board_array) == board_array[0][0]) and board_array[0][0] is not None:
        return board_array[0][0]
    if np.all(np.diag(np.fliplr(board_array)) == board_array[0][size - 1]) and board_array[0][size - 1] is not None:
        return board_array[0][size - 1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    import numpy as np
    board_array = np.array(board)
    _winner = winner(board)
    if _winner is not None or np.all(board_array != None):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    terminal_board = terminal(board)
    if terminal_board:
        _winner = winner(board)
        if _winner == X:
            return 1
        elif _winner == O:
            return -1
        else:
            return 0


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board_array.
    """
    if terminal(board):
        return None
    elif board == initial_state():
        return random.choice(list(actions(board)))
    elif player(board) is X:
        plays = []
        for action in actions(board):
            plays.append([min_value(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]
    elif player(board) is O:
        plays = []
        for action in actions(board):
            plays.append([max_value(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0])[0][1]


if __name__ == "__main__":
    term = winner([

        [O, X, X],
        [X, X, O],
        [X, O, O]

    ])
    print(term)
