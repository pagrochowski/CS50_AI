from nim import Nim, NimAI
import random


def main():

    game = Nim()
    ai = NimAI()
    state = (0, 0, 0, 2)
    action =  (3, 2)
    #print(ai.get_q_value(state, action))
    #print(game.available_actions((0, 0, 0, 2)))

    #print(random.random())
    
    ai.update_q_value(state, action, 0, 0, 1)


def test_get_q_value():
    # Initialise AI object
    ai = NimAI()
    state = (0, 0, 0, 2)
    action =  (3, 2)

    assert ai.get_q_value(state, action) == 0

    ai.q[(state, action)] = 0.6
    assert ai.get_q_value(state, action) == 0.6


if __name__ == "__main__":
    main()