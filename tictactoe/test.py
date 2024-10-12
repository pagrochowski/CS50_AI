from tictactoe import initial_state, player, actions, result, winner, terminal, utility, min_value, max_value

X = "X"
O = "O"
EMPTY = None
def test_initial_state():
    assert initial_state() == [[None, None, None], [None, None, None], [None, None, None]]

def test_player():
    assert player([[None, None, None], [None, None, None], [None, None, None]]) == X
    assert player([["X", None, None], [None, None, None], [None, None, None]]) == O
    assert player([["X", "O", None], [None, None, None], [None, None, None]]) == X
    assert player([["X", "O", "X"], 
                   ["O", "X", "O"], 
                   [None, "X", "O"]]) == X
    assert player([["X", "O", "X"], 
                   ["O", "X", None], 
                   [None, None, None]]) == O


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
    assert result([["X", "O", "X"], ["O", "X", None], [None, None, None]], (1, 2)) == [["X", "O", "X"], ["O", "X", "O"], [None, None, None]]

def test_winner():
    assert winner([[None, None, None], [None, None, None], [None, None, None]]) == None
    assert winner([["X", None, None], [None, None, None], [None, None, None]]) == None
    assert winner([["X", "O", None], [None, None, None], [None, None, None]]) == None
    # Row winner
    assert winner([["X", "X", "X"], [None, None, None], [None, None, None]]) == "X"
    # Column winner
    assert winner([["O", None, None], ["O", None, None], ["O", None, None]]) == "O"
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

def test_utlity_of_result():
    assert utility(result([[None, None, None], [None, None, None], [None, None, None]], (0, 0))) == 0
    assert utility(result([["X", None, None], [None, None, None], [None, None, None]], (0, 1))) == 0
    assert utility(result([["X", None, None], ["X", "O", None], [None, None, None]], (0, 2))) == 0
    assert utility(result([["X", "X", "X"], ["O", "O", None], [None, None, None]], (1, 0))) == 1
    assert utility(result([["O", "X", None], ["X", "O", None], [None, "X", "O"]], (1, 0))) == -1


def test_min_value():
    assert min_value([[None, "O", "O"], 
                      ["O", "X", "X"], 
                      [None, "X", "X"]]) == (-1, (0, 0))
    
    expected_actions = {(1, (0, 2)), (1, (1, 2))}
    assert min_value([["X", "X", None], 
                      ["O", "X", None], 
                      [None, None, "O"]]) in expected_actions
    
    expected_actions = {(-1, (2, 2)), (-1, (1, 0))}
    assert min_value([["X", "X", "O"], 
                      [None, "O", "O"], 
                      ["X", "X", None]]) in expected_actions


def test_max_value():
    assert max_value([[None, "O", "O"], 
                      ["O", "X", "X"], 
                      ["O", "X", "X"]]) == (1, (0, 0))
    
    expected_actions = {(1, (0, 2)), (1, (1, 2))}
    assert max_value([["X", "X", None], 
                      ["O", "X", None], 
                      [None, None, "O"]]) in expected_actions
    
    expected_actions = {(-1, (2, 2)), (-1, (1, 0))}
    assert max_value([["X", "X", "O"], 
                      [None, "O", "O"], 
                      ["X", "X", None]]) in expected_actions

"""
def main():
    min_value([[None, None, "X"], 
               [None, None, None], 
               [None, "O", None]]) 
    

if __name__ == "__main__":
    main()
"""