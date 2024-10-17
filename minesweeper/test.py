from minesweeper import Minesweeper, Sentence, MinesweeperAI

def main():
    board = Minesweeper(height=1, width=1, mines=1)
    board.print()
    cells = {(0, 0)}
    count = 1
    sentence = Sentence(cells, count)
    print(sentence)
    print(sentence.known_mines())


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