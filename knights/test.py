from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
def main():
    sentence = And(Not(AKnight), Not(AKnave))
    print(sentence.formula())


if __name__ == "__main__":
    main()