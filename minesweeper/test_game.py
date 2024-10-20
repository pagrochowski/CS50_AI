import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI


def main():
    # Initiate 3x3 board
    gameAI = MinesweeperAI(3, 3)
    # Click on cell (0, 0)
    gameAI.add_knowledge((0, 0), 0)

    # Click on cell (0, 1) 
    #gameAI.add_knowledge((0, 1), 1)

    # Click on cell (0, 2) 
    #gameAI.add_knowledge((0, 2), 1)

    # Click on cell (2, 1) 
    #gameAI.add_knowledge((2, 1), 2)


if __name__ == "__main__":
    main()