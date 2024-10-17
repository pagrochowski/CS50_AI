from minesweeper import Minesweeper, Sentence, MinesweeperAI

def main():
    ...


"""
TESTING MinesweeperAI CLASS
"""


def test_add_knowledge():
    # Cell being checked is (0, 0) with a count of 1
    cell = (0, 0)
    count = 1

    # Test adding knowledge
    gameAI = MinesweeperAI()
    gameAI.add_knowledge(cell, count)

    # Assert knowledge has been added
    assert gameAI.knowledge[0].cells == {(0, 0)}
    assert gameAI.knowledge[0].count == 1


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