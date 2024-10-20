from minesweeper import Minesweeper, Sentence, MinesweeperAI

def main():
    ...


"""
TESTING MinesweeperAI CLASS
"""
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
"""


def test_mark_cells_as_safe_or_mines_in_add_knowledge():
    gameAI = MinesweeperAI(4, 4)

    # Click on cell (0, 0) which has 3 mines around
    gameAI.add_knowledge((0, 0), 3)

    assert gameAI.safes == {(0, 0)}
    assert gameAI.mines == {(0, 1), (1, 0), (1, 1)}

    # Click on cell (2, 2) which has no mines around
    gameAI.add_knowledge((3, 3), 0)
    assert gameAI.safes == {(0, 0), (3, 2), (2, 2), (2, 3), (3, 3)}


def test_make_safe_move():
    gameAI = MinesweeperAI(3, 3)
    safe_cells = {(0, 0), (0, 1)}
    mine_cells = {(1, 0), (1, 1)}

    for cell in safe_cells:
        gameAI.mark_safe(cell)

    for cell in mine_cells:
        gameAI.mark_mine(cell)
    
    assert gameAI.make_safe_move() in safe_cells and gameAI.make_safe_move() not in mine_cells


def make_random_move():
    gameAI = MinesweeperAI(3, 3)
    safe_cells = {(0, 0), (0, 1)}
    mine_cells = {(1, 0), (1, 1)}

    for cell in safe_cells:
        gameAI.mark_safe(cell)

    for cell in mine_cells:
        gameAI.mark_mine(cell)

    assert gameAI.make_random_move() not in safe_cells and gameAI.make_random_move() not in mine_cells


def test_mark_safe_AI():
    gameAI = MinesweeperAI(2, 2)
    gameAI.knowledge.append(Sentence({(0,0), (0, 1), (1, 0), (1, 1)}, 2))

    gameAI.mark_safe((0, 0))
    assert gameAI.safes == {(0, 0)}
    assert gameAI.knowledge[0].cells == {(0, 1), (1, 0), (1, 1)}
    assert gameAI.knowledge[0].count == 2

    gameAI.mark_safe((0, 1))
    assert gameAI.safes == {(0, 0), (0, 1)}
    assert gameAI.knowledge[0].cells == {(1, 0), (1, 1)}
    assert gameAI.knowledge[0].count == 2


def test_mark_mine_AI():
    gameAI = MinesweeperAI(2, 2)
    gameAI.knowledge.append(Sentence({(0,0), (0, 1), (1, 0), (1, 1)}, 2))

    gameAI.mark_mine((0, 0))
    assert gameAI.mines == {(0, 0)}
    assert gameAI.knowledge[0].cells == {(0, 1), (1, 0), (1, 1)}
    assert gameAI.knowledge[0].count == 1

    gameAI.mark_mine((0, 1))
    assert gameAI.mines == {(0, 0), (0, 1)}
    assert gameAI.knowledge[0].cells == {(1, 0), (1, 1)}
    assert gameAI.knowledge[0].count == 0


"""
TESTING SENTENCE CLASS
"""
def test_mark_safe():
    cells = {(0, 0), (0, 1), (1, 0), (1, 1)}
    sentence = Sentence(cells, 0)

    sentence.mark_safe((0, 0))
    assert sentence.cells == {(0, 1), (1, 0), (1, 1)}
    sentence.mark_safe((0, 1))
    assert sentence.cells == {(1, 0), (1, 1)}
    sentence.mark_safe((1, 0))
    assert sentence.cells == {(1, 1)}
    sentence.mark_safe((1, 1))
    assert sentence.cells == set()


def test_mark_mine():
    cells = {(0, 0), (0, 1), (1, 0), (1, 1)}
    sentence = Sentence(cells, 4)

    sentence.mark_mine((0, 0))
    assert sentence.cells == {(0, 1), (1, 0), (1, 1)}
    assert sentence.count == 3
    sentence.mark_mine((0, 1))
    assert sentence.cells == {(1, 0), (1, 1)}
    assert sentence.count == 2
    sentence.mark_mine((1, 0))
    assert sentence.cells == {(1, 1)}
    assert sentence.count == 1
    sentence.mark_mine((1, 1))
    assert sentence.cells == set()
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
    assert sentence.known_mines() == set()

    # Test mines 8 out of 9
    cells = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
    count = 9
    sentence = Sentence(cells, count)
    assert sentence.known_mines() == {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}

    # Test mines 0 out of 9
    sentence = Sentence({(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}, 0)
    assert sentence.known_mines() == set()


if __name__ == "__main__":
    main()
    test_known_mines()