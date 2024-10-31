from nim import Nim, NimAI


def main():

    ai = NimAI()
    state = (0, 0, 0, 2)
    action =  (3, 2)
    print(ai.get_q_value(state, action))
    


def test_get_q_value():
    # Initialise AI object
    ai = NimAI()
    state = (0, 0, 0, 2)
    action =  (3, 2)

    assert ai.get_q_value(state, action) == 0


if __name__ == "__main__":
    main()