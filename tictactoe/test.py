from tictactoe import initial_state, player, actions, result, winner, terminal, utility

X = "X"
O = "O"
EMPTY = None
def test_initial_state():
    assert initial_state() == [[None, None, None], [None, None, None], [None, None, None]]

def test_player():
    assert player([[None, None, None], [None, None, None], [None, None, None]]) == X
    assert player([["X", None, None], [None, None, None], [None, None, None]]) == O
    assert player([["X", "O", None], [None, None, None], [None, None, None]]) == X
    assert player([["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]) == O


def test_actions():
    assert actions([[None, None, None], [None, None, None], [None, None, None]]) == {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
    assert actions([["X", None, None], [None, None, None], [None, None, None]]) == {(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
    assert actions([["X", "O", None], [None, None, None], [None, None, None]]) == {(0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
    assert actions([["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]) == set()

def test_result():
    assert result([[None, None, None], [None, None, None], [None, None, None]], (0, 0)) == [["X", None, None], [None, None, None], [None, None, None]]
    assert result([["X", None, None], [None, None, None], [None, None, None]], (0, 1)) == [["X", "O", None], [None, None, None], [None, None, None]]
    assert result([["X", "O", None], [None, None, None], [None, None, None]], (0, 2)) == [["X", "O", "X"], [None, None, None], [None, None, None]]
    assert result([["X", "O", "X"], [None, None, None], [None, None, None]], (1, 0)) == [["X", "O", "X"], ["O", None, None], [None, None, None]]
    assert result([["X", "O", "X"], ["O", None, None], [None, None, None]], (2, 0)) == [["X", "O", "X"], ["O", None, None], ["X", None, None]]

def test_winner():
    assert winner([[None, None, None], [None, None, None], [None, None, None]]) == None
    assert winner([["X", None, None], [None, None, None], [None, None, None]]) == None
    assert winner([["X", "O", None], [None, None, None], [None, None, None]]) == None
    # Row winner
    assert winner([["X", "X", "X"], [None, None, None], [None, None, None]]) == "X"
    # Column winner
    assert winner([["X", None, None], ["X", None, None], ["X", None, None]]) == "X"
    # Diagonal winner
    assert winner([["X", None, None], [None, "X", None], [None, None, "X"]]) == "X"
    # Tie
    assert winner([["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]) == None

def test_terminal():
    assert terminal([[None, None, None], [None, None, None], [None, None, None]]) == False
    assert terminal([["X", None, None], [None, None, None], [None, None, None]]) == False
    assert terminal([["X", "O", None], [None, None, None], [None, None, None]]) == False
    assert terminal([["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]) == True
    assert terminal([["X", None, None], [None, "X", None], [None, None, "X"]]) == True
    assert terminal([["X", "X", "X"], [None, None, None], [None, None, None]]) == True
    assert terminal([["X", None, None], [None, "X", None], [None, None, "X"]]) == True

def test_utility():
    # No winner = 0, X wins = 1, O wins = -1
    assert utility([[None, None, None], [None, None, None], [None, None, None]]) == 0
    assert utility([["X", None, None], [None, None, None], [None, None, None]]) == 0
    assert utility([["O", None, None], ["O", None, None], ["O", None, None]]) == -1
    assert utility([["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]) == 0
    assert utility([["X", "X", "X"], [None, None, None], [None, None, None]]) == 1
    assert utility([["X", None, None], [None, "X", None], [None, None, "X"]]) == 1