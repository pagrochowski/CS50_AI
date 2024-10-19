from minesweeper import Minesweeper, Sentence, MinesweeperAI

def main():
    ...


"""
TESTING MinesweeperAI CLASS
"""
def test_knowledge_inference():
    # Initiate 3x3 board
    gameAI = MinesweeperAI(3, 3)
    # Click on cell (0, 0)
    gameAI.add_knowledge((0, 0), 1)
    assert gameAI.knowledge[0].cells == {(0, 1), (1, 0), (1, 1)}
    # Click on cell (0, 1) 
    gameAI.add_knowledge((0, 1), 1)
    assert gameAI.knowledge[0].cells == {(1, 0), (1, 1)}
    assert gameAI.knowledge[1].cells == {(0, 2), (1, 0), (1, 1), (1, 2)}
    
    # Click on cell (0, 2) 
    gameAI.add_knowledge((0, 2), 1)
    assert gameAI.knowledge[0].cells == {(1, 0), (1, 1)}
    assert gameAI.knowledge[1].cells == {(1, 0), (1, 1), (1, 2)}
    assert gameAI.knowledge[2].cells == {(1, 1), (1, 2)}

    # Click on cell (2, 1) 
    gameAI.add_knowledge((2, 1), 2)
    assert gameAI.knowledge[0].cells == {(1, 0), (1, 1)}
    assert gameAI.knowledge[1].cells == {(1, 0), (1, 1), (1, 2)}
    assert gameAI.knowledge[2].cells == {(1, 1), (1, 2)}
    assert gameAI.knowledge[3].cells == {(1, 0), (1, 1), (1, 2), (2, 0), (2, 2)}
    #assert gameAI.knowledge[4].cells == {(2, 0), (2, 2)}





def test_add_knowledge_2x2_1_mine():
    # Cell being checked is (0, 0) with a count of 1
    cell = (0, 0)
    count = 1

    # Test adding knowledge
    gameAI = MinesweeperAI()
    gameAI.add_knowledge(cell, count)

    # Assert knowledge has been added
    assert gameAI.knowledge[0].cells == {(0, 1), (1, 0), (1, 1)}
    assert gameAI.knowledge[0].count == 1

def test_add_knowledge_2x2_3_mines():
    """ 
    Test marking any additional cells as safe or mines
    CASE 1 - all neighbors are mines
    """
    cell = (0, 0)
    count = 3

    gameAI = MinesweeperAI()
    gameAI.add_knowledge(cell, count)

    assert gameAI.knowledge[0].cells == {(0, 1), (1, 0), (1, 1)}
    assert gameAI.knowledge[0].count == 3
    assert gameAI.mines == {(0, 1), (1, 0), (1, 1)}
    assert gameAI.safes == {(0, 0)}


def test_add_knowledge_2x2_0_mines():
    """ 
    Test marking any additional cells as safe or mines
    CASE 2 - all neighbors are safe
    """
    cell = (0, 0)
    count = 0

    gameAI = MinesweeperAI()
    gameAI.add_knowledge(cell, count)

    assert gameAI.knowledge[0].cells == {(0, 1), (1, 0), (1, 1)}
    assert gameAI.knowledge[0].count == 0
    assert gameAI.mines == set()
    assert gameAI.safes == {(0, 0), (0, 1), (1, 0), (1, 1)}

def test_make_safe_move():
    # Cells being checked are (0, 0), (0, 1), (1, 0), (1, 1) with a count of 2
    safe_cells = {(0, 0), (0, 1)}
    mine_cells = {(1, 0), (1, 1)}

    # Test adding knowledge
    gameAI = MinesweeperAI()
    for cell in safe_cells:
        gameAI.mark_safe(cell)

    for cell in mine_cells:
        gameAI.mark_mine(cell)
    
    assert gameAI.make_safe_move() in safe_cells and gameAI.make_safe_move() not in mine_cells


def make_random_move():
    gameAI = MinesweeperAI()
    safe_cells = {(0, 0), (0, 1)}
    mine_cells = {(1, 0), (1, 1)}

    for cell in safe_cells:
        gameAI.mark_safe(cell)

    for cell in mine_cells:
        gameAI.mark_mine(cell)

    assert gameAI.make_random_move() not in safe_cells and gameAI.make_random_move() not in mine_cells


"""
TESTING SENTENCE CLASS
"""
def test_mark_safe():
    # Test marking safe location at (0, 0)
    cells = {(0, 0), (0, 1), (1, 0), (1, 1)}
    count = 1
    sentence = Sentence(cells, count)
    sentence.mark_safe((0, 0))
    assert sentence.cells == {(0, 1), (1, 0), (1, 1)}
    assert sentence.count == 1

def test_mark_mine():
    # Test marking a mine at location (0, 0)
    cells = {(0, 0), (0, 1), (1, 0), (1, 1)}
    count = 1
    sentence = Sentence(cells, count)
    sentence.mark_mine((0, 0))
    assert sentence.cells == {(0, 1), (1, 0), (1, 1)}
    assert sentence.count == 0

def test_known_safes():
    # Test safes 0 out of 1
    cells = {(0, 0)}
    count = 0
    sentence = Sentence(cells, count)
    assert sentence.known_safes() == {(0, 0)}

    # Test safes 0 out of 4
    cells = {(0, 0), (0, 1), (1, 0), (1, 1)}
    count = 0
    sentence = Sentence(cells, count)
    assert sentence.known_safes() == {(0, 0), (0, 1), (1, 0), (1, 1)}

    # Test safes 1 out of 4
    cells = {(0, 0), (0, 1), (1, 0), (1, 1)}
    count = 1
    sentence = Sentence(cells, count)
    assert sentence.known_safes() == set()

def test_known_mines():
    # Test mines 1 out of 1
    cells = {(0, 0)}
    count = 1
    sentence = Sentence(cells, count)
    assert sentence.known_mines() == {(0, 0)}

    # Test mines 4 out of 4
    cells = {(0, 0), (0, 1), (1, 0), (1, 1)}
    count = 4
    sentence = Sentence(cells, count)
    assert sentence.known_mines() == {(0, 0), (0, 1), (1, 0), (1, 1)}

    # Test mines 1 out of 4
    cells = {(0, 0), (0, 1), (1, 0), (1, 1)}
    count = 1
    sentence = Sentence(cells, count)
    print(sentence.known_mines())
    assert sentence.known_mines() == set()


if __name__ == "__main__":
    main()
    test_known_mines()