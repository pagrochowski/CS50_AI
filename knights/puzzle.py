from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either knight or knave
    Or(AKnight, AKnave),
    # A is not both knight and knave
    Not(And(AKnight, AKnave)),
    # A knight always tells the truth
    Implication(AKnight, And(AKnight, AKnave)),
    # A knave never tells the truth
    Not(Implication(AKnave, And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A and B are either knight or knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # A knave always lies and implies A and B are both knaves
    Not(Implication(AKnave, And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A and B are either knight or knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A and B are the same kind 
    Implication(AKnight, BKnight),
    Implication(AKnave, Not(BKnave)),
    # A and B are different kinds
    Implication(BKnight, AKnave),
    Implication(BKnave, Not(AKnight)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A, B and C are either knight or knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # If A is a knight, A's statement "I am a knight" is true
    Implication(AKnight, AKnight),

    # If A is a knave, A's statement "I am a knave" is false
    Implication(AKnave, Not(AKnave)),

    # If B is a knight, then "A said 'I am a knave'"" must be true
    Implication(BKnight, AKnave),

    # If B is a knight, then C is a knave
    Implication(BKnight, CKnave),

    # C says A is a knight, if A is a knight, then C is also a knight
    Biconditional(CKnight, AKnight) 
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
